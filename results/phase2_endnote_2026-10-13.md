# Phase 2 end-of-note residual, 2026-10-13

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Script: `phase2_endnote.py`. Runner: `run_endnote.sh`. Log: `results/endnote-2026-10-13-0117.log`. Layer −1. Same fit/eval split as the note-text baseline.

Full public-ask prompt. Residual at the last token of the note span, before the ask tokens that name the proposition.

## Result

| Walk | End-of-note | Note-only | Pre-button | Note-text |
| --- | --- | --- | --- | --- |
| Qwen | 30/55 = 0.545 [0.415, 0.670] | 33/55 = 0.600 | 50/55 = 0.909 | 39/55 = 0.709 |
| Mistral | 43/55 = 0.782 [0.656, 0.871] | 43/55 = 0.782 | 48/55 = 0.873 | 47/55 = 0.855 |
| Aya | 48/55 = 0.873 [0.760, 0.937] | 45/55 = 0.818 | 55/55 = 1.000 | 46/55 = 0.836 |
| Gemma | 40/53 = 0.755 [0.624, 0.851] | 37/53 = 0.698 | 48/53 = 0.906 | 42/53 = 0.792 |
| Falcon | 43/55 = 0.782 [0.656, 0.871] | 42/55 = 0.764 | 53/55 = 0.964 | 45/55 = 0.818 |

None clear the note-text bar. Aya is above the point estimate and overlaps. Qwen is below, and its interval does not overlap the baseline: the note span is worse than the note text.

## What this means

Knowing a question is coming does not put the button in the note span. The pre-button win was the ask tokens. The residual before those tokens does not predict the public button.

Not a plan readout. Not a handover. Phase 2 stays open. The signal that beat the baseline lives in the ask, which names the proposition.
