# Intent readout search

Can we build an \(r\) and a bank \(D\) that track **strategy given topic**?

This is not the hinge paper. The hinge and the last-token / mean-pool probes live in [kummahiih/regret-heuristic](https://github.com/kummahiih/regret-heuristic). That repo stays a glossary. Sensors that fail the topic test live here.

## Already failed (baselines, not the next attempt)

From regret-heuristic `experiment_results.md` on Qwen2.5-7B-Instruct 4-bit, same-topic n=2:

| sensor | deceptive vs D | honest vs D |
| --- | --- | --- |
| last-token identity | 0.7742 | 0.8003 |
| mean-pool identity | 0.8575 | 0.8524 |

Topic smear. Mean-pool mixed more.

## This repo

- [PROTOCOL.md](PROTOCOL.md) — metric: strategy gap given topic; topic probe on \(r\) should fail.
- [data/pairs.jsonl](data/pairs.jsonl) — two topics, honest vs omit-cost plan, same frame.
- [pair_metrics.py](pair_metrics.py) — 4-bit last-token identity: prints strategy cosines and a linear topic probe on those vectors.

```bash
source /media/pauli/datapata/rh-venv/bin/activate
python pair_metrics.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs.jsonl
```

Identity last-token is expected to fail again (topic probe works, strategy gap dies). That is a control, not a success.

## Ledger

[results/README.md](results/README.md)
