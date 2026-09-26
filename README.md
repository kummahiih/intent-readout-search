# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-27)

Mid-layer last-token contrast is a **hint** on two families. It lives on the bank speech act (`User asked` / `I will`) and on a `Desk note:` prefix of that act. Office-log / radio genre is a different walk and does not vote.

- Qwen L8 last: plan 0.105, topic L2 **0.06**, paraphrase 0.108 $p=0$, 8-topic frame 0.102 $p=0$.
- Mistral L9 last: plan 0.116, topic L2 0.12, paraphrase 0.123 $p=0$, 8-topic frame 0.125 $p=0$.
- K-step / SIREN $f(1)$ / mid3 are the same arrow. Last layer fails topic.
- Hiking is thin on the *shared* axis even in-set (LOTO ~0.01 / 0.03). Quiet room, not genre.
- Voice genre LOTO held ~0.00 / 0.04. Out of the voter set.

Do not freeze $r$. Do not fill $D$. Not reduced deception.

Voters: [PROTOCOL.md](PROTOCOL.md). Numbers: [results/README.md](results/README.md).
