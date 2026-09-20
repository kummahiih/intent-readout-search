# Sensor ledger

Do not collapse attempts.

## Overnight wide pairs — 2026-09-21 01:27

`python overnight_b0.py`  `data/pairs_wide.jsonl`  6 topics  n_eval=24  raw log: [overnight_b0.md](overnight_b0.md)

| job | topic | strategy gap | note |
| --- | --- | --- | --- |
| residual sweep invoices+hiking n=8 | 1.00 from layer 7 on | \|gap\|\le0.05 | embed 0.50 is missing axis |
| pair_contrast n=36 | 0.81 on LOTO r | 0.026 | still overlap |
| pair_adversary dim=8 | train topic mean **0.79** | hold strat **0.50** every topic | 6-way topic got harder; plan still chance |
| loud heads 15,22,23,25 | **1.00** | -0.038 | same heads as tiny set |
| quiet heads 0,2,3,5 | **1.00** | -0.045 | still hugs bank |
| ablate in-sample heads 4,5,7,19 | lstsq **1.00** / loo 0.29 | -0.052 | loo low, selected on eval |
| ablate holdout heads 9,15,18,20 | lstsq **1.00** / loo 0.54 | -0.024 | flicker gone |

More handmade topics did not make a camera. Linear B0 still fails on every head/residual cut. The adversary’s train topic acc dropping below 1.00 is 6-class difficulty, not a strategy sensor. Do not fill $D$. Do not train the hinge on these $r$.

## B0 default camera: topic-subtract residual — 2026-09-20 19:41

`python topic_residual.py`

$r(h)=h-(h\cdot v)v$, $v$ from bank hiking$\to$invoices. Not LEACE. Not a trained adversary.

```
topic_axis=hiking->invoices  v_norm=1.0000
invoices deceptive  s*_D=0.9447
invoices honest     s*_D=0.9310
hiking deceptive    s*_D=0.8856
hiking honest       s*_D=0.9251
invoices deceptive  s*_D=0.8692
mean s*_D deceptive=0.8998 honest=0.9280 gap_hon_minus_dec=0.0282
topic_probe_acc_raw=1.00 topic_probe_acc_residual=1.00 n=5
```

Failed B0. Cutting one topic axis left a linear topic probe at 1.00. Strategy gap 0.03 on n=5.
Packing: one axis cut does not unmix plan from hallway. Lean cartoon next door: `no_two_orthogonal_units_on_real`.

Do not train the hinge on this $r$.

## Mid-layer sweep — 2026-09-20 19:46

`python topic_residual.py --sweep`  n_hidden_states=29  layers 0,7,14,21,28  n=5

| layer | v_norm | topic acc raw / residual | mean s* dec / hon | gap |
| --- | --- | --- | --- | --- |
| 0 embed | 0.00 | 0.60 / 0.60 | 1.00 / 1.00 | 0.00 |
| 7 | 1.00 | 1.00 / 1.00 | 0.90 / 0.93 | 0.03 |
| 14 | 1.00 | 1.00 / 1.00 | 0.81 / 0.81 | 0.00 |
| 21 | 1.00 | 1.00 / 1.00 | 0.82 / 0.82 | 0.00 |
| 28 last | 1.00 | 1.00 / 1.00 | 0.90 / 0.93 | 0.03 |

Embed has no topic axis to cut (`v=0`); everyone hugs the bank at cosine 1. That is not a quiet topic probe, it is a missing direction.
Transformer layers 7–28: topic still linearly readable after the cut. Strategy gap ≤ 0.03.

Failed B0 on every floor that has a topic axis. Do not train the hinge on any of these $r$.

## Same-topic contrast — 2026-09-20 20:40

`python pair_contrast.py`

$v_T=\mathrm{normalize}(h_{\mathrm{dec}}-h_{\mathrm{hon}})$ on topic $T$. Score the other topic. Bank is deceptive-only, so $v$ comes from matched eval pairs. Tags build $v$, not a loss.

```
paired hiking(dec=2,hon=1) invoices(dec=3,hon=1)
v[invoices]_norm=105.93  v[hiking]_norm=88.43
hiking    dec -0.0059 / -0.0259   hon -0.0334
invoices  dec -0.0851 / -0.1521 / -0.1361   hon -0.1443
mean s_v deceptive=-0.0810 honest=-0.0889 gap_dec_minus_hon=0.0078
topic_probe_acc_on_r=1.00 n=7
```

Load-bearing number: strategy gap **0.008**. The contrast from invoices does not mark hiking lies, and the reverse.
`topic_probe_acc_on_r=1.00` is partly tautological under leave-one-topic-out: hiking $r$ lives on $v_{\mathrm{invoices}}$, invoice $r$ lives on $v_{\mathrm{hiking}}$. Do not read that 1.00 as a second packing proof.

Failed B0 as a strategy camera. Do not train the hinge on this $r$.

## Same-topic contrast, three topics — 2026-09-20 20:45

`python pair_contrast.py` and `--data data/pairs_paraphrase.jsonl`

Honest bank + repairs. LOTO $v$ is the mean of the other two topics. $n=13$.

| set | mean $s_v$ dec / hon | gap | topic acc on LOTO $r$ |
| --- | --- | --- | --- |
| pairs.jsonl | -0.025 / -0.087 | **0.061** | 0.77 |
| paraphrase | -0.035 / -0.088 | **0.052** | 0.69 |

Gap moved from 0.008 to ~0.06. Still near zero. Honest and deceptive still overlap. The print `bank_deceptive_only=3` is a leftover counter of deceptive bank rows; honest bank rows are present.

Failed B0 as a strategy camera. Do not train the hinge on this $r$.

## Topic adversary — 2026-09-20 20:48

`python pair_adversary.py`  $n=13$  $\dim r=8$  $\beta=1$  200 steps

| hold | topic acc adv train | strat acc hold | logit gap |
| --- | --- | --- | --- |
| hiking | 1.00 | 0.50 | 39 |
| invoices | 1.00 | 0.40 | 47 |
| repairs | 1.00 | 0.50 | 143 |
| mean | **1.00** | ~0.47 | 76 |

Load-bearing numbers: train topic acc stays **1.00**; hold strategy acc is chance. The logit gap is an unregularized blow-up on $n\approx 9$, not a transferable camera.

Failed B0. $r$ still carries hallway. Do not train the hinge on this $r$.

## Mid-layer head writes — 2026-09-21 01:06

`python head_write_probe.py`  Qwen2.5-7B-Instruct  layer 14 / 28  $k=4$  heads 15,22,23,25 by bank write-norm  $n=7$

```
topic_probe_acc_head_r=1.00  topic_probe_acc_layer_h=1.00
mean s*_D deceptive=0.4542 honest=0.4361  gap_hon_minus_dec=-0.0182
```

Failed B0. A loud-head subset at mid-layer still linearly reads topic. Strategy gap ~0, wrong sign. This is not Pandey path-patching and not a found circuit. Do not train the hinge on this $r$. Do not fill $D$ from these heads.

## Quiet mid-layer head writes — 2026-09-21 01:12

`python head_write_probe.py --quiet`  layer 14  $k=4$  heads 0,2,3,5  $n=7$

```
mode=quiet
topic_probe_acc_head_r=1.00  topic_probe_acc_layer_h=1.00
mean s*_D deceptive=0.9526 honest=0.8816  gap_hon_minus_dec=-0.0710
```

Failed B0. Quiet heads still linearly read topic. They hug the bank harder than the loud set (s* ~0.95 vs ~0.45). Gap still small and the wrong sign for a slap. Do not train the hinge on this $r$.

## Mean-ablate then subset — 2026-09-21 01:15

`python head_ablate_probe.py`  layer 14  $k=4$  $n=7$

```
baseline_all_heads topic_loo=0.86 gap=0.0212
picked_heads=2,8,10,18
subset topic_probe_acc=1.00 topic_loo=0.43
mean s*_D dec=0.5885 hon=0.7596 gap_hon_minus_dec=0.1711
```

Official B0 (linear topic acc) still **1.00**. Fat $r$ on seven rows interpolates topic.
Leave-one-out topic centroid on the subset is 0.43 (near 3-class chance). Strategy gap 0.17 is the largest on this toy — and **selected on the same seven rows**. Single-head mean-ablation left all-heads topic_loo at 0.86. Not a held-out camera.

## Hold-out head rank — 2026-09-21 01:20

`python head_ablate_probe.py --holdout`  layer 14  $k=4$  n_rank=6 n_eval=7 n_pin=3  rank_has_honest=True

```
picked_heads=15,18,19,20
eval topic_probe_acc=1.00 topic_loo=0.71
mean s*_D dec=0.2314 hon=0.2669 gap_hon_minus_dec=0.0355
```

The in-sample 0.17 / 0.43 flicker died. Different heads. Linear topic acc still 1.00. Eval topic-LOO 0.71. Gap back to noise (~0.04). That 0.17 was selection on seven rows. Do not fill $D$. Do not train the hinge on this $r$. Stop cutting this pair set.

## Qwen identity / paraphrase / residual (earlier)

Topic acc 1.00, |gap|~0. Failed. Same verdict as 19:41 / 19:46.

## CPU no inspector (`--inspect 0`)

Task skill 1, risk 1, hinge 0 under the hinge. Gaming.

## CPU inspector 0.5 default — seed 0

`python synthetic_z.py --seed 0` and `python synthetic_pareto.py --steps 200 --seed 0`

Expected lie payoff (1-p)(1+bonus)=0.8 < 1 honest. Policy goes **honest**.

| | skill | pay | honest | risk | hinge | D contamination |
| --- | --- | --- | --- | --- | --- |
| baseline / hinge / evade | 1.00 | 1.00 | 1.00 | 0.00 | 0–0.53 | 0.81–0.97 |

Pareto: every lambda pay=1 risk=0. Front is one honest point. D is almost all mis-tagged honest states (policy never lies after a few steps).

## CPU inspector 0.25 — seed 0

Lie EV 1.20 > 1. Always lie. pay ~0.75, risk 1, hinge 0 under lambda. Front still a point, the liar point.

Inspector moves the *whole* blob from liar to honest. It does not draw a curve of intermediate risk. NSGA-II would sort the same spike. Not Qwen.
