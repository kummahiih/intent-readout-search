# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Reader takeaway (2026-09-26)

Layer-8 last-token LOTO contrast is a **hint**, not $r_{\mathrm{strat}}$.

- 6-topic: plan gap 0.066, topic L2 **0.17** (chance), $p=0$.
- 8-topic: plan gap 0.105, paraphrase gap 0.108, $p=0$. Hiking +0.011. Invoices transfer dies.
- Last layer on the same 8-topic files: gap 0.029, topic L2 0.23, paraphrase $p=0.25$. Fail.
- Wipe: leftover topic 0.08, plan LOTO 0.58. Fail.
- Loud heads topic 0.69. Quiet heads empty.

One cell still unlogged: 8-topic layer-8 `topic_loo_l2_on_scalar`. Run `tests-2026-09-26-3.sh`.

Full note: [results/READERS.md](results/READERS.md). Ledger: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).

## What we tried earlier (plain language)

Official topic gate is leave-one-out, not same-row least squares.

- Lstsq topic can hit 1.00 on the same rows. Official LOO on heads / layer still above six-way chance.
- Linear adversary hold strategy acc 0.53.
- Last-layer contrast (old 6-topic) gap 0.026, topic L2 0.31. Dead.
- Verbal oracle plan 0.50.
- Same-model chat grades are not nature.

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
bash tests-2026-09-26-3.sh
```
