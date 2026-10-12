# Phase 2 ask-only residual, 2026-10-13

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Script: `phase2_askonly.py`. Log: `results/askonly-2026-10-13-0141.log`. Layer −1. Same fit/eval split.

Prompt is the ask alone. No note. Last-token residual.

## Result

| Walk | Ask-only | Pre-button (note then ask) | Note-only | Note-text |
| --- | --- | --- | --- | --- |
| Qwen | 23/55 = 0.418 [0.297, 0.550] | 50/55 = 0.909 | 33/55 = 0.600 | 39/55 = 0.709 |
| Mistral | 38/55 = 0.691 [0.560, 0.797] | 48/55 = 0.873 | 43/55 = 0.782 | 47/55 = 0.855 |
| Aya | 23/55 = 0.418 [0.297, 0.550] | 55/55 = 1.000 | 45/55 = 0.818 | 46/55 = 0.836 |
| Gemma | 35/53 = 0.660 [0.526, 0.773] | 48/53 = 0.906 | 37/53 = 0.698 | 42/53 = 0.792 |
| Falcon | 13/55 = 0.236 [0.144, 0.363] | 53/55 = 0.964 | 42/55 = 0.764 | 45/55 = 0.818 |

All five are below the note-text baseline. All five intervals do not overlap it. Falcon is anti-predictive.

## What this means

The note was not irrelevant. The ask alone does not predict the button. Note-only did not. End-of-note did not. The order swap did not. The pre-button win needed both, in that order: note first, ask last, residual at the end.

That is the model having read the note and then the question. It is not a plan in the note. It is not the question by itself.

## Loop

Phase 2 has no candidate that predicts the realized button on held-out ids without the ask tokens, and no candidate that does it from the ask alone. The bar-clearing state is the full prompt in the original order. Not a plan readout. Not a handover. Phase 2 stays open. Do not fill *D*.
