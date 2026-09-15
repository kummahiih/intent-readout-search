# Sensor ledger

Do not collapse attempts. A drop in cosine is not reduced deception.

## Identity / paraphrase / residual (Qwen)

See prior rows. Topic acc 1.00, |gap|~0. Failed.

## CPU synthetic_z seed 0

Hinge 0 with lie_D still 1 (mask) or lie_out 0.75 (open). Task 1.

## CPU Pareto seed 0, steps 200, noise 0.2 — 2026-09-16

`python synthetic_pareto.py --steps 200 --seed 0`

Axes: max task, min risk=P(lie_D or lie_out), min hinge.

Every lambda, held-out closed or open: **task=1.000 risk=1.000**. Hinge 0 except one open/lam=0 point (0.099).
Front is degenerate: lying does not cost the task, so there is no task–risk tradeoff to pick a lambda on.

A risk frontier needs an env where honesty and task compete. This toy does not. Not Qwen.
