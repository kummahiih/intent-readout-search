# Sensor ledger

Do not collapse attempts.

## Verbal oracle chat template — 2026-09-21 19:53

`python intent_oracle.py --data data/pairs_wide.jsonl`  n=24

```
oracle_plan_acc=0.50  oracle_topic_acc=0.67
plan_acc_topic_miss=0.62 n_miss=8  plan_acc_topic_hit=0.44
mean_loto_plan_acc=0.79
```

Every row printed `pred_plan=deceptive` (m_plan +5 to +17). Plan 0.50 is the always-deceptive baseline. LOTO 0.79 is a threshold on four rows, not a camera. Raw-prompt plan was 0.54 / miss 0.43. Chat wrap did not find plan; it collapsed to one word. Do not fill $D$.

## Generate / notes fact-judge / OLS wipe

notes chat 11.46/0.92. generated chat 6.46/0.58. leftover topic 0.00 plan LOTO 0.58.
