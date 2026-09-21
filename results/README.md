# Sensor ledger

Do not collapse attempts.

## Fact-judge raw vs chat on notes — 2026-09-21 19:45

`python fact_grade.py --data data/pairs_wide.jsonl`  n=24

```
raw  gap=4.786  sign=0.79
chat gap=11.456 sign=0.92
```

Chat wrap makes the note-judge *sharper*, not weaker. Generated-reply collapse (gap 1.17) was not "forgot the template on notes." `generate_fact_grade.py` still uses raw `fact_margin`. Do not fill $D$.

## OLS topic wipe — 19:43

loo leftover 0.00 plan LOTO 0.58.

## Generate then fact-grade (raw) — 19:30

gap 1.17 sign 0.46 vs note raw 4.79.
