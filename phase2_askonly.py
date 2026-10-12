#!/usr/bin/env python3
"""Phase 2 ask-only residual.

Prompt is the ask alone. No note. Last-token residual.
Same direction, same split, same bar.

If this clears the bar, the note was irrelevant.
Not a camera. Not handoverPass. Do not fill D. Do not freeze r.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

import numpy as np

from hide_bank import load_tok_model
from reply_mutate import chat

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
            if d.get("arm") != "public" or d.get("button") not in ("YES", "NO"):
                continue
            rows.append({
                "scenario_id": d["scenario_id"],
                "split": sid_split.get(d["scenario_id"], "unknown"),
                "ask": d.get("ask", ""),
                "y": 1 if d["button"] == "YES" else 0,
            })
    return rows


def ask_prompt(tok, rec: dict) -> str:
    msgs = [
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


def extract(model_name: str, model_path: str, rows: list[dict], layer: int) -> np.ndarray:
    cache = Path(f"results/askonly_{model_name}_L{layer}.npy")
    meta = Path(f"results/askonly_{model_name}_L{layer}.json")
    if cache.exists() and meta.exists():
        saved = json.loads(meta.read_text())
        if saved.get("n") == len(rows) and saved.get("layer") == layer:
            print(f"cache hit {cache}")
            return np.load(cache)
    tok, model = load_tok_model(model_path)
    vecs = []
    for i, rec in enumerate(rows):
        vecs.append(last_token(model, tok, ask_prompt(tok, rec), layer))
        if (i + 1) % 20 == 0:
            print(f"extracted {i+1}/{len(rows)}")
    X = np.stack(vecs)
    np.save(cache, X)
    meta.write_text(json.dumps({"n": len(rows), "layer": layer}))
    return X


def probe(X, y, fit_idx, ev_idx) -> tuple[int, int]:
    Xf, yf = X[fit_idx], y[fit_idx]
    direction = Xf[yf == 1].mean(0) - Xf[yf == 0].mean(0)
    norm = np.linalg.norm(direction)
    if norm < 1e-8:
        return 0, len(ev_idx)
    direction /= norm
    thr = 0.5 * ((Xf[yf == 1] @ direction).mean() + (Xf[yf == 0] @ direction).mean())
    pred = (X[ev_idx] @ direction >= thr).astype(int)
    return int((pred == y[ev_idx]).sum()), len(ev_idx)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="qwen")
    p.add_argument("--path", default="")
    p.add_argument("--layer", type=int, default=-1)
    args = p.parse_args()
    env = {"qwen": "QWEN", "mistral": "MISTRAL", "aya": "AYA",
           "gemma": "GEMMA", "falcon": "FALCON"}.get(args.model, "")
    path = args.path or os.environ.get(env, "")
    if not path:
        raise SystemExit(f"set {env} or pass --path")

    sid_split = load_split()
    rows = public_rows(DUMPS[args.model], sid_split)
    print(f"{args.model} public rows={len(rows)} layer={args.layer} ask-only")
    X = extract(args.model, path, rows, args.layer)
    y = np.array([r["y"] for r in rows])
    fit_idx = np.array([i for i, r in enumerate(rows) if r["split"] == "fit"])
    ev_idx = np.array([i for i, r in enumerate(rows) if r["split"] == "eval"])
    k, n = probe(X, y, fit_idx, ev_idx)
    acc, lo, hi = wilson(k, n)
    b = BASELINE[args.model]
    print(f"askonly {k}/{n} = {acc:.3f} [{lo:.3f}, {hi:.3f}]")
    print(f"note-text {b[0]}/{b[1]} = {b[2]:.3f}")
    print("above baseline" if acc > b[2] else "not above baseline")
    print("intervals overlap" if not (hi < b[2] or lo > b[2]) else "intervals do not overlap")
    print("not a camera. not handoverPass. Do not fill D.")


if __name__ == "__main__":
    main()
