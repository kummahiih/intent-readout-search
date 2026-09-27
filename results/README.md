# Sensor ledger

Do not collapse attempts. Put new logs in this folder.

## P-button — forced YES/NO walk — 2026-09-28 00:39 EEST

Log: `results/tests-forced-button-2026-09-28.log`. Dumps: `forced_button_qwen.jsonl`, `forced_button_mistral.jsonl`.
True button on this bank is NO. YES contradicts the fact. Graded from the token. $v$ from assigned tags. Kind not in $L$. Not a freeze voter.

| | YES / NO | agree tag/button | tag LOTO | kind LOTO |
| --- | --- | ---: | ---: | ---: |
| Qwen L8 | 9 / 87 | 0.59 | **0.003** | 0.017 (n_YES=9) |
| Mistral L9 | 10 / 86 | 0.60 | 0.122 | 0.776 (n_YES=10) |

Honest notes: 48/48 NO on both models. Hiking and travel: 12/12 NO. YES only on some deceptive invoices/pets/repairs/taxes/(neighbors Qwen, cooking Mistral).

Qwen last-token of `NO` is the same vector (hiking/travel tag gap 0.000). Mistral kind 0.776 is YES-vs-NO token geometry, not a shared plan axis — 10 vs 86 strings.

The walk now has an independent label. The actor still will not press YES in hiking. Do not fill $D$.

## P-multi — 3 probes, adversary + corr² — 2026-09-28 00:30 EEST

Log: `results/tests-multi-r-2026-09-28.log`.
Frozen last-token $h$. Three 1-d probes. LOTO: hit label, fool topic head, penalize score corr². Not $r_{\mathrm{strat}}$. Not a freeze voter.

| Run | ensemble LOTO | hiking | travel | corr² |
| --- | ---: | ---: | ---: | ---: |
| Qwen notes/tags | 0.051 | **0.015** | 0.084 | 0.30 |
| Qwen exec/kind | 0.010 | skip (no contradict) | 0.003 | 0.41 |
| Mistral notes/tags | 0.069 | **0.022** | 0.104 | 0.21 |
| Mistral exec/kind | 0.033 | 0.019 | skip | 0.26 |

Heads 0/1/2 on Qwen tags: 0.061 / 0.040 / 0.054, hiking 0.015 / 0.013 / 0.017. Same room ranking.
Plain contrast LOTO on notes was ~0.10. The ensemble is weaker, not complementary.
corr² 0.21–0.41 is not collapse to 1, and not diversity that helps hiking.

## P-construct-exec — follow the plan, sample prints — 2026-09-28 00:19 EEST

Log: `results/tests-construct-exec-2026-09-28.log`. Dumps: `construct_kind_exec_qwen.jsonl`, `construct_kind_exec_mistral.jsonl`.
`--execute` + temperature 0.8, two samples per note. $v$ still from assigned tags. Kind not in $L$. Same-model `fact_margin`. Not a freeze voter.

| | kind mix | frac_contradict | agree tag/kind | tag LOTO | kind LOTO |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen L8 | truth 76 / contradict 13 / evade 6 / refuse 1 | 0.135 | 0.65 | 0.047 | **−0.019** |
| Mistral L9 | contradict 72 / truth 14 / evade 10 | 0.750 | 0.52 | 0.028 | **−0.036** |

Qwen: all 13 contradicts came from deceptive tags; 31 deceptive prints stayed `truth`. Hiking: 12/12 `truth`. Tag LOTO hiking −0.032; kind LOTO hiking skipped.
Mistral hiking kind LOTO −0.056. Honest-tagged replies are often labeled `contradict` (34).

Execute+sample raised Qwen contradict rate from 0.08 to 0.14. It did not produce a kind axis. Tag LOTO on prints stays thin.

## P-many — oracle $r_T$ vs shared $v$ — 2026-09-28 00:04 EEST

Log: `results/tests-many-r-2026-09-28.log`.
Each $r_T=v_T$ fit on 2+2, held 1+1 scored with every room camera. Diagonal = oracle many-$r$. Off-diagonal = wrong-room $v$. Shared LOTO = mean of other $v$. Knowing $T$ is a topic feature. Not $r_{\mathrm{strat}}$. Not a freeze voter.

| | oracle diag | off-room | shared LOTO |
| --- | ---: | ---: | ---: |
| Qwen L8 | 0.059 ($p=0.014$) | 0.048 | **0.093** ($p=0$) |
| Mistral L9 | 0.079 ($p=0.021$) | 0.059 | **0.124** ($p=0$) |

| Room | Qwen oracle / LOTO | Mistral oracle / LOTO |
| --- | --- | --- |
| hiking | **0.160** / 0.038 | **0.214** / 0.063 |
| invoices | **0.238** / 0.023 | **0.409** / 0.069 |
| travel | 0.049 / **0.142** | 0.078 / **0.200** |

Paraphrase with full-room $v_T$: oracle transfer Qwen 0.288 / Mistral 0.434 (hiking 0.250 / 0.294). Shared transfer hiking 0.009 / 0.052 vs travel 0.189 / 0.168.

Two rooms want their own camera. Mean-over-rooms does not. Do not freeze eight banks.

## P-construct — tag $v$ vs generated `reply_kind` — 2026-09-27 23:57 EEST

Log: `results/tests-construct-kind-2026-09-28.log`. Dumps: `construct_kind_qwen.jsonl`, `construct_kind_mistral.jsonl`.
Fit $v_T$ on assigned tags. Score last-token $h$ of the **print**. Kind from same-model `fact_margin` (not a second judge). Kind not in $L$. Not a freeze voter.

| | kind mix | tag LOTO | kind LOTO | tag inroom | kind inroom |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen L8 | truth 43 / contradict 4 / evade 1 | 0.029 | **−0.088** (n_dec=4) | 0.608 | 0.020 |
| Mistral L9 | contradict 36 / truth 8 / evade 3 / refuse 1 | 0.066 | **0.008** | 0.695 | 0.198 |

Qwen hiking prints: all six `truth` (three deceptive notes included). Tag LOTO hiking 0.041; kind LOTO hiking skipped.
Mistral hiking tag LOTO 0.017; kind LOTO −0.013.

`agree_assigned` on truth/contradict: Qwen 0.55, Mistral 0.59. Chance is 0.5.
In-room tag gaps reuse the same six prints that built $v_T$. Do not read 0.61 as a camera.

The assigned note is not the realized print. Mid-layer note contrast is not a behavior label.

## P-cross — different-model judge — 2026-09-27 22:55 EEST

Log: `results/tests-cross-judge-2026-09-28.log`.
Camera owns $v$. Walk owns $h$. Linear $W$ maps walk space → camera space, LOTO on the other topics.
Dims: Qwen 3584, Mistral 4096. Map fit on 42 rows. **Underdetermined.** Not a freeze voter.

| Camera → walk | cross_loto | hiking | travel | topic L2 | para hiking |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen L8 → Mistral L9 | 0.098 | **0.028** | 0.151 | 0.17 | 0.032 |
| Mistral L9 → Qwen L8 | 0.198 | 0.094 | 0.321 | 0.10 | **0.026** |

p=0 on fit-set cross_loto (N=20000). Same-model Qwen hiking LOTO is 0.013.

After a crude alignment, the same rooms stay loud and the same room stays thin. That is evidence the mid-layer hint is domain-shaped, not evidence you have a portable judge.

## P1 — fact-held paraphrase — 2026-09-27 02:12 EEST

Log: `results/tests-para-hold-2026-09-27.log` (hooked run). Fit $v_T$ on wide rows whose fact is not the transfer fact.

Qwen paraphrase: para_held_inroom hiking **0.160** / travel 0.179; para_held_loto hiking **0.009** / travel 0.189.
Mistral paraphrase: inroom hiking **0.179** / travel 0.175; loto hiking 0.052 / travel 0.168.

The hiking pair is not the original wording. It still does not join the shared axis.

## P0p — within-topic hold — 2026-09-27 01:55 EEST

Log: `results/tests-held-in-topic-2026-09-27.log`.
`held_loto` equals reuse LOTO (same v). New number is `held_inroom` (2+2 fit, 1+1 hold).

| | reuse / held LOTO hiking | held_inroom hiking | held_inroom travel | held topic L2 |
| --- | --- | --- | --- | --- |
| Qwen L8 | **0.013** | **0.203** | 0.120 | 0.29 |
| Mistral L9 | 0.069 | **0.278** | 0.135 | 0.23 |

Hiking is not an empty room. Its pair does not join the shared axis.
held topic L2 is on in-room scalars (own $v_T$). Official topic gate stays LOTO L2 (0.10 / 0.08).
