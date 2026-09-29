# Scale without changing the object

2026-09-29. Weights and HF datasets stay on disk (`models/`, `datasets/` are gitignored).
Do not fill $D$. Kind not in $L$.

## What the new files are

| Path | Use |
| --- | --- |
| `models/gemma-3-4b-it` | New *walk*. Encode our notes and act prompts. |
| `models/Phi-4-mini-instruct` | New walk. |
| `models/Falcon3-7B-Instruct` | New walk. |
| `models/aya-expanse-8b` | New walk. |
| `datasets/DeceptionBench` | Extra *prompts* / domains. Not a frozen $S$. |
| `datasets/lie-detection-rollouts` | Other models' prints + `is_lie`. Labels are not this walk's $S$. |
| `datasets/difraud` | Fraud-text classification. Off-construct unless remapped. |
| `datasets/deception-probes-activations` | Hidden states of **Gemma-3-27B** / **Llama-3.3-70B**. Do not treat those tensors as $h$ for our 4B–8B walks. |

A probe fitted on 70B layer 20 is not $r$ for Phi-4-mini.

## Wave 1 — same eight rooms, four new walks

Keep `data/pairs_wide.jsonl`. Layer $\approx 0.3$ depth (confirm `n_layers` on load).

Guesses until `config.json` is read:

| Local dir | Layer guess |
| --- | ---: |
| gemma-3-4b-it | 8 |
| Phi-4-mini-instruct | 10 |
| Falcon3-7B-Instruct | 8 |
| aya-expanse-8b | 10 |

Per model:

1. Note last-token tag LOTO + `held_inroom` (hiking must stay).
2. `--act` generate YES/NO (hiking mixed?).
3. `--h-site pre --label act` LOTO.

Report the same chart as Qwen vs Mistral: note hint vs hide-button compliance vs pre$\to$act gap.

A new note-token 0.10 is **not** a pass. A pre$\to$act gap that owns hiking is the only freeze candidate.

## Wave 2 — extra rooms, not extra $r$ architectures

DeceptionBench domains (economy / healthcare / education / social / entertainment) can become extra *topics* with hide vs name notes, same speech act as `pairs_wide`. Then LOTO must include hiking **and** the new rooms. Dropping hiking to make a pass is still `seven_is_not_eight`.

lie-detection-rollouts: use only as a source of *asks*, then regenerate on *our* walk. Foreign `is_lie` is not $S$ for $h$ we did not produce.

## Wave 3 — parked

Circuit Breakers, SAE, PPO: still blocked until a camera pass on wave 1 or 2.
