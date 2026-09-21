# Sensor ledger

Do not collapse attempts.

## Loud heads, official LOO topic — 2026-09-21 16:35

`python head_write_probe.py --data data/pairs_wide.jsonl`  layer 14  heads 15,22,23,25  n=24

```
topic_lstsq_head_r=1.00  topic_lstsq_layer_h=1.00
topic_loo_head_r=0.79    topic_loo_layer_h=0.62
gap_hon_minus_dec=-0.038
```

Lstsq 1.00 is the memorizer. Official LOO: heads 0.79, full layer 0.62. Six-way chance is ~0.17, so topic is still in $r$, just not perfect. Strategy gap ~0. Not a camera. Do not fill $D$.

## Adversary argmax — 2026-09-21 16:27

mean_strat_acc_hold=0.53 old=0.50 train topic 0.79. Broken threshold fixed; hold still chance.

## Activation patch / oracle / mutate

Patch bleed 0. Oracle plan 0.54 miss-slice 0.43. Mutate confusion. Do not fill $D$.
