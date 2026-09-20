#!/usr/bin/env python3
"""Run the B0 probes on pairs_wide.jsonl. Append stdout to results/overnight_b0.md.

Does not train a hinge. Does not fill D. GPU required.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "pairs_wide.jsonl"
OUT = ROOT / "results" / "overnight_b0.md"
SLICE = ROOT / "data" / "_overnight_two_topic.jsonl"

JOBS = [
    ["python", "topic_residual.py", "--data", str(SLICE), "--sweep"],
    ["python", "pair_contrast.py", "--data", str(DATA)],
    ["python", "pair_adversary.py", "--data", str(DATA)],
    ["python", "head_write_probe.py", "--data", str(DATA)],
    ["python", "head_write_probe.py", "--data", str(DATA), "--quiet"],
    ["python", "head_ablate_probe.py", "--data", str(DATA)],
    ["python", "head_ablate_probe.py", "--data", str(DATA), "--holdout"],
]


def two_topic_slice(src: Path, dest: Path, a: str, b: str) -> None:
    rows = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
    keep = [r for r in rows if r.get("topic") in {a, b}]
    dest.write_text("".join(json.dumps(r) + "\n" for r in keep))


def run_job(cmd: list[str], log: Path) -> int:
    title = " ".join(cmd)
    started = datetime.now(timezone.utc).isoformat()
    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"\n## {title}\n\nstarted {started}\n\n```\n")
        fh.flush()
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        fh.write(proc.stdout or "")
        fh.write(f"\n```\n\nexit {proc.returncode}\n")
    return proc.returncode


def main() -> int:
    if not DATA.exists():
        print(f"ERROR: missing {DATA}", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    two_topic_slice(DATA, SLICE, "invoices", "hiking")
    header = (
        f"# Overnight B0\n\n"
        f"started {datetime.now(timezone.utc).isoformat()}\n"
        f"data {DATA.relative_to(ROOT)}\n"
        f"two-topic slice invoices+hiking for topic_residual only\n"
    )
    if not OUT.exists():
        OUT.write_text(header, encoding="utf-8")
    else:
        OUT.write_text(OUT.read_text(encoding="utf-8") + "\n---\n\n" + header, encoding="utf-8")
    failed = []
    for cmd in JOBS:
        print("RUN", " ".join(cmd), flush=True)
        code = run_job(cmd, OUT)
        print("exit", code, flush=True)
        if code != 0:
            failed.append((cmd, code))
    with OUT.open("a", encoding="utf-8") as fh:
        fh.write("\n## summary\n\n")
        if failed:
            for cmd, code in failed:
                fh.write(f"- FAIL {code}: {' '.join(cmd)}\n")
        else:
            fh.write("- all jobs exit 0\n")
        fh.write(f"\nfinished {datetime.now(timezone.utc).isoformat()}\n")
    if SLICE.exists():
        SLICE.unlink()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
