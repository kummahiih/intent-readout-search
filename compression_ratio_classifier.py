#!/usr/bin/env python3
"""Compression-ratio classifier for shared structure.

Computes the ratio

    R(a, b) = (|a| + |b|) / |a << b|

where |x| is the length of x after compression and << is concatenation.

Interpretation (diagnostic only):

- R ≈ 1 : little shared structure (concatenation does not compress better than the sum).
- R > 1 : the concatenation compressed better; shared description is present.
- Larger R means more shared structure under the compressor.

This is a practical approximation to the MDL / Kolmogorov idea that a shared
intent is a short program that makes the joint description shorter. It is not a
camera, does not fill D, and does not freeze r. The current protocol still says
no strategy camera on this bank.

Related: Normalized Compression Distance (Cilibrasi & Vitányi) is

    NCD(a, b) = (|a<<b| - min(|a|, |b|)) / max(|a|, |b|)

R and NCD both rise or fall with shared structure; they are different normalizations.

Usage
-----
    python compression_ratio_classifier.py --a "note one" --b "note two"
    python compression_ratio_classifier.py --files case1.txt case2.txt case3.txt
    echo -e "hide the rain\nhide the rain tomorrow" | python compression_ratio_classifier.py --stdin

Requires only the standard library (zlib).
"""

from __future__ import annotations

import argparse
import sys
import zlib
from pathlib import Path


def compressed_len(data: bytes) -> int:
    """Length in bytes of zlib-compressed data."""
    return len(zlib.compress(data, level=9))


def ratio(a: bytes, b: bytes) -> float:
    """(|a| + |b|) / |a << b|."""
    ca = compressed_len(a)
    cb = compressed_len(b)
    cab = compressed_len(a + b)
    if cab == 0:
        return float("inf")
    return (ca + cb) / cab


def ncd(a: bytes, b: bytes) -> float:
    """Normalized compression distance for reference."""
    ca = compressed_len(a)
    cb = compressed_len(b)
    cab = compressed_len(a + b)
    return (cab - min(ca, cb)) / max(ca, cb) if max(ca, cb) else 0.0


def main() -> int:
    p = argparse.ArgumentParser(description="Compression-ratio shared-structure classifier.")
    p.add_argument("--a", type=str, default=None, help="first string")
    p.add_argument("--b", type=str, default=None, help="second string")
    p.add_argument("--files", type=str, nargs="*", default=None, help="files to pair")
    p.add_argument("--stdin", action="store_true", help="read lines from stdin as cases")
    p.add_argument("--threshold", type=float, default=1.05, help="R above this flags shared structure")
    args = p.parse_args()

    pairs: list[tuple[bytes, bytes, str]] = []

    if args.a is not None and args.b is not None:
        pairs.append((args.a.encode(), args.b.encode(), "cli"))
    elif args.files and len(args.files) >= 2:
        texts = [Path(f).read_bytes() for f in args.files]
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                pairs.append((texts[i], texts[j], f"{args.files[i]}<<{args.files[j]}"))
    elif args.stdin:
        lines = [ln.encode() for ln in sys.stdin.read().splitlines() if ln.strip()]
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                pairs.append((lines[i], lines[j], f"line{i}<<line{j}"))
    else:
        p.error("supply --a and --b, or --files, or --stdin")

    print("compression ratio classifier  R = (|a| + |b|) / |a<<b|")
    print("diagnostic only; not a camera; do not fill D; do not freeze r")
    print(f"shared_structure_threshold = {args.threshold}")
    print()

    for a, b, label in pairs:
        r = ratio(a, b)
        d = ncd(a, b)
        flag = "shared" if r > args.threshold else "independent"
        print(f"{label}: R = {r:.4f}  NCD = {d:.4f}  call = {flag}")

    print()
    print("protocol_says_no_camera = true")
    print("this_log_does_not_override_protocol = true")
    return 0


if __name__ == "__main__":
    sys.exit(main())
