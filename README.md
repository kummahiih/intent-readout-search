# Intent readout search

Can we build an \(r\) and a bank \(D\) that track **strategy given topic**?

This is not the hinge paper. Glossary: [kummahiih/regret-heuristic](https://github.com/kummahiih/regret-heuristic). Neighbors: [RELATED.md](RELATED.md).

## Already failed

Old jsonl last-token 0.77 / 0.80; mean-pool 0.86 / 0.85.  
`pairs.jsonl` identity (2026-09-16): mean s* 0.918 deceptive / 0.928 honest, topic probe **1.00**. Failed.

## This repo

[PROTOCOL.md](PROTOCOL.md) — gap must survive a topic probe **and** a paraphrase.

```bash
source /media/pauli/datapata/rh-venv/bin/activate
python pair_metrics.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs.jsonl
```

## Ledger

[results/README.md](results/README.md)
