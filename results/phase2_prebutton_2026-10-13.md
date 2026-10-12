# Phase 2 pre-button residual, 2026-10-13

Not a camera. Not `handoverPass`. Not topic invariance. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Script: `phase2_prebutton.py`. Cache: `results/prebutton_qwen_L-1.npy`. Dump: `results/scenario_qwen_2026-10-12-0031.jsonl`. Split: fit/eval by `scenario_id`, same as the note-text baseline.

## What was measured

Last-token residual of the public-ask prompt, before any YES/NO token. Layer −1. Direction is the mean difference between train YES and train NO, threshold at the midpoint of the train projections. Eval ids only.

The prompt is the note plus the public ask. It is not the note alone.

## Result

| Walk | Pre-button L−1 | Note-text baseline |
| --- | --- | --- |
| Qwen | 50/55 = 0.909 [0.804, 0.961] | 39/55 = 0.709 [0.579, 0.812] |

The intervals do not overlap. The point estimate is above the baseline.

## What this is not

One model. One layer. The residual sees the ask, which names the proposition, so it is not a note-only readout. It is a prediction of the button from the state just before the button. That is closer to "the decision is already in the last token" than to "a plan readout independent of the output."

Not a handover. Not a fill of *D*. Phase 2 stays open until the same bar is met on the other walks, and until a residual that does not see the ask is tested.

## Six checks

- Isolation: split by `scenario_id` before the direction is fit. Eval ids absent from train.
- Accounting: 114 public rows, 59 fit, 55 eval, 0 left out.
- Target: public button. Note and ask are in the prompt. Incentive is not a feature.
- Baseline: the note-text table.
- Uncertainty: 50/55, Wilson 95%.
- Reproducibility: cached residual, fixed dump, fixed split, fixed script.
