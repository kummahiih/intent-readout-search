# Sensor ledger

Do not collapse attempts.

## P0e — rewritten hiking/invoices — 2026-09-26 23:20 EEST

Source: `results/tests-2026-09-26-5.log` section 5.
$v$ from cooking/neighbors/pets/repairs/taxes/travel. Score original held rooms and `data/pairs_voice.jsonl`.

```
fit_kept   gap=0.1361  topic L2=0.11  p=0     (6-way chance 0.167)
fit_held   gap=0.0341  p=0.0971              hiking +0.017 invoices +0.052
transfer_held voice gap=-0.0298 p=0.3109     hiking -0.019 invoices -0.040
```

New voice does **not** carry the plan signal. Those two rooms are dead in the geometry, not only in the old template. Do not fill $D$.

## P0d — hold travel/neighbors out of v

```
fit_kept 0.0657 p=0   fit_held 0.1489 p=0.005
transfer_kept 0.0714 p=0.0003   transfer_held 0.163 p=0.056 n=8
```

## P0c — 8-topic layer-8

```
fit 0.1045  topic L2 0.06  p=0
transfer 0.1084 p=0
```

## Scoreboard

| camera | plan | topic L2 | transfer |
| --- | --- | --- | --- |
| layer 8, 8-topic | 0.105 | 0.06 | p=0 |
| layer 8, hold travel/neighbors | kept 0.066 / held 0.149 | 0.17 | kept p=0.0003 |
| layer 8, hold hiking/invoices | kept 0.136 / held 0.034 | 0.11 | voice p=0.31 flip |
| last layer 8-topic | 0.029 | 0.23 | p=0.25 |
