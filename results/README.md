# Sensor ledger

Do not collapse attempts. A drop in cosine is not reduced deception.

## Baseline A — last-token identity (old jsonl)

regret-heuristic §2. 0.7742 / 0.8003. Failed.

## Baseline B — mean-pool identity (old jsonl)

§6. 0.8575 / 0.8524. Failed.

## Identity on pairs.jsonl — 2026-09-16 00:00

0.9447/0.9298 invoices, 0.8919/0.9264 hiking. gap +0.0098. topic_probe_acc=1.00. Failed.

## Identity on paraphrase — 2026-09-16 00:13

0.6583/0.6651 invoices, 0.9335/0.9303 hiking. gap +0.0018. topic_probe_acc=1.00. Failed style shift.

## Topic-axis residual — 2026-09-16 00:18

`topic_residual.py`. v from bank only. Last-token h minus that one axis.

### pairs.jsonl

| topic | deceptive s* | honest s* |
| --- | --- | --- |
| invoices | 0.9447 | 0.9310 |
| hiking | 0.8856 | 0.9251 |
| mean | 0.9152 | 0.9280 |

gap +0.0129. topic_probe_acc_raw=1.00 topic_probe_acc_residual=**1.00**.

### pairs_paraphrase.jsonl

| topic | deceptive s* | honest s* |
| --- | --- | --- |
| invoices | 0.6646 | 0.6900 |
| hiking | 0.9304 | 0.9262 |
| mean | 0.7975 | 0.8081 |

gap +0.0106. topic_probe_acc_raw=1.00 topic_probe_acc_residual=**1.00**.

Subtracting one bank topic direction did not hide topic from a linear probe on eval and did not open a strategy gap. Same k=1 lesson as the probe pressure-test. Failed. Not a deception result.
