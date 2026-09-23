# Sensor ledger

Do not collapse attempts.

## Contrast scalar LOTO — 2026-09-23 20:20

`python pair_contrast.py --data data/pairs_wide.jsonl`  n=36, 6 topics, pool=last layer=-1

```
mean s_v deceptive=-0.0017 honest=-0.0277 gap_dec_minus_hon=0.0260
topic_lstsq_on_scalar=0.31 topic_loo_cos_on_scalar=0.17 topic_loo_l2_on_scalar=0.31
```

Official topic gate is L2 0.31 (chance ~0.17). Plan gap 0.026. Not a camera.

## Contrast mean-pool last layer — 2026-09-23 21:49

`--pool mean --layer -1`  n=36

```
gap_dec_minus_hon=0.0297  topic_loo_l2_on_scalar=0.22
```

Fail.

## Contrast last-token mid layer — 2026-09-23 21:50

`--pool last --layer 16`  n=36

```
mean s_v deceptive=0.0475 honest=-0.0240 gap_dec_minus_hon=0.0714
topic_lstsq_on_scalar=0.28 topic_loo_cos_on_scalar=0.14 topic_loo_l2_on_scalar=0.22
```

Best plan gap so far. Still tiny. Topic leftover 0.22. Fail.

## Contrast mean-pool mid layer — 2026-09-23 21:52

`--pool mean --layer 16`  n=36

```
mean s_v deceptive=-0.8511 honest=-0.8530 gap_dec_minus_hon=0.0019
topic_lstsq_on_scalar=0.33 topic_loo_cos_on_scalar=0.33 topic_loo_l2_on_scalar=1.00
```

Scores cluster by topic (~-0.83 cooking, ~-0.85 hiking, ~-0.73 invoices). Honest and deceptive match inside a topic. Topic L2 = 1. Plan gap 0. This is hallway wallpaper. Fail hard. Do not fill D.

## Metric repairs — 2026-09-22

- OLS wipe: global leftover + cosine LOO 0.00 retired. Fold-fit still unrun on GPU.
- Generated fact-grade: agree_assigned_strategy is not judge accuracy.
- Chat oracle: plan 0.50 always-deceptive; LOTO 0.79 tentative n_hold=4.

## Verbal oracle chat template — 2026-09-21 19:53

```
oracle_plan_acc=0.50  oracle_topic_acc=0.67
mean_loto_plan_acc=0.79
```

## Notes vs generated fact-judge — 19:45 / 19:49

notes chat gap 11.46 agree 0.92. generated chat gap 6.46 agree 0.58.
