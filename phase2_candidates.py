#!/usr/bin/env python3
"""Phase 2 candidates computable on the night-press dumps.

Predict the realized public button on held-out scenario-ids.
Same split and same dumps as phase2_note_baseline.py.
Not a camera. Not handoverPass. Do not fill D. Do not freeze r.

Candidates:
  belief      public ~ belief button
  name        public ~ name-ask button
  belief+note unigram note + belief bit
  cross       other models' public buttons, fit-only weights
  room        unigram logistic fit per room
"""
from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

DUMPS = {
    "qwen": "results/scenario_qwen_2026-10-12-0031.jsonl",
    "mistral": "results/scenario_mistral_2026-10-12-0031.jsonl",
    "aya": "results/scenario_aya_2026-10-12-0031.jsonl",
    "gemma": "results/scenario_gemma_2026-10-12-0031.jsonl",
    "falcon": "results/scenario_falcon_2026-10-12-0031.jsonl",
}
SCENARIOS = "data/scenarios_all.jsonl"
TOP_WORDS = 80
Z = 1.96


def wilson(k: int, n: int, z: float = Z) -> tuple[float, float, float]:
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    z2 = z * z
    den = 1 + z2 / n
    center = (p + z2 / (2 * n)) / den
    margin = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / den
    return p, max(0.0, center - margin), min(1.0, center + margin)


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def load_split() -> dict[str, str]:
    out = {}
    with open(SCENARIOS) as f:
        for line in f:
            d = json.loads(line)
            out[d["scenario_id"]] = d["split"]
    return out


def load_arms(path: str, sid_split: dict[str, str]) -> list[dict]:
    """One row per (scenario_id, incentive, note) with belief/public/name buttons."""
    by = defaultdict(dict)
    with open(path) as f:
        for line in f:
            d = json.loads(line)
            key = (d["scenario_id"], d.get("incentive"), d.get("note"))
            by[key][d.get("arm")] = d
    rows = []
    for (sid, inc, note), arms in by.items():
        pub = arms.get("public", {})
        if pub.get("button") not in ("YES", "NO"):
            continue
        bel = arms.get("belief", {}).get("button")
        name = arms.get("name", {}).get("button")
        rows.append({
            "scenario_id": sid,
            "split": sid_split.get(sid, "unknown"),
            "topic": pub.get("topic", ""),
            "incentive": inc,
            "note": note or "",
            "y": 1 if pub["button"] == "YES" else 0,
            "belief": 1 if bel == "YES" else (0 if bel == "NO" else None),
            "name": 1 if name == "YES" else (0 if name == "NO" else None),
        })
    return rows


def fit_logit(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Bias + weights. Newton on logistic. Falls back to majority."""
    n, d = X.shape
    Xb = np.concatenate([np.ones((n, 1)), X], axis=1)
    w = np.zeros(d + 1)
    for _ in range(25):
        z = Xb @ w
        p = 1 / (1 + np.exp(-np.clip(z, -20, 20)))
        W = p * (1 - p)
        H = Xb.T @ (Xb * W[:, None]) + 1e-4 * np.eye(d + 1)
        g = Xb.T @ (p - y)
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            return w
        w -= step
        if np.max(np.abs(step)) < 1e-6:
            break
    return w


def predict(w: np.ndarray, X: np.ndarray) -> np.ndarray:
    Xb = np.concatenate([np.ones((X.shape[0], 1)), X], axis=1)
    z = Xb @ w
    return (1 / (1 + np.exp(-np.clip(z, -20, 20))) >= 0.5).astype(int)


def vocab(notes: list[str]) -> list[str]:
    counts: dict[str, int] = defaultdict(int)
    for note in notes:
        for t in set(tokenize(note)):
            counts[t] += 1
    return [w for w, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:TOP_WORDS]]


def bow(notes: list[str], words: list[str]) -> np.ndarray:
    idx = {w: i for i, w in enumerate(words)}
    X = np.zeros((len(notes), len(words)))
    for i, note in enumerate(notes):
        for t in set(tokenize(note)):
            if t in idx:
                X[i, idx[t]] = 1.0
    return X


def score(y: np.ndarray, pred: np.ndarray) -> tuple[int, int, float, float, float]:
    k = int((pred == y).sum())
    n = len(y)
    p, lo, hi = wilson(k, n)
    return k, n, p, lo, hi


def run_model(name: str, rows: list[dict], all_rows: dict[str, list[dict]]) -> list[dict]:
    fit = [r for r in rows if r["split"] == "fit"]
    ev = [r for r in rows if r["split"] == "eval"]
    if not fit or not ev:
        return []
    y_fit = np.array([r["y"] for r in fit])
    y_ev = np.array([r["y"] for r in ev])
    out = []

    # 1. belief
    both = [(r, i) for i, r in enumerate(ev) if r["belief"] is not None]
    fit_b = [r for r in fit if r["belief"] is not None]
    if fit_b and both:
        # map belief->public from fit: if belief YES, predict the majority public among belief-YES fit
        by_b = defaultdict(list)
        for r in fit_b:
            by_b[r["belief"]].append(r["y"])
        mapping = {b: int(np.mean(vs) >= 0.5) for b, vs in by_b.items()}
        pred = np.array([mapping.get(r["belief"], int(y_fit.mean() >= 0.5)) for r, _ in both])
        yt = np.array([r["y"] for r, _ in both])
        k, n, p, lo, hi = score(yt, pred)
        out.append({"model": name, "candidate": "belief", "k": k, "n": n, "p": p, "lo": lo, "hi": hi})

    # 2. name
    both = [(r, i) for i, r in enumerate(ev) if r["name"] is not None]
    fit_n = [r for r in fit if r["name"] is not None]
    if fit_n and both:
        by_n = defaultdict(list)
        for r in fit_n:
            by_n[r["name"]].append(r["y"])
        mapping = {b: int(np.mean(vs) >= 0.5) for b, vs in by_n.items()}
        pred = np.array([mapping.get(r["name"], int(y_fit.mean() >= 0.5)) for r, _ in both])
        yt = np.array([r["y"] for r, _ in both])
        k, n, p, lo, hi = score(yt, pred)
        out.append({"model": name, "candidate": "name", "k": k, "n": n, "p": p, "lo": lo, "hi": hi})

    # 3. belief + note
    words = vocab([r["note"] for r in fit])
    Xf = bow([r["note"] for r in fit], words)
    Xe = bow([r["note"] for r in ev], words)
    bel_f = np.array([[r["belief"] if r["belief"] is not None else 0.5] for r in fit])
    bel_e = np.array([[r["belief"] if r["belief"] is not None else 0.5] for r in ev])
    w = fit_logit(np.concatenate([Xf, bel_f], axis=1), y_fit)
    pred = predict(w, np.concatenate([Xe, bel_e], axis=1))
    k, n, p, lo, hi = score(y_ev, pred)
    out.append({"model": name, "candidate": "belief+note", "k": k, "n": n, "p": p, "lo": lo, "hi": hi})

    # 4. cross-model: other models' public y, weights fit on fit ids only
    others = [m for m in DUMPS if m != name]
    # index other models by (sid, incentive, note)
    idx = {}
    for m in others:
        idx[m] = {(r["scenario_id"], r["incentive"], r["note"]): r["y"] for r in all_rows[m]}
    def cross_X(subset):
        X = np.zeros((len(subset), len(others)))
        for i, r in enumerate(subset):
            key = (r["scenario_id"], r["incentive"], r["note"])
            for j, m in enumerate(others):
                X[i, j] = idx[m].get(key, 0.5)
        return X
    w = fit_logit(cross_X(fit), y_fit)
    pred = predict(w, cross_X(ev))
    k, n, p, lo, hi = score(y_ev, pred)
    out.append({"model": name, "candidate": "cross", "k": k, "n": n, "p": p, "lo": lo, "hi": hi})

    # 5. room-conditional note text
    rooms = sorted({r["topic"] for r in fit})
    pred = np.zeros(len(ev), dtype=int)
    for room in rooms:
        fsub = [r for r in fit if r["topic"] == room]
        esub_idx = [i for i, r in enumerate(ev) if r["topic"] == room]
        if not fsub or not esub_idx:
            continue
        words_r = vocab([r["note"] for r in fsub])
        if not words_r:
            pred[esub_idx] = int(np.mean([r["y"] for r in fsub]) >= 0.5)
            continue
        Xf = bow([r["note"] for r in fsub], words_r)
        Xe = bow([ev[i]["note"] for i in esub_idx], words_r)
        yf = np.array([r["y"] for r in fsub])
        w = fit_logit(Xf, yf)
        pred[esub_idx] = predict(w, Xe)
    k, n, p, lo, hi = score(y_ev, pred)
    out.append({"model": name, "candidate": "room", "k": k, "n": n, "p": p, "lo": lo, "hi": hi})

    return out


def main() -> None:
    sid_split = load_split()
    all_rows = {m: load_arms(path, sid_split) for m, path in DUMPS.items()}
    results = []
    for m, rows in all_rows.items():
        results.extend(run_model(m, rows, all_rows))

    # note-text baseline numbers from the logged run, for the table
    baseline = {
        "qwen": (39, 55, 0.709),
        "mistral": (47, 55, 0.855),
        "aya": (46, 55, 0.836),
        "gemma": (42, 53, 0.792),
        "falcon": (45, 55, 0.818),
    }

    lines = [
        "# Phase 2 candidates, computable now",
        "",
        "Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*.",
        "",
        "Same dumps and same fit/eval split as `phase2_note_baseline.py`. "
        "Target is the realized public button. Assigned incentive is not a feature. "
        "A missing button is left out.",
        "",
        "| Model | Candidate | Correct | Note-text baseline |",
        "| --- | --- | --- | --- |",
    ]
    for r in results:
        b = baseline.get(r["model"], (0, 0, 0))
        beat = " **" if r["n"] and r["k"] / r["n"] > b[2] else ""
        lines.append(
            f"| {r['model']} | {r['candidate']} | {r['k']}/{r['n']} = {r['p']:.3f} "
            f"[{r['lo']:.3f}, {r['hi']:.3f}]{beat} | {b[0]}/{b[1]} = {b[2]:.3f} |"
        )
    lines += [
        "",
        "A `**` marks a point estimate above the note-text baseline. "
        "Overlapping intervals are not a pass. A pass is a better readout "
        "on the same held-out ids. Not a handover.",
    ]
    Path("results/phase2_candidates.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
