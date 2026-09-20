# Intent readout search

Can $r$ track strategy when the tag is a random variable?

B0 default camera is topic-subtract (`topic_residual.py`). Last-layer cut already failed the topic probe (acc 1.00, gap 0.03). Next cheap check: same cut at other layers. Packing fights a clean split. The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic).

```bash
python topic_residual.py --sweep      # GPU; embed / 1/4 / 1/2 / 3/4 / last
python topic_residual.py --layer -1   # last hidden only (old default)
python synthetic_z.py                 # inspector 0.5 default
python synthetic_z.py --inspect 0     # old no-cost lie
python synthetic_pareto.py            # pay vs lie-rate vs hinge
python pair_metrics.py --data data/pairs.jsonl
```

[PROTOCOL.md](PROTOCOL.md) · [results/README.md](results/README.md)
