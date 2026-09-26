# Sensor ledger

Do not collapse attempts.

## P0f — SIREN f(1) — 2026-09-26 23:32 EEST

Source: `results/tests-2026-09-26-6.log`. Query $f(1)$. $\theta$ not in $L$.

```
layer 8 siren_mse=2599  cos_to_last=0.35   # not last-token in a wig
8-topic     gap=0.140  topic L2=0.08  transfer=0.141 p=0
hold T/N    kept=0.100 topic L2=0.28  held=0.165 p=0.005  xfer_kept p=0.0008
hold H/I    kept=0.186 topic L2=0.06  held=0.036 p=0.20   voice=-0.004 p=0.82
last-layer  gap=0.038  topic L2=0.21  transfer=0.040 p=0.005  cos_to_last=0.57
theta L2    plan-diff~71  topic-diff~75   # weights store both
```

$f(1)$ at layer 8 is a bit louder than last-token and still hallway-local. Voice hiking/invoices stay dead. $\theta$ L2 does not split plan from topic. Do not fill $D$ from $\theta$.

## P0e — voice hiking/invoices (last-token)

voice transfer $-0.030$ $p=0.31$. Dead rooms.

## P0d / P0c last-token layer 8

8-topic gap 0.105 topic L2 0.06 paraphrase $p=0$.
Hold travel/neighbors held 0.149 $p=0.005$.
