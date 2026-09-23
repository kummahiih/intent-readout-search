# Sensor ledger

Do not collapse attempts.

## Contrast layer sweep — 2026-09-23 night

Last-token LOTO `v`, n=36, 6 topics. Official topic gate = L2 on the scalar.

| layer / pool | plan gap | topic L2 |
| --- | --- | --- |
| -1 last | 0.026 | 0.31 |
| 24 last | 0.027 | 0.31 |
| 16 last | 0.071 | 0.22 |
| 8 last | 0.066 | **0.17** |
| -1 mean | 0.030 | 0.22 |
| 16 mean | 0.002 | **1.00** |

Early last-token: topic gate at chance, plan still ~0.07. Late last-token: topic returns. Mean mid-layer is wallpaper. None of these is a camera. Do not fill D.

## Contrast scalar LOTO — 2026-09-23 20:20

`--pool last --layer -1`

```
gap_dec_minus_hon=0.0260  topic_loo_l2_on_scalar=0.31
```

## Contrast mean-pool last layer — 21:49

`--pool mean --layer -1` gap=0.0297 topic L2=0.22. Fail.

## Contrast last-token mid layer — 21:50

`--pool last --layer 16` gap=0.0714 topic L2=0.22. Fail.

## Contrast last-token early layer — 21:54

`--pool last --layer 8` gap=0.0657 topic L2=0.17 lstsq=0.28. Official topic chance. Plan tiny. Not D.

## Contrast last-token late layer — 21:55

`--pool last --layer 24`

```
mean s_v deceptive=-0.0324 honest=-0.0589 gap_dec_minus_hon=0.0265
topic_lstsq_on_scalar=0.31 topic_loo_cos_on_scalar=0.20 topic_loo_l2_on_scalar=0.31
```

Looks like last layer. Topic back. Fail.

## Contrast mean-pool mid layer — 21:52

`--pool mean --layer 16` gap=0.0019 topic L2=1.00. Wallpaper.

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
