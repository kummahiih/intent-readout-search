# Intent readout search

Can we build an \(r\) and a bank \(D\) that track **strategy given topic**?

Glossary: [kummahiih/regret-heuristic](https://github.com/kummahiih/regret-heuristic). [RELATED.md](RELATED.md). [PROTOCOL.md](PROTOCOL.md).

Identity last-token failed on `pairs.jsonl` and `pairs_paraphrase.jsonl` (topic acc 1.00, |gap| ≤ 0.01).

Next sensor: drop the bank topic axis.

```bash
source /media/pauli/datapata/rh-venv/bin/activate
python topic_residual.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs.jsonl
python topic_residual.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs_paraphrase.jsonl
```

[results/README.md](results/README.md)
