# Sensor ledger

Do not collapse attempts.

## Contrast scalar LOTO — 2026-09-23 20:20

`python pair_contrast.py --data data/pairs_wide.jsonl`  n=36, 6 topics

```
mean s_v deceptive=-0.0017 honest=-0.0277 gap_dec_minus_hon=0.0260
topic_lstsq_on_scalar=0.31 topic_loo_cos_on_scalar=0.17 topic_loo_l2_on_scalar=0.31
```

Official topic gate is L2 0.31 (chance ~0.17). Cosine 0.17 is sign-only. Plan gap 0.026. Not a camera. Do not fill D.

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
