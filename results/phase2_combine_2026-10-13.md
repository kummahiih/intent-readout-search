# Phase 2 combination, mid-layer note + pre-button, 2026-10-13

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Script: `phase2_combine.py`. Log: `results/combine-2026-10-13-0130.log`. Mid layer is the plan-LOTO layer: Qwen 8, Mistral 9, Aya 10, Gemma 10, Falcon 8. Pre-button is L−1 from the earlier cache. Same fit/eval split.

Two scalars. Each direction fit on fit ids. A logistic on the pair predicts the public button on eval ids.

## Result

| Walk | Joint | Mid-layer note alone | Pre-button alone | Note-text |
| --- | --- | --- | --- | --- |
| Qwen L8 | 52/55 = 0.945 [0.851, 0.981] | 37/55 | 50/55 = 0.909 | 39/55 = 0.709 |
| Mistral L9 | 53/55 = 0.964 [0.877, 0.990] | 38/55 | 48/55 = 0.873 | 47/55 = 0.855 |
| Aya L10 | 54/55 = 0.982 [0.904, 0.997] | 35/55 | 55/55 = 1.000 | 46/55 = 0.836 |
| Gemma L10 | 52/53 = 0.981 [0.901, 0.997] | 26/53 | 48/53 = 0.906 | 42/53 = 0.792 |
| Falcon L8 | 49/55 = 0.891 [0.782, 0.949] | 34/55 | 53/55 = 0.964 | 45/55 = 0.818 |

Four walks clear the note-text bar with no overlap. Falcon is above and overlaps.

## What this means

The mid-layer note direction alone is at or below majority on every walk. It does not predict the button. The joint score is carried by the pre-button residual, which still sees the ask.

On Qwen, Mistral, and Gemma the mid-layer scalar adds a few points. On Aya and Falcon it costs a few. That is not a plan readout. The plan LOTO separated assigned tags. It does not call the realized button from the note.

Not a handover. Phase 2 stays open. The signal that beats the baseline still lives in the ask tokens.
