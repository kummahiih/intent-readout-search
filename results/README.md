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

## Topic-axis residual — slot

```bash
python topic_residual.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs.jsonl
python topic_residual.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs_paraphrase.jsonl
```

Paste both stdouts. Do not edit the identity tables.
