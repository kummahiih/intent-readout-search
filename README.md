# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-26)

Mid-layer last-token contrast is a **hint** on two families, not $r_{\mathrm{strat}}$.

- Qwen2.5-7B layer 8 last-token: gap 0.105, topic L2 0.06, paraphrase $p=0$.
- Mistral-7B layer 9 last-token: gap 0.116, topic L2 0.12, paraphrase $p=0$.
- Mistral layer 9 K-step: gap 0.192, topic L2 0.10, paraphrase $p=0$. $\cos$ to last 0.67.
- SIREN $f(1)$ follows the same rooms, weaker gap on Mistral.
- Last layer fails the topic gate on both models.
- Rewritten hiking/invoices: voice $p\ge 0.6$ on every Mistral pool. Dead rooms travel too.

Qwen K-step has not been run (the log named qwen-kstep loaded Mistral because `MODEL` was set).

Do not freeze $r$. Do not fill $D$. Not reduced deception.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).
