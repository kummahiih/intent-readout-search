# Phase 2 candidates, computable now

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*.

Same dumps and same fit/eval split as `phase2_note_baseline.py`. Target is the realized public button. Assigned incentive is not a feature. A missing button is left out.

| Model | Candidate | Correct | Note-text baseline |
| --- | --- | --- | --- |
| qwen | belief | 44/55 = 0.800 [0.676, 0.884] ** | 39/55 = 0.709 |
| qwen | name | 42/55 = 0.764 [0.637, 0.856] ** | 39/55 = 0.709 |
| qwen | belief+note | 40/55 = 0.727 [0.598, 0.827] ** | 39/55 = 0.709 |
| qwen | cross | 41/55 = 0.745 [0.617, 0.842] ** | 39/55 = 0.709 |
| qwen | room | 40/55 = 0.727 [0.598, 0.827] ** | 39/55 = 0.709 |
| mistral | belief | 45/55 = 0.818 [0.697, 0.898] | 47/55 = 0.855 |
| mistral | name | 46/55 = 0.836 [0.717, 0.911] | 47/55 = 0.855 |
| mistral | belief+note | 47/55 = 0.855 [0.738, 0.924] | 47/55 = 0.855 |
| mistral | cross | 45/55 = 0.818 [0.697, 0.898] | 47/55 = 0.855 |
| mistral | room | 45/55 = 0.818 [0.697, 0.898] | 47/55 = 0.855 |
| aya | belief | 50/55 = 0.909 [0.804, 0.961] ** | 46/55 = 0.836 |
| aya | name | 52/55 = 0.945 [0.851, 0.981] ** | 46/55 = 0.836 |
| aya | belief+note | 43/55 = 0.782 [0.656, 0.871] | 46/55 = 0.836 |
| aya | cross | 46/55 = 0.836 [0.717, 0.911] ** | 46/55 = 0.836 |
| aya | room | 39/55 = 0.709 [0.579, 0.812] | 46/55 = 0.836 |
| gemma | belief | 46/53 = 0.868 [0.752, 0.935] ** | 42/53 = 0.792 |
| gemma | name | 42/53 = 0.792 [0.665, 0.880] ** | 42/53 = 0.792 |
| gemma | belief+note | 40/53 = 0.755 [0.624, 0.851] | 42/53 = 0.792 |
| gemma | cross | 41/53 = 0.774 [0.645, 0.865] | 42/53 = 0.792 |
| gemma | room | 41/53 = 0.774 [0.645, 0.865] | 42/53 = 0.792 |
| falcon | belief | 49/55 = 0.891 [0.782, 0.949] ** | 45/55 = 0.818 |
| falcon | name | 52/55 = 0.945 [0.851, 0.981] ** | 45/55 = 0.818 |
| falcon | belief+note | 44/55 = 0.800 [0.676, 0.884] | 45/55 = 0.818 |
| falcon | cross | 49/55 = 0.891 [0.782, 0.949] ** | 45/55 = 0.818 |
| falcon | room | 49/55 = 0.891 [0.782, 0.949] ** | 45/55 = 0.818 |

A `**` marks a point estimate above the note-text baseline. Overlapping intervals are not a pass. A pass is a better readout on the same held-out ids. Not a handover.
