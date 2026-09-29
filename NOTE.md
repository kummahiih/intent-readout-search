# A mid-layer plan hint that is not a camera

2026-09-29. Search repo only. The hinge in [regret-heuristic](https://github.com/kummahiih/regret-heuristic) does not consume this.

## Question

Can a readout $r(h)$ of a transformer residual stream separate *plan* (hide the fact vs name it) from *subject* (hiking vs invoices) tightly enough to freeze a prototype bank $D$?

Official gates: plan leave-one-topic-out above chance; topic LOO L2 on the scalar near chance; paraphrase keeps the plan call; rooms are not a subset. Tags build the contrast set. They are not a loss input. Do not fill $D$ from a hint.

Within-topic hold (`--held-in-topic`) and fact-held paraphrase (`para_hold`) are diagnostics. They are not a fifth freeze gate.

## Setup

Fit file: `data/pairs_wide.jsonl`, eight topics, three deceptive and three honest notes each. Speech act: `User asked` / `I will`.

Transfer files that may vote: `data/pairs_paraphrase.jsonl` (same act, reworded) and `data/pairs_frame.jsonl` (same sentences plus prefix `Desk note:`).

Models: Qwen2.5-7B-Instruct layer 8 and Mistral-7B-Instruct-v0.3 layer 9 (~0.3 depth). Official pool: last token. Contrast $v_T=\bar h_{\mathrm{dec},T}-\bar h_{\mathrm{hon},T}$, score other topics with the mean of the remaining $v$. Topic gate: `loo_l2_acc` on those scalars. Eight-way chance is $0.125$.

## What held

| | plan fit | topic L2 | paraphrase | 8-topic frame |
| --- | --- | --- | --- | --- |
| Qwen L8 last | $0.105$ | $0.06$ | $0.108$, $p=0$ | $0.102$, $p=0$ |
| Mistral L9 last | $0.116$ | $0.12$ | $0.123$, $p=0$ | $0.125$, $p=0$ |

Last layer fails the topic gate on both models ($0.17$–$0.29$).

K-step, SIREN $f(1)$, and their unit-sum (`mid3`) track the same rooms. $\cos(\mathrm{mid3},h_T)\approx 0.84$. They are one arrow, not four cameras. SIREN $\theta$ does not split plan from topic. $\hat m$ (talker count at rel $0.05$) is $6$ on every $6$-note topic.

**Hold (log only).** A 2+2 / 1+1 fold inside each room still finds a hiking pair *on the note last token*: Qwen `held_inroom` $0.203$, Mistral $0.278$. Fact-held paraphrase keeps that pair (Qwen $0.160$, Mistral $0.179$). Travel is loud on both the hold and LOTO. The same hold on pre-button $h$ does not (Qwen $0.005$, Mistral $0.009$).

## What failed

**Genre.** Office-log / radio / trail-desk rewrites of the same facts kill LOTO even on loud rooms (travel, neighbors): Qwen held $0.004$, $p=0.87$; Mistral $0.036$, $p=0.13$. A three-word prefix on the bank text does not. That voice style is out of the voter set. It is not paraphrase.

**Rooms.** Hiking is thin on the *shared* axis after a lexical rewrite that pulled shared ridge/washout nouns off one side of the pair. Qwen hiking LOTO $0.013$ / paraphrase $0.009$ / frame $0.016$. Mistral $0.069$ / $0.052$ / $0.070$. Travel on the same runs is $\sim 0.16$. The axis is not outdoor-route general on Qwen. Hiking stays in the eight-room set. Dropping it would manufacture a pass. A loud in-room hold does not count as rooms-uniform.

**Cross-model judge.** Camera owns $v$, walk owns $h$, linear $W$ maps walk space into camera space (LOTO). Dims 3584 vs 4096; $W$ fit on 42 rows (underdetermined). Qwen-cam on Mistral walk: hiking $0.028$ / travel $0.151$. Mistral-cam on Qwen walk: fit-set hiking $0.094$, paraphrase hiking $0.026$. After a crude alignment, the same rooms stay loud and the same room stays thin. That is evidence the mid-layer hint is domain-shaped, not evidence you have a portable judge.

**Pre-button $h$.** P-act print LOTO on Mistral ($0.680$ tag / $0.993$ kind) is the YES/NO cell plus tag–button agreement. Same dumps, last token of the *prompt* (plan + question, before the button): tag LOTO $0.011$ on **both** models. In-room hold on unique notes at that same token: Qwen $0.005$, Mistral $0.009$ (hiking $0.001$ / $0.013$). The note-text hiking pair ($0.203$ / $0.278$) is not sitting at the decision token, shared or local.

**Atlas print kind.** Note last-token $h$, label = free-text `reply_kind` on the exec dumps. Tag-fit reproduces the candidate (Qwen LOTO $0.105$, Mistral $0.126$). Kind-fit does not: Qwen $0.057$ on five rooms with $n_{\mathrm{dec}}=5$; hiking/cooking/invoices have no contradict side (hiking 6/6 truth). Mistral kind LOTO skipped — only taxes is two-sided. The assigned tag is still the only label that yields the hint. The print is not that label.

**Elicit fact-bite.** YES/NO on the named fact plus follow-the-plan. Qwen `two_sided_rooms` 8/8 including hiking; Mistral 3/8, hiking has no truth. Almost every print is `NO` plus a restatement of the fact. Deceptive invoices still admit the wire has not left. Kind flips are often `fact_margin` noise on the same speech act, not a hide plan.

**Bailey tax.** In-place wipe on the stored residual: $s_v$ goes to $0$ (`instrument=ok`). Print kind keep is $0.833$ on both models (hiking Qwen $1.00$, Mistral $0.83$). Neighbors is the fragile room (Qwen $0.50$). Quiet-prompt keep stays $0.81$ / $0.46$. This tag $v$ is cheap to zero without changing most prints. That is a reason not to freeze it as $r_{\mathrm{strat}}$.

## What this is not

Not $r_{\mathrm{strat}}$. Not a frozen camera. Not reduced deception. Not a reason to train $L_{\mathrm{reg}}$ or run PPO. SAE latents were not run through these gates and do not enter $L$.

The honest sentence: a mid-layer last-token contrast is paraphrase- and prefix-stable on two 7B instruct models, genre-fragile, not uniform across rooms, and cheap to wipe while the print keeps kind. Hiking has its own pair on the *note*; that pair is not the eight-room direction, not the pre-button state, and not a reliable hide-print. Do not fill $D$.

Numbers: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).
