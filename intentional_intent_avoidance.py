#!/usr/bin/env python3
"""Intentional intent avoidance detection.

Judges when a collection of individual cases becomes shorter under a
shared-intent description than under independent cases, even though the
current protocol (cameraPass / handoverPass) says no strategy camera
exists on this bank.

This is a description-length diagnostic. It is not a camera, it does not
fill D, and it does not freeze r. Parent note:
https://github.com/kummahiih/regret-heuristic/blob/main/mdl_intent.md

Model (from the parent MDL note):

    L_independent(n) = a * n
    L_shared(n)      = b + c * n

Shared is shorter once n > b / (a - c), provided a > c.

a = per-case cost of listing the case alone
b = fixed cost of the shared program (the intent)
c = per-case residual cost once the shared program is known

Usage
-----
    python intentional_intent_avoidance.py --n 12 --a 8 --b 40 --c 3
    python intentional_intent_avoidance.py --cases 5 6 4 7 5 --b 30 --c 2

The second form estimates a from the mean of the supplied case lengths.
"""

from __future__ import annotations

import argparse
import sys


def length_independent(a: float, n: float) -> float:
    return a * n


def length_shared(b: float, c: float, n: float) -> float:
    return b + c * n


def crossover(a: float, b: float, c: float) -> float | None:
    if a <= c:
        return None
    return b / (a - c)


def prefers_shared(a: float, b: float, c: float, n: float) -> bool:
    return length_shared(b, c, n) < length_independent(a, n)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Intentional intent avoidance detection (MDL crossover)."
    )
    p.add_argument("--n", type=float, default=None, help="number of cases")
    p.add_argument(
        "--cases",
        type=float,
        nargs="*",
        default=None,
        help="optional list of individual case description lengths; a is their mean",
    )
    p.add_argument("--a", type=float, default=None, help="per-case independent cost")
    p.add_argument("--b", type=float, required=True, help="fixed cost of shared intent")
    p.add_argument("--c", type=float, required=True, help="per-case residual under shared intent")
    args = p.parse_args()

    if args.cases:
        n = float(len(args.cases))
        a = sum(args.cases) / n
        case_note = f"a estimated as mean of {len(args.cases)} case lengths"
    elif args.n is not None and args.a is not None:
        n = args.n
        a = args.a
        case_note = "a supplied"
    else:
        p.error("supply either --n and --a, or --cases")

    b, c = args.b, args.c
    lind = length_independent(a, n)
    lsh = length_shared(b, c, n)
    thr = crossover(a, b, c)
    pref = prefers_shared(a, b, c, n)

    print("intentional intent avoidance detection")
    print("diagnostic only; not a camera; do not fill D; do not freeze r")
    print(f"n = {n:g}  a = {a:g}  b = {b:g}  c = {c:g}  ({case_note})")
    print(f"L_independent = {lind:g}")
    print(f"L_shared      = {lsh:g}")
    if thr is None:
        print("crossover = undefined (a <= c; shared never compresses)")
    else:
        print(f"crossover n > {thr:g}")
    print(f"prefers_shared = {pref}")
    print("protocol_says_no_camera = true  (cameraPass no, handoverPass no)")
    print("this_log_does_not_override_protocol = true")
    return 0


if __name__ == "__main__":
    sys.exit(main())
