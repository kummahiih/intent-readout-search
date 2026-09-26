# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

## Conclusions (2026-09-27)

A mid-layer last-token contrast is a **hint** on two instruct families. K-step, SIREN $f(1)$, and their unit-sum (`mid3`) track the same rooms. They are not four cameras. Last layer fails the topic gate. Hiking and invoices die under a voice rewrite. $\hat m$ does not mark those rooms.

Eight-way chance is 0.125. Official topic gate is LOO L2 on the scalar.

| model / readout | plan | topic L2 | paraphrase | voice hiking/invoices |
| --- | --- | --- | --- | --- |
| Qwen2.5-7B L8 last | 0.105 | **0.06** | $p=0$ | dead |
| Qwen L8 K-step | 0.195 | 0.15 | $p=0$ | $p=0.65$ |
| Qwen L8 SIREN $f(1)$ | 0.140 | 0.08 | $p=0$ | $p=0.82$ |
| Qwen L8 mid3 | 0.164 | 0.15 | $p=0$ | $p=0.66$ |
| Mistral-7B L9 last | 0.116 | 0.12 | $p=0$ | $p=0.80$ |
| Mistral L9 K-step | 0.192 | 0.10 | $p=0$ | $p=0.62$ |
| Mistral L9 SIREN $f(1)$ | 0.058 | **0.04** | $p=0$ | $p=0.83$ |
| Mistral L9 mid3 | 0.140 | **0.00** | $p=0$ | $p=0.92$ |
| last layer, both models | ~0.03–0.08 | 0.17–0.29 | leftover topic | — |

`mid3` $=\mathrm{normalize}(\hat h_T+\widehat{\mathrm{kstep}}+\widehat{f(1)})$. $\cos(\mathrm{mid3},h_T)\approx 0.84$. last–kstep $\approx 0.70$. last–SIREN $\approx 0.34$. $\theta$ L2 does not split plan from topic. $\theta$ stays out of $L$.

$\hat m$ (talker count, rel 0.05) is 6 on every 6-note topic, hiking and travel included. The stack is full rank. Crowded hallway is not the slap.

Do not freeze $r$. Do not fill $D$. Not reduced deception.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).
