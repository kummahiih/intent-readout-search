# Protocol meters on Llama-3.1 and Gemma-2 (2026-11-01)

Same files and meters as the 7B protocol runs: `pair_contrast.py` on `data/pairs_wide.jsonl`, last-token pool, 20 000 within-topic permutations, paraphrase transfer from `data/pairs_paraphrase.jsonl`. Held-in-topic is a diagnostic, not a freeze gate. Raw log: `results/protocol-new-models-2026-11-01.log`.

Chance on 8 topics is 0.125. Official topic gate is `topic_loo_l2_on_scalar`.

## Aggregate plan LOTO and paraphrase

| Model | Layer | Plan LOTO gap | Topic L2 | Paraphrase gap |
| --- | ---: | ---: | ---: | ---: |
| Llama-3.1-8B | 8 | 0.092 | 0.17 | 0.081 |
| Llama-3.1-8B-Instruct | 8 | 0.134 | 0.12 | 0.125 |
| gemma-2-2b | 8 | 0.069 | 0.23 | 0.061 |
| gemma-2-2b-it | 8 | 0.097 | 0.10 | 0.102 |
| gemma-2-9b-it | 10 | 0.130 | 0.08 | 0.123 |
| Qwen2.5-7B (ref) | 8 | 0.105 | 0.06 | 0.108 |
| Mistral-7B (ref) | 9 | 0.116 | 0.12 | 0.123 |

All five new walks keep a positive aggregate gap under the tested paraphrase. Within-topic permutation p is near 0 on every fit and transfer gap.

## Held-in-topic (diagnostic)

| Model | held_inroom gap | held_loto gap | para_held_inroom gap |
| --- | ---: | ---: | ---: |
| Llama-3.1-8B | 0.118 | 0.092 | 0.132 |
| Llama-3.1-8B-Instruct | 0.162 | 0.134 | (see log) |
| gemma-2-2b | 0.093 | 0.069 | 0.111 |
| gemma-2-2b-it | 0.144 | 0.097 | 0.155 |
| gemma-2-9b-it | 0.185 | 0.130 | 0.190 |

Within-room hold is larger than shared LOTO on every walk, same shape as the 7B hiking split. This is a log, not a fifth freeze gate.

## Topic gate

- Llama-3.1-8B-Instruct (0.12) and gemma-2-9b-it (0.08) sit at or below chance.
- Llama-3.1-8B (0.17) and gemma-2-2b-it (0.10) are near chance.
- gemma-2-2b (0.23) fails the topic gate more clearly; the score still names the hallway.

## What this is not

- Not `cameraPass`. Rooms are not shown to be a single shared axis; held-in-room is larger than LOTO.
- Not `handoverPass`. No action tracking, no frozen inspector.
- Not a strategy camera. Tags are observations. Do not train the hinge on these scores.
- Do not fill \(D\). Do not freeze \(r\).

Same status as the 7B ledger: candidate plan-related signal on the aggregate, topic leakage on some walks, hiking-style room-local pairs. The new models do not change the open item.
