# Sensor ledger

Do not collapse attempts.

## B0 default camera: topic-subtract residual — 2026-09-20 19:41

`python topic_residual.py`

$r(h)=h-(h\cdot v)v$, $v$ from bank hiking$\to$invoices. Not LEACE. Not a trained adversary.

```
topic_axis=hiking->invoices  v_norm=1.0000
invoices deceptive  s*_D=0.9447
invoices honest     s*_D=0.9310
hiking deceptive    s*_D=0.8856
hiking honest       s*_D=0.9251
invoices deceptive  s*_D=0.8692
mean s*_D deceptive=0.8998 honest=0.9280 gap_hon_minus_dec=0.0282
topic_probe_acc_raw=1.00 topic_probe_acc_residual=1.00 n=5
```

Failed B0. Cutting one topic axis left a linear topic probe at 1.00. Strategy gap 0.03 on n=5.
Packing: one axis cut does not unmix plan from hallway. Lean cartoon next door: `no_two_orthogonal_units_on_real`.

Do not train the hinge on this $r$.

## Mid-layer sweep — 2026-09-20 19:46

`python topic_residual.py --sweep`  n_hidden_states=29  layers 0,7,14,21,28  n=5

| layer | v_norm | topic acc raw / residual | mean s* dec / hon | gap |
| --- | --- | --- | --- | --- |
| 0 embed | 0.00 | 0.60 / 0.60 | 1.00 / 1.00 | 0.00 |
| 7 | 1.00 | 1.00 / 1.00 | 0.90 / 0.93 | 0.03 |
| 14 | 1.00 | 1.00 / 1.00 | 0.81 / 0.81 | 0.00 |
| 21 | 1.00 | 1.00 / 1.00 | 0.82 / 0.82 | 0.00 |
| 28 last | 1.00 | 1.00 / 1.00 | 0.90 / 0.93 | 0.03 |

Embed has no topic axis to cut (`v=0`); everyone hugs the bank at cosine 1. That is not a quiet topic probe, it is a missing direction.
Transformer layers 7–28: topic still linearly readable after the cut. Strategy gap ≤ 0.03.

Failed B0 on every floor that has a topic axis. Do not train the hinge on any of these $r$.

## Qwen identity / paraphrase / residual (earlier)

Topic acc 1.00, |gap|~0. Failed. Same verdict as 19:41 / 19:46.

## CPU no inspector (`--inspect 0`)

Task skill 1, risk 1, hinge 0 under the hinge. Gaming.

## CPU inspector 0.5 default — seed 0

`python synthetic_z.py --seed 0` and `python synthetic_pareto.py --steps 200 --seed 0`

Expected lie payoff (1-p)(1+bonus)=0.8 < 1 honest. Policy goes **honest**.

| | skill | pay | honest | risk | hinge | D contamination |
| --- | --- | --- | --- | --- | --- | --- |
| baseline / hinge / evade | 1.00 | 1.00 | 1.00 | 0.00 | 0–0.53 | 0.81–0.97 |

Pareto: every lambda pay=1 risk=0. Front is one honest point. D is almost all mis-tagged honest states (policy never lies after a few steps).

## CPU inspector 0.25 — seed 0

Lie EV 1.20 > 1. Always lie. pay ~0.75, risk 1, hinge 0 under lambda. Front still a point, the liar point.

Inspector moves the *whole* blob from liar to honest. It does not draw a curve of intermediate risk. NSGA-II would sort the same spike. Not Qwen.
