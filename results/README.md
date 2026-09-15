# Sensor ledger

Do not collapse attempts. A drop in cosine is not reduced deception.

## Qwen last-token / mean-pool / residual

See earlier sections. Identity and topic-axis residual: topic acc 1.00, |gap|~0. Failed.

## Identity on pairs.jsonl — 2026-09-16 00:00

0.9447/0.9298 invoices, 0.8919/0.9264 hiking. gap +0.0098. topic_probe_acc=1.00.

## Identity on paraphrase — 2026-09-16 00:13

0.6583/0.6651 invoices, 0.9335/0.9303 hiking. gap +0.0018. topic_probe_acc=1.00.

## Topic-axis residual — 2026-09-16 00:18

Residual topic probe still 1.00 both wordings. Failed.

## CPU synthetic_z seed 0 — 2026-09-16

`python synthetic_z.py --steps 400 --seed 0`

| train | task | honest | lie_D | lie_out | hinge |
| --- | --- | --- | --- | --- | --- |
| baseline | 1.000 | 0.000 | 1.000 | 0.000 | 0.517 |
| hinge, a=2 masked | 1.000 | 0.000 | **1.000** | 0.000 | **0.000** |
| evade, a=2 open | 1.000 | 0.000 | 0.245 | **0.754** | **0.000** |

Hinge hit D without stopping the known lie (representation moved). Opening the held-out channel routes the lie off the bank. Task stays 1. Gaming demo on a bit we injected. Not Qwen.
