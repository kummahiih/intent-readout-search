# Sensor ledger

Do not collapse attempts.

## T3 same-gate scoreboard — 2026-09-26 22:56 EEST

Official columns: plan LOTO gap, topic LOO L2 on that same score, paraphrase gap / $p$, hiking sign. $z$ not in $L$. Do not fill $D$.
SAE latents are out of family until a public Qwen2.5-7B pack exists. Do not put SAE in Adam.

| camera | n topics | plan gap | topic L2 | transfer gap | transfer $p$ | hiking |
| --- | --- | --- | --- | --- | --- | --- |
| last-token layer -1 (6-topic) | 6 | 0.026 | 0.31 | — | 0.32 last-layer perm | mixed |
| last-token layer 8 (6-topic) | 6 | 0.066 | **0.17** | 0.027 | 0.10 | ~0 |
| last-token layer 8 (8-topic) | 8 | 0.105 | **missing** | **0.108** | **0** | +0.011 |
| last-token layer 16 | 6 | 0.071 | 0.22 | — | — | same 3 rooms |
| mean-pool layer -1 | 6 | 0.030 | 0.22 | — | — | — |
| mean-pool layer 16 | 6 | 0.002 | 1.00 | — | — | wallpaper |
| $m_{\mathrm{hat}}$ transfer cloud | 8 | — | — | — | — | rank 25/32 |
| last-token layer -1 (8-topic) | 8 | **run** | **run** | **run** | **run** | **run** |
| fold-fit topic wipe `leace_residual.py` | 8 | **run** | **run** | n/a | n/a | n/a |
| loud heads layer 8 `head_write_probe.py` | 8 | **run** | **run** | n/a | n/a | n/a |
| quiet heads layer 8 `--quiet` | 8 | **run** | **run** | n/a | n/a | n/a |
| public SAE latents | — | skip | skip | skip | skip | no pack |

Layer 8 last-token is the only row that has cleared topic chance *and* paraphrase $p=0$ on the 8-topic file. Hiking and invoices still fail uniformity. Topic L2 on that 8-topic fit is still not in git.

4070 next (same venv, pull first):

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer -1 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
python leace_residual.py --data data/pairs_wide.jsonl
python head_write_probe.py --data data/pairs_wide.jsonl --layer 8 --k 4
python head_write_probe.py --data data/pairs_wide.jsonl --layer 8 --k 4 --quiet
```

## Talker-count $m_{\mathrm{hat}}$ — 2026-09-26 22:53 EEST

Layer 8 last-token, `rel=0.05`, `d=3584`. Log only. Not in $L$. Not $r$.
Fit `m_hat_fit_*` lines were off this photo.

```
m_hat_transfer_topic_*=4 n=4     (every room)
m_hat_transfer_all=25 n=32
m_hat_transfer_dec=16 n=16
m_hat_transfer_hon=16 n=16
```

Per room, rank saturates the sample. High $\hat m$ is the default when $n \ll d$. It does not name plan.

## P0b — 8-topic layer-8 + full paraphrase — 2026-09-26 22:47 EEST

```
fit gap_dec_minus_hon=0.1045  p=0.0000
transfer gap_dec_minus_hon=0.1084  p=0.0000
hiking fit +0.0113  invoices transfer -0.0012
```

Keep as a stronger hint. Do not freeze r. Do not fill D.

## P0 — 6-topic layer-8 — 2026-09-26 22:39 EEST

```
fit gap=0.0657  topic_loo_l2_on_scalar=0.17  p=0.0000
transfer gap=0.0268 p=0.1006   # old 3-topic + mush file
last-layer control p=0.324
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

- OLS wipe retired. Fold-fit script is `leace_residual.py` (T3, unrun on 8-topic).
- Generated fact-grade: agree_assigned_strategy is not judge accuracy.
- Chat oracle: plan 0.50 always-deceptive; LOTO 0.79 tentative n_hold=4.
