# Intent readout search

Can $r$ track strategy when the tag is a random variable?

Topic-subtract and same-topic contrast failed B0 (topic acc 1.00; contrast gap ~0.06). Next camera: a small $r$ scored for strategy while an adversary reads topic (`pair_adversary.py`). Tags are losses only. The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic).

```bash
python pair_adversary.py              # GPU extract; CPU linear r vs topic adversary
python pair_contrast.py               # GPU; v = h_dec - h_hon, leave-one-topic-out
python topic_residual.py --sweep      # GPU; embed / 1/4 / 1/2 / 3/4 / last
python topic_residual.py --layer -1   # last hidden only
python synthetic_z.py                 # inspector 0.5 default
python synthetic_z.py --inspect 0     # old no-cost lie
python synthetic_pareto.py            # pay vs lie-rate vs hinge
python pair_metrics.py --data data/pairs.jsonl
```

[PROTOCOL.md](PROTOCOL.md) · [results/README.md](results/README.md)
