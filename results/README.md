# Sensor ledger

Do not collapse attempts.

## Talker-count $m_{\mathrm{hat}}$ — wired 2026-09-26 22:52 EEST

Same SVD energy rank as `regret-heuristic/simulation_source_count.py`.
Now logged by `pair_contrast.py` (`source_count.py`, `--mhat-rel 0.05`).
Not in $L$. Not $r$. Crowded hallway is not the slap.

No Qwen $m_{\mathrm{hat}}$ yet. Rerun layer 8 to fill:

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
```

Want from that run: `m_hat_fit_all`, `m_hat_fit_dec`, `m_hat_fit_hon`, `m_hat_fit_contrast_v`, per-topic `m_hat_fit_topic_*`, and the transfer twins. Also still need `topic_loo_l2_on_scalar` from P0b scrollback.

## P0b — 8-topic layer-8 + full paraphrase — 2026-09-26 22:47 EEST

Same command on the widened files. Topic L2 line was off the photo; paste it if you still have scrollback. Eight-way chance is 0.125.
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

### Verdict vs P0

The 3-topic paraphrase kill does **not** survive the wider file. Transfer gap matches fit (0.108 vs 0.105). Both permutation tests are 0/20000.

Still not a camera:

- Hiking stays near zero on fit (+0.011).
- Invoices transfer dies (-0.001).
- Travel and neighbors, which I just wrote, are the loudest rooms.
- Topic L2 on the 8-topic scalar is not in this photo.
- Paraphrase twins are close in template to the fit notes.

Keep as a stronger hint. Do not freeze r. Do not fill D. Do not train the hinge.

Need from scrollback: `topic_loo_l2_on_scalar` on the 8-topic fit.

## P0 — kill or keep the layer-8 hint — 2026-09-26 22:39 EEST

4070 run on the *old* 6-topic files (3-topic paraphrase + mush hiking row).
Do not fill D.

### Fit on `pairs_wide.jsonl` (n=36, 6 topics)

```
fit gap_dec_minus_hon=0.0657  dec=0.0421  hon=-0.0236  n_dec=18 n_hon=18
topic_lstsq_on_scalar=0.28  topic_loo_cos_on_scalar=0.17  topic_loo_l2_on_scalar=0.17
within_topic_perm N=20000 p=0.0000 n_ge=0
per-topic LOTO gaps:
  cooking  +0.0907
  hiking   +0.0017
  invoices +0.0181
  pets     +0.0855
  repairs  +0.1034
  taxes    +0.0949
```

### Transfer on old paraphrase (3 topics + mush)

```
transfer gap_dec_minus_hon=0.0268  dec=0.0254  hon=-0.0015  n_dec=7 n_hon=6
within_topic_perm N=20000 p=0.1006 n_ge=2012
```

That kill was file-size, not a law. Superseded as a paraphrase verdict by P0b. Hiking ~0 still holds.

### Last-layer control on published LOTO scalars (overnight 2026-09-20)

```
gap_dec_minus_hon=0.0259  within_topic_perm p=0.3240
```

Last-layer gap 0.026 is noise.

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

## Contrast scalar LOTO — 2026-09-23 20:20

`--pool last --layer -1` gap=0.0260 topic L2=0.31.

## Contrast mean-pool last layer — 21:49

`--pool mean --layer -1` gap=0.0297 topic L2=0.22. Fail.

## Contrast last-token mid layer — 21:50

`--pool last --layer 16` gap=0.0714 topic L2=0.22. Fail.

## Contrast last-token early layer — 21:54

`--pool last --layer 8` gap=0.0657 topic L2=0.17 lstsq=0.28.

## Contrast last-token late layer — 21:55

`--pool last --layer 24` gap=0.0265 topic L2=0.31. Fail.

## Contrast mean-pool mid layer — 21:52

`--pool mean --layer 16` gap=0.0019 topic L2=1.00. Wallpaper.

## Metric repairs — 2026-09-22

- OLS wipe: global leftover + cosine LOO 0.00 retired. Fold-fit still unrun on GPU.
- Generated fact-grade: agree_assigned_strategy is not judge accuracy.
- Chat oracle: plan 0.50 always-deceptive; LOTO 0.79 tentative n_hold=4.

## Verbal oracle chat template — 2026-09-21 19:53

```
oracle_plan_acc=0.50  oracle_topic_acc=0.67
mean_loto_plan_acc=0.79
```

## Notes vs generated fact-judge — 19:45 / 19:49

notes chat gap 11.46 agree 0.92. generated chat gap 6.46 agree 0.58.

## Contrast last-token layer 4 — 22:08

`--pool last --layer 4` gap=0.0438 topic L2=0.25. Fail.

## Contrast last-token layer 12 — 22:09

`--pool last --layer 12` gap=0.0581 topic L2=0.39. Fail.
