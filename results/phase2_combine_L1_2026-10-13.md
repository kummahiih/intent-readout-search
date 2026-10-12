# Phase 2 combination, last-layer pair, 2026-10-13

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*.

Two scalars from existing caches. Note-only L−1 direction and pre-button L−1 direction, each fit on fit ids. A logistic on the two scores predicts the public button on eval ids. No new extraction.

## Result

| Walk | Joint L−1 | Pre-button alone | Note-text |
| --- | --- | --- | --- |
| Qwen | 50/55 = 0.909 [0.804, 0.961] | 50/55 = 0.909 | 39/55 = 0.709 |
| Mistral | 53/55 = 0.964 [0.877, 0.990] | 48/55 = 0.873 | 47/55 = 0.855 |
| Aya | 54/55 = 0.982 [0.904, 0.997] | 55/55 = 1.000 | 46/55 = 0.836 |
| Gemma | 51/53 = 0.962 [0.872, 0.990] | 48/53 = 0.906 | 42/53 = 0.792 |
| Falcon | 50/55 = 0.909 [0.804, 0.961] | 53/55 = 0.964 | 45/55 = 0.818 |

All five clear the note-text bar. Intervals do not overlap it. Mistral and Gemma improve on pre-button alone. Aya and Falcon drop a little. Qwen ties.

## What this is

The note-only direction alone was majority. It adds something only when the pre-button score is already in the model. The pre-button residual still sees the ask. This is not a plan readout from the note.

The plan LOTO lived at mid layer. `phase2_combine.py` extracts the note residual there and pairs it with the same pre-button score. That run is not in this table.
