# Sensor ledger

Do not collapse attempts.

## Reply mutate mid-walk — 2026-09-21 02:41

`python reply_mutate.py --data data/pairs_wide.jsonl`  n=24

```
tail_plan_acc=0.46  tail_topic_acc=0.46  bleed_rate=0.08
mean_loto_plan_acc=0.58
hold: cooking 0.50 hiking 0.50 invoices 0.75 pets 0.75 repairs 0.50 taxes 0.50
```

Almost every `m_plan` is large-negative. The continuation is “there might be some confusion,” not a stall and not a confession. Bleed 0.08: source topic rarely leaks into the tail. Topic 0.46 is chance (6-way). LOTO 0.58 is n=4 noise, not a camera. FO implicit-reject analogy does not fire: the model comments on the swapped ask. Do not fill $D$. Path-patch stays gated.

## Verbal intent oracle — 2026-09-21 02:17

`python intent_oracle.py --data data/pairs_wide.jsonl`  Qwen2.5-7B-Instruct  n=24

```
oracle_plan_acc=0.54  oracle_topic_acc=0.71
mean_loto_plan_acc=0.50
hold plan acc: cooking 0.50 hiking 0.50 invoices 0.75 pets 0.50 repairs 0.25 taxes 0.50
```

Forced-choice logprobs. Plan is chance. LOTO plan is chance (invoices 0.75 is n=4). Verbal topic 0.71 is the first topic score well below the linear-$h$ 1.00 — the mouth is a worse hallway reader than last-token $h$, and still not a plan checker. Taxes/repairs often predicted as hiking. Not $z$. Do not fill $D$.

## Overnight wide pairs — 2026-09-21 01:27

`python overnight_b0.py`  `data/pairs_wide.jsonl`  6 topics  n_eval=24  raw log: [overnight_b0.md](overnight_b0.md)

Linear B0 still fails on every head/residual cut. Adversary train topic mean 0.79 is 6-class difficulty. Do not fill $D$.

## Earlier residual / heads / CPU

Topic acc 1.00 on $h$ cuts. Hold-out head gap 0.04. Inspector moves the whole blob. See prior rows in git history if a line was shortened. Do not train the hinge.
