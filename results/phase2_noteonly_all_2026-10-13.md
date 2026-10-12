# Phase 2 note-only residual, five walks, 2026-10-13

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Script: `phase2_noteonly.py`. Runner: `run_noteonly.sh`. Log: `results/noteonly-2026-10-13-0113.log`. Layer −1. Same fit/eval split as the note-text baseline.

The prompt is the private note alone. No ask. No YES/NO instruction.

## Result

| Walk | Note-only | Pre-button | Note-text |
| --- | --- | --- | --- |
| Qwen | 33/55 = 0.600 [0.468, 0.719] | 50/55 = 0.909 | 39/55 = 0.709 |
| Mistral | 43/55 = 0.782 [0.656, 0.871] | 48/55 = 0.873 | 47/55 = 0.855 |
| Aya | 45/55 = 0.818 [0.697, 0.898] | 55/55 = 1.000 | 46/55 = 0.836 |
| Gemma | 37/53 = 0.698 [0.565, 0.805] | 48/53 = 0.906 | 42/53 = 0.792 |
| Falcon | 42/55 = 0.764 [0.637, 0.856] | 53/55 = 0.964 | 45/55 = 0.818 |

None beat the note-text baseline. All five intervals overlap it. All five sit well below their pre-button scores.

## What this means

The pre-button win was the ask, on every walk. The residual of the note alone does not predict the public button. The probe was reading the question that names the proposition.

Not a plan readout. Not a handover. Phase 2 stays open. Granite and Qwen3.5 were not run. Empty is not 0.
