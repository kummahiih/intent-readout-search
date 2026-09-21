# Sensor ledger

Do not collapse attempts.

## Generate raw vs chat fact-judge — 2026-09-21 19:49

`python generate_fact_grade.py --data data/pairs_wide.jsonl`  n=24

```
raw  gap=1.174  sign=0.46
chat gap=6.462  sign=0.58
```

Notes were raw 4.79 / chat 11.46. On generated replies chat widens the gap because *honest* answers go more negative (clearly match the fact). Deceptive means stay negative. "Payment was processed" is still chat=-0.75. Sign 0.58 is chance-ish. Actor is not adopting the stall. Do not fill $D$.

## Fact-judge on notes — 19:45

raw 4.79/0.79  chat 11.46/0.92.

## OLS topic wipe — 19:43

loo leftover 0.00 plan LOTO 0.58.
