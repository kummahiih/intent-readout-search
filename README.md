# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-26)

Layer-8 last-token LOTO contrast is a **hint**, not $r_{\mathrm{strat}}$. SIREN $f(1)$ on the same layer is the same hint, not a new camera.

- Last-token 8-topic: gap 0.105, topic L2 **0.06**, paraphrase $p=0$.
- SIREN $f(1)$ 8-topic: gap 0.140, topic L2 **0.08**, paraphrase $p=0$. $\cos(f(1),h_T)=0.35$ (not last-token). $\theta$ L2 plan~71 topic~75.
- Hold travel/neighbors: both sensors still separate those rooms.
- Rewritten hiking/invoices: last-token $p=0.31$, SIREN $p=0.82$. Dead.
- Last-layer SIREN: gap 0.038, topic L2 0.21. Fail.

Do not put $\theta$ in $L$. Do not fill $D$. Not reduced deception.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).
