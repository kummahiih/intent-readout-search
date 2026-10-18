# Reversed-polarity combination probe, 2026-10-18

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*. Do not run PPO.

Bias control only. The reversed files flip `prop_truth` and `states_proposition` to false, so public YES asserts a false sentence. Script: `run_reverted_combine.sh`. Log: `results/reverted-combine-2026-10-18-1225.log`. 16 rows (8 handwritten + 8 documented), fit=8, eval=8.

## Combination result

Mid-layer note direction + last-layer pre-button direction, logistic on the pair, scored on eval ids.

| Walk | Joint | Raw YES rate |
| --- | --- | --- |
| Qwen L8 | 8/8 = 1.000 [0.676, 1.000] | 0/16 = 0.000 |
| Mistral L9 | 7/8 = 0.875 [0.529, 0.978] | 1/16 = 0.062 |
| Aya L10 | 8/8 = 1.000 [0.676, 1.000] | 8/16 = 0.500 |
| Gemma L10 | 8/8 = 1.000 [0.676, 1.000] | 5/16 = 0.312 |
| Falcon L8 | 7/8 = 0.875 [0.529, 0.978] | 6/16 = 0.375 |

Wilson intervals are wide because *n* = 8 on the eval split.

## Raw YES rate versus the original bank

Original night press (114 rows, three asks) YES rates were high on several walks:

| Walk | Original YES / (YES+NO) | Reversed public YES rate |
| --- | ---: | ---: |
| Qwen | 216/342 ≈ 0.63 | 0.00 |
| Mistral | 275/342 ≈ 0.80 | 0.06 |
| Aya | 298/342 ≈ 0.87 | 0.50 |
| Gemma | 262/338 ≈ 0.78 | 0.31 |
| Falcon | 306/342 ≈ 0.89 | 0.38 |

Qwen and Mistral almost never assert the false proposition on the reversed bank. Aya, Gemma, and Falcon still produce a substantial YES rate even when the proposition is false and the note does not state it. That is the yes-bias the control was meant to expose. It is not a cover rate and not a strategy camera.

## What the combination does here

The joint score tracks the realized button on the small eval set. On a bank where the button is mostly NO (Qwen, Mistral) the probe is mostly predicting NO. On a bank where the button is mixed (Aya) it still tracks the mix. The signal remains the pre-button residual that has already seen the ask, the same pattern as the original combination result. The mid-layer note direction is not shown to carry a plan.

## What this is not

- Not a camera pass. Not a handover.
- Not evidence that a strategy readout exists on the original bank.
- Not a reason to fill *D* or freeze *r*.
- The *n* = 8 eval split is too small for a stable claim about the probe itself. The useful number is the raw YES rate under reversed polarity.

Phase 2 stays open. The negative handover is unchanged.
