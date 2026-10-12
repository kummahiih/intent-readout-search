# Phase 2 candidates, 2026-10-13

Not a camera. Not `handoverPass`. Not topic invariance. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Script: `phase2_candidates.py`. Same dumps and same fit/eval split as `phase2_note_baseline.py`. Target is the realized public button. Assigned incentive is not a feature. A missing button is left out.

## Result

| Model | Best candidate | Score | Note-text baseline |
| --- | --- | --- | --- |
| Qwen | belief | 44/55 = 0.800 [0.676, 0.884] | 39/55 = 0.709 |
| Mistral | belief+note | 47/55 = 0.855 [0.738, 0.924] | 47/55 = 0.855 |
| Aya | name | 52/55 = 0.945 [0.851, 0.981] | 46/55 = 0.836 |
| Gemma | belief | 46/53 = 0.868 [0.752, 0.935] | 42/53 = 0.792 |
| Falcon | name | 52/55 = 0.945 [0.851, 0.981] | 45/55 = 0.818 |

Belief and name beat the note-text point estimate on Qwen, Aya, Gemma, and Falcon. Every interval overlaps the baseline. Overlap is not a pass.

## What the candidates are

- `belief` and `name` are other buttons from the same model on the same item. Predicting public from them is a consistency check, not an independent readout of the plan.
- `belief+note` adds the belief bit to the unigram note. It ties Mistral and does not beat the others.
- `cross` uses other models' public buttons, weights fit on fit ids only. It does not beat the baseline cleanly.
- `room` is a per-room unigram logistic. It does not beat the baseline cleanly.

## Status

Phase 2 remains open. A pass is a better readout on the same held-out scenario-ids, with a non-overlapping interval, that is not another button from the same press. None of these are that. Not a handover.
