#!/usr/bin/env python3
"""Intentional-absence check on the Phase 1 bank.

Hypothesis (from regret-heuristic mdl_intent.md):

    If L_shared(C) < L_ind(C) under a fixed code,
    and a residual probe that could have seen a plan fails to predict
    the button from the note alone,
    and no surface control rescues a camera,
    then the missing readout is recorded as intentional avoidance
    of the shared description, not as the absence of shared structure.

This script computes the description-length side on the scenario file
with zlib, and reads the probe side and the surface controls from the
logged negative handover and the bias/length ledgers.

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

PROBE = {
    "note_only_clears_bar": False,
    "prebutton_clears_bar_only_with_ask": True,
    "ask_removal_controls_fail": True,
    "camera_pass": False,
    "handover_pass": False,
}

SURFACE = {
    "ask_removal": {
        "note_only": "failed to clear note-text bar",
        "end_of_note": "failed",
        "order_swap": "failed",
        "ask_only": "failed",
        "rescues_camera": False,
    },
    "reversed_polarity": {
        "source": "results/reverted_combine_2026-10-18.md",
        "qwen_yes_rate": 0.00,
        "mistral_yes_rate": 0.06,
        "aya_yes_rate": 0.50,
        "gemma_yes_rate": 0.31,
        "falcon_yes_rate": 0.38,
        "rescues_camera": False,
        "note": "yes-bias on Aya/Gemma/Falcon; Qwen/Mistral near zero",
    },
    "length": {
        "handwritten_long_lie": "3/23 vs 4/23 short; one row, not a length effect",
        "prop_padded": "known set collapsed (Qwen 4/159); control failed its own condition",
        "rescues_camera": False,
    },
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
    p.add_argument("--control", default="data/scenarios_reworded_control.jsonl",
                   help="reworded surface control; empty string to skip")
    args = p.parse_args()

    rows = load(args.data)
    by_id: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_id[r["scenario_id"]].append(r)

    ratios = []
    for sid, group in by_id.items():
        hide = [r for r in group if r.get("incentive") == "hide"]
        name = [r for r in group if r.get("incentive") == "name"]
        if hide and name:
            ratios.append(pair_ratio(hide[0]["note"], name[0]["note"]))

    n_pairs = len(ratios)
    n_shared = sum(1 for r in ratios if r > args.threshold)
    mean_r = sum(ratios) / n_pairs if n_pairs else 0.0

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
    if args.control:
        try:
            crow = load(args.control)
            cby = defaultdict(list)
            for r in crow:
                cby[r["scenario_id"]].append(r)
            cratios = []
            for sid, group in cby.items():
                hide = [r for r in group if r.get("incentive") == "hide"]
                name = [r for r in group if r.get("incentive") == "name"]
                if hide and name:
                    cratios.append(pair_ratio(hide[0]["note"], name[0]["note"]))
            if cratios:
                cmean = sum(cratios) / len(cratios)
                print(f"  reworded-control mean R = {cmean:.3f}  (original {mean_r:.3f})")
                print(f"  drop = {mean_r - cmean:.3f}")
                print("  note: on short strings zlib R > 1.05 even for unrelated text")
        except FileNotFoundError:
            print(f"  control file not found: {args.control}")
    print()
    print("probe side (logged negative handover)")
    for k, v in PROBE.items():
        print(f"  {k} = {v}")
    capable_probe_finds_none_from_note = (
        not PROBE["note_only_clears_bar"] and PROBE["ask_removal_controls_fail"]
    )
    print(f"  capable_probe_finds_none_from_note = {capable_probe_finds_none_from_note}")
    print()
    print("surface controls (logged)")
    for name, block in SURFACE.items():
        rescues = block.get("rescues_camera", False)
        print(f"  {name}: rescues_camera = {rescues}")
        for k, v in block.items():
            if k != "rescues_camera":
                print(f"    {k}: {v}")
    surface_rescues = any(b.get("rescues_camera") for b in SURFACE.values())
    print(f"  any_surface_control_rescues_camera = {surface_rescues}")
    print()
    intentional = mdl_supports and capable_probe_finds_none_from_note and not surface_rescues
    print(f"intentional_absence = {intentional}")
    print()
    print("boundaries")
    print("  code fixed before probe: zlib, threshold from CLI")
    print("  probe is the logged note-only / ask-removal result, not a new fit")
    print("  surface controls are the logged ask-removal, reversed-polarity, and length results")
    print("  chance cross under random-intent null: not measured here")
    print("  this log does not override the negative handover")
    print("  cameraPass remains no; handoverPass remains no")
    print()
    print("faults in this check (see regret-heuristic mdl_intent.md)")
    print("  1. shared compression is true by construction: hide/name notes share the proposition")
    print("  2. the capable probe is the note-only result, already known to be blind to a plan")
    print("  3. the verdict cannot fail on this bank: probe side hardcoded, length side guaranteed")
    print("  intentional_absence above is not evidence that the absence is intentional")


if __name__ == "__main__":
    main()
