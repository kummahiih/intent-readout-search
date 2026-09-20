# Sensor ledger

Do not collapse attempts.

## Verbal intent oracle — 2026-09-21 02:17

`python intent_oracle.py --data data/pairs_wide.jsonl`  Qwen2.5-7B-Instruct  n=24

```
oracle_plan_acc=0.54  oracle_topic_acc=0.71
mean_loto_plan_acc=0.50
hold plan acc: cooking 0.50 hiking 0.50 invoices 0.75 pets 0.50 repairs 0.25 taxes 0.50
```

Forced-choice logprobs. Plan is chance. LOTO plan is chance (invoices 0.75 is n=4). Verbal topic 0.71 is the first topic score well below the linear-h 1.00 — the mouth is a worse hallway reader than last-token $h$, and still not a plan checker. Taxes/repairs often predicted as hiking. Not $z$. Do not fill $D$.

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

See earlier sections below for the tiny-n residual / contrast / adversary / head probes. All official linear topic acc 1.00 except embed. Do not train the hinge.

## Hold-out head rank — 2026-09-21 01:20

In-sample 0.17 gap died on hold-out (gap 0.04, topic acc 1.00).

## CPU inspector

Inspector moves the whole blob honest or liar. Not a Qwen camera.
