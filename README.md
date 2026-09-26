# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-26)

Layer-8 last-token LOTO contrast is a **hint**, not $r_{\mathrm{strat}}$.

- 6-topic: plan gap 0.066, topic L2 **0.17** (six-way chance), $p=0$.
- 8-topic: plan gap 0.105, topic L2 **0.06** (below eight-way chance 0.125), paraphrase gap 0.108, $p=0$. Hiking +0.011. Invoices transfer dies.
- Last layer on the same 8-topic files: gap 0.029, topic L2 0.23, paraphrase $p=0.25$. Fail.
- Wipe: leftover topic 0.08, plan LOTO 0.58. Fail.
- Loud heads topic 0.69. Quiet heads empty.
- Layer-8 fit $\hat m=29/48$. Contrast $v_T$ rank 8.

A training hinge needs a strategy camera. Identity last-token / mean-pool fail. Layer 8 is the only contrast row that is topic-blind on the official L2 gate *and* keeps a transferred gap, while last layer on the same files does not. Hiking and invoices still fail uniformity. The residual is high-rank. Not a frozen $r$. Not reduced deception.

Numbers: [results/README.md](results/README.md). Source: `results/tests-2026-09-26-3.log`. Rules: [PROTOCOL.md](PROTOCOL.md).
