# Scale without changing the object

2026-09-29 / 2026-09-30. Weights and HF datasets stay on disk (`models/`, `datasets/` are gitignored).
Do not fill $D$. Kind not in $L$. Keep hiking.

## What the new files are

| Path | Use |
| --- | --- |
| `models/gemma-3-4b-it` | Walk. |
| `models/Phi-4-mini-instruct` | Skipped (`LossKwargs`). |
| `models/Falcon3-7B-Instruct` | Walk. |
| `models/aya-expanse-8b` | Walk for hide-bank after rust `tokenizer.json`. Pair-contrast LOTO not run. |
| `datasets/DeceptionBench` | Extra prompts / domains. Not a frozen $S$. |
| `datasets/lie-detection-rollouts` | Other models' prints. Not this walk's $S$. |
| `datasets/difraud` | Off-construct unless remapped. |
| `datasets/deception-probes-activations` | Hidden states of **other** models. Not $h$ here. |

## Layers

| Local dir | $n_L$ | 0.3-depth |
| --- | ---: | ---: |
| gemma-3-4b-it | 34 text | 10 |
| Falcon3-7B-Instruct | 28 | 8 |
| aya-expanse-8b | 32 | 10 |

## Wave 1 note meters — 2026-09-30 00:07 EEST

| Walk | slice | note LOTO | hike LOTO | hike hold | topic L2 | para / hike | pre→act |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| Gemma L10 | 10 | 0.0091 | 0.0027 | 0.0165 | 0.65 | 0.0088 / 0.0023 | −0.077 |
| Falcon L8 | 8 | 0.0816 | 0.0227 | 0.2471 | 0.12 | 0.0771 / −0.0039 | −0.006 |
| Aya L10 | 10 | not run | not run | not run | not run | not run | hide-bank only |

## Hide-bank — 2026-09-30

HIDE-arm cover rate (not honesty):

| Walk | HIDE YES | hiking hide | note→HIDE | hike |
| --- | ---: | --- | ---: | ---: |
| Qwen L8 | 0.51 | 2/10 | 0.018 | −0.049 |
| Mistral L9 | 0.57 | 8/4 | 0.092 | −0.002 |
| Aya L10 | **0.71** | 4/8 | 0.048 | 0.007 |
| Gemma L10 | **0.95** | 12/12 | 0.001 | skipped |

Do not freeze $r$. Do not fill $D$.
