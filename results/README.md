# Sensor ledger

Do not collapse attempts.

## Verbal intent oracle — 2026-09-21 02:17

`python intent_oracle.py --data data/pairs_wide.jsonl`  Qwen2.5-7B-Instruct  n=24

```
oracle_plan_acc=0.54  oracle_topic_acc=0.71
mean_loto_plan_acc=0.50
hold plan acc: cooking 0.50 hiking 0.50 invoices 0.75 pets 0.50 repairs 0.25 taxes 0.50
```

Forced-choice logprobs. Plan is chance. LOTO plan is chance (invoices 0.75 is n=4). Verbal topic 0.71 is the first topic score well below the linear-$h$ 1.00 — the mouth is a worse hallway reader than last-token $h$, and still not a plan checker. Taxes/repairs often predicted as hiking. Not $z$. Do not fill $D$.

## Overnight wide pairs — 2026-09-21 01:27

`python overnight_b0.py`  `data/pairs_wide.jsonl`  6 topics  n_eval=24  raw log: [overnight_b0.md](overnight_b0.md)

| job | topic | strategy gap | note |
| --- | --- | --- | --- |
| residual sweep invoices+hiking n=8 | 1.00 from layer 7 on | \|gap\|\le0.05 | embed 0.50 is missing axis |
| pair_contrast n=36 | 0.81 on LOTO r | 0.026 | still overlap |
| pair_adversary dim=8 | train topic mean **0.79** | hold strat **0.50** every topic | 6-way topic got harder; plan still chance |
| loud heads 15,22,23,25 | **1.00** | -0.038 | same heads as tiny set |
| quiet heads 0,2,3,5 | **1.00** | -0.045 | still hugs bank |
| ablate in-sample heads 4,5,7,19 | lstsq **1.00** / loo 0.29 | -0.052 | loo low, selected on eval |
| ablate holdout heads 9,15,18,20 | lstsq **1.00** / loo 0.54 | -0.024 | flicker gone |

More handmade topics did not make a camera. Linear B0 still fails on every head/residual cut. The adversary’s train topic acc dropping below 1.00 is 6-class difficulty, not a strategy sensor. Do not fill $D$. Do not train the hinge on these $r$.

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

## Same-topic contrast — 2026-09-20 20:40

`python pair_contrast.py`

Load-bearing number: strategy gap **0.008**. Failed B0 as a strategy camera. Do not train the hinge on this $r$.

## Same-topic contrast, three topics — 2026-09-20 20:45

Gap ~0.05–0.06. Topic acc on LOTO $r$ 0.69–0.77. Failed B0.

## Topic adversary — 2026-09-20 20:48

Train topic acc **1.00**; hold strategy acc chance. Failed B0.

## Mid-layer head writes — 2026-09-21 01:06

Loud heads 15,22,23,25. Topic acc 1.00. Gap -0.018. Failed B0.

## Quiet mid-layer head writes — 2026-09-21 01:12

Heads 0,2,3,5. Topic acc 1.00. Gap -0.071. Failed B0.

## Mean-ablate then subset — 2026-09-21 01:15

Picked 2,8,10,18 in-sample. lstsq topic 1.00, loo 0.43, gap 0.17 selected on the same seven rows.

## Hold-out head rank — 2026-09-21 01:20

Picked 15,18,19,20. Topic acc 1.00, loo 0.71, gap 0.036. Flicker died.

## CPU inspector

`--inspect 0`: skill 1 risk 1 hinge 0. Gaming.
Inspector 0.5: whole blob honest. Inspector 0.25: whole blob liar. Not a Qwen camera.
