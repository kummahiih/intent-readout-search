# Sensor ledger

Do not collapse attempts.

## Talker-count $m_{\mathrm{hat}}$ — 2026-09-26 22:53 EEST

Layer 8 last-token, `rel=0.05`, `d=3584`. Log only. Not in $L$. Not $r$.
Fit `m_hat_fit_*` lines were off this photo.

```
m_hat_transfer_topic_*=4 n=4     (every room)
m_hat_transfer_all=25 n=32
m_hat_transfer_dec=16 n=16
m_hat_transfer_hon=16 n=16
```

Per room, rank saturates the sample: four notes, four loud singular values. Dec and hon each saturate too (16/16). The 32-note cloud keeps 25 directions above 5% of $s_{\max}$.

That is not the dummy 1-source vs 2-source cartoon. Qwen layer-8 last tokens are a crowded residual, not two planted axes plus 0.02 noise. High $\hat m$ is the default when $n \ll d$. It does not name plan. It does not fill $D$.

Still want from scrollback: `m_hat_fit_all`, `m_hat_fit_contrast_v`, `topic_loo_l2_on_scalar`.

## P0b — 8-topic layer-8 + full paraphrase — 2026-09-26 22:47 EEST

Same command on the widened files. Topic L2 line was off the photo. Eight-way chance is 0.125.
Do not fill D.

### Fit on `pairs_wide.jsonl` (n=48, 8 topics)

```
fit gap_dec_minus_hon=0.1045
within_topic_perm N=20000 p=0.0000 n_ge=0
per-topic LOTO gaps:
  cooking    +0.1205
  hiking     +0.0113
  invoices   +0.0428
  neighbors  +0.1673
  pets       +0.1009
  repairs    +0.1222
  taxes      +0.1076
  travel     +0.1633
```

### Transfer on 8-topic `pairs_paraphrase.jsonl` (n=32, 2+2 each, no mush)

```
transfer gap_dec_minus_hon=0.1084  dec=0.1021  hon=-0.0063  n_dec=16 n_hon=16
within_topic_perm N=20000 p=0.0000 n_ge=0
per-topic LOTO gaps:
  cooking    +0.1293
  hiking     +0.0402
  invoices   -0.0012
  neighbors  +0.1714
  pets       +0.1238
  repairs    +0.0925
  taxes      +0.1197
  travel     +0.1920
```

Keep as a stronger hint. Do not freeze r. Do not fill D.

## P0 — kill or keep the layer-8 hint — 2026-09-26 22:39 EEST

4070 run on the *old* 6-topic files (3-topic paraphrase + mush hiking row).

```
fit gap_dec_minus_hon=0.0657  topic_loo_l2_on_scalar=0.17  p=0.0000
transfer gap=0.0268 p=0.1006
```

Last-layer control (overnight 2026-09-20): gap 0.0259 within-topic $p=0.324$.

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

None of these is a camera. Do not fill D.

## Older contrast rows — 2026-09-23

`--pool last --layer -1` gap=0.0260 topic L2=0.31.
`--pool mean --layer -1` gap=0.0297 topic L2=0.22.
`--pool last --layer 16` gap=0.0714 topic L2=0.22.
`--pool last --layer 8` gap=0.0657 topic L2=0.17.
`--pool last --layer 24` gap=0.0265 topic L2=0.31.
`--pool mean --layer 16` gap=0.0019 topic L2=1.00.
`--pool last --layer 4` gap=0.0438 topic L2=0.25.
`--pool last --layer 12` gap=0.0581 topic L2=0.39.

## Metric repairs — 2026-09-22

- OLS wipe: global leftover + cosine LOO 0.00 retired. Fold-fit still unrun on GPU.
- Generated fact-grade: agree_assigned_strategy is not judge accuracy.
- Chat oracle: plan 0.50 always-deceptive; LOTO 0.79 tentative n_hold=4.
