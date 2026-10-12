# Phase 2 pre-button residual, five walks, 2026-10-13

Not a camera. Not `handoverPass`. Not topic invariance. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Script: `phase2_prebutton.py`. Runner: `run_prebutton.sh`. Log: `results/prebutton-2026-10-13-0107.log`. Layer −1. Same fit/eval split as the note-text baseline.

Last-token residual of the public-ask prompt, before any YES/NO token. Direction fit on fit ids only. The prompt is the note plus the ask.

## Result

| Walk | Pre-button L−1 | Note-text | Intervals |
| --- | --- | --- | --- |
| Qwen | 50/55 = 0.909 [0.804, 0.961] | 39/55 = 0.709 | no overlap |
| Mistral | 48/55 = 0.873 [0.760, 0.937] | 47/55 = 0.855 | overlap |
| Aya | 55/55 = 1.000 [0.935, 1.000] | 46/55 = 0.836 | no overlap |
| Gemma | 48/53 = 0.906 [0.797, 0.959] | 42/53 = 0.792 | no overlap |
| Falcon | 53/55 = 0.964 [0.877, 0.990] | 45/55 = 0.818 | no overlap |

Four walks clear the note-text bar with non-overlapping intervals. Mistral is above the point estimate and overlaps.

## What this is not

The residual sees the ask, which names the proposition. A note-only residual is the next check. One layer. Granite and Qwen3.5 had no button and were not run. Empty is not 0.

Not a handover. Not a fill of *D*. Phase 2 stays open until a residual that does not see the ask is scored.
