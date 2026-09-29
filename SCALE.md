# Scale without changing the object

2026-09-29 / 2026-09-30. Weights and HF datasets stay on disk (`models/`, `datasets/` are gitignored).
Do not fill $D$. Kind not in $L$. Keep hiking.

## What the new files are

| Path | Use |
| --- | --- |
| `models/gemma-3-4b-it` | New *walk*. Encode our notes and act prompts. |
| `models/Phi-4-mini-instruct` | Skipped (`LossKwargs`). Not a walk. |
| `models/Falcon3-7B-Instruct` | New walk. |
| `models/aya-expanse-8b` | Weights local. Tokenizer Hub-gated + transformers-5 TokenizersBackend miss. Not a walk until `tokenizer.json` rust-loads. |
| `datasets/DeceptionBench` | Extra *prompts* / domains. Not a frozen $S$. |
| `datasets/lie-detection-rollouts` | Other models' prints + `is_lie`. Labels are not this walk's $S$. |
| `datasets/difraud` | Fraud-text classification. Off-construct unless remapped. |
| `datasets/deception-probes-activations` | Hidden states of **Gemma-3-27B** / **Llama-3.3-70B**. Do not treat those tensors as $h$ for our 4B–8B walks. |

A probe fitted on 70B layer 20 is not $r$ for Phi-4-mini.

## Layers (read `config.json`, do not guess)

Depth match is $\approx 0.3$ of *text* `num_hidden_layers` (Qwen L8 / 28 $\approx 0.29$, Mistral L9 / 32 $\approx 0.28$).

| Local dir | `n_layers` | 0.3-depth layer | Notes |
| --- | ---: | ---: | --- |
| gemma-3-4b-it | **34** (text) | **10** | Logged. |
| Phi-4-mini-instruct | — | — | Skip. `LossKwargs`. |
| Falcon3-7B-Instruct | **28** | **8** | Logged. |
| aya-expanse-8b | **32** | **10** | No encode. Gate + rust tokenizer. |

## Wave 1 — logged 2026-09-30 00:07 EEST

Logs: `results/tests-wave1-gemma-L10-2026-09-29.log`, `results/tests-wave1-falcon-L8-2026-09-29.log`, `results/tests-wave1-aya-L10-2026-09-29.log`.
Eight rooms on `data/pairs_wide.jsonl`. Hiking stayed.

| Walk | slice | note LOTO | hiking LOTO | hiking hold | topic L2 | para LOTO / hike | act mixed | pre→act |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| Qwen 7B (prior) | L8 | 0.105 | 0.013 | 0.203 | 0.06 | 0.108 / 0.009 | hike skip on preact | 0.038 (hike skip) |
| Mistral 7B (prior) | L9 | 0.116 | 0.069 | 0.278 | 0.12 | 0.123 / 0.052 | yes | 0.016 / hike 0.012 |
| **Gemma-3-4B-it** | **L10** | **0.0091** $p{=}0$ | **0.0027** | **0.0165** (all-room hold 0.0115 $p{=}0.90$) | **0.65** | 0.0088 / 0.0023 | yes 9/9 | **−0.0767** / hike 0.000 |
| **Falcon3-7B** | **L8** | **0.0816** $p{=}0$ | **0.0227** | **0.2471** (all-room hold 0.1192 $p{=}0$) | **0.12** | 0.0771 / **−0.0039** | yes 5 + no 13 | **−0.0062** / hike −0.0046 |
| Aya-expanse-8B | L10 | — | — | — | — | — | — | tokenizer miss |

Read, not a freeze:

- Gemma L10 is not a Qwen-class hint. Gap is one-hundredth of the 7B last-token hint. Topic L2 0.65 (chance 0.125) means the scalar is *room*-shaped. In-room hold is noise ($p=0.90$). Pre$\to$act gap is the wrong sign. Hiking mixed on the button and still $0$ on $h_{\mathrm{pre}}$.
- Falcon L8 *looks* like the 7B note hint on the shared axis (0.082, topic L2 at chance) and again owns a hiking *pair* on the note (hold 0.247) that dies on paraphrase LOTO (−0.004). Same seven-is-not-eight shape. Print tag LOTO 0.007 and pre$\to$act −0.006 do not carry the hide button. All eight rooms press both YES and NO.
- Aya is still not a camera miss. Cohere tokenizer is TokenizersBackend-only; Hub repo is gated (`https://huggingface.co/CohereLabs/aya-expanse-8b`). Local rust-load of `tokenizer.json` or skip. Do not invent an Aya gap.
- Phi-4 stays skipped.

A new note-token 0.08 is **not** a pass. A pre$\to$act gap that owns hiking is the only freeze candidate. Neither new walk has that. Do not fill $D$.

## Wave 2 — extra rooms, not extra $r$ architectures

DeceptionBench domains can become extra *topics* with hide vs name notes, same speech act as `pairs_wide`. Then LOTO must include hiking **and** the new rooms. Dropping hiking to make a pass is still `seven_is_not_eight`.

## Wave 3 — parked

Circuit Breakers, SAE, PPO: still blocked until a camera pass on wave 1 or 2.
