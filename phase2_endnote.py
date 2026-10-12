#!/usr/bin/env python3
"""Phase 2 candidate: end-of-note residual inside the full prompt.

The public-ask prompt is built as usual. The residual is taken at the
last token of the note span, before the ask tokens that name the
proposition. Direction fit on fit scenario-ids only.

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
            if d.get("arm") != "public" or d.get("button") not in ("YES", "NO"):
                continue
            rows.append({
                "scenario_id": d["scenario_id"],
                "split": sid_split.get(d["scenario_id"], "unknown"),
                "note": d.get("note", ""),
                "ask": d.get("ask", ""),
                "y": 1 if d["button"] == "YES" else 0,
            })
    return rows


def full_prompt(tok, rec: dict) -> str:
    msgs = [
        {"role": "system", "content": SYS.format(note=rec["note"])},
        {"role": "user", "content": rec["ask"] + " Answer with only YES or NO."},
    ]
    return chat(tok, msgs)


def note_end_offset(tok, rec: dict, full_ids: list[int]) -> int:
    """Index of the last token that belongs to the note span.

    Tokenize the prompt truncated at the end of the note text.
    That length, clamped to the full sequence, is the boundary.
    """
    # prefix: system content up through the note, no ask
    prefix_msgs = [
        {"role": "system", "content": "Private note:\n" + rec["note"]},
    ]
    if hasattr(tok, "apply_chat_template"):
        prefix = tok.apply_chat_template(
            prefix_msgs, tokenize=False, add_generation_prompt=False
        )
    else:
        prefix = "system: Private note:\n" + rec["note"]
    prefix_ids = tok(prefix, add_special_tokens=False)["input_ids"]
    # the full prompt may add a bos the prefix call did not, or vice versa
    # walk until the prefix ids are a subsequence near the start
    n = len(prefix_ids)
    if n == 0:
        return 0
    # find where prefix_ids sit inside full_ids
    for start in range(0, max(1, len(full_ids) - n + 1)):
        if full_ids[start:start + n] == prefix_ids:
            return start + n - 1
    # fallback: proportion of characters
    full = full_prompt(tok, rec)
    cut = full.find(rec["note"])
    if cut < 0:
        return max(0, len(full_ids) // 2)
    ratio = (cut + len(rec["note"])) / max(1, len(full))
    return min(len(full_ids) - 1, max(0, int(ratio * len(full_ids)) - 1))


def endnote_residual(model, tok, rec: dict, layer: int):
    import torch
    text = full_prompt(tok, rec)
    enc = tok(text, return_tensors="pt", truncation=True, max_length=512)
    ids = enc["input_ids"][0].tolist()
    off = note_end_offset(tok, rec, ids)
    off = min(off, enc["input_ids"].shape[1] - 1)
    enc = {k: v.to(model.device) for k, v in enc.items()}
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    return out.hidden_states[layer][0, off, :].float().cpu().numpy()


def extract(model_name: str, model_path: str, rows: list[dict], layer: int) -> np.ndarray:
    cache = Path(f"results/endnote_{model_name}_L{layer}.npy")
    meta = Path(f"results/endnote_{model_name}_L{layer}.json")
    if cache.exists() and meta.exists():
        saved = json.loads(meta.read_text())
        if saved.get("n") == len(rows) and saved.get("layer") == layer:
            print(f"cache hit {cache}")
            return np.load(cache)
    tok, model = load_tok_model(model_path)
    vecs = []
    for i, rec in enumerate(rows):
        vecs.append(endnote_residual(model, tok, rec, layer))
        if (i + 1) % 20 == 0:
            print(f"extracted {i+1}/{len(rows)}")
    X = np.stack(vecs)
    np.save(cache, X)
    meta.write_text(json.dumps({"n": len(rows), "layer": layer}))
    return X


def probe(X: np.ndarray, y: np.ndarray, fit_idx: np.ndarray, ev_idx: np.ndarray) -> tuple[int, int]:
    Xf, yf = X[fit_idx], y[fit_idx]
    direction = Xf[yf == 1].mean(0) - Xf[yf == 0].mean(0)
    norm = np.linalg.norm(direction)
    if norm < 1e-8:
        return 0, len(ev_idx)
    direction /= norm
    train_scores = Xf @ direction
    thr = 0.5 * (train_scores[yf == 1].mean() + train_scores[yf == 0].mean())
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
    print(f"{args.model} public rows={len(rows)} layer={args.layer}")
    X = extract(args.model, path, rows, args.layer)
    y = np.array([r["y"] for r in rows])
    fit_idx = np.array([i for i, r in enumerate(rows) if r["split"] == "fit"])
    ev_idx = np.array([i for i, r in enumerate(rows) if r["split"] == "eval"])
    k, n = probe(X, y, fit_idx, ev_idx)
    acc, lo, hi = wilson(k, n)
    b = BASELINE[args.model]
    print(f"endnote {k}/{n} = {acc:.3f} [{lo:.3f}, {hi:.3f}]")
    print(f"note-text {b[0]}/{b[1]} = {b[2]:.3f}")
    print("above baseline" if acc > b[2] else "not above baseline")
    print("intervals overlap" if not (hi < b[2] or lo > b[2]) else "intervals do not overlap")
    print("not a camera. not handoverPass. Do not fill D.")


if __name__ == "__main__":
    main()
