# Sensor ledger

Do not collapse attempts.

## P0g — Mistral-7B-Instruct-v0.3 layer 9 — 2026-09-26 23:54 EEST

Source: `results/tests-mistral-2026-09-26.log`.
`tests-qwen-kstep-2026-09-26.log` is **Mistral layer 8 kstep** (`MODEL` was still set). Qwen K-step is not in.

Eight-way chance 0.125. Voice hiking/invoices stay dead on every pool.

| pool L9 | plan | topic L2 | paraphrase | voice $p$ |
| --- | --- | --- | --- | --- |
| last | **0.116** | **0.12** | 0.123 $p=0$ | 0.80 |
| kstep K=8 | **0.192** | **0.10** | 0.185 $p=0$ | 0.62 |
| siren $f(1)$ | 0.058 | **0.04** | 0.055 $p=0$ | 0.83 |
| last layer last | 0.037 | 0.17 | 0.032 | — |
| last layer kstep | 0.076 | 0.29 | 0.076 | — |
| last layer siren | 0.049 | 0.17 | 0.060 | — |

kstep $\cos$ to last 0.67. SIREN $\cos$ to last 0.34. $\theta$ L2 plan~9 topic~9.5.
Hold travel/neighbors last: held 0.146 $p=0.005$. kstep held 0.226 $p=0.005$.

Mid-layer hint is **not Qwen-only**. Same two rooms still die under a voice change. Do not fill $D$.

## P0f Qwen SIREN / P0c Qwen last-token layer 8

Qwen last 0.105 / L2 0.06. Qwen SIREN 0.140 / L2 0.08. Voice dead.
