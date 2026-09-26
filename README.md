# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-27)

Mid-layer contrast is a **hint** on two families, not $r_{\mathrm{strat}}$.

- Qwen layer 8 last-token: gap 0.105, topic L2 **0.06**, paraphrase $p=0$.
- Qwen layer 8 K-step: gap 0.195, topic L2 0.15, paraphrase $p=0$. $\cos$ to last 0.70.
- Qwen layer 8 SIREN $f(1)$: gap 0.140, topic L2 0.08, paraphrase $p=0$.
- Mistral layer 9 last / K-step / SIREN: same pattern (0.116 / 0.192 / 0.058).
- Last layer fails the topic gate on both models.
- Rewritten hiking/invoices: voice $p\ge 0.6$ on every pool. Dead rooms travel.

K-step is a louder last-window, not a new axis. Do not freeze $r$. Do not fill $D$.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).
