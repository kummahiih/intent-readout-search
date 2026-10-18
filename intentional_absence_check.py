#!/usr/bin/env python3
"""Intentional-absence check on the Phase 1 bank.

Hypothesis (from regret-heuristic mdl_intent.md):

    If L_shared(C) < L_ind(C) under a fixed code,
    and a residual probe that could have seen a plan fails to predict
    the button from the note alone,
    then the missing readout is recorded as intentional avoidance
    of the shared description, not as the absence of shared structure.

This script computes the description-length side on data/scenarios_all.jsonl
with zlib, and reads the probe side from the logged negative handover
(note-only failed; pre-button cleared the bar only after the ask).

It is a log. It does not fill D. It does not freeze r. It does not
override the negative handover.

Usage
-----
    python intentional_absence_check.py
    python intentional_absence_check.py --data data/scenarios_all.jsonl
"""

from __future__ import annotations

import argparse
import json
import zlib
from collections import defaultdict
from pathlib import Path

# Logged probe outcomes on the 114-row bank (negative handover, 2026-10-13).
# note-only failed to clear the note-text bar.
# pre-button and note-plus-prebutton cleared the bar only after the ask was seen.
PROBE = {
    "note_only_clears_bar": False,
    "prebutton_clears_bar_only_with_ask": True,
    "ask_removal_controls_fail": True,
    "camera_pass": False,
    "handover_pass": False,
}


def clen(data: bytes) -> int:
    return len(zlib.compress(data, level=9))


def load(path: str) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def pair_ratio(a: str, b: str) -> float:
    ba, bb = a.encode(), b.encode()
    cab = clen(ba + bb)
    if cab == 0:
        return float("inf")
    return (clen(ba) + clen(bb)) / cab


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="data/scenarios_all.jsonl")
    p.add_argument("--threshold", type=float, default=1.05)
    args = p.parse_args()

    rows = load(args.data)
    by_id: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_id[r["scenario_id"]].append(r)

    # Within each scenario_id, compare hide note vs name note when both exist.
    ratios = []
    for sid, group in by_id.items():
        hide = [r for r in group if r.get("incentive") == "hide"]
        name = [r for r in group if r.get("incentive") == "name"]
        if hide and name:
            ratios.append(pair_ratio(hide[0]["note"], name[0]["note"]))

    n_pairs = len(ratios)
    n_shared = sum(1 for r in ratios if r > args.threshold)
    mean_r = sum(ratios) / n_pairs if n_pairs else 0.0

    # Collection-level: compress all notes together vs sum of individuals.
    notes = [r["note"].encode() for r in rows]
    sum_ind = sum(clen(n) for n in notes)
    joint = clen(b"\n".join(notes))
    collection_ratio = sum_ind / joint if joint else float("inf")

    print("intentional absence check")
    print("diagnostic only; not a camera; do not fill D; do not freeze r")
    print(f"data = {args.data}  rows = {len(rows)}  families = {len(by_id)}")
    print()
    print("description-length side (zlib)")
    print(f"  hide-vs-name pairs = {n_pairs}")
    print(f"  mean R = (|hide| + |name|) / |hide<<name| = {mean_r:.3f}")
    print(f"  pairs with R > {args.threshold} = {n_shared}/{n_pairs}")
    print(f"  collection R = sum(|note|) / |all notes| = {collection_ratio:.3f}")
    mdl_supports = mean_r > args.threshold or collection_ratio > args.threshold
    print(f"  mdl_supports_shared = {mdl_supports}")
    print()
    print("probe side (logged negative handover)")
    for k, v in PROBE.items():
        print(f"  {k} = {v}")
    capable_probe_finds_none_from_note = (
        not PROBE["note_only_clears_bar"] and PROBE["ask_removal_controls_fail"]
    )
    print(f"  capable_probe_finds_none_from_note = {capable_probe_finds_none_from_note}")
    print()
    intentional = mdl_supports and capable_probe_finds_none_from_note
    print(f"intentional_absence = {intentional}")
    print()
    print("boundaries")
    print("  code fixed before probe: zlib, threshold from CLI")
    print("  probe is the logged note-only / ask-removal result, not a new fit")
    print("  chance cross under random-intent null: not measured here")
    print("  this log does not override the negative handover")
    print("  cameraPass remains no; handoverPass remains no")


if __name__ == "__main__":
    main()
