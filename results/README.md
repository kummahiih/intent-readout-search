# Sensor ledger

Do not collapse attempts.

## P0 — kill or keep the layer-8 hint — 2026-09-26

Command for the 4070 (not run in the no-GPU sandbox):

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
```

Do not fill D.

### Last-layer control on published LOTO scalars (overnight 2026-09-20)

Same 36 rows, last hidden state. Not layer 8.

```
gap_dec_minus_hon=0.0259  dec=-0.0017  hon=-0.0277  n=36
within_topic_perm N=20000 p=0.3240
global_perm N=20000 p=0.4149
per-topic LOTO gaps:
  cooking  +0.0088
  hiking   +0.0422
  invoices +0.0145
  pets     -0.0423
  repairs  +0.0604
  taxes    +0.0720
```

Last-layer gap 0.026 is noise. Pets has the wrong sign. This kills the last-layer contrast as a camera. It does **not** kill layer 8: raw layer-8 scalars were never logged, so the published 0.0657 / topic L2 0.17 row still has no p-value and no paraphrase transfer.

### Layer 8 — still open

Published 2026-09-23: plan gap 0.066, topic L2 0.17, lstsq 0.28. Ledger said repairs/cooking/pets carry it; hiking ~0. No itemized s_v in git. Paraphrase file exists (3 topics + one mush hiking line) and was not scored.

Until the command above is run on GPU:

- do not treat layer 8 as confirmed
- do not treat layer 8 as killed
- do not freeze r or fill D

## Contrast layer sweep — 2026-09-23 night

Last-token LOTO `v`, n=36, 6 topics. Official topic gate = L2 on the scalar.

| layer / pool | plan gap | topic L2 |
| --- | --- | --- |
| 4 last | 0.044 | 0.25 |
| **8 last** | **0.066** | **0.17** |
| 12 last | 0.058 | 0.39 |
| 16 last | 0.071 | 0.22 |
| 24 last | 0.027 | 0.31 |
| -1 last | 0.026 | 0.31 |
| -1 mean | 0.030 | 0.22 |
| 16 mean | 0.002 | 1.00 |

Layer 8: topic chance; gap from repairs/cooking/pets; hiking ~0.
Layer 16: loudest gap; leftover topic; same three topics carry it.
Layer 12: topic bump, not a midpoint.
None of these is a camera. Do not fill D.

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

## Contrast last-token layer 4 — 22:08

`--pool last --layer 4` gap=0.0438 topic L2=0.25. Weaker than 8. Fail.

## Contrast last-token layer 12 — 22:09

`--pool last --layer 12` gap=0.0581 topic L2=0.39. Topic worse than neighbors. Fail.
