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

Fit gap 0.1045 $p=0$. Transfer gap 0.1084 $p=0$. Hiking fit +0.011. Invoices transfer -0.001.
Topic L2 still missing from photos. Do not fill D.

## P0 — 6-topic layer-8 — 2026-09-26 22:39 EEST

Fit gap 0.0657 topic L2 0.17 $p=0$. Old 3-topic transfer gap 0.0268 $p=0.10$. Last-layer control $p=0.32$.

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

None of these is a camera. Do not fill D.
