# Scale without changing the object

2026-09-29. Weights and HF datasets stay on disk (`models/`, `datasets/` are gitignored).
Do not fill $D$. Kind not in $L$. Keep hiking.

## What the new files are

| Path | Use |
| --- | --- |
| `models/gemma-3-4b-it` | New *walk*. Encode our notes and act prompts. |
| `models/Phi-4-mini-instruct` | Skipped (`LossKwargs`). Not a walk. |
| `models/Falcon3-7B-Instruct` | New walk. |
| `models/aya-expanse-8b` | New walk. |
| `datasets/DeceptionBench` | Extra *prompts* / domains. Not a frozen $S$. |
| `datasets/lie-detection-rollouts` | Other models' prints + `is_lie`. Labels are not this walk's $S$. |
| `datasets/difraud` | Fraud-text classification. Off-construct unless remapped. |
| `datasets/deception-probes-activations` | Hidden states of **Gemma-3-27B** / **Llama-3.3-70B**. Do not treat those tensors as $h$ for our 4B–8B walks. |

A probe fitted on 70B layer 20 is not $r$ for Phi-4-mini.

## Layers (read `config.json`, do not guess)

Depth match is $\approx 0.3$ of *text* `num_hidden_layers` (Qwen L8 / 28 $\approx 0.29$, Mistral L9 / 32 $\approx 0.28$).

| Local dir | `n_layers` | 0.3-depth layer | Notes |
| --- | ---: | ---: | --- |
| gemma-3-4b-it | **34** (text; DeepMind Gemma3-4B) | **10** | Hub default `Gemma3TextConfig` is 26/2304 — that is not the 4B card. 4B is 34 / 2560. Nested under `text_config` on the multimodal json. L8 is $\approx 0.24$ depth; if L8 already ran, log it *and* L10. |
| Phi-4-mini-instruct | — | — | Skip. `LossKwargs`. |
| Falcon3-7B-Instruct | **28** (`LlamaForCausalLM`) | **8** | |
| aya-expanse-8b | **32** (`CohereForCausalLM`) | **10** | |

On load print `n_layers` from the *text* config. Gemma-3-4B-it is `Gemma3ForConditionalGeneration` plus a vision tower. Text-only encode via `AutoModelForCausalLM` / `Gemma3ForCausalLM` so the vision tower stays off. If that path raises `LossKwargs` or a vision-only forward, skip the walk and log the exception. Do not substitute `datasets/deception-probes-activations`.

`python wave1_layers.py` reads local `models/*/config.json` with no CUDA.

## Wave 1 — same eight rooms, three new walks

Keep `data/pairs_wide.jsonl`. Hiking stays in the eight. Kind not in $L$.

Per model, official slice first (Gemma **L10**, Falcon **L8**, Aya **L10**):

1. Note last-token tag LOTO + `held_inroom` (hiking must stay).
2. `--act` generate YES/NO (hiking mixed?).
3. `--h-site pre --label act` LOTO.

```bash
bash wave1_run.sh gemma    # models/gemma-3-4b-it  L10 (+ L8 if already started)
bash wave1_run.sh falcon   # models/Falcon3-7B-Instruct  L8
bash wave1_run.sh aya      # models/aya-expanse-8b  L10
```

Report the same chart as Qwen vs Mistral: note hint vs hide-button compliance vs pre$\to$act gap.

A new note-token 0.10 is **not** a pass. A pre$\to$act gap that owns hiking is the only freeze candidate.

This agent session has **no CUDA**. Do not invent Gemma / Falcon / Aya gaps. Ledger stays empty until the walk machine writes `results/tests-wave1-*.log`.

## Wave 2 — extra rooms, not extra $r$ architectures

DeceptionBench domains (economy / healthcare / education / social / entertainment) can become extra *topics* with hide vs name notes, same speech act as `pairs_wide`. Then LOTO must include hiking **and** the new rooms. Dropping hiking to make a pass is still `seven_is_not_eight`.

lie-detection-rollouts: use only as a source of *asks*, then regenerate on *our* walk. Foreign `is_lie` is not $S$ for $h$ we did not produce.

## Wave 3 — parked

Circuit Breakers, SAE, PPO: still blocked until a camera pass on wave 1 or 2.
