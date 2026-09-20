# Sensor ledger

Do not collapse attempts.

## B0 default camera: topic-subtract residual

`python topic_residual.py`

$r(h)=h-(h\cdot v)v$ with $v$ from the two-topic bank. Not LEACE. Not a trained adversary.

Already on the ledger: topic acc 1.00 after the subtract, strategy |gap| ~ 0. Failed B0.
Packing: one axis cut does not unmix plan from hallway. Lean cartoon next door: `no_two_orthogonal_units_on_real`.

Do not train the hinge on this $r$. Do not invent a third residual until this number is re-run or a different probe is named.

## Qwen identity / paraphrase / residual

Topic acc 1.00, |gap|~0. Failed.

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
