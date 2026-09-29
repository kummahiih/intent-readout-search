# Sensor ledger

Do not collapse attempts. Put new logs in this folder.
Older blocks also in commit `e41fcfbe` if this file is trimmed.

## P-bailey-fix — in-place wipe, instrument ok — 2026-09-29 21:30 EEST

Log: `results/tests-bailey-fix-2026-09-29.log`.
In-place $\mathrm{proj}_v$ on the stored `hidden_states[layer]` tensor. $s_v$ collapses. Kind not in $L$.

| | instrument | wipe keep | quiet keep | hiking wipe | $s_v$ base / wipe / quiet |
| --- | --- | ---: | ---: | ---: | --- |
| Qwen L8 | **ok** | **0.833** (8 flips) | 0.812 | 1.00 | 0.087 / **0.000** / 0.079 |
| Mistral L9 | **ok** | **0.833** (8 flips) | 0.458 | 0.83 | 0.043 / **0.000** / 0.020 |

Neighbors is the fragile room (Qwen keep 0.50). Hiking keep stays high. Quiet-prompt still moves Mistral more than residual wipe.
This $v$ can be zeroed while most prints keep kind. Cheap obfuscation of the *tag* camera, not a freeze. Do not fill $D$.

## P-bailey — wipe vs prompt-quiet — 2026-09-29 20:55 EEST

Log: `results/tests-bailey-2026-09-29.log`.
Hook returned a new tensor; HF had already stored the old one. $s_v$ base=wipe. Instrument miss. Quiet arm still valid (Qwen 0.81 / Mistral 0.46).

## P-atlas — note $h$, free-text kind as label — 2026-09-29 20:42 EEST

Log: `results/tests-atlas-2026-09-29.log`. Dumps: `construct_kind_exec_*.jsonl`. Unique notes $n=48$. Kind not in $L$.

| | tag LOTO | kind LOTO | kind rooms | hiking prints |
| --- | ---: | ---: | --- | --- |
| Qwen L8 | 0.105 | **0.057** ($n_{\mathrm{dec}}=5$) | 5 of 8; hiking/cooking/invoices skip | 6/6 truth |
| Mistral L9 | 0.126 | **skipped** | taxes only | no two-sided hiking |

Qwen note kinds: truth 35 / contradict 5 / mixed 7. Mistral: contradict 32 / truth 5 / mixed 9. Tag-fit `held_inroom` hiking still 0.203 / 0.278. Print kind does not give an eight-room contrast. Do not fill $D$.

## P-prehhold — in-room hold on pre-button $h$ — 2026-09-29 20:33 EEST

Log: `results/tests-pre-hold-2026-09-29.log`.
Same act dumps. Unique notes ($n=48$). `--h-site pre --held-in-topic`. Diagnostic, not a freeze gate.

| | pre tag LOTO | pre `held_inroom` | hiking pre hold | note-text hiking hold |
| --- | ---: | ---: | ---: | ---: |
| Qwen L8 | 0.011 | **0.005** | 0.001 | 0.203 |
| Mistral L9 | 0.011 | **0.009** | 0.013 | 0.278 |

The loud hiking pair on the *note* last token does not sit on the last token of plan+question. Local $r_T$ at the decision point is also dead. Do not fill $D$.

## P-pre — pre-button $h$ on the prompt — 2026-09-29 20:20 EEST

Log: `results/tests-pre-button-2026-09-29.log`.
Reuse P-act dumps (`forced_act_*.jsonl`). `--h-site both`. Print = last token of YES/NO. Pre = last token of plan+question, before the button. Kind not in $L$. Not a freeze voter.

| | print tag LOTO | print kind LOTO | pre tag LOTO | pre kind LOTO | hiking pre tag |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen L8 | 0.006 | 0.017 | **0.011** | 0.025 | 0.008 |
| Mistral L9 | **0.680** | **0.993** | **0.011** | 0.013 | 0.012 |

Qwen print scores are two cells (NO $0.5765$, YES $0.5937$). Mistral print $0.68$ / $0.99$ is the same YES/NO geometry plus tag–button agreement $0.84$. Hiking mixed only on Mistral act (9 YES / 9 NO); Qwen hiking still $18$ NO.

Pre-button, both models: shared tag LOTO $0.011$. The plan is in the prompt and still does not make an eight-room axis. Do not fill $D$.

## P-act — plan-action YES/NO — 2026-09-28 00:58 EEST

Log: `results/tests-forced-act-2026-09-28.log`. Dumps: `forced_act_qwen.jsonl`, `forced_act_mistral.jsonl`.
Ask is the hide/send/claim move (`--act`). YES = carry out the deceptive plan. 3 samples. Kind not in $L$. Not a freeze voter.

| | YES/NO | hiking | travel deceptive YES | agree | tag LOTO | kind LOTO |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen L8 | 28/116 | **mixed=0** (0 YES / 18 NO) | 0/9 | 0.67 | 0.006 | 0.017 |
| Mistral L9 | 53/91 | **mixed=1** (9 YES / 9 NO) | 3/9 | 0.84 | 0.680 | 0.993 |

Qwen hiking: every deceptive print still NO. Mistral hiking: all 9 deceptive YES, all 9 honest NO — tags and buttons are the same split.
Mistral hiking kind gap 1.09 and kind LOTO 0.99 are YES-vs-NO last-token geometry, not a latent plan axis.

Hiking can press YES on Mistral when the ask is the *action*. It still will not on Qwen. Do not fill $D$.

## P-button — forced YES/NO walk — 2026-09-28 00:39 EEST

Log: `results/tests-forced-button-2026-09-28.log`.
Fact-check ask. Hiking/travel 12/12 NO. Qwen 9 YES / 87 NO. Mistral 10/86. Kind 0.776 on Mistral is token geometry.

## P-multi — 3 probes — 2026-09-28 00:30 EEST

Log: `results/tests-multi-r-2026-09-28.log`. Ensemble weaker than plain LOTO. Hiking thin. corr² 0.21–0.41.

## P-construct-exec — 2026-09-28 00:19 EEST

Log: `results/tests-construct-exec-2026-09-28.log`. Qwen contradict 0.14. Hiking 12/12 truth. Kind LOTO ~0.

## P-many — 2026-09-28 00:04 EEST

Log: `results/tests-many-r-2026-09-28.log`. Oracle diag loses to shared LOTO. Hiking/invoices want $W_{T}$. Travel wants shared $v$.

## P-construct — 2026-09-27 23:57 EEST

Log: `results/tests-construct-kind-2026-09-28.log`. Tags $\neq$ prints.

## P-cross — 2026-09-27 22:55 EEST

Log: `results/tests-cross-judge-2026-09-28.log`. Same rooms loud, hiking thin. $W$ underdetermined.

## P1 / P0p — 2026-09-27

Logs: `tests-para-hold-2026-09-27.log`, `tests-held-in-topic-2026-09-27.log`.
Qwen hiking held_inroom 0.203 / para 0.160 / LOTO 0.013.
