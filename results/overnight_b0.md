# Overnight B0

started 2026-09-20T22:27:12.765235+00:00
data data/pairs_wide.jsonl
two-topic slice invoices+hiking for topic_residual only

## python topic_residual.py --data /home/pauli/dockers/intent-readout-search/data/_overnight_two_topic.jsonl --sweep

started 2026-09-20T22:27:12.765341+00:00

```

Loading weights:   0%|          | 0/339 [00:00<?, ?it/s]
Loading weights:   1%|          | 2/339 [00:00<00:17, 18.91it/s]
Loading weights:   9%|▊         | 29/339 [00:00<00:01, 158.91it/s]
Loading weights:  22%|██▏       | 76/339 [00:00<00:00, 294.96it/s]
Loading weights:  35%|███▌      | 120/339 [00:00<00:00, 350.63it/s]
Loading weights:  48%|████▊     | 162/339 [00:00<00:00, 368.90it/s]
Loading weights:  62%|██████▏   | 209/339 [00:00<00:00, 398.01it/s]
Loading weights:  76%|███████▌  | 256/339 [00:00<00:00, 419.31it/s]
Loading weights:  88%|████████▊ | 300/339 [00:00<00:00, 424.91it/s]
Loading weights: 100%|██████████| 339/339 [00:00<00:00, 373.65it/s]
VRAM allocated_GiB=5.18 reserved_GiB=5.33
n_hidden_states=29 layers=[0, 7, 14, 21, -1]
--- layer=0 topic_axis=hiking->invoices v_norm=0.0000
pair cosine to residual bank (topic axis removed):
  topic=invoices strategy=deceptive s*_D=1.0000
  topic=invoices strategy=honest s*_D=1.0000
  topic=hiking strategy=deceptive s*_D=1.0000
  topic=hiking strategy=honest s*_D=1.0000
  topic=invoices strategy=deceptive s*_D=1.0000
  topic=invoices strategy=honest s*_D=1.0000
  topic=hiking strategy=deceptive s*_D=1.0000
  topic=hiking strategy=honest s*_D=1.0000
mean s*_D deceptive=1.0000 honest=1.0000 gap_hon_minus_dec=0.0000
topic_probe_acc_raw=0.50 topic_probe_acc_residual=0.50 n=8 topics=['hiking', 'invoices']
--- layer=7 topic_axis=hiking->invoices v_norm=1.0000
pair cosine to residual bank (topic axis removed):
  topic=invoices strategy=deceptive s*_D=0.9392
  topic=invoices strategy=honest s*_D=0.9339
  topic=hiking strategy=deceptive s*_D=0.9230
  topic=hiking strategy=honest s*_D=0.9274
  topic=invoices strategy=deceptive s*_D=0.9045
  topic=invoices strategy=honest s*_D=0.8762
  topic=hiking strategy=deceptive s*_D=0.9103
  topic=hiking strategy=honest s*_D=0.9007
mean s*_D deceptive=0.9193 honest=0.9096 gap_hon_minus_dec=-0.0097
topic_probe_acc_raw=1.00 topic_probe_acc_residual=1.00 n=8 topics=['hiking', 'invoices']
--- layer=14 topic_axis=hiking->invoices v_norm=1.0000
pair cosine to residual bank (topic axis removed):
  topic=invoices strategy=deceptive s*_D=0.8525
  topic=invoices strategy=honest s*_D=0.7895
  topic=hiking strategy=deceptive s*_D=0.8724
  topic=hiking strategy=honest s*_D=0.8232
  topic=invoices strategy=deceptive s*_D=0.8126
  topic=invoices strategy=honest s*_D=0.7292
  topic=hiking strategy=deceptive s*_D=0.8270
  topic=hiking strategy=honest s*_D=0.8140
mean s*_D deceptive=0.8411 honest=0.7890 gap_hon_minus_dec=-0.0522
topic_probe_acc_raw=1.00 topic_probe_acc_residual=1.00 n=8 topics=['hiking', 'invoices']
--- layer=21 topic_axis=hiking->invoices v_norm=1.0000
pair cosine to residual bank (topic axis removed):
  topic=invoices strategy=deceptive s*_D=0.8547
  topic=invoices strategy=honest s*_D=0.8081
  topic=hiking strategy=deceptive s*_D=0.8584
  topic=hiking strategy=honest s*_D=0.8218
  topic=invoices strategy=deceptive s*_D=0.8044
  topic=invoices strategy=honest s*_D=0.7296
  topic=hiking strategy=deceptive s*_D=0.8232
  topic=hiking strategy=honest s*_D=0.7995
mean s*_D deceptive=0.8352 honest=0.7898 gap_hon_minus_dec=-0.0454
topic_probe_acc_raw=1.00 topic_probe_acc_residual=1.00 n=8 topics=['hiking', 'invoices']
--- layer=28 topic_axis=hiking->invoices v_norm=1.0000
pair cosine to residual bank (topic axis removed):
  topic=invoices strategy=deceptive s*_D=0.9447
  topic=invoices strategy=honest s*_D=0.9310
  topic=hiking strategy=deceptive s*_D=0.8856
  topic=hiking strategy=honest s*_D=0.9251
  topic=invoices strategy=deceptive s*_D=0.8220
  topic=invoices strategy=honest s*_D=0.8509
  topic=hiking strategy=deceptive s*_D=0.9120
  topic=hiking strategy=honest s*_D=0.8868
mean s*_D deceptive=0.8911 honest=0.8985 gap_hon_minus_dec=0.0074
topic_probe_acc_raw=1.00 topic_probe_acc_residual=1.00 n=8 topics=['hiking', 'invoices']
v is estimated from bank only. Residual is not a trained adversary.
Not a deception result.

```

exit 0

## python pair_contrast.py --data /home/pauli/dockers/intent-readout-search/data/pairs_wide.jsonl

started 2026-09-20T22:27:19.496589+00:00

```
paired_topics=cooking(dec=3,hon=3),hiking(dec=3,hon=3),invoices(dec=3,hon=3),pets(dec=3,hon=3),repairs(dec=3,hon=3),taxes(dec=3,hon=3)
bank_deceptive_only=6 (no honest bank; v from matched pairs, leave-one-topic-out)

Loading weights:   0%|          | 0/339 [00:00<?, ?it/s]
Loading weights:   1%|          | 2/339 [00:00<00:17, 18.80it/s]
Loading weights:   9%|▊         | 29/339 [00:00<00:01, 158.01it/s]
Loading weights:  22%|██▏       | 76/339 [00:00<00:00, 292.47it/s]
Loading weights:  35%|███▌      | 120/339 [00:00<00:00, 347.17it/s]
Loading weights:  48%|████▊     | 162/339 [00:00<00:00, 365.29it/s]
Loading weights:  62%|██████▏   | 209/339 [00:00<00:00, 395.38it/s]
Loading weights:  76%|███████▌  | 256/339 [00:00<00:00, 416.08it/s]
Loading weights:  88%|████████▊ | 298/339 [00:00<00:00, 416.67it/s]
Loading weights: 100%|██████████| 339/339 [00:00<00:00, 370.61it/s]
VRAM allocated_GiB=5.18 reserved_GiB=5.33
v[invoices]_norm=74.2589
v[hiking]_norm=65.7389
v[repairs]_norm=88.0340
v[cooking]_norm=74.4728
v[taxes]_norm=60.5892
v[pets]_norm=85.2290
leave-one-topic-out scores (v from other topics):
  topic=cooking strategy=deceptive s_v=-0.1495
  topic=cooking strategy=deceptive s_v=-0.0599
  topic=cooking strategy=deceptive s_v=-0.0278
  topic=cooking strategy=honest s_v=-0.1673
  topic=cooking strategy=honest s_v=-0.0250
  topic=cooking strategy=honest s_v=-0.0713
  topic=hiking strategy=deceptive s_v=-0.0616
  topic=hiking strategy=deceptive s_v=0.0661
  topic=hiking strategy=deceptive s_v=-0.0206
  topic=hiking strategy=honest s_v=-0.1724
  topic=hiking strategy=honest s_v=-0.0279
  topic=hiking strategy=honest s_v=0.0576
  topic=invoices strategy=deceptive s_v=-0.0597
  topic=invoices strategy=deceptive s_v=-0.0148
  topic=invoices strategy=deceptive s_v=0.1288
  topic=invoices strategy=honest s_v=-0.0678
  topic=invoices strategy=honest s_v=-0.0373
  topic=invoices strategy=honest s_v=0.1158
  topic=pets strategy=deceptive s_v=-0.0372
  topic=pets strategy=deceptive s_v=0.0604
  topic=pets strategy=deceptive s_v=0.2173
  topic=pets strategy=honest s_v=0.0781
  topic=pets strategy=honest s_v=0.0961
  topic=pets strategy=honest s_v=0.1932
  topic=repairs strategy=deceptive s_v=-0.0113
  topic=repairs strategy=deceptive s_v=-0.0583
  topic=repairs strategy=deceptive s_v=0.0034
  topic=repairs strategy=honest s_v=-0.2036
  topic=repairs strategy=honest s_v=-0.0427
  topic=repairs strategy=honest s_v=-0.0012
  topic=taxes strategy=deceptive s_v=-0.0203
  topic=taxes strategy=deceptive s_v=0.0314
  topic=taxes strategy=deceptive s_v=-0.0172
  topic=taxes strategy=honest s_v=-0.0763
  topic=taxes strategy=honest s_v=-0.0322
  topic=taxes strategy=honest s_v=-0.1136
mean s_v deceptive=-0.0017 honest=-0.0277 gap_dec_minus_hon=0.0260
topic_probe_acc_on_r=0.81 n=36 topics=['cooking', 'hiking', 'invoices', 'pets', 'repairs', 'taxes']
v built from pair tags. Tags are not a loss input.
Not a deception result. Do not train the hinge on this r yet.

```

exit 0

## python pair_adversary.py --data /home/pauli/dockers/intent-readout-search/data/pairs_wide.jsonl

started 2026-09-20T22:27:26.644973+00:00

```

Loading weights:   0%|          | 0/339 [00:00<?, ?it/s]
Loading weights:   1%|          | 2/339 [00:00<00:18, 18.70it/s]
Loading weights:   9%|▊         | 29/339 [00:00<00:01, 157.04it/s]
Loading weights:  22%|██▏       | 76/339 [00:00<00:00, 291.54it/s]
Loading weights:  35%|███▌      | 120/339 [00:00<00:00, 346.81it/s]
Loading weights:  48%|████▊     | 162/339 [00:00<00:00, 365.34it/s]
Loading weights:  62%|██████▏   | 209/339 [00:00<00:00, 395.25it/s]
Loading weights:  76%|███████▌  | 257/339 [00:00<00:00, 412.97it/s]
Loading weights:  90%|████████▉ | 304/339 [00:00<00:00, 429.21it/s]
Loading weights: 100%|██████████| 339/339 [00:00<00:00, 372.48it/s]
VRAM allocated_GiB=5.18 reserved_GiB=5.33
n=36 topics=['cooking', 'hiking', 'invoices', 'pets', 'repairs', 'taxes'] dim_r=8 beta=1.0 steps=200
hold=cooking n_train=30 n_hold=6 topic_acc_adv_train=0.70 strat_acc_hold=0.50 logit_dec=-345.8472 logit_hon=-530.8939 gap_dec_minus_hon=185.0468
hold=hiking n_train=30 n_hold=6 topic_acc_adv_train=0.67 strat_acc_hold=0.50 logit_dec=-581.9681 logit_hon=-525.8040 gap_dec_minus_hon=-56.1641
hold=invoices n_train=30 n_hold=6 topic_acc_adv_train=1.00 strat_acc_hold=0.50 logit_dec=-273.7042 logit_hon=-302.9212 gap_dec_minus_hon=29.2170
hold=pets n_train=30 n_hold=6 topic_acc_adv_train=0.87 strat_acc_hold=0.50 logit_dec=-540.6214 logit_hon=-415.6704 gap_dec_minus_hon=-124.9510
hold=repairs n_train=30 n_hold=6 topic_acc_adv_train=0.53 strat_acc_hold=0.50 logit_dec=-650.7950 logit_hon=-641.1513 gap_dec_minus_hon=-9.6438
hold=taxes n_train=30 n_hold=6 topic_acc_adv_train=1.00 strat_acc_hold=0.50 logit_dec=-323.0489 logit_hon=-360.0275 gap_dec_minus_hon=36.9787
mean_gap=10.0806 mean_topic_acc_adv_train=0.79
Tags build CE only. Frozen-I is not this r. No hinge.
Not a deception result.

```

exit 0

## python head_write_probe.py --data /home/pauli/dockers/intent-readout-search/data/pairs_wide.jsonl

started 2026-09-20T22:27:34.655248+00:00

```

Loading weights:   0%|          | 0/339 [00:00<?, ?it/s]
Loading weights:   1%|          | 2/339 [00:00<00:17, 18.74it/s]
Loading weights:   9%|▊         | 29/339 [00:00<00:01, 156.62it/s]
Loading weights:  22%|██▏       | 76/339 [00:00<00:00, 289.35it/s]
Loading weights:  35%|███▍      | 118/339 [00:00<00:00, 338.51it/s]
Loading weights:  47%|████▋     | 161/339 [00:00<00:00, 370.19it/s]
Loading weights:  61%|██████▏   | 208/339 [00:00<00:00, 397.94it/s]
Loading weights:  74%|███████▎  | 250/339 [00:00<00:00, 403.94it/s]
Loading weights:  86%|████████▋ | 293/339 [00:00<00:00, 411.72it/s]
Loading weights: 100%|██████████| 339/339 [00:00<00:00, 367.84it/s]
VRAM allocated_GiB=5.18 reserved_GiB=5.33
n_layers=28 layer=14 k=4 mode=loud
picked_heads=15,22,23,25 write_norm=5.8998,3.8260,5.1146,5.1170
pair cosine of r to bank-deceptive head-writes:
  topic=invoices strategy=deceptive s*_D=0.5016
  topic=invoices strategy=honest s*_D=0.4779
  topic=hiking strategy=deceptive s*_D=0.5738
  topic=hiking strategy=honest s*_D=0.5068
  topic=repairs strategy=deceptive s*_D=0.4763
  topic=repairs strategy=honest s*_D=0.4333
  topic=cooking strategy=deceptive s*_D=0.4868
  topic=cooking strategy=honest s*_D=0.4733
  topic=taxes strategy=deceptive s*_D=0.5457
  topic=taxes strategy=honest s*_D=0.5411
  topic=pets strategy=deceptive s*_D=0.4258
  topic=pets strategy=honest s*_D=0.3810
  topic=invoices strategy=deceptive s*_D=0.3770
  topic=invoices strategy=honest s*_D=0.2752
  topic=hiking strategy=deceptive s*_D=0.4150
  topic=hiking strategy=honest s*_D=0.3949
  topic=repairs strategy=deceptive s*_D=0.4175
  topic=repairs strategy=honest s*_D=0.4231
  topic=cooking strategy=deceptive s*_D=0.3063
  topic=cooking strategy=honest s*_D=0.2440
  topic=taxes strategy=deceptive s*_D=0.3763
  topic=taxes strategy=honest s*_D=0.3408
  topic=pets strategy=deceptive s*_D=0.4559
  topic=pets strategy=honest s*_D=0.4136
mean s*_D deceptive=0.4465 honest=0.4087 gap_hon_minus_dec=-0.0378
topic_probe_acc_head_r=1.00 topic_probe_acc_layer_h=1.00 n=24 topics=['cooking', 'hiking', 'invoices', 'pets', 'repairs', 'taxes']
Heads picked on bank write-norm only. Not a deception result.
Topic acc 1.00 on r is a fail.

```

exit 0

## python head_write_probe.py --data /home/pauli/dockers/intent-readout-search/data/pairs_wide.jsonl --quiet

started 2026-09-20T22:27:41.844588+00:00

```

Loading weights:   0%|          | 0/339 [00:00<?, ?it/s]
Loading weights:   1%|          | 2/339 [00:00<00:18, 18.55it/s]
Loading weights:   9%|▊         | 29/339 [00:00<00:01, 156.07it/s]
Loading weights:  22%|██▏       | 76/339 [00:00<00:00, 288.28it/s]
Loading weights:  35%|███▍      | 118/339 [00:00<00:00, 336.47it/s]
Loading weights:  47%|████▋     | 161/339 [00:00<00:00, 367.11it/s]
Loading weights:  61%|██████▏   | 208/339 [00:00<00:00, 394.55it/s]
Loading weights:  73%|███████▎  | 249/339 [00:00<00:00, 398.96it/s]
Loading weights:  86%|████████▋ | 293/339 [00:00<00:00, 407.43it/s]
Loading weights: 100%|██████████| 339/339 [00:00<00:00, 364.94it/s]
VRAM allocated_GiB=5.18 reserved_GiB=5.33
n_layers=28 layer=14 k=4 mode=quiet
picked_heads=0,2,3,5 write_norm=0.6579,0.6092,0.6405,0.7030
pair cosine of r to bank-deceptive head-writes:
  topic=invoices strategy=deceptive s*_D=0.9574
  topic=invoices strategy=honest s*_D=0.7840
  topic=hiking strategy=deceptive s*_D=0.9324
  topic=hiking strategy=honest s*_D=0.9331
  topic=repairs strategy=deceptive s*_D=0.9764
  topic=repairs strategy=honest s*_D=0.9449
  topic=cooking strategy=deceptive s*_D=0.9839
  topic=cooking strategy=honest s*_D=0.9772
  topic=taxes strategy=deceptive s*_D=0.9780
  topic=taxes strategy=honest s*_D=0.9818
  topic=pets strategy=deceptive s*_D=0.9785
  topic=pets strategy=honest s*_D=0.8662
  topic=invoices strategy=deceptive s*_D=0.9769
  topic=invoices strategy=honest s*_D=0.9590
  topic=hiking strategy=deceptive s*_D=0.9506
  topic=hiking strategy=honest s*_D=0.8591
  topic=repairs strategy=deceptive s*_D=0.9666
  topic=repairs strategy=honest s*_D=0.9777
  topic=cooking strategy=deceptive s*_D=0.9768
  topic=cooking strategy=honest s*_D=0.8599
  topic=taxes strategy=deceptive s*_D=0.9663
  topic=taxes strategy=honest s*_D=0.9780
  topic=pets strategy=deceptive s*_D=0.9778
  topic=pets strategy=honest s*_D=0.9631
mean s*_D deceptive=0.9685 honest=0.9237 gap_hon_minus_dec=-0.0448
topic_probe_acc_head_r=1.00 topic_probe_acc_layer_h=1.00 n=24 topics=['cooking', 'hiking', 'invoices', 'pets', 'repairs', 'taxes']
Heads picked on bank write-norm only. Not a deception result.
Topic acc 1.00 on r is a fail.

```

exit 0

## python head_ablate_probe.py --data /home/pauli/dockers/intent-readout-search/data/pairs_wide.jsonl

started 2026-09-20T22:27:48.900032+00:00

```

Loading weights:   0%|          | 0/339 [00:00<?, ?it/s]
Loading weights:   1%|          | 2/339 [00:00<00:18, 18.54it/s]
Loading weights:   9%|▊         | 29/339 [00:00<00:01, 155.61it/s]
Loading weights:  22%|██▏       | 76/339 [00:00<00:00, 286.76it/s]
Loading weights:  34%|███▎      | 114/339 [00:00<00:00, 320.41it/s]
Loading weights:  47%|████▋     | 161/339 [00:00<00:00, 364.89it/s]
Loading weights:  61%|██████▏   | 208/339 [00:00<00:00, 391.81it/s]
Loading weights:  73%|███████▎  | 249/339 [00:00<00:00, 397.14it/s]
Loading weights:  86%|████████▌ | 292/339 [00:00<00:00, 405.84it/s]
Loading weights:  98%|█████████▊| 333/339 [00:00<00:00, 403.27it/s]
Loading weights: 100%|██████████| 339/339 [00:00<00:00, 359.49it/s]
VRAM allocated_GiB=5.18 reserved_GiB=5.33
n_layers=28 layer=14 k=4 mode=in_sample
n_rank=24 n_eval=24 n_pin=6 rank_has_honest=True
head topic_loo_rank |gap_rank| score
   0 0.21 0.0109 -0.1975
   1 0.33 0.0154 -0.3180
   2 0.25 0.1296 -0.1204
   3 0.42 0.0084 -0.4082
   4 0.08 0.0000 -0.0833
   5 0.08 0.0000 -0.0833
   6 0.33 0.0019 -0.3314
   7 0.08 0.0000 -0.0833
   8 0.21 0.0163 -0.1920
   9 0.42 0.0327 -0.3840
  10 0.38 0.0404 -0.3346
  11 0.58 0.0296 -0.5537
  12 0.33 0.0035 -0.3298
  13 0.42 0.0549 -0.3617
  14 0.42 0.0028 -0.4139
  15 0.42 0.0510 -0.3657
  16 0.62 0.0125 -0.6125
  17 0.58 0.0324 -0.5509
  18 0.46 0.0420 -0.4163
  19 0.29 0.2009 -0.0907
  20 0.50 0.0628 -0.4372
  21 0.54 0.0709 -0.4708
  22 0.75 0.0069 -0.7431
  23 0.83 0.0084 -0.8249
  24 0.88 0.0032 -0.8718
  25 0.46 0.0369 -0.4214
  26 0.67 0.0184 -0.6482
  27 0.83 0.0087 -0.8246
picked_heads=4,5,7,19
eval topic_probe_acc=1.00 topic_loo=0.29 mean s*_D dec=0.9683 hon=0.9165 gap_hon_minus_dec=-0.0518 n=24 topics=['cooking', 'hiking', 'invoices', 'pets', 'repairs', 'taxes']
Heads ranked off eval when --holdout. Topic acc 1.00 on r is a fail.
Not a deception result.

```

exit 0

## python head_ablate_probe.py --data /home/pauli/dockers/intent-readout-search/data/pairs_wide.jsonl --holdout

started 2026-09-20T22:27:56.103026+00:00

```

Loading weights:   0%|          | 0/339 [00:00<?, ?it/s]
Loading weights:   1%|          | 2/339 [00:00<00:18, 18.72it/s]
Loading weights:   9%|▊         | 29/339 [00:00<00:01, 157.87it/s]
Loading weights:  22%|██▏       | 76/339 [00:00<00:00, 292.01it/s]
Loading weights:  35%|███▍      | 118/339 [00:00<00:00, 341.06it/s]
Loading weights:  47%|████▋     | 161/339 [00:00<00:00, 371.74it/s]
Loading weights:  61%|██████▏   | 208/339 [00:00<00:00, 399.52it/s]
Loading weights:  74%|███████▎  | 250/339 [00:00<00:00, 405.97it/s]
Loading weights:  86%|████████▋ | 293/339 [00:00<00:00, 411.62it/s]
Loading weights: 100%|██████████| 339/339 [00:00<00:00, 369.31it/s]
VRAM allocated_GiB=5.18 reserved_GiB=5.33
n_layers=28 layer=14 k=4 mode=holdout
n_rank=12 n_eval=24 n_pin=6 rank_has_honest=True
head topic_loo_rank |gap_rank| score
   0 0.58 0.0041 -0.5792
   1 0.92 0.0991 -0.8176
   2 0.17 0.0545 -0.1121
   3 0.58 0.0481 -0.5353
   4 0.25 0.0000 -0.2500
   5 0.08 0.0000 -0.0833
   6 0.50 0.0718 -0.4282
   7 0.17 0.0000 -0.1667
   8 0.25 0.0222 -0.2278
   9 0.08 0.2493 0.1660
  10 0.83 0.1122 -0.7212
  11 1.00 0.0840 -0.9160
  12 0.58 0.1363 -0.4470
  13 0.25 0.1462 -0.1038
  14 0.83 0.2611 -0.5723
  15 0.42 0.5519 0.1353
  16 0.58 0.5015 -0.0819
  17 0.58 0.3506 -0.2328
  18 0.50 0.4949 -0.0051
  19 0.58 0.5057 -0.0776
  20 0.50 0.5016 0.0016
  21 0.58 0.1208 -0.4625
  22 0.83 0.1069 -0.7265
  23 0.92 0.3218 -0.5948
  24 1.00 0.1543 -0.8457
  25 0.50 0.3561 -0.1439
  26 0.67 0.2153 -0.4514
  27 0.75 0.2112 -0.5388
picked_heads=9,15,18,20
eval topic_probe_acc=1.00 topic_loo=0.54 mean s*_D dec=0.3789 hon=0.3545 gap_hon_minus_dec=-0.0244 n=24 topics=['cooking', 'hiking', 'invoices', 'pets', 'repairs', 'taxes']
Heads ranked off eval when --holdout. Topic acc 1.00 on r is a fail.
Not a deception result.

```

exit 0

## summary

- all jobs exit 0

finished 2026-09-20T22:28:03.449828+00:00
