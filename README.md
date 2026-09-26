# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-26)

Layer-8 last-token LOTO contrast is a **hint**, not $r_{\mathrm{strat}}$.

- 6-topic: gap 0.066, topic L2 **0.17**, $p=0$.
- 8-topic: gap 0.105, topic L2 **0.06**, paraphrase $p=0$.
- Hold travel/neighbors out of $v$: kept gap 0.066; held gap **0.149** $p=0.005$. Transfer of the six old rooms $p=0.0003$. Held paraphrase $p=0.056$ (n=8).
- Last layer on the same 8-topic files: gap 0.029, topic L2 0.23, paraphrase $p=0.25$. Fail.
- Hiking fit ~0. Invoices transfer ~0. Wipe and heads fail.

The new rooms were not the only source of the 8-topic gap. They still separate when they never enter $v$. That is not a license to freeze $r$: two hallways stay dead, notes share a template family, $\hat m$ is high-rank. Not reduced deception.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).
