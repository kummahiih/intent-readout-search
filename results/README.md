# Sensor ledger

Do not collapse attempts. Put new logs in this folder.
Older blocks also in commit `e41fcfbe` if this file is trimmed.

## P-hidebank — crossed HIDE/NAME, S ≠ tag — 2026-09-30 00:53 EEST

Log: `results/tests-hide-bank-2026-09-30.log`. Dumps: `hide_bank_{qwen,mistral,gemma}.jsonl`.
Same notes. HIDE arm asks for the cover (YES). NAME arm asks to refuse it (NO). $S$ = button. Then `note_act` on HIDE only. Kind not in $L$.

| Walk | HIDE frac YES | hide on hiking | HIDE agree tag | note→act HIDE | hiking |
| --- | ---: | --- | ---: | ---: | ---: |
| Qwen L8 | 0.51 | **yes** (2 YES / 10 NO; majority 1+5) | 0.68 | **0.018** (8/8 rooms) | **−0.049** |
| Mistral L9 | 0.57 | **yes** (8 YES / 4 NO) | 0.79 | **0.092** (8/8) | **−0.002** |
| Gemma L10 | **0.95** | all YES | 0.55 | 0.001 (3 rooms) | skipped |

Qwen hiking finally pressed hide. That was the missing bank. The desk-note last token still does not call that $S$ (hiking −0.049). Mistral HIDE hiking mixes honest YES, so $S$ is less glued to the tag than P-act, and hiking note→act is still ~0. Gemma HIDE saturates (no NO on hiking), so it cannot vote. Not a freeze. Do not fill $D$.

## P-noteact — note $h \to$ hide button on P-act dumps

Qwen 0.043 hiking skipped. Mistral 0.085 / hiking 0.096 (button=tag). Gemma hiking 0.009.

## P-wave1 / P-preact / P-bailey-fix

Gemma L10 wallpaper. Falcon 7B-shaped. Pre→act dead. Wipe keep 0.83.

## Older blocks

P-atlas, P-elicit, P-many, P-cross, P1 / P0p in prior commits. Qwen hiking held_inroom $0.203$ / LOTO $0.013$.
