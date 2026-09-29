# Early sensor ledger (commit `e41fcfbe`)

Restored in full. Do not collapse. Later blocks live in [README.md](README.md).

## P-button — forced YES/NO walk — 2026-09-28 00:39 EEST

Log: `results/tests-forced-button-2026-09-28.log`. True button on this bank is NO. YES contradicts the fact. Kind not in $L$.

| | YES / NO | agree tag/button | tag LOTO | kind LOTO |
| --- | --- | ---: | ---: | ---: |
| Qwen L8 | 9 / 87 | 0.59 | **0.003** | 0.017 (n_YES=9) |
| Mistral L9 | 10 / 86 | 0.60 | 0.122 | 0.776 (n_YES=10) |

Honest notes: 48/48 NO. Hiking and travel: 12/12 NO. Mistral kind 0.776 is YES-vs-NO token geometry. Do not fill $D$.

## P-multi — 3 probes, adversary + corr² — 2026-09-28 00:30 EEST

Log: `results/tests-multi-r-2026-09-28.log`.

| Run | ensemble LOTO | hiking | travel | corr² |
| --- | ---: | ---: | ---: | ---: |
| Qwen notes/tags | 0.051 | **0.015** | 0.084 | 0.30 |
| Qwen exec/kind | 0.010 | skip | 0.003 | 0.41 |
| Mistral notes/tags | 0.069 | **0.022** | 0.104 | 0.21 |
| Mistral exec/kind | 0.033 | 0.019 | skip | 0.26 |

Ensemble weaker than plain contrast LOTO ~0.10. Same room ranking.

## P-construct-exec — follow the plan, sample prints — 2026-09-28 00:19 EEST

Log: `results/tests-construct-exec-2026-09-28.log`.

| | frac_contradict | agree tag/kind | tag LOTO | kind LOTO |
| --- | ---: | ---: | ---: | ---: |
| Qwen L8 | 0.135 | 0.65 | 0.047 | **−0.019** |
| Mistral L9 | 0.750 | 0.52 | 0.028 | (see log) |

## P-many — oracle $r_T$ vs shared $v$ — 2026-09-28 00:04 EEST

Log in that era. Local $r_T$ helps hiking/invoices; mean of locals loses to shared LOTO on the loud rooms. Not an ensemble camera.

## P-construct — tag $v$ vs generated `reply_kind` — 2026-09-27 23:57 EEST

| | kind mix | kind LOTO | tag in-room |
| --- | --- | ---: | ---: |
| Qwen L8 | T43 C4 E1 | **−0.088** (n_dec=4) | 0.608 |
| Mistral L9 | C36 T8 E3 R1 | **0.008** | 0.695 |

Qwen hiking: all six `truth`. Assigned note is not the print.

## P-cross — different-model judge — 2026-09-27 22:55 EEST

Log: `results/tests-cross-judge-2026-09-28.log`. $W$ fit on 42 rows. Underdetermined.

| Camera → walk | cross_loto | hiking | travel | para hiking |
| --- | ---: | ---: | ---: | ---: |
| Qwen L8 → Mistral L9 | 0.098 | **0.028** | 0.151 | 0.032 |
| Mistral L9 → Qwen L8 | 0.198 | 0.094 | 0.321 | **0.026** |

Same rooms loud, hiking thin. Domain-shaped hint, not a portable judge.

## P1 — fact-held paraphrase — 2026-09-27 02:12 EEST

Log: `results/tests-para-hold-2026-09-27.log`.

| | para_held_inroom hike / travel | para_held_loto hike / travel |
| --- | --- | --- |
| Qwen L8 | **0.160** / 0.179 | **0.009** / 0.189 |
| Mistral L9 | **0.179** / 0.175 | 0.052 / 0.168 |

## P0p — within-topic hold — 2026-09-27 01:55 EEST

Log: `results/tests-held-in-topic-2026-09-27.log`.

| | LOTO hiking | held_inroom hiking | held_inroom travel |
| --- | ---: | ---: | ---: |
| Qwen L8 | **0.013** | **0.203** | 0.120 |
| Mistral L9 | 0.069 | **0.278** | 0.135 |

Hiking is not empty. Its pair does not join the shared axis. Do not fill $D$.
