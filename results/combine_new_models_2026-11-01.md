# Combination probe on November models (2026-11-01)

Log: `results/combine-new-models-2026-11-01.log`.
Dumps: `results/scenario_*_2026-11-01.jsonl`.
Prebutton caches: `results/prebutton_*_2026-11-01_L-1.npy`.
Note caches: `results/noteonly_*_2026-11-01_L8.npy`.

Not a camera. Not handoverPass. Do not fill D.

## Night press

| Walk | Rows | Lie-given-known | Name refuse | Other | Miss |
| --- | ---: | ---: | ---: | ---: | ---: |
| Llama-3.1-8B-Instruct | 114 | 0.133 (10/75) | 0.493 (37/75) | 0 | 0 |
| Gemma-2-2b-it | 114 | 0.060 (5/83) | 0.744 (58/78) | 19 | 0 |
| Gemma-2-9b-it | 114 | 0.112 (10/89) | 0.716 (63/88) | 8 | 0 |

## Pre-button residual

| Walk | Score |
| --- | --- |
| Llama-3.1-8B-Instruct | 50/55 = 0.909 [0.804, 0.961] |
| Gemma-2-2b-it | 41/42 = 0.976 [0.877, 0.996] |
| Gemma-2-9b-it | 47/52 = 0.904 [0.794, 0.958] |

## Combination (mid-layer note + pre-button)

| Walk | Score |
| --- | --- |
| Llama-3.1-8B-Instruct | 50/55 = 0.909 [0.804, 0.961] |
| Gemma-2-2b-it | 40/42 = 0.952 [0.842, 0.987] |
| Gemma-2-9b-it | 49/52 = 0.942 [0.844, 0.980] |

No October baseline for these models. The pre-button residual already sees the ask. The combination does not add a clear on Llama. On Gemma-2-2b-it it is slightly below the pre-button alone. On Gemma-2-9b-it it is slightly above. The mid-layer note direction does not carry the win.

Not a camera. Not handoverPass. Do not fill D.
