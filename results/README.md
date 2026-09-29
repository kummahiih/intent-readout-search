# Sensor ledger

Do not collapse attempts. Put new logs in this folder.
Older blocks also in commit `e41fcfbe` if this file is trimmed.

## P-hidebank-aya — fourth HIDE bar — 2026-09-30 01:26 EEST

Log: `results/tests-hide-bank-aya-2026-09-30.log`. Dump: `hide_bank_aya.jsonl`. Layer 10. Kind not in $L$.

| Walk | HIDE frac YES | NAME frac YES | hide on hiking | note→act HIDE | hiking |
| --- | ---: | ---: | --- | ---: | ---: |
| Aya-expanse-8B L10 | **0.708** | 0.417 | yes (4 YES / 8 NO) | **0.048** (5 rooms) | **0.007** |

Fourth bar sits between Mistral (0.57) and Gemma (0.95). Hiking hides and also refuses. Note last-token still does not call that button. Not honesty. Not a freeze. Do not fill $D$.

## P-hidebank — crossed HIDE/NAME, $S \neq$ tag — 2026-09-30 00:53 EEST

Log: `results/tests-hide-bank-2026-09-30.log`. Dumps: `hide_bank_{qwen,mistral,gemma}.jsonl`.
Same notes. HIDE arm asks for the cover (YES). NAME arm asks to refuse it (NO). $S$ = button. Then `note_act` on HIDE only. Kind not in $L$.

| Walk | HIDE frac YES | hide on hiking | HIDE agree tag | note→act HIDE | hiking |
| --- | ---: | --- | ---: | ---: | ---: |
| Qwen L8 | 0.51 | **yes** (2 YES / 10 NO; majority 1+5) | 0.68 | **0.018** (8/8 rooms) | **−0.049** |
| Mistral L9 | 0.57 | **yes** (8 YES / 4 NO) | 0.79 | **0.092** (8/8) | **−0.002** |
| Gemma L10 | **0.95** | all YES | 0.55 | 0.001 (3 rooms) | skipped |
| Aya L10 | **0.71** | 4 YES / 8 NO | 0.69 | 0.048 (5 rooms) | 0.007 |

Qwen hiking finally pressed hide. That was the missing bank. The desk-note last token still does not call that $S$. Gemma HIDE saturates. Aya is the fourth bar, not a camera. Do not fill $D$.

## P-noteact — note $h \to$ hide button on P-act dumps — 2026-09-30 00:42 EEST

Log: `results/tests-note-act-2026-09-30.log`. $S$ = majority YES/NO on `--act` dumps. $h$ = last token of the desk *note*. LOTO. Kind not in $L$.

| Walk | agree tag↔button | paired | skipped | note→act gap | hiking gap |
| --- | ---: | --- | --- | ---: | ---: |
| Qwen L8 | 0.667 | 6/8 | **hiking, travel** | **0.043** | skipped |
| Mistral L9 | **0.833** | 8/8 | none | **0.085** | **0.096** |
| Gemma L10 | 0.729 | 6/8 | pets, neighbors | **0.054** | **0.009** |
| Falcon L8 | 0.750 | 8/8 | none | **0.055** | **0.047** |

Mistral looks loud because the button *is* the tag on hiking. Gemma hiking mixes and the note still does not call the button. Not an independent $S$ camera. Not a freeze. Do not fill $D$.

## P-wave1 — Gemma L10 + Falcon L8 — 2026-09-30 00:07 EEST

Logs: `tests-wave1-gemma-L10-2026-09-29.log`, `tests-wave1-falcon-L8-2026-09-29.log`, `tests-wave1-aya-L10-2026-09-29.log`.
Dumps: `forced_act_gemma.jsonl` / `pre_act_gemma.jsonl`, `forced_act_falcon.jsonl` / `pre_act_falcon.jsonl`.
Same eight rooms. Hiking stayed. Kind not in $L$. Not a freeze.

| Walk | $n_L$ | slice | note LOTO | hike LOTO | hike hold | topic L2 | para LOTO / hike | hike mixed | print tag | pre→act / hike |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| Gemma-3-4B-it | 34 | L10 | **0.0091** $p{=}0$ | **0.0027** | **0.0165** (all 0.0115 $p{=}0.90$) | **0.65** | 0.0088 / 0.0023 | 9 YES / 9 NO | 0.054 | **−0.0767** / **0.000** (pets+neighbors skip) |
| Falcon3-7B-Instruct | 28 | L8 | **0.0816** $p{=}0$ | **0.0227** | **0.2471** (all 0.1192 $p{=}0$) | **0.12** | 0.0771 / **−0.0039** | 5 YES + 13 NO | 0.007 | **−0.0062** / −0.0046 (8/8 rooms) |
| Aya-expanse-8B | 32 | L10 | — | — | — | — | — | — | — | tokenizer then loaded for hide-bank only |

Gemma L10 is not the 7B last-token hint. Tiny shared gap, topic L2 far above chance, in-room hold is a coin flip. The hide button mixes on hiking and $h_{\mathrm{pre}}$ still does not call it.

Falcon L8 is the same *shape* as Qwen/Mistral: mid-layer note hint with topic L2 at eight-way chance, a loud hiking *pair* on the note that does not survive paraphrase LOTO, and a dead pre-button. Print tag LOTO 0.007. Do not drop hiking.

Phi-4 still `LossKwargs`. 27B/70B deception-probe tensors are not $h$.

## P-preact — $r(h_{\mathrm{pre}})\to$ YES/NO — 2026-09-29 22:55 EEST

Log: `results/tests-pre-act-2026-09-29.log`. Same P-act dumps. Majority button per note. $v=\bar h_{\mathrm{YES}}-\bar h_{\mathrm{NO}}$. LOTO. Kind not in $L$.

| | paired rooms | skipped | act LOTO gap | hiking gap |
| --- | --- | --- | ---: | ---: |
| Qwen L8 | 6/8 | **hiking, travel** (no YES) | **0.038** ($n_{\mathrm{YES}}=8$) | skipped |
| Mistral L9 | **8/8** | none | **0.016** | **0.012** |

Mistral hiking *does* press YES on deceptive notes. That contrast is not sitting on $h_{\mathrm{pre}}$. Qwen never gives hiking a YES side, so it cannot vote. Pre-action last token does not predict the hide button. Not a freeze. Do not fill $D$.

## P-elicit — fact-bite YES/NO — 2026-09-29 21:40 EEST

Log: `results/tests-elicit-2026-09-29.log`. Dumps: `elicit_kind_qwen.jsonl`, `elicit_kind_mistral.jsonl`.
Ask names the hidden fact. First word YES/NO. Follow the plan. Kind not in $L$.

| | two-sided rooms | hiking | kind counts |
| --- | --- | --- | --- |
| Qwen | **8/8** | dec 2C+1T; hon evade/C/T | T21 C23 E4 |
| Mistral | **3/8** (invoices, pets, travel) | 5C + 1 evade, **no truth** | T5 C38 E5 |

Almost every print is `NO` plus a restatement of the fact. Deceptive tags still admit the unpaid invoice / unchecked trail. `two_sided` on Qwen is often `fact_margin` twitching around the same speech act. Not a freeze. Do not fill $D$.

## P-bailey-fix — in-place wipe, instrument ok — 2026-09-29 21:30 EEST

Log: `results/tests-bailey-fix-2026-09-29.log`.
In-place $\mathrm{proj}_v$ on the stored `hidden_states[layer]` tensor. $s_v$ collapses. Kind not in $L$.

| | instrument | wipe keep | quiet keep | hiking wipe | $s_v$ base / wipe / quiet |
| --- | --- | ---: | ---: | ---: | --- |
| Qwen L8 | **ok** | **0.833** (8 flips) | 0.812 | 1.00 | 0.087 / **0.000** / 0.079 |
| Mistral L9 | **ok** | **0.833** (8 flips) | 0.458 | 0.83 | 0.043 / **0.000** / 0.020 |

Neighbors is the fragile room (Qwen keep 0.50). Hiking keep stays high. Quiet-prompt still moves Mistral more than residual wipe.
This $v$ can be zeroed while most prints keep kind. Cheap obfuscation of the *tag* camera, not a freeze. Do not fill $D$.

## P-atlas — note $h$, free-text kind as label — 2026-09-29 20:42 EEST

Log: `results/tests-atlas-2026-09-29.log`. Kind-fit thin. Hiking Qwen 6/6 truth on exec dumps. Do not fill $D$.

## P-prehhold / P-pre / P-act

Pre tag LOTO $0.011$ both models. Pre hold $0.005$ / $0.009$. Mistral print $0.68$ is YES/NO geometry. Note hiking hold $0.203$ / $0.278$.

## Older blocks

P-bailey instrument miss, P-button, P-multi, P-many, P-cross, P1 / P0p in prior commits. Qwen hiking held_inroom $0.203$ / para $0.160$ / LOTO $0.013$.
