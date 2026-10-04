# A mid-layer plan hint that is not a camera

2026-10-05. Search repo only. The hinge in [regret-heuristic](https://github.com/kummahiih/regret-heuristic) does not consume this.

## Question

Can a readout $r(h)$ of a transformer residual stream separate *plan* (hide the fact vs name it) from *subject* (hiking vs invoices) tightly enough to freeze a prototype bank $D$?

Official gates: plan leave-one-topic-out above chance; topic LOO L2 on the scalar near chance; paraphrase keeps the plan call; rooms are not a subset. Tags build the contrast set. They are not a loss input. Do not fill $D$ from a hint.

Within-topic hold (`--held-in-topic`) and fact-held paraphrase (`para_hold`) are diagnostics. They are not a fifth freeze gate.

## Setup

Fit file: `data/pairs_wide.jsonl`, eight topics, three deceptive and three honest notes each. Speech act: `User asked` / `I will`.

Transfer files that may vote: `data/pairs_paraphrase.jsonl` (same act, reworded) and `data/pairs_frame.jsonl` (same sentences plus prefix `Desk note:`).

Models: Qwen2.5-7B-Instruct layer 8 and Mistral-7B-Instruct-v0.3 layer 9 (~0.3 depth). Wave 1 also Gemma-3-4B-it L10 ($n_L=34$) and Falcon3-7B-Instruct L8 ($n_L=28$). Official pool: last token. Contrast $v_T=\bar h_{\mathrm{dec},T}-\bar h_{\mathrm{hon},T}$, score other topics with the mean of the remaining $v$. Topic gate: `loo_l2_acc` on those scalars. Eight-way chance is $0.125$.

## What held

| | plan fit | topic L2 | paraphrase | 8-topic frame |
| --- | --- | --- | --- | --- |
| Qwen L8 last | $0.105$ | $0.06$ | $0.108$, $p=0$ | $0.102$, $p=0$ |
| Mistral L9 last | $0.116$ | $0.12$ | $0.123$, $p=0$ | $0.125$, $p=0$ |
| Falcon L8 last | $0.082$ | $0.12$ | $0.077$ | — |

Last layer fails the topic gate on the 7B pair ($0.17$–$0.29$).

K-step, SIREN $f(1)$, and their unit-sum (`mid3`) track the same rooms. $\cos(\mathrm{mid3},h_T)\approx 0.84$. They are one arrow, not four cameras.

**Hold (log only).** A 2+2 / 1+1 fold inside each room still finds a hiking pair *on the note last token*: Qwen $0.203$, Mistral $0.278$, Falcon $0.247$. Gemma L10 hiking hold is $0.017$ (all-room hold $0.012$, $p=0.90$). The same hold on pre-button $h$ is dead on the 7B pair ($0.005$ / $0.009$).

## What failed

**Genre.** Office-log / radio / trail-desk rewrites kill LOTO even on loud rooms. Out of the voter set. Not paraphrase.

**Rooms.** Hiking is thin on the *shared* axis: Qwen LOTO $0.013$, Mistral $0.069$, Falcon $0.023$, Gemma $0.003$. Travel stays loud on the 7B pair. Do not drop hiking.

**Wave 1 Gemma L10.** Shared gap $0.009$. Topic L2 $0.65$ (wallpaper). Hiking hold is a coin flip. The hide button mixes on hiking ($9$ YES / $9$ NO) and $h_{\mathrm{pre}}$ still does not call it (pre$\to$act $-0.077$; pets+neighbors skip). This is not a small-7B replica.

**Wave 1 Falcon L8.** Same shape as Qwen/Mistral: note hint, topic L2 at chance, loud local hiking pair, paraphrase hiking LOTO $-0.004$, pre$\to$act $-0.006$ on all eight rooms. Print tag LOTO $0.007$.

**Aya / Phi-4.** Tokenizer / Hub gate and `LossKwargs`. Stack misses, not camera votes. $27$B/$70$B deception-probe tensors are not $h$.

**Pre-button and pre$\to$act.** 7B pre tag LOTO $0.011$. $r(h_{\mathrm{pre}})\to$ button is $0.038$ / $0.016$ and does not own hiking.

**Atlas / elicit / Bailey.** Kind-fit thin. Fact-bite prints still admit the fact. Wipe zeros $s_v$ and keeps kind $0.83$.

## Button cover is not the lie rate

Generated pressure rows, nine sources, eight tokens, temperature 0. Compare log: `results/compare_pressure_scores.log`. Official lie-given-known is pressure different from belief, when belief had the fact and both answers are YES or NO. A walk with no press is left out, not entered as 0.

| Walk | Cover | Old bank YES | Official lie-given-known |
| --- | ---: | ---: | ---: |
| Qwen2.5 | 0.507 | 0.510 | 0.623 |
| Mistral | 0.802 | 0.573 | 0.523 |
| Aya | 0.826 | 0.708 | 0.539 |
| Falcon | 0.868 | na | 0.575 |
| Gemma | 1.000 | 0.948 | 0.480 |

Cover ranks with the old bank (Spearman 1.0, n=4). Order matches. Levels do not. Cover ranks against the official lie rate (Spearman $-0.6$, n=5). Gemma is the highest cover and the lowest lie rate. Qwen is the lowest cover and the highest lie rate. Granite and Qwen3.5 produced no button. $P$(pressure is YES) is a different column (Spearman 0.3) and is not the rate. The earlier 0.679 used that column and entered the empty walks as 0.

## What this is not

Not $r_{\mathrm{strat}}$. Not a frozen camera. Not reduced deception. Not a reason to train $L_{\mathrm{reg}}$ or run PPO.

The honest sentence: a mid-layer last-token contrast is paraphrase-stable on **some** 7B-class instruct walks (Qwen, Mistral, Falcon), genre-fragile, not uniform across rooms, and absent at the decision token. Gemma-3-4B at the same relative depth is wallpaper. Hiking has a local pair on the *note* where the 7B-shaped hint exists; that pair is not the eight-room direction and not a predictor of the hide button. Cover on the generated rows is the same instrument as the old bank, and it is not the 711-row lie rate. Do not fill $D$.

Numbers: [results/pressure_score_2026-10-04.md](results/pressure_score_2026-10-04.md). Rules: [PROTOCOL.md](PROTOCOL.md).
