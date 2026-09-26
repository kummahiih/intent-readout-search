# Sensor ledger

Do not collapse attempts.

## P0c — 8-topic layer-8 topic L2 — 2026-09-26 23:09 EEST

Source: `results/tests-2026-09-26-3.log` (`5c243c0`). Same gaps as the photo. The missing cell is in.

```
layer=8 pool=last n=48
fit gap=0.1045  topic_loo_l2_on_scalar=0.06  lstsq=0.21  loo_cos=0.15  p=0
transfer gap=0.1084  p=0
m_hat_fit_all=29 n=48  m_hat_fit_dec=24  m_hat_fit_hon=22  m_hat_fit_contrast_v=8
m_hat_transfer_all=25 n=32
v norms 10.0..17.4
hiking fit +0.0113  invoices transfer -0.0012
```

Eight-way chance is 0.125. Official topic L2 **0.06** is under chance. Do not fill $D$. Hiking / invoices still fail uniformity.

## T3 same-gate scoreboard

| camera | n topics | plan gap / acc | topic L2 | transfer gap | transfer $p$ | hiking |
| --- | --- | --- | --- | --- | --- | --- |
| last-token layer 8 (8-topic) | 8 | **0.105** | **0.06** | **0.108** | **0** | +0.011 |
| last-token layer 8 (6-topic) | 6 | 0.066 | **0.17** | 0.027 | 0.10 | ~0 |
| last-token layer -1 (8-topic) | 8 | 0.029 | 0.23 | 0.019 | **0.25** | +0.036 |
| last-token layer -1 (6-topic) | 6 | 0.026 | 0.31 | — | 0.32 | mixed |
| last-token layer 16 | 6 | 0.071 | 0.22 | — | — | same 3 rooms |
| mean-pool layer -1 | 6 | 0.030 | 0.22 | — | — | — |
| mean-pool layer 16 | 6 | 0.002 | 1.00 | — | — | wallpaper |
| fold-fit wipe last-token | 8 | LOTO acc **0.58** | leftover **0.08** | n/a | n/a | hold 0.50 |
| loud heads layer 8 | 8 | gap 0.074 | **0.69** | n/a | n/a | topic loud |
| quiet heads layer 8 | 8 | gap 0.001 | **0.12** | n/a | n/a | all cos ~0.96 |
| $m_{\mathrm{hat}}$ layer-8 fit | 8 | — | — | — | — | 29/48; $v_T$ rank 8 |
| $m_{\mathrm{hat}}$ last-layer fit | 8 | — | — | — | — | 15/48 |
| public SAE | — | skip | skip | skip | skip | no pack |

## T3 raw — last-token layer -1, 8-topic

```
fit gap=0.0291  topic_loo_l2=0.23  p=0.0300
transfer gap=0.0185  p=0.2475
```

## T3 raw — fold-fit wipe / heads

Wipe leftover topic L2 0.08, plan LOTO 0.58.
Loud heads 10,12,15,19 topic 0.69. Quiet 23,24,26,27 topic 0.12 gap 0.001.

## Contrast layer sweep — 2026-09-23 night (6-topic)

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
