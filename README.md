# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-26)

Layer-8 last-token LOTO contrast is a **hint**, not $r_{\mathrm{strat}}$.

- 8-topic: gap 0.105, topic L2 **0.06**, paraphrase $p=0$.
- Hold travel/neighbors out of $v$: those rooms still separate (held 0.149, $p=0.005$).
- Hold hiking/invoices out of $v$: original held gap 0.034 $p=0.10$. Rewritten voice file gap **-0.030** $p=0.31$.
- Last layer on the same 8-topic files fails paraphrase ($p=0.25$).

Hiking and invoices are dead rooms, not a wording glitch. The hint lives in a subset of hallways that share a note family. Not a frozen $r$. Not reduced deception.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).
