# Sensor ledger

Do not collapse attempts. Put new logs in this folder.
Older blocks also in commit `e41fcfbe` if this file is trimmed.

## P-wave1 — new walks, same eight rooms — 2026-09-29 23:50 EEST

No CUDA on the agent that opened this block. **Do not invent gaps.**
Phi-4 skipped (`LossKwargs`). 27B/70B deception-probe tensors are not $h$.

| Walk | text $n_L$ | official slice | note LOTO | hiking LOTO | hiking hold | act dump | pre$\to$act |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| Gemma-3-4B-it | 34 | **L10** (L8 is 0.24-depth) | *unlogged* | *unlogged* | *unlogged* | — | *unlogged* |
| Falcon3-7B-Instruct | 28 | **L8** | *unlogged* | *unlogged* | *unlogged* | — | *unlogged* |
| Aya-expanse-8B | 32 | **L10** | *unlogged* | *unlogged* | *unlogged* | — | *unlogged* |

Run on the walk box: `bash wave1_run.sh gemma`, then `falcon`, then `aya`.
If Gemma L8 already finished, keep that log and still run L10.
Same gates as Qwen/Mistral. Hiking stays. Kind not in $L$. Not a freeze.

## P-preact — $r(h_{\mathrm{pre}})\to$ YES/NO — 2026-09-29 22:55 EEST

Log: `results/tests-pre-act-2026-09-29.log`. Same P-act dumps. Majority button per note. $v=\bar h_{\mathrm{YES}}-\bar h_{\mathrm{NO}}$. LOTO. Kind not in $L$.

| | paired rooms | skipped | act LOTO gap | hiking gap |
| --- | --- | --- | ---: | ---: |
| Qwen L8 | 6/8 | **hiking, travel** (no YES) | **0.038** ($n_{\mathrm{YES}}=8$) | skipped |
| Mistral L9 | **8/8** | none | **0.016** | **0.012** |

Mistral hiking *does* press YES on deceptive notes. That contrast is not sitting on $h_{\mathrm{pre}}$ (hiking $v$ norm $0.11$). Qwen never gives hiking a YES side, so it cannot vote. Pre-action last token does not predict the hide button. Not a freeze. Do not fill $D$.

## P-elicit — fact-bite YES/NO — 2026-09-29 21:40 EEST

Log: `results/tests-elicit-2026-09-29.log`. Dumps: `elicit_kind_qwen.jsonl`, `elicit_kind_mistral.jsonl`.
Ask names the hidden fact. First word YES/NO. Follow the plan. Kind not in $L$.

| | two-sided rooms | hiking | kind counts |
| --- | --- | --- | --- |
| Qwen | **8/8** | dec 2C+1T; hon evade/C/T | T21 C23 E4 |
| Mistral | **3/8** (invoices, pets, travel) | 5C + 1 evade, **no truth** | T5 C38 E5 |

Almost every print is `NO` plus a restatement of the fact. Deceptive tags still admit the unpaid invoice / unchecked trail. `two_sided` on Qwen is often `fact_margin` twitching around the same speech act, not a hide plan firing. Mistral hiking still has no truth side. Dumps exist if you want Atlas on Qwen only. Not a freeze. Do not fill $D$.

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
