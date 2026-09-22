# Sensor ledger

Do not collapse attempts.

## Metric repairs — 2026-09-22 (not yet rerun on GPU)

- Scalar topic: official gate is `topic_loo_l2_on_scalar`. Cosine LOO 0.17 was sign-only. Do not read it as topic-blind.
- OLS wipe: global leftover + cosine LOO 0.00 is retired (held-out same-topic centroid is −r/(n−1)). Use `topic_loo_l2_leftover_foldfit` and `mean_loto_plan_leftover_foldfit`.
- Generated fact-grade: `agree_assigned_strategy` is not judge accuracy. Needs reply-level labels.
- Chat oracle: zero-threshold plan 0.50 is always-deceptive. LOTO 0.79 is a threshold fit on other topics, n_hold=4. Tentative calibration, not dismissed and not a camera.

## Verbal oracle chat template — 2026-09-21 19:53

```
oracle_plan_acc=0.50  oracle_topic_acc=0.67
mean_loto_plan_acc=0.79
```

Every row `pred_plan=deceptive` at the default pick. LOTO 0.79 is four rows after a threshold from the other topics.

## Notes vs generated fact-judge — 19:45 / 19:49

notes chat gap 11.46 agree 0.92. generated chat gap 6.46 agree 0.58. Agree is vs assigned note strategy, not vs a labeled reply.
