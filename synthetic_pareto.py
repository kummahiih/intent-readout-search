#!/usr/bin/env python3
"""Pareto front: realized task pay vs lie-rate vs hinge. CPU."""

from __future__ import annotations

import argparse

import torch

from synthetic_z import eval_net, train_one


def dominates(a: dict, b: dict) -> bool:
    ge = a["task_pay"] >= b["task_pay"] - 1e-9
    le_r = a["risk"] <= b["risk"] + 1e-9
    le_h = a["hinge"] <= b["hinge"] + 1e-9
    gt = (
        a["task_pay"] > b["task_pay"] + 1e-9
        or a["risk"] < b["risk"] - 1e-9
        or a["hinge"] < b["hinge"] - 1e-9
    )
    return ge and le_r and le_h and gt


def front(points: list[dict]) -> list[dict]:
    out = []
    for p in points:
        if any(dominates(q, p) for q in points if q is not p):
            continue
        out.append(p)
    out.sort(key=lambda r: (r["risk"], -r["task_pay"], r["hinge"]))
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=200)
    p.add_argument("--bonus", type=float, default=0.6)
    p.add_argument("--tau", type=float, default=0.3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--noise", type=float, default=0.2)
    p.add_argument("--inspect", type=float, default=0.5)
    args = p.parse_args()
    device = torch.device("cpu")
    print("=== risk frontier (pay, lie-rate, hinge). Inspector on. ===")
    print(
        f"steps={args.steps} bonus={args.bonus} tau={args.tau} "
        f"seed={args.seed} noise={args.noise} inspect={args.inspect}"
    )
    _, D = train_one(
        "baseline", args.steps, args.bonus, 0.0, args.tau, False, None,
        args.noise, args.seed, device, inspect=args.inspect,
    )
    lams = [0.0, 0.5, 1.0, 2.0, 4.0]
    points = []
    i = 0
    for allow in (False, True):
        for lam in lams:
            net, _ = train_one(
                "hinge" if not allow else "evade",
                args.steps, args.bonus, lam, args.tau, allow, D,
                args.noise, args.seed + 1 + i, device, inspect=args.inspect,
            )
            m = eval_net(net, D, args.tau, allow, device, inspect=args.inspect)
            rec = {
                "allow_out": int(allow),
                "lam": lam,
                "task_pay": m["task_pay"],
                "task_skill": m["task_skill"],
                "risk": m["p_lie_D"] + m["p_lie_out"],
                "hinge": m["hinge"],
                "p_lie_D": m["p_lie_D"],
                "p_lie_out": m["p_lie_out"],
            }
            points.append(rec)
            print(
                f"out={allow} lam={lam:.1f}  pay={rec['task_pay']:.3f}  "
                f"skill={rec['task_skill']:.3f}  risk={rec['risk']:.3f}  "
                f"hinge={rec['hinge']:.3f}  lie_D={rec['p_lie_D']:.3f} "
                f"lie_out={rec['p_lie_out']:.3f}"
            )
            i += 1
    F = front(points)
    print("--- non-dominated ---")
    for rec in F:
        print(
            f"out={bool(rec['allow_out'])} lam={rec['lam']:.1f}  "
            f"pay={rec['task_pay']:.3f}  risk={rec['risk']:.3f}  hinge={rec['hinge']:.3f}"
        )
    print("pay is realized task under inspector, not topic-skill.")
    print("Not Qwen.")


if __name__ == "__main__":
    main()
