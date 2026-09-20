# Sensor ledger

Do not collapse attempts.

## Verbal oracle coincidence slice — 2026-09-21 02:45

`python intent_oracle.py --data data/pairs_wide.jsonl`  n=24

```
oracle_plan_acc=0.54  oracle_topic_acc=0.71  mean_loto_plan_acc=0.50
plan_acc_topic_miss=0.43  n_miss=7
plan_acc_topic_hit=0.59  n_hit=17
```

Where the mouth missed the subject, plan acc is still chance. Delayed-choice verbal slice is null. Do not fill $D$.

## Reply mutate mid-walk — 2026-09-21 02:41

`python reply_mutate.py`  tail_plan=0.46 tail_topic=0.46 bleed=0.08 LOTO=0.58. Confusion, not stall. Path-patch gated.

## Overnight / residual / heads / CPU

Linear topic acc 1.00 on $h$ cuts. Hold-out head gap 0.04. Inspector moves the whole blob. Do not train the hinge.
