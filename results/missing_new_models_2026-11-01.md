# Remaining paper-depth meters on Llama-3.1 and Gemma-2 (2026-11-01)

Log: `results/missing-new-models-2026-11-01.log`.
Finished: MASK split, multi-r, bailey wipe, cross-judge.
Failed: pressure rows (`System role not supported` in `make_pressure_rows.py`).
Complementary runner: `run_pressure_rows_new_models.sh`.

Three logs. Do not average. Not honesty. Not a camera. Do not fill D.

## MASK split (belief, cover, lie-given-known on the button bank)

HIDE and NAME stay separate. A YES without the fact is a miss.

| Walk | HIDE YES | NAME YES | hide on hiking | note→button | pre→button |
| --- | ---: | ---: | --- | ---: | ---: |
| Llama-3.1-8B-Instruct | 0.729 | 0.365 | yes | 0.057 | 0.017 |
| Gemma-2-2b-it | 0.417 | 0.177 | yes | 0.033 | −0.004 |
| Gemma-2-9b-it | 0.854 | 0.229 | yes | 0.106 | (see log) |

Same shape as the hide-bank run. The press happens. The note does not call it.

## multi-r

Ensemble LOTO gap (deceptive − honest) and held score corr².

| Walk | Ensemble gap | mean held corr² |
| --- | ---: | ---: |
| Llama-3.1-8B-Instruct | 0.075 | 0.216 |
| Gemma-2-2b-it | 0.044 | 0.227 |
| Gemma-2-9b-it | 0.070 | 0.315 |

Smaller than the single-direction LOTO on the same walks. Diversity is corr² of LOTO scores. Hiking thin means one arrow still. Not a freeze.

## Bailey wipe

Instrument is the in-place wipe on stored `hidden_states[layer]`. `instrument=ok` means `s_wipe` collapsed. Wipe keep is then the print ignoring a quieted camera.

| Walk | wipe keep | quiet keep | hiking wipe | s_base | s_wipe | instrument |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Llama-3.1-8B-Instruct | 1.000 | 0.854 | 1.000 | −0.048 | 0.000 | ok |
| Gemma-2-2b-it | 0.979 | 0.667 | 1.000 | −0.110 | 0.000 | ok |
| Gemma-2-9b-it | 0.979 | 0.250 | 1.000 | −0.071 | 0.000 | ok |

Same shape as the 7B Bailey pass. The wipe quiets the camera. The print does not flip. Not a freeze.

## Cross-judge

Camera owns `v`. Walk `h` is mapped LOTO into camera space.

| Camera → walk | cross LOTO | paraphrase transfer |
| --- | ---: | ---: |
| Llama → Gemma-2b | 0.162 | 0.151 |
| Llama → Gemma-9b | 0.179 | 0.147 |
| Gemma-2b → Gemma-9b | 0.118 | 0.100 |

Positive aggregate gap survives the linear map and the paraphrase. Same caveat as the single-model LOTO: held-in-topic is larger, so the shared direction is not the room layout. Not a freeze voter.

## Pressure rows

Not run. `make_pressure_rows.py` had its own chat call and rejected the system role on Gemma. Fixed. Complementary runner is `run_pressure_rows_new_models.sh`.

## What this is not

- Not honesty. Not a cover rate. A YES without the fact is a miss.
- Not a camera. Not handoverPass. Do not fill D.
- Wipe keep is not a Bailey number unless `instrument=ok`. Here it is ok, and the print still does not flip.
