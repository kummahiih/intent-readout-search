# Intent readout search

Can we build an \(r\) and a bank \(D\) that track **strategy given topic**?

Glossary: [kummahiih/regret-heuristic](https://github.com/kummahiih/regret-heuristic). [RELATED.md](RELATED.md). [PROTOCOL.md](PROTOCOL.md).

Qwen identity / paraphrase / one-axis residual: topic probe 1.00, strategy gap ~0. Failed.

## CPU known-z harness

Tiny MLP. Ground-truth action is z. No 7B. No GPU.

```bash
python synthetic_z.py
```

Seed 0: baseline always `lie_D` (hinge 0.52). Hinge with `lie_out` masked: still always `lie_D`, hinge **0** (rotated off D). Evade with `lie_out` open: `lie_out` 0.75, hinge 0. Gaming, not honesty. [results/README.md](results/README.md).
