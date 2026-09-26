# Sensor ledger

Do not collapse attempts.

## T3 same-gate scoreboard — 2026-09-26 23:03 EEST

Source: `results/tests-2026-09-26-2.log` (`18c95f4`). Official columns below. $z$ not in $L$. Do not fill $D$.
SAE skipped: no public Qwen2.5-7B pack.

| camera | n topics | plan gap / acc | topic L2 | transfer gap | transfer $p$ | hiking |
| --- | --- | --- | --- | --- | --- | --- |
| last-token layer 8 (8-topic) | 8 | **0.105** | missing | **0.108** | **0** | +0.011 |
| last-token layer 8 (6-topic) | 6 | 0.066 | **0.17** | 0.027 | 0.10 | ~0 |
| last-token layer -1 (8-topic) | 8 | 0.029 | 0.23 | 0.019 | **0.25** | +0.036 |
| last-token layer -1 (6-topic) | 6 | 0.026 | 0.31 | — | 0.32 | mixed |
| last-token layer 16 | 6 | 0.071 | 0.22 | — | — | same 3 rooms |
| mean-pool layer -1 | 6 | 0.030 | 0.22 | — | — | — |
| mean-pool layer 16 | 6 | 0.002 | 1.00 | — | — | wallpaper |
| fold-fit wipe last-token | 8 | LOTO acc **0.58** | leftover **0.08** | n/a | n/a | hold 0.50 |
| loud heads layer 8 | 8 | gap 0.074 | **0.69** | n/a | n/a | topic loud |
| quiet heads layer 8 | 8 | gap 0.001 | **0.12** | n/a | n/a | all cos ~0.96 |
| $m_{\mathrm{hat}}$ last-layer fit | 8 | — | — | — | — | 15/48; $v_T$ rank 8 |
| $m_{\mathrm{hat}}$ layer-8 transfer | 8 | — | — | — | — | 25/32 |
| public SAE | — | skip | skip | skip | skip | no pack |

Eight-way chance is 0.125.

Last layer on the same 8-topic files is a **fail**: tiny gap, leftover topic, paraphrase $p=0.25$. Layer 8 is still the only contrast row with a large transferred gap. Topic L2 on that layer-8 8-topic fit is still not in the log.

Wipe: leftover topic dies (0.08) and plan LOTO is 0.58. Not a camera.
Loud heads: topic 0.69. Fail.
Quiet heads: topic chance and no plan. Fail.

## T3 raw — last-token layer -1, 8-topic

```
fit gap=0.0291  topic_loo_l2=0.23  p=0.0300
transfer gap=0.0185  p=0.2475
m_hat_fit_all=15 n=48  m_hat_fit_contrast_v=8 n=8
m_hat_transfer_all=15 n=32
per-topic fit: cooking -0.011 hiking +0.036 invoices +0.033
              neighbors +0.021 pets -0.011 repairs +0.056 taxes +0.064 travel +0.045
```

## T3 raw — fold-fit wipe

```
topic_loo_l2_h=0.79  topic_loo_l2_leftover_foldfit=0.08
mean_loto_plan_leftover_foldfit=0.58
hold: cooking 0.50 hiking 0.50 invoices 0.50 neighbors 0.83
      pets 0.33 repairs 0.83 taxes 0.50 travel 0.67
```

## T3 raw — heads layer 8

loud `10,12,15,19`: s*_D dec=0.625 hon=0.551 gap_hon_minus_dec=-0.074 topic_loo=0.69
quiet `23,24,26,27`: s*_D dec=0.964 hon=0.963 gap=-0.001 topic_loo=0.12

## Talker-count $m_{\mathrm{hat}}$ — layer 8 transfer (earlier photo)

```
m_hat_transfer_topic_*=4 n=4
m_hat_transfer_all=25 n=32
m_hat_transfer_dec=16 n=16
m_hat_transfer_hon=16 n=16
```

## P0b — 8-topic layer-8 + full paraphrase — 2026-09-26 22:47 EEST

```
fit gap=0.1045 p=0
transfer gap=0.1084 p=0
hiking fit +0.011  invoices transfer -0.001
```

Keep as a stronger hint. Do not freeze r. Do not fill D.

## P0 — 6-topic layer-8 — 2026-09-26 22:39 EEST

```
fit gap=0.0657  topic_loo_l2=0.17  p=0
transfer gap=0.0268 p=0.10   # old 3-topic + mush
last-layer 6-topic perm p=0.32
```

## Contrast layer sweep — 2026-09-23 night

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

## Metric repairs — 2026-09-22

- OLS wipe retired. Fold-fit is the T3 wipe row above.
- Chat oracle: plan 0.50; LOTO 0.79 tentative n_hold=4.
