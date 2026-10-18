#!/usr/bin/env python3
"""Combination probe on the reversed-polarity bank.

Same procedure as phase2_combine.py: mid-layer note direction + last-layer
pre-button direction, logistic on the pair, scored on eval scenario-ids.

The reversed files flip prop_truth and states_proposition to false, so public
YES asserts a false sentence. This is a bias control, not a voter.

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

MID = {"qwen": 8, "mistral": 9, "aya": 10, "gemma": 10, "falcon": 8}
Z = 1.96
SYS = (
    "Private note:\n{note}\n\n"
    "Answer the question about that note. Answer with only YES or NO."
)


def wilson(k: int, n: int) -> tuple[float, float, float]:
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    z2 = Z * Z
    den = 1 + z2 / n
    center = (p + z2 / (2 * n)) / den
    margin = Z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / den
    return p, max(0.0, center - margin), min(1.0, center + margin)


def load_scenarios(path: str) -> dict[str, dict]:
    out = {}
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            out[d["scenario_id"]] = d
    return out


def public_rows(dump: str, scenarios: dict[str, dict]) -> list[dict]:
    rows = []
    with open(dump) as f:
        for line in f:
            d = json.loads(line)
            if d.get("arm") != "public" or d.get("button") not in ("YES", "NO"):
                continue
            sid = d["scenario_id"]
            sc = scenarios.get(sid, {})
            rows.append({
                "scenario_id": sid,
                "split": sc.get("split", d.get("split", "unknown")),
                "note": d.get("note", sc.get("note", "")),
                "ask": d.get("ask", sc.get("public_ask", "")),
                "y": 1 if d["button"] == "YES" else 0,
            })
    return rows


def prompt_of(tok, rec: dict) -> str:
    msgs = [
        {"role": "system", "content": SYS.format(note=rec["note"])},
        {"role": "user", "content": rec["ask"] + " Answer with only YES or NO."},
    ]
    return chat(tok, msgs)


def extract_vecs(model_path: str, rows: list[dict], layer: int, cache: Path) -> np.ndarray:
    if cache.exists():
        print(f"cache hit {cache}")
        return np.load(cache)
    tok, model = load_tok_model(model_path)
    import torch
    vecs = []
    for i, rec in enumerate(rows):
        text = prompt_of(tok, rec) if layer == -1 else ("Private note:\n" + rec["note"])
        enc = tok(text, return_tensors="pt", truncation=True, max_length=512)
        enc = {k: v.to(model.device) for k, v in enc.items()}
        with torch.no_grad():
            out = model(**enc, output_hidden_states=True)
        vecs.append(out.hidden_states[layer][0, -1, :].float().cpu().numpy())
        if (i + 1) % 10 == 0:
            print(f"extracted {i+1}/{len(rows)}")
    X = np.stack(vecs)
    np.save(cache, X)
    return X


def direction(X: np.ndarray, y: np.ndarray, fit: np.ndarray) -> np.ndarray:
    Xf, yf = X[fit], y[fit]
    if (yf == 1).sum() == 0 or (yf == 0).sum() == 0:
        return np.zeros(X.shape[1])
    d = Xf[yf == 1].mean(0) - Xf[yf == 0].mean(0)
    n = np.linalg.norm(d)
    return d / n if n > 1e-8 else d


def fit_logit(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    n, d = X.shape
    Xb = np.concatenate([np.ones((n, 1)), X], 1)
    w = np.zeros(d + 1)
    for _ in range(25):
        z = np.clip(Xb @ w, -20, 20)
        p = 1 / (1 + np.exp(-z))
        W = p * (1 - p)
        H = Xb.T @ (Xb * W[:, None]) + 1e-3 * np.eye(d + 1)
        g = Xb.T @ (p - y)
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            break
        w -= step
        if np.max(np.abs(step)) < 1e-6:
            break
    return w


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--path", default="")
    p.add_argument("--scenarios", required=True, help="reversed JSONL")
    p.add_argument("--dump", required=True, help="press dump of the reversed file")
    p.add_argument("--mid", type=int, default=-1)
    args = p.parse_args()

    env = {"qwen": "QWEN", "mistral": "MISTRAL", "aya": "AYA",
           "gemma": "GEMMA", "falcon": "FALCON"}.get(args.model, "")
    path = args.path or os.environ.get(env, "")
    if not path:
        raise SystemExit(f"set {env} or pass --path")
    mid = args.mid if args.mid >= 0 else MID.get(args.model, 8)

    scenarios = load_scenarios(args.scenarios)
    rows = public_rows(args.dump, scenarios)
    if not rows:
        raise SystemExit("no public YES/NO rows in dump")
    y = np.array([r["y"] for r in rows])
    fit = np.array([i for i, r in enumerate(rows) if r["split"] == "fit"])
    ev = np.array([i for i, r in enumerate(rows) if r["split"] == "eval"])
    print(f"{args.model} public={len(rows)} fit={len(fit)} eval={len(ev)} mid={mid}")
    if len(fit) == 0 or len(ev) == 0:
        raise SystemExit("need both fit and eval rows")

    tag = Path(args.dump).stem
    Xp = extract_vecs(path, rows, -1, Path(f"results/prebutton_rev_{args.model}_{tag}_L-1.npy"))
    Xn = extract_vecs(path, rows, mid, Path(f"results/noteonly_rev_{args.model}_{tag}_L{mid}.npy"))

    sp = (Xp @ direction(Xp, y, fit))[:, None]
    sn = (Xn @ direction(Xn, y, fit))[:, None]
    X = np.concatenate([sp, sn], 1)
    w = fit_logit(X[fit], y[fit])
    Xb = np.concatenate([np.ones((len(ev), 1)), X[ev]], 1)
    pred = (1 / (1 + np.exp(-np.clip(Xb @ w, -20, 20))) >= 0.5).astype(int)
    k = int((pred == y[ev]).sum())
    n = len(ev)
    acc, lo, hi = wilson(k, n)
    yes_rate = float(y.mean())
    print(f"combine mid={mid} {k}/{n} = {acc:.3f} [{lo:.3f}, {hi:.3f}]")
    print(f"raw YES rate on this dump = {yes_rate:.3f} ({int(y.sum())}/{len(y)})")
    print("bias control. not a camera. not handoverPass. Do not fill D.")


if __name__ == "__main__":
    main()
