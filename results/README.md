# Sensor ledger

Do not collapse attempts. Put new logs in this folder.
Full early writeups also in [LEDGER_EARLY.md](LEDGER_EARLY.md) and commit `e41fcfbe`.

## P-hidebank-aya — fourth HIDE bar — 2026-09-30 01:26 EEST

Log: `results/tests-hide-bank-aya-2026-09-30.log`. Dump: `hide_bank_aya.jsonl`. Layer 10. Kind not in $L$.

| Walk | HIDE frac YES | NAME frac YES | hide on hiking | note→act HIDE | hiking |
| --- | ---: | ---: | --- | ---: | ---: |
| Aya-expanse-8B L10 | **0.708** | 0.417 | yes (4 YES / 8 NO) | **0.048** (5 rooms) | **0.007** |

Fourth bar sits between Mistral (0.57) and Gemma (0.95). Not honesty. Not a freeze. Do not fill $D$.

## P-hidebank — crossed HIDE/NAME, $S \neq$ tag — 2026-09-30 00:53 EEST

Log: `results/tests-hide-bank-2026-09-30.log`. Dumps: `hide_bank_{qwen,mistral,gemma}.jsonl`.

| Walk | HIDE frac YES | hide on hiking | HIDE agree tag | note→act HIDE | hiking |
| --- | ---: | --- | ---: | ---: | ---: |
| Qwen L8 | 0.51 | **yes** (2 YES / 10 NO) | 0.68 | **0.018** (8/8) | **−0.049** |
| Mistral L9 | 0.57 | **yes** (8 YES / 4 NO) | 0.79 | **0.092** (8/8) | **−0.002** |
| Gemma L10 | **0.95** | all YES | 0.55 | 0.001 | skipped |
| Aya L10 | **0.71** | 4 YES / 8 NO | 0.69 | 0.048 | 0.007 |

## P-noteact — note $h \to$ P-act button — 2026-09-30 00:42 EEST

Log: `results/tests-note-act-2026-09-30.log`.

| Walk | agree tag↔button | paired | note→act | hiking |
| --- | ---: | --- | ---: | ---: |
| Qwen L8 | 0.667 | 6/8 | **0.043** | skipped |
| Mistral L9 | **0.833** | 8/8 | **0.085** | **0.096** |
| Gemma L10 | 0.729 | 6/8 | **0.054** | **0.009** |
| Falcon L8 | 0.750 | 8/8 | **0.055** | **0.047** |

## P-wave1 — Gemma L10 + Falcon L8 — 2026-09-30 00:07 EEST

| Walk | slice | note LOTO | hike LOTO | hike hold | topic L2 | para LOTO / hike | pre→act / hike |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Gemma-3-4B-it | L10 | **0.0091** | **0.0027** | **0.0165** | **0.65** | 0.0088 / 0.0023 | **−0.077** / 0.000 |
| Falcon3-7B | L8 | **0.0816** | **0.0227** | **0.2471** | **0.12** | 0.0771 / **−0.004** | **−0.006** / −0.005 |
| Aya-8B | L10 | — (tokenizer then) | — | — | — | — | hide-bank only |

## P-preact — $r(h_{\mathrm{pre}})\to$ button — 2026-09-29 22:55 EEST

| | rooms | skipped | act LOTO | hiking |
| --- | --- | --- | ---: | ---: |
| Qwen L8 | 6/8 | hiking, travel | **0.038** | skipped |
| Mistral L9 | 8/8 | none | **0.016** | **0.012** |

## P-elicit — fact-bite — 2026-09-29 21:40 EEST

Qwen two-sided 8/8 (often `fact_margin` noise). Mistral 3/8, hiking no truth. Do not fill $D$.

## P-bailey-fix — wipe — 2026-09-29 21:30 EEST

| | wipe keep | quiet keep | $s_v$ base / wipe |
| --- | ---: | ---: | --- |
| Qwen L8 | **0.833** | 0.812 | 0.087 / **0.000** |
| Mistral L9 | **0.833** | 0.458 | 0.043 / **0.000** |

## P-atlas — kind as label — 2026-09-29 20:42 EEST

Kind-fit thin. Qwen hiking 6/6 truth on exec dumps.

## P-prehhold / P-pre / P-act

Pre tag LOTO $0.011$ both. Pre hold $0.005$ / $0.009$. Mistral print $0.68$ is YES/NO geometry. Note hiking hold $0.203$ / $0.278$.

## P-button — 2026-09-28

| | YES/NO | tag LOTO | kind LOTO |
| --- | --- | ---: | ---: |
| Qwen L8 | 9/87 | **0.003** | 0.017 |
| Mistral L9 | 10/86 | 0.122 | 0.776 |

Hiking/travel 12/12 NO. Kind 0.776 is token geometry.

## P-multi — 2026-09-28

Qwen ensemble LOTO 0.051 hiking **0.015**. Mistral 0.069 hiking **0.022**. Weaker than plain ~0.10. Same rooms.

## P-cross — 2026-09-27

| Camera → walk | cross LOTO | hiking | para hiking |
| --- | ---: | ---: | ---: |
| Qwen → Mistral | 0.098 | **0.028** | 0.032 |
| Mistral → Qwen | 0.198 | 0.094 | **0.026** |

## P1 / P0p — 2026-09-27

| | LOTO hike | held_inroom hike | para_hold hike | para LOTO hike |
| --- | ---: | ---: | ---: | ---: |
| Qwen L8 | **0.013** | **0.203** | **0.160** | **0.009** |
| Mistral L9 | 0.069 | **0.278** | **0.179** | 0.052 |

P-construct / P-construct-exec / P-many: [LEDGER_EARLY.md](LEDGER_EARLY.md). Do not fill $D$.
