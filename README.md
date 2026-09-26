# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-27)

Mid-layer contrast is a **hint** on two families. last-token, K-step, SIREN $f(1)$, and their unit-sum (`mid3`) are one arrow, not four cameras.

- Qwen L8 mid3: gap 0.164, topic L2 0.15, paraphrase $p=0$, $\cos$ to last 0.85.
- Mistral L9 mid3: gap 0.140, topic L2 **0.00**, paraphrase $p=0$, $\cos$ to last 0.83.
- Voice hiking/invoices: Qwen $p=0.66$, Mistral $p=0.92$. Dead.
- Last-layer mid3 fails the topic gate on both models.

Do not freeze $r$. Do not fill $D$. Not reduced deception.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).
