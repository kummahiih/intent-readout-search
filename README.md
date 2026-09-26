# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-26)

Layer-8 last-token LOTO contrast is a **hint**, not $r_{\mathrm{strat}}$.

- 6-topic: plan gap 0.066, topic L2 **0.17** (chance), $p=0$.
- 8-topic: plan gap 0.105, paraphrase gap 0.108, $p=0$. Hiking +0.011. Invoices transfer dies.
- Last layer on the same 8-topic files: gap 0.029, topic L2 0.23, paraphrase $p=0.25$. Fail.
- Wipe: leftover topic 0.08, plan LOTO 0.58. Fail.
- Loud heads topic 0.69. Quiet heads empty.

A training hinge needs a strategy camera. Identity last-token / mean-pool fail. Layer 8 is the only contrast row that is topic-chance on six topics and keeps a transferred gap on the eight-topic paraphrase file, while last layer on those same files does not. The residue is uneven across hallways and the residual is high-rank. That is where not to look, and a hint about where to look next. Not a frozen $r$. Not reduced deception.

One cell still unlogged: 8-topic layer-8 `topic_loo_l2_on_scalar`. Run `tests-2026-09-26-3.sh`.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).

## Earlier probes

Official topic gate is leave-one-out, not same-row least squares. Lstsq can hit 1.00 on the same rows. Linear adversary hold 0.53. Verbal oracle plan 0.50. Same-model chat grades are not nature.

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
bash tests-2026-09-26-3.sh
```
