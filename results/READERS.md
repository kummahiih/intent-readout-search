# Reader conclusions — 2026-09-26

This is what a stranger should take from the two repos. Not a camera handover. Not reduced deception.

## What was asked

Can a readout of the printed walk see *plan* (honest vs deceptive, same topic) without also seeing the *hallway* (hiking vs invoices)?
If yes, freeze that readout and slap a prototype-avoidance hinge on it.
If no, do not train the hinge and do not fill $D$.

## What passed the project's own gates

| Gate | Last-token identity | Layer-8 contrast $v$ | Last layer contrast $v$ | Wipe / heads |
| --- | --- | --- | --- | --- |
| Plan LOTO above chance | no (same-topic smear 0.77/0.80) | yes on these notes | weak 0.029 | no |
| Topic L2 near chance | no | **0.17** on 6 topics (chance) | 0.23 on 8 topics | wipe leftover 0.08; loud heads 0.69 |
| Paraphrase holds | n/a | **yes** on 8-topic file ($p=0$, gap 0.108) | no ($p=0.25$) | n/a |
| Uniform across rooms | no | **no** (hiking ~0, invoices transfer dies) | no | no |

Layer-8 last-token LOTO $v$ is a **hint**: topic-blind on the 6-topic official scalar, transferred on the 8-topic paraphrase file, permutation $0/20000$ in-sample. It is **not** $r_{\mathrm{strat}}$. Hiking is a dead hallway. The two new rooms written the same night are the loudest.

## What a reader must not conclude

- The model is less deceptive.
- $D$ can be filled from $v$.
- PPO / $\beta R$ / SAE-in-the-loss is next.
- $K$-step, SIREN, or $\hat m$ is the camera. $\hat m$ is a crowded-residual log (25/32 at layer 8, 15/48 at last layer). Lean: `totalLoss_ignores_sourceCount`.
- Quiet hinge is safety. Flattening toys already show a silent trained slap and a loud frozen $I$.

## What is still missing as a measurement

`topic_loo_l2_on_scalar` on the **8-topic layer-8 fit**. Six-topic L2 is 0.17. Eight-way chance is 0.125. Run `tests-2026-09-26-3.sh` on the 4070 to close that cell. Until it is logged, do not claim the 8-topic fit is topic-blind.

## One paragraph for a paper-shaped note

A training hinge $L_{\mathrm{task}}+\lambda\mathrm{ReLU}(\max_k\cos(r,d_k)-\tau)$ needs a strategy camera $r$. Identity last-token and mean-pool fail: they hug topic. A leave-one-topic-out contrast at Qwen2.5-7B layer 8 yields a small plan gap that is not a within-topic shuffle accident and that survives paraphrase on an eight-topic handmade set, while the last layer on the same files does not. The residue is uneven across hallways and the hidden state is high-rank. That is evidence about *where not to look*, and a hint about *where to look next*. It is not a frozen $r$ and not a deception result.
