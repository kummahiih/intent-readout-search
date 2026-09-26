# Sensor ledger

Do not collapse attempts.

## P0i — mid3 unit-sum — 2026-09-27 00:13 EEST

`r = normalize(hat last + hat kstep + hat f(1))`.
Qwen log `tests-qwen-mid3-2026-09-27.log`. Mistral `tests-mistral-mid3-2026-09-27.log`.

| model | plan | topic L2 | para | voice $p$ | mid3$\cdot$last |
| --- | --- | --- | --- | --- | --- |
| Qwen L8 | 0.164 | 0.15 | 0.160 $p=0$ | **0.66** | 0.85 |
| Mistral L9 | 0.140 | **0.00** | 0.140 $p=0$ | **0.92** | 0.83 |
| Qwen last layer | 0.049 | 0.27 | 0.048 | — | 0.84 |
| Mistral last layer | 0.055 | 0.23 | 0.060 | — | 0.81 |

Pairwise: last–kstep ~0.70, last–siren ~0.34. Same dead rooms. Not a fourth axis.

## P0h Qwen K-step L8

0.195 / L2 0.15 / para $p=0$ / voice $p=0.65$.

## P0g Mistral L9 last/kstep/siren

last 0.116 / L2 0.12. kstep 0.192 / L2 0.10. siren 0.058 / L2 0.04. Voice dead.
