# Phase 2 note-only residual, 2026-10-13

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Script: `phase2_noteonly.py`. Cache: `results/noteonly_qwen_L-1.npy`. Same dump and same fit/eval split as the pre-button probe.

## What changed

The prompt is the private note alone. No ask. No YES/NO instruction. Same last-token residual, same mean-difference direction, same threshold rule.

## Result

| Walk | Note-only L−1 | Pre-button L−1 | Note-text |
| --- | --- | --- | --- |
| Qwen | 33/55 = 0.600 [0.468, 0.719] | 50/55 = 0.909 [0.804, 0.961] | 39/55 = 0.709 |

Note-only is the majority rate (33/55). It is below the note-text baseline. Its interval overlaps the baseline and does not overlap the pre-button result.

## What this means

The pre-button win was the ask. The residual of the note alone does not predict the public button. The model reads the question that names the proposition, and that is what the probe used.

Not a plan readout. Not a handover. Phase 2 stays open. One model. One layer. The other walks are not scored on note-only yet.
