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

`python intent_oracle.py --data data/pairs_wide.jsonl`  n=24

```
oracle_plan_acc=0.54  oracle_topic_acc=0.71  mean_loto_plan_acc=0.50
```

Plan chance. Mouth is a worse hallway reader than last-token $h$ (0.71 vs 1.00). Do not fill $D$.

## Overnight wide pairs — 2026-09-21 01:27

`python overnight_b0.py`  raw: [overnight_b0.md](overnight_b0.md)

| job | topic | strategy gap | note |
| --- | --- | --- | --- |
| residual sweep | 1.00 from layer 7 | \|gap\|\le0.05 | embed 0.50 missing axis |
| pair_contrast n=36 | 0.81 LOTO r | 0.026 | overlap |
| pair_adversary dim=8 | train topic 0.79 | hold strat 0.50 | 6-class |
| loud heads 15,22,23,25 | 1.00 | -0.038 | |
| quiet heads 0,2,3,5 | 1.00 | -0.045 | hugs bank |
| ablate in-sample | lstsq 1.00 / loo 0.29 | -0.052 | selected on eval |
| ablate holdout | lstsq 1.00 / loo 0.54 | -0.024 | flicker gone |

## B0 topic-subtract residual — 2026-09-20 19:41

`topic_residual.py` topic acc raw=1.00 residual=1.00 gap 0.03 n=5. Failed B0.

## Mid-layer sweep — 2026-09-20 19:46

Layers 7–28 topic 1.00 after cut. Embed v=0. Failed B0.

## Same-topic contrast — 20:40 / 20:45

Gap 0.008 then ~0.05. Failed B0.

## Topic adversary — 20:48

Train topic 1.00; hold strat chance. Failed B0.

## Head writes — 2026-09-21 01:06 / 01:12 / 01:15 / 01:20

Loud and quiet topic 1.00. In-sample gap 0.17 died on hold-out (0.036). Failed B0.

## CPU inspector

Inspect 0: gaming. 0.5 whole blob honest. 0.25 whole blob liar.
