# Gate-packages run, 2026-10-18

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*.

Log: `results/gate-packages-2026-10-18-1437.log`. Scores: `results/probe_scores.jsonl` (114 rows), built from a scenario dump with `--pred-from-button`.

## What the log printed

| Package | Cross-topic | Topic exclusion | Paraphrase | Coverage | Pass |
| --- | --- | --- | --- | --- | --- |
| A strict | pass (lo=0.514) | unmeasured | unmeasured | unmeasured | no |
| B moderate | pass (lo=0.514) | unmeasured | unmeasured | unmeasured | no |
| C exploratory | point=0.605, not flagged | unmeasured | unmeasured | unmeasured | no |

## Why the cross-topic pass is not a result

`pred` was copied from the public button. The scorer then compared `pred` to `y` on held-out topics. That is the label scored against itself, not a probe. A cross-topic pass under that condition does not show transfer of a strategy signal.

Topic exclusion, paraphrase agreement, and coverage were unmeasured because the scores file has no `topic_pred`, `paraphrase_of`, or `score` column.

## What a real run needs

A scores file with probe outputs:

- `pred` from a residual probe, not from the button
- `loto_pred` fitted on all topics except the row's topic
- `topic_pred` from a topic classifier on the same residual
- `paraphrase_of` linking each paraphrase to its original id
- `score` if coverage is to be a projection rather than fraction correct

Until those columns exist, A and B cannot pass, and C is a log with nothing to flag except the smoke-test point estimate.

The negative handover is unchanged.
