#!/usr/bin/env python3
"""Build a scores JSONL for gate_packages.py from a scenario dump.

Uses the public-arm button as y. If the dump has no probe prediction,
pred is left unset and the scorer will mark probe gates unmeasured.
Pass --pred-from-button only for a smoke test; that is not a probe.

Usage
-----
    python build_probe_scores.py \\
        --dump results/scenario_qwen_2026-10-12-0031.jsonl \\
        --out results/probe_scores.jsonl
"""

from __future__ import annotations

import argparse
import json


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dump", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--pred-from-button", action="store_true",
                   help="smoke test only: copy button into pred")
    args = p.parse_args()

    n = 0
    with open(args.dump) as f, open(args.out, "w") as out:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            if d.get("arm") != "public":
                continue
            if d.get("button") not in ("YES", "NO"):
                continue
            row = {
                "scenario_id": d["scenario_id"],
                "topic": d.get("topic", "unknown"),
                "split": d.get("split", "unknown"),
                "y": 1 if d["button"] == "YES" else 0,
            }
            if args.pred_from_button:
                row["pred"] = row["y"]
            out.write(json.dumps(row) + "\n")
            n += 1
    print(f"wrote {n} rows to {args.out}")
    if args.pred_from_button:
        print("pred copied from button. smoke test. not a probe.")
    else:
        print("no pred column. probe gates will be unmeasured.")


if __name__ == "__main__":
    main()
