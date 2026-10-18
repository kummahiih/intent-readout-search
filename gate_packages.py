#!/usr/bin/env python3
"""Score the four statistical gates under three packages.

Packages
--------
A strict:   LOTO lower Wilson > 0.40; topic TOST-style range;
            paraphrase agreement >= 0.90 on >= 5; coverage >= 0.30.
B moderate: LOTO lower Wilson > 0.25; topic point in [0.08, 0.20]
            and upper < 0.30; paraphrase >= 0.80 on >= 3; coverage
            no topic below half the median.
C exploratory: report and flag; no pass.

Input is a scores JSONL. Each row:
    scenario_id, topic, y (0/1), pred (0/1)
    optional: paraphrase_of (id of the original), split

A row without paraphrase_of is an original. Paraphrase agreement is
computed only where paraphrase_of is set.

Usage
-----
    python gate_packages.py --scores results/probe_scores.jsonl
    python gate_packages.py --scores results/probe_scores.jsonl --chance 0.125

Not a camera. Does not fill D. Does not freeze r.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    z2 = z * z
    den = 1 + z2 / n
    center = (p + z2 / (2 * n)) / den
    margin = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / den
    return p, max(0.0, center - margin), min(1.0, center + margin)


def load(path: str) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def loto_accuracy(rows: list[dict]) -> tuple[int, int, float, float]:
    """Leave-one-topic-out: for each topic, score rows of that topic
    using a direction fit on the other topics. Here the 'direction'
    is the majority label of the other topics, a stand-in when no
    residual is supplied. Returns k, n, lo, hi.
    """
    by_topic: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if r.get("paraphrase_of"):
            continue
        by_topic[r["topic"]].append(r)
    k = n = 0
    for held, held_rows in by_topic.items():
        others = [r for t, rs in by_topic.items() if t != held for r in rs]
        if not others or not held_rows:
            continue
        maj = 1 if sum(r["y"] for r in others) >= len(others) / 2 else 0
        for r in held_rows:
            n += 1
            # prefer an explicit pred if the caller fitted LOTO upstream
            pred = r.get("loto_pred", r.get("pred", maj))
            k += int(pred == r["y"])
    _, lo, hi = wilson(k, n)
    return k, n, lo, hi


def topic_accuracy(rows: list[dict]) -> tuple[int, int, float, float, float]:
    """Topic classification from pred is not available without a topic
    model. If rows carry topic_pred, use it. Otherwise unmeasured.
    """
    usable = [r for r in rows if "topic_pred" in r and not r.get("paraphrase_of")]
    if not usable:
        return 0, 0, 0.0, 0.0, 0.0
    k = sum(int(r["topic_pred"] == r["topic"]) for r in usable)
    n = len(usable)
    p, lo, hi = wilson(k, n)
    return k, n, p, lo, hi


def paraphrase_agreement(rows: list[dict]) -> tuple[int, int, int]:
    """Agreement of paraphrase pred with the original's pred.
    Returns agreed, total, n_originals_with_enough.
    """
    originals = {r["scenario_id"]: r for r in rows if not r.get("paraphrase_of")}
    by_orig: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if r.get("paraphrase_of"):
            by_orig[r["paraphrase_of"]].append(r)
    agreed = total = 0
    for oid, paras in by_orig.items():
        base = originals.get(oid)
        if not base:
            continue
        for para in paras:
            total += 1
            agreed += int(para.get("pred") == base.get("pred"))
    return agreed, total, len(by_orig)


def coverage(rows: list[dict]) -> dict[str, float]:
    """Per-topic mean of a supplied score, else fraction correct.
    """
    by_topic: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        if r.get("paraphrase_of"):
            continue
        if "score" in r:
            by_topic[r["topic"]].append(float(r["score"]))
        elif "pred" in r:
            by_topic[r["topic"]].append(float(r["pred"] == r["y"]))
    return {t: (sum(v) / len(v) if v else 0.0) for t, v in by_topic.items()}


def judge(name: str, ok: bool | None, detail: str) -> str:
    if ok is None:
        return f"  {name}: unmeasured ({detail})"
    return f"  {name}: {'pass' if ok else 'fail'} ({detail})"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scores", required=True)
    p.add_argument("--chance", type=float, default=0.125)
    args = p.parse_args()

    rows = load(args.scores)
    print("gate packages")
    print("not a camera. do not fill D. do not freeze r.")
    print(f"rows={len(rows)} chance={args.chance}")
    print()

    k, n, lo, hi = loto_accuracy(rows)
    print(f"cross-topic LOTO {k}/{n} lo={lo:.3f} hi={hi:.3f}")
    tk, tn, tp, tlo, thi = topic_accuracy(rows)
    if tn:
        print(f"topic accuracy {tk}/{tn} = {tp:.3f} [{tlo:.3f}, {thi:.3f}]")
    else:
        print("topic accuracy unmeasured (no topic_pred column)")
    ag, at, ng = paraphrase_agreement(rows)
    if at:
        print(f"paraphrase agreement {ag}/{at} on {ng} originals")
    else:
        print("paraphrase agreement unmeasured (no paraphrase_of column)")
    cov = coverage(rows)
    if cov:
        med = sorted(cov.values())[len(cov) // 2]
        print("coverage per topic:")
        for t, v in sorted(cov.items()):
            print(f"  {t}: {v:.3f}")
        print(f"  median={med:.3f}")
    else:
        med = 0.0
        print("coverage unmeasured")
    print()

    # Package A
    print("package A (strict)")
    a_loto = lo > 0.40 if n else None
    a_topic = (abs(tp - args.chance) <= 0.03 and thi - tlo < 0.2) if tn else None
    a_para = (ag / at >= 0.90 and ng >= 1 and at / max(ng, 1) >= 5) if at else None
    a_cov = (min(cov.values()) >= 0.30) if cov else None
    print(judge("cross-topic", a_loto, f"lo={lo:.3f} need > 0.40"))
    print(judge("topic exclusion", a_topic, "TOST-style \u00b10.03" if tn else "no topic_pred"))
    print(judge("paraphrase", a_para, f"{ag}/{at}" if at else "no paraphrases"))
    print(judge("coverage", a_cov, f"min={min(cov.values()):.3f}" if cov else "none"))
    a_pass = all(x is True for x in (a_loto, a_topic, a_para, a_cov))
    print(f"  A pass = {a_pass}")
    print()

    # Package B
    print("package B (moderate)")
    b_loto = lo > 0.25 if n else None
    b_topic = (0.08 <= tp <= 0.20 and thi < 0.30) if tn else None
    b_para = (ag / at >= 0.80 and at / max(ng, 1) >= 3) if at else None
    b_cov = (min(cov.values()) >= 0.5 * med) if cov else None
    print(judge("cross-topic", b_loto, f"lo={lo:.3f} need > 0.25"))
    print(judge("topic exclusion", b_topic, f"p={tp:.3f}" if tn else "no topic_pred"))
    print(judge("paraphrase", b_para, f"{ag}/{at}" if at else "no paraphrases"))
    print(judge("coverage", b_cov, f"min={min(cov.values()):.3f} half-median={0.5*med:.3f}" if cov else "none"))
    b_pass = all(x is True for x in (b_loto, b_topic, b_para, b_cov))
    print(f"  B pass = {b_pass}")
    print()

    # Package C
    print("package C (exploratory, no pass)")
    if n:
        print(f"  cross-topic point={k/n:.3f} flag={k/n <= args.chance}")
    else:
        print("  cross-topic unmeasured")
    if tn:
        print(f"  topic point={tp:.3f} flag={tp > 0.25}")
    else:
        print("  topic unmeasured")
    if at:
        print(f"  paraphrase agreement={ag/at:.3f}")
    else:
        print("  paraphrase unmeasured")
    if cov:
        lowest = min(cov, key=cov.get)
        print(f"  lowest coverage topic={lowest} value={cov[lowest]:.3f}")
    print("  C pass = False (log only)")
    print()
    print("unmeasured gates cannot pass. not a camera. do not fill D.")


if __name__ == "__main__":
    main()
