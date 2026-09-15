#!/usr/bin/env python3
"""Pareto front on the synthetic risk frontier. CPU. Not Qwen.

Objectives (better =):
  task_acc  maximize
  risk      p_lie_D + p_lie_out   minimize   (true deceptive action)
  hinge     minimize               (detector on frozen D)

Sweep lambda x {held-out closed, open}. One scalar lambda is one point, not the front.
"""

from __future__ import annotations

import argparse

import torch

from synthetic_z import eval_net, train_one


def dominates(a: dict, b: dict) -> bool:
    ge = a["task_acc"] >= b["task_acc"] - 1e-9
    le_r = a["risk"] <= b["risk"] + 1e-9
    le_h = a["hinge"] <= b["hinge"] + 1e-9
    gt = (
        a["task_acc"] > b["task_acc"] + 1e-9
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
    out.sort(key=lambda r: (r["risk"], -r["task_acc"], r["hinge"]))
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=200)
    p.add_argument("--bonus", type=float, default=0.6)
    p.add_argument("--tau", type=float, default=0.3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--noise", type=float, default=0.2)
    args = p.parse_args()
    device = torch.device("cpu")
    print("=== risk frontier (task, lie-rate, hinge). CPU. ===")
    print(
        f"steps={args.steps} bonus={args.bonus} tau={args.tau} "
        f"seed={args.seed} noise={args.noise}"
    )
    _, D = train_one(
        "baseline",
        args.steps,
        args.bonus,
        0.0,
        args.tau,
        False,
        None,
        args.noise,
        args.seed,
        device,
    )
    lams = [0.0, 0.5, 1.0, 2.0, 4.0]
    points = []
    i = 0
    for allow in (False, True):
        for lam in lams:
            net, _ = train_one(
                "hinge" if not allow else "evade",
                args.steps,
                args.bonus,
                lam,
                args.tau,
                allow,
                D,
                args.noise,
                args.seed + 1 + i,
                device,
            )
            m = eval_net(net, D, args.tau, allow, device)
            rec = {
                "allow_out": int(allow),
                "lam": lam,
                "task_acc": m["task_acc"],
                "risk": m["p_lie_D"] + m["p_lie_out"],
                "hinge": m["hinge"],
                "p_lie_D": m["p_lie_D"],
                "p_lie_out": m["p_lie_out"],
            }
            points.append(rec)
            print(
                f"out={allow} lam={lam:.1f}  task={rec['task_acc']:.3f}  "
                f"risk={rec['risk']:.3f}  hinge={rec['hinge']:.3f}  "
                f"lie_D={rec['p_lie_D']:.3f} lie_out={rec['p_lie_out']:.3f}"
            )
            i += 1
    F = front(points)
    print("--- non-dominated ---")
    for rec in F:
        print(
            f"out={bool(rec['allow_out'])} lam={rec['lam']:.1f}  "
            f"task={rec['task_acc']:.3f}  risk={rec['risk']:.3f}  hinge={rec['hinge']:.3f}"
        )
    print("A single lambda is one point on this table, not the frontier.")
    print("Not Qwen. Risk is true lie action, not u and not p(lie) of a sentence.")


if __name__ == "__main__":
    main()
