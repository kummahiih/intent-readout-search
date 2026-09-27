# Sensor ledger

Do not collapse attempts. Put new logs in this folder.

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
