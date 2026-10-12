#!/usr/bin/env python3
"""Judge for the Phase 2 residual probes.

Scores every cached residual against the note-text baseline.
Not a camera. Not handoverPass. Do not fill D.

A clear is a point estimate above the baseline with no interval overlap.
Overlap is not a pass. Empty cache is not 0.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

SCENARIOS = "data/scenarios_all.jsonl"
DUMPS = {
    "qwen": "results/scenario_qwen_2026-10-12-0031.jsonl",
    "mistral": "results/scenario_mistral_2026-10-12-0031.jsonl",
    "aya": "results/scenario_aya_2026-10-12-0031.jsonl",
    "gemma": "results/scenario_gemma_2026-10-12-0031.jsonl",
    "falcon": "results/scenario_falcon_2026-10-12-0031.jsonl",
}
BASELINE = {
    "qwen": 0.709, "mistral": 0.855, "aya": 0.836, "gemma": 0.792, "falcon": 0.818,
}
# probe name -> (file pattern, layer or "")
PROBES = [
    ("prebutton", "results/prebutton_{m}_L-1.npy"),
    ("noteonly", "results/noteonly_{m}_L-1.npy"),
    ("endnote", "results/endnote_{m}_L-1.npy"),
    ("swap", "results/swap_{m}_L-1.npy"),
    ("askonly", "results/askonly_{m}_L-1.npy"),
    ("note_mid", None),  # mid layer, filled below
]
MID = {"qwen": 8, "mistral": 9, "aya": 10, "gemma": 10, "falcon": 8}
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


def public_y(path: str, sid_split: dict[str, str]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rows = []
    with open(path) as f:
        for line in f:
            d = json.loads(line)
            if d.get("arm") != "public" or d.get("button") not in ("YES", "NO"):
                continue
            rows.append((sid_split.get(d["scenario_id"], "?"), 1 if d["button"] == "YES" else 0))
    y = np.array([r[1] for r in rows])
    fit = np.array([i for i, r in enumerate(rows) if r[0] == "fit"])
    ev = np.array([i for i, r in enumerate(rows) if r[0] == "eval"])
    return y, fit, ev


def score_X(X: np.ndarray, y, fit, ev) -> tuple[int, int, float, float, float]:
    Xf, yf = X[fit], y[fit]
    d = Xf[yf == 1].mean(0) - Xf[yf == 0].mean(0)
    nrm = np.linalg.norm(d)
    if nrm < 1e-8:
        return 0, len(ev), 0.0, 0.0, 0.0
    d /= nrm
    thr = 0.5 * ((Xf[yf == 1] @ d).mean() + (Xf[yf == 0] @ d).mean())
    pred = (X[ev] @ d >= thr).astype(int)
    k = int((pred == y[ev]).sum())
    n = len(ev)
    acc, lo, hi = wilson(k, n)
    return k, n, acc, lo, hi


def fit_logit(X, y):
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
    return w


def main() -> None:
    sid_split = load_split()
    rows_out = []
    for model, dump in DUMPS.items():
        y, fit, ev = public_y(dump, sid_split)
        base = BASELINE[model]
        # single residual probes
        files = {
            "prebutton": f"results/prebutton_{model}_L-1.npy",
            "noteonly": f"results/noteonly_{model}_L-1.npy",
            "endnote": f"results/endnote_{model}_L-1.npy",
            "swap": f"results/swap_{model}_L-1.npy",
            "askonly": f"results/askonly_{model}_L-1.npy",
            "note_mid": f"results/noteonly_{model}_L{MID[model]}.npy",
        }
        scored = {}
        for name, path in files.items():
            if not Path(path).exists():
                rows_out.append({"model": model, "probe": name, "status": "missing"})
                continue
            X = np.load(path)
            k, n, acc, lo, hi = score_X(X, y, fit, ev)
            clear = acc > base and not (lo <= base <= hi)
            scored[name] = (X, k, n, acc, lo, hi, clear)
            rows_out.append({
                "model": model, "probe": name, "k": k, "n": n,
                "p": round(acc, 3), "lo": round(lo, 3), "hi": round(hi, 3),
                "baseline": base, "clear": clear,
            })
        # combine: prebutton + note_mid
        if "prebutton" in scored and "note_mid" in scored:
            Xp = scored["prebutton"][0]
            Xn = scored["note_mid"][0]
            def direc(X):
                d = X[fit][y[fit] == 1].mean(0) - X[fit][y[fit] == 0].mean(0)
                return d / np.linalg.norm(d)
            sp = (Xp @ direc(Xp))[:, None]
            sn = (Xn @ direc(Xn))[:, None]
            X = np.concatenate([sp, sn], 1)
            w = fit_logit(X[fit], y[fit])
            Xb = np.concatenate([np.ones((len(ev), 1)), X[ev]], 1)
            pred = (1 / (1 + np.exp(-np.clip(Xb @ w, -20, 20))) >= 0.5).astype(int)
            k = int((pred == y[ev]).sum())
            n = len(ev)
            acc, lo, hi = wilson(k, n)
            clear = acc > base and not (lo <= base <= hi)
            rows_out.append({
                "model": model, "probe": "combine", "k": k, "n": n,
                "p": round(acc, 3), "lo": round(lo, 3), "hi": round(hi, 3),
                "baseline": base, "clear": clear,
            })

    Path("results/probe_judge.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in rows_out)
    )
    lines = [
        "# Probe judge",
        "",
        "Not a camera. Not `handoverPass`. Do not fill *D*.",
        "",
        "A clear is above the note-text baseline with no interval overlap. "
        "Overlap is not a pass. A missing cache is not 0.",
        "",
        "| Model | Probe | Score | Baseline | Clear |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows_out:
        if r.get("status") == "missing":
            lines.append(f"| {r['model']} | {r['probe']} | missing | | |")
            continue
        mark = "yes" if r["clear"] else "no"
        lines.append(
            f"| {r['model']} | {r['probe']} | {r['k']}/{r['n']} = {r['p']:.3f} "
            f"[{r['lo']:.3f}, {r['hi']:.3f}] | {r['baseline']:.3f} | {mark} |"
        )
    lines += [
        "",
        "The pre-button and combine rows see the ask. Note-only, end-of-note, "
        "swap, and ask-only do not clear the bar. Not a plan readout.",
    ]
    Path("results/probe_judge.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
