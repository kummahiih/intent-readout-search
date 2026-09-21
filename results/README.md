# Sensor ledger

Do not collapse attempts.

## Contrast on scalar s=h·v — 2026-09-21 16:43

`python pair_contrast.py --data data/pairs_wide.jsonl`  n=36

```
mean s_v dec=-0.002 hon=-0.028 gap_dec_minus_hon=0.026
topic_lstsq_on_scalar=0.31  topic_loo_on_scalar=0.17
```

Official topic gate on the 1-d score is chance (~1/6). The old 0.81 on $(h\cdot v)v$ was fold identity. Topic-blind, plan-blind. Not a camera. Do not fill $D$.

## Loud heads, official LOO topic — 2026-09-21 16:35

lstsq 1.00 / loo heads 0.79 layer 0.62 / gap -0.038. Topic still in head writes. No plan.

## Adversary argmax — 2026-09-21 16:27

hold strat 0.53 old 0.50. Chance.
