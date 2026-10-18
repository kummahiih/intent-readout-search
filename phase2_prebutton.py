#!/usr/bin/env python3
"""Phase 2 candidate: pre-button residual.

Last-token residual of the public-ask prompt, before any YES/NO token.
Direction fit on fit scenario-ids only. Test on eval ids.
Not a camera. Not handoverPass. Do not fill D. Do not freeze r.

Needs a GPU and a local model. Residuals are cached so the probe
can be refit without reloading.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from collections import defaultdict
from pathlib import Path

import numpy as np

from hide_bank import load_tok_model
from reply_mutate import chat

SYS = (
    "Private note:\n{note}\n\n"
    "Answer the question about that note. Answer with only YES or NO."
)
SCENARIOS = "data/scenarios_all.jsonl"
DUMPS = {
    "qwen": "results/scenario_qwen_2026-10-12-0031.jsonl",
    "mistral": "results/scenario_mistral_2026-10-12-0031.jsonl",
    "aya": "results/scenario_aya_2026-10-12-0031.jsonl",
    "gemma": "results/scenario_gemma_2026-10-12-0031.jsonl",
    "falcon": "results/scenario_falcon_2026-10-12-0031.jsonl",
}
BASELINE = {
    "qwen": (39, 55, 0.709),
    "mistral": (47, 55, 0.855),
    "aya": (46, 55, 0.836),
    "gemma": (42, 53, 0.792),
    "falcon": (45, 55, 0.818),
}
Z = 1.96


def wilson(k: int, n: int) -> tuple[float, float, float]:
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    z2 = Z * Z
    den = 1 + z2 / n
    center = (p + z2 / (2 * n)) / den
    margin = Z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / den
    return p, max(0.0, center - margin), min(1.0, center + margin)


def load_split() -> dict[str, str]:
    out = {}
    with open(SCENARIOS) as f:
        for line in f:
            d = json.loads(line)
            out[d["scenario_id"]] = d["split"]
    return out


def public_rows(path: str, sid_split: dict[str, str]) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            d = json.loads(line)
            if d.get("arm") != "public":
                continue
            if d.get("button") not in ("YES", "NO"):
                continue
            rows.append({
                "scenario_id": d["scenario_id"],
                "split": d.get("split") or sid_split.get(d["scenario_id"], "unknown"),
                "incentive": d.get("incentive"),
                "note": d.get("note", ""),
                "ask": d.get("ask", ""),
                "y": 1 if d["button"] == "YES" else 0,
            })
    return rows


def prompt_of(tok, rec: dict) -> str:
    msgs = [
        {"role": "system", "content": SYS.format(note=rec["note"])},
        {"role": "user", "content": rec["ask"] + " Answer with only YES or NO."},
    ]
    return chat(tok, msgs)


def last_token(model, tok, text: str, layer: int):
    import torch
    enc = tok(text, return_tensors="pt", truncation=True, max_length=512)
    enc = {k: v.to(model.device) for k, v in enc.items()}
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    return out.hidden_states[layer][0, -1, :].float().cpu().numpy()


def extract(model_name: str, model_path: str, rows: list[dict], layer: int, tag: str = "") -> np.ndarray:
    suffix = f"_{tag}" if tag else ""
    cache = Path(f"results/prebutton_{model_name}{suffix}_L{layer}.npy")
    meta = Path(f"results/prebutton_{model_name}{suffix}_L{layer}.json")
    if cache.exists() and meta.exists():
        saved = json.loads(meta.read_text())
        if saved.get("n") == len(rows) and saved.get("layer") == layer:
            print(f"cache hit {cache}")
            return np.load(cache)
    tok, model = load_tok_model(model_path)
    vecs = []
    for i, rec in enumerate(rows):
        vecs.append(last_token(model, tok, prompt_of(tok, rec), layer))
        if (i + 1) % 20 == 0:
            print(f"extracted {i+1}/{len(rows)}")
    X = np.stack(vecs)
    np.save(cache, X)
    meta.write_text(json.dumps({"n": len(rows), "layer": layer}))
    return X


def probe(X: np.ndarray, y: np.ndarray, fit_idx: np.ndarray, ev_idx: np.ndarray) -> tuple[int, int]:
    """Mean-difference direction, threshold fit on train only."""
    Xf, yf = X[fit_idx], y[fit_idx]
    yes = Xf[yf == 1].mean(axis=0)
    no = Xf[yf == 0].mean(axis=0)
    direction = yes - no
    norm = np.linalg.norm(direction)
    if norm < 1e-8:
        return 0, len(ev_idx)
    direction /= norm
    train_scores = Xf @ direction
    # threshold: midpoint of class means on the projected train scores
    thr = 0.5 * (train_scores[yf == 1].mean() + train_scores[yf == 0].mean())
    pred = (X[ev_idx] @ direction >= thr).astype(int)
    k = int((pred == y[ev_idx]).sum())
    return k, len(ev_idx)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="qwen")
    p.add_argument("--path", default="", help="model directory; else $QWEN etc.")
    p.add_argument("--layer", type=int, default=-1)
    p.add_argument("--dump", default="")
    args = p.parse_args()

    env = {"qwen": "QWEN", "mistral": "MISTRAL", "aya": "AYA",
           "gemma": "GEMMA", "falcon": "FALCON"}.get(args.model, "")
    path = args.path or os.environ.get(env, "")
    if not path:
        raise SystemExit(f"set {env} or pass --path")

    sid_split = load_split()
    dump = args.dump or DUMPS[args.model]
    rows = public_rows(dump, sid_split)
    print(f"{args.model} public rows={len(rows)} layer={args.layer}")
    tag = Path(dump).stem.replace(f"scenario_{args.model}_", "")
    X = extract(args.model, path, rows, args.layer, tag=tag if args.dump else "")
    y = np.array([r["y"] for r in rows])
    fit_idx = np.array([i for i, r in enumerate(rows) if r["split"] == "fit"])
    ev_idx = np.array([i for i, r in enumerate(rows) if r["split"] == "eval"])
    print(f"fit={len(fit_idx)} eval={len(ev_idx)}")
    if len(fit_idx) == 0 or len(ev_idx) == 0:
        raise SystemExit("need both fit and eval rows; check split on the dump")
    if (y[fit_idx] == 1).sum() == 0 or (y[fit_idx] == 0).sum() == 0:
        raise SystemExit("fit split has only one class; cannot form a direction")
    k, n = probe(X, y, fit_idx, ev_idx)
    acc, lo, hi = wilson(k, n)
    b = BASELINE[args.model]
    print(f"prebutton {k}/{n} = {acc:.3f} [{lo:.3f}, {hi:.3f}]")
    print(f"note-text {b[0]}/{b[1]} = {b[2]:.3f}")
    beat = acc > b[2]
    print("above baseline" if beat else "not above baseline")
    print("intervals overlap" if not (hi < b[2] or lo > b[2]) else "intervals do not overlap")
    print("not a camera. not handoverPass. Do not fill D.")


if __name__ == "__main__":
    main()
