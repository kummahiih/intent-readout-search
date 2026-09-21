# Sensor ledger

Do not collapse attempts.

## OLS topic wipe — 2026-09-21 19:43

`python leace_residual.py --data data/pairs_wide.jsonl`  n=36

```
topic_loo_h=0.83  topic_loo_leftover=0.00
topic_lstsq_leftover=0.64
mean_loto_plan_leftover=0.58
```

Not Belrose LEACE. Linear hallway is gone under official LOO. Plan LOTO 0.58 on n_hold=6 (folds 0.33–0.83). The leftover is topic-blind and still plan-blind. Do not fill $D$.

## Generate then fact-grade — 19:30

gap 1.17 sign 0.46 vs note-only 4.79 / 0.79.

## Contrast / heads / adversary / mutate

scalar topic 0.17. heads LOO 0.79. hold strat 0.53. mutate plan 0.50.
