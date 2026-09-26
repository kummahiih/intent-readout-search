# Sensor ledger

Do not collapse attempts.

## P0d — hold travel/neighbors out of v — 2026-09-26 23:16 EEST

Source: `results/tests-2026-09-26-4.log`. Layer 8. $v$ from the six older rooms only.

```
fit_kept   gap=0.0657  topic L2=0.17  p=0.0000   (n=36, 6-way chance 0.167)
fit_held   gap=0.1489  p=0.0053                 neighbors +0.150 travel +0.148
transfer_kept gap=0.0714 p=0.0003
transfer_held gap=0.1633 p=0.0562               n=8
hiking fit_kept +0.0017
invoices transfer_kept -0.0017
```

Hold-out did **not** kill. The new rooms still separate when they never enter $v$. The 8-topic 0.105 was 0.066 kept averaged with 0.149 held. Hiking / invoices still dead. Do not fill $D$.

## P0c — 8-topic layer-8 topic L2 — 2026-09-26 23:09 EEST

```
fit gap=0.1045  topic_loo_l2=0.06  p=0
transfer gap=0.1084  p=0
m_hat_fit_all=29/48  contrast_v rank 8
```

## T3 scoreboard

| camera | plan | topic L2 | transfer $p$ |
| --- | --- | --- | --- |
| layer 8, 8-topic | 0.105 | **0.06** | 0 |
| layer 8, 6-topic / fit_kept | 0.066 | **0.17** | 0.0003 on 6-topic paraphrase |
| layer 8, held travel/neighbors | 0.149 | n/a | 0.056 n=8 |
| last layer 8-topic | 0.029 | 0.23 | 0.25 |
| wipe | acc 0.58 | leftover 0.08 | n/a |
| loud heads l8 | 0.074 | 0.69 | n/a |
| quiet heads l8 | 0.001 | 0.12 | n/a |
