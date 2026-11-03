#!/usr/bin/env python3
"""Phase 2 combination: mid-layer note direction + pre-button direction.

Two scalars. Each direction is fit on fit scenario-ids only.
A logistic on the two scores predicts the public button on eval ids.

The plan LOTO lived at mid layer (Qwen 8, Mistral 9). The pre-button
win lived at last layer and saw the ask. This asks whether the mid-layer
note direction adds anything.

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
from cache_meta import cached_array, check_loaded, want_meta
from prompt_text import encode_prompt

NOTE_PROMPT_VERSION = "noteonly-v1"  # "Private note:\n" + note, last token
MAX_LENGTH = 512

SCENARIOS = "data/scenarios_all.jsonl"
DUMPS = {
    "qwen": "results/scenario_qwen_2026-10-12-0031.jsonl",
    "mistral": "results/scenario_mistral_2026-10-12-0031.jsonl",
    "aya": "results/scenario_aya_2026-10-12-0031.jsonl",
    "gemma": "results/scenario_gemma_2026-10-12-0031.jsonl",
    "falcon": "results/scenario_falcon_2026-10-12-0031.jsonl",
}
MID = {"qwen": 8, "mistral": 9, "aya": 10, "gemma": 10, "falcon": 8}
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
                "split": d.get("split") or sid_split.get(d["scenario_id"], "unknown"),
                "note": d.get("note", ""),
                "y": 1 if d["button"] == "YES" else 0,
            })
    return rows


def note_input(rec: dict) -> str:
    return "Private note:\n" + rec["note"]


def extract_note_mid(model_name: str, model_path: str, rows: list[dict], layer: int, tag: str = "") -> np.ndarray:
    suffix = f"_{tag}" if tag else ""
    cache = Path(f"results/noteonly_{model_name}{suffix}_L{layer}.npy")
    meta = Path(f"results/noteonly_{model_name}{suffix}_L{layer}.json")
    want = want_meta(rows, layer, model_path, NOTE_PROMPT_VERSION, MAX_LENGTH, inputs=[note_input(r) for r in rows])
    return cached_array(cache, meta, want, lambda: _extract_note_mid(model_path, rows, layer))


def _extract_note_mid(model_path: str, rows: list[dict], layer: int):
    tok, model = load_tok_model(model_path)
    import torch
    vecs = []
    for i, rec in enumerate(rows):
        text = note_input(rec)
        enc = encode_prompt(tok, text, return_tensors="pt", truncation=True, max_length=MAX_LENGTH)
        enc = {k: v.to(model.device) for k, v in enc.items()}
        with torch.no_grad():
            out = model(**enc, output_hidden_states=True)
        vecs.append(out.hidden_states[layer][0, -1, :].float().cpu().numpy())
        if (i + 1) % 20 == 0:
            print(f"extracted {i+1}/{len(rows)}")
    return np.stack(vecs), getattr(tok, "name_or_path", model_path)


def direction(X: np.ndarray, y: np.ndarray, fit: np.ndarray) -> np.ndarray:
    Xf, yf = X[fit], y[fit]
    d = Xf[yf == 1].mean(0) - Xf[yf == 0].mean(0)
    n = np.linalg.norm(d)
    return d / n if n > 1e-8 else d


def fit_logit(X: np.ndarray, y: np.ndarray, max_iter: int = 25, tol: float = 1e-6) -> tuple[np.ndarray, dict]:
    """Newton logistic fit. Returns (w, info); info["converged"] is False when the step never fell
    below tol within max_iter, the Hessian was singular, or the weights are not finite (audit 2026-11-03)."""
    n, d = X.shape
    info = {"converged": False, "iters": 0, "reason": "max_iter"}
    Xb = np.concatenate([np.ones((n, 1)), X], 1)
    w = np.zeros(d + 1)
    for it in range(max_iter):
        info["iters"] = it + 1
        z = np.clip(Xb @ w, -20, 20)
        p = 1 / (1 + np.exp(-z))
        W = p * (1 - p)
        H = Xb.T @ (Xb * W[:, None]) + 1e-3 * np.eye(d + 1)
        g = Xb.T @ (p - y)
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            info["reason"] = "singular"; break
        w -= step
        if np.max(np.abs(step)) < tol:
            info.update(converged=True, reason="tol"); break
    if not np.all(np.isfinite(w)):
        info.update(converged=False, reason="nonfinite")
    return w, info


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="qwen")
    p.add_argument("--path", default="")
    p.add_argument("--mid", type=int, default=-1, help="mid layer; default from MID table")
    p.add_argument("--dump", default="", help="scenario dump; default is the night press")
    args = p.parse_args()
    env = {"qwen": "QWEN", "mistral": "MISTRAL", "aya": "AYA",
           "gemma": "GEMMA", "falcon": "FALCON"}.get(args.model, "")
    path = args.path or os.environ.get(env, "")
    if not path:
        raise SystemExit(f"set {env} or pass --path")
    mid = args.mid if args.mid >= 0 else MID.get(args.model)
    if mid is None:
        raise SystemExit(f"pass --mid for {args.model}; not in MID table")

    sid_split = load_split()
    dump = args.dump or DUMPS[args.model]
    rows = public_rows(dump, sid_split)
    y = np.array([r["y"] for r in rows])
    fit = np.array([i for i, r in enumerate(rows) if r["split"] == "fit"])
    ev = np.array([i for i, r in enumerate(rows) if r["split"] == "eval"])
    print(f"fit={len(fit)} eval={len(ev)}")
    if len(fit) == 0 or len(ev) == 0:
        raise SystemExit("need both fit and eval rows; check split on the dump")

    tag = Path(dump).stem.replace(f"scenario_{args.model}_", "")
    pre_path = Path(f"results/prebutton_{args.model}_{tag}_L-1.npy")
    if not pre_path.exists() and tag == "2026-10-12-0031":
        pre_path = Path(f"results/prebutton_{args.model}_L-1.npy")
    if not pre_path.exists():
        raise SystemExit(f"missing {pre_path}; extract prebutton on this dump first")
    Xp = np.load(pre_path)
    check_loaded(Xp, pre_path.with_suffix(".json"), rows, "prebutton Xp", model_path=path)
    Xn = extract_note_mid(args.model, path, rows, mid, tag=tag)

    sp = (Xp @ direction(Xp, y, fit))[:, None]
    sn = (Xn @ direction(Xn, y, fit))[:, None]
    X = np.concatenate([sp, sn], 1)
    w, conv = fit_logit(X[fit], y[fit])
    if not conv["converged"]:
        print(f"WARN fit_logit not converged ({conv['reason']}, {conv['iters']} iters): combine result INVALID")
    Xb = np.concatenate([np.ones((len(ev), 1)), X[ev]], 1)
    pred = (1 / (1 + np.exp(-np.clip(Xb @ w, -20, 20))) >= 0.5).astype(int)
    k = int((pred == y[ev]).sum())
    n = len(ev)
    acc, lo, hi = wilson(k, n)
    b = BASELINE.get(args.model)
    print(f"combine mid={mid} {k}/{n} = {acc:.3f} [{lo:.3f}, {hi:.3f}]"
          + ("" if conv["converged"] else " INVALID (logit not converged)"))
    if b:
        print(f"note-text {b[0]}/{b[1]} = {b[2]:.3f}")
    if b:
        print("above baseline" if acc > b[2] else "not above baseline")
        print("intervals overlap" if not (hi < b[2] or lo > b[2]) else "intervals do not overlap")
    else:
        print("no October baseline for this model")
    print("not a camera. not handoverPass. Do not fill D.")


if __name__ == "__main__":
    main()
