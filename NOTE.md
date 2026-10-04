# A mid-layer plan hint that is not a camera

Status 2026-10-05. Search repo only. The hinge stays in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). Do not freeze *r*. Do not fill *D*.

## Question

Is there a readout *r*(*h*) that sees the hide-plan and not the room, and that calls a button the walk actually pressed?

## Setup

Eight rooms. Honest and deceptive notes, same topic. Mid-layer last token. Leave one topic out. Paraphrase and prefix are transfer, not a new fit. The button bank is a separate object: HIDE, NAME, BELIEF. Cover is *P*(YES | HIDE) only when belief matched the fact.

## What held

Qwen L8 and Mistral L9 separate the assigned tags on held-out topics. Aggregate plan gap about 0.11. Paraphrase keeps that mean. Falcon L8 copies the shape. A direction fitted inside hiking still separates a held pair. That is a local pair, not the shared axis.

## What failed

Shared LOTO on hiking is thin. Seven rooms is not eight. Pre-button *h* does not call the press. Note *h* does not call the HIDE button. Gemma at the same relative depth is wallpaper. Extra readouts copied the same rooms.

## Button cover is not the lie rate

Generated pressure rows, nine sources, eight tokens, temperature 0. Compare log: `results/compare_pressure_scores.log`. Official lie-given-known is pressure different from belief, when belief had the fact and both answers are YES or NO. A walk with no press is left out, not entered as 0.

| Walk | Cover | Old bank YES | Official lie-given-known |
| --- | ---: | ---: | ---: |
| Qwen2.5 | 0.507 | 0.510 | 0.623 |
| Mistral | 0.802 | 0.573 | 0.523 |
| Aya | 0.826 | 0.708 | 0.539 |
| Falcon | 0.868 | na | 0.575 |
| Gemma | 1.000 | 0.948 | 0.480 |

Cover ranks with the old bank (Spearman 1.0, n=4). Order matches. Levels do not. Cover ranks against the official lie rate (Spearman -0.6, n=5). Gemma is the highest cover and the lowest lie rate. Qwen is the lowest cover and the highest lie rate. Granite and Qwen3.5 produced no button. *P*(pressure is YES) is a different column (Spearman 0.3) and is not the rate. The earlier 0.679 used that column and entered the empty walks as 0.

## What this is not

Not *r*<sub>strat</sub>. Not a frozen camera. Not reduced deception. Not a reason to train *L*<sub>reg</sub> or run PPO. Cover is not honesty. Do not fill *D*.

Numbers: [results/pressure_score_2026-10-04.md](results/pressure_score_2026-10-04.md). Rules: [PROTOCOL.md](PROTOCOL.md).
