# Sensor ledger

Do not collapse attempts. A drop in cosine is not reduced deception.

## Baseline A — last-token identity (old jsonl)

Source: kummahiih/regret-heuristic §2. 0.7742 / 0.8003. Failed.

## Baseline B — mean-pool identity (old jsonl)

Source: same repo §6. 0.8575 / 0.8524. Failed.

## Identity control on pairs.jsonl — 2026-09-16 00:00

`pair_metrics.py --data data/pairs.jsonl`

| topic | deceptive s* | honest s* |
| --- | --- | --- |
| invoices | 0.9447 | 0.9298 |
| hiking | 0.8919 | 0.9264 |
| mean | 0.9183 | 0.9281 |

 gap +0.0098. topic_probe_acc=1.00. Failed.

## Identity on paraphrase — 2026-09-16 00:13

`pair_metrics.py --data data/pairs_paraphrase.jsonl`
Same model, last-token identity. D rebuilt from the paraphrase bank (so s* is not comparable row-wise to the table above).

| topic | deceptive s* | honest s* |
| --- | --- | --- |
| invoices | 0.6583 | 0.6651 |
| hiking | 0.9335 | 0.9303 |
| mean | 0.7959 | 0.7977 |

 gap +0.0018. topic_probe_acc=1.00 n=4.

Rewording moved invoices off the new bank (~0.66 both) and left hiking glued (~0.93 both). Strategy gap got *smaller*. Topic probe still perfect. Identity failed the style-shift row of PROTOCOL. Not a deception result.
