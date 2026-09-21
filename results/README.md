# Sensor ledger

Do not collapse attempts.

## Fact judge on notes — 2026-09-21 17:08

`python fact_grade.py --data data/pairs_wide.jsonl`  n=24

```
mean_fact_m deceptive=3.792 honest=-0.995 gap_dec_minus_hon=4.786
fact_sign_acc=0.79
```

Judge sees fact + note, not the strategy tag. Deceptive notes plan to fight the fact and score high. Honest notes usually do not. This is judge calibration, not a residual camera. Some honest rows still go positive. Do not fill $D$.

## Reply mutate, tail-only — 16:57

plan 0.50 dst topic 0.62 LOTO 0.38. Confusion.

## Contrast scalar / heads LOO / adversary

scalar topic 0.17 gap 0.03. Heads LOO 0.79. Hold strat 0.53.
