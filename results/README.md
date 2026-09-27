# Sensor ledger

Do not collapse attempts. Put new logs in this folder.

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
