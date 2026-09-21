# Sensor ledger

Do not collapse attempts.

## Adversary argmax — 2026-09-21 16:27

`python pair_adversary.py --data data/pairs_wide.jsonl`  n=36  dim_r=8

```
mean_topic_acc_adv_train=0.79
mean_strat_acc_hold=0.53          # argmax of two logits
mean_strat_acc_hold_old=0.50      # logits[:,1] > 0
hold strat_acc: cooking 0.83 hiking 0.50 invoices 0.33 pets 0.17 repairs 0.67 taxes 0.67
```

Old rule was 0.50 on every fold: class-1 logits were huge-negative, so `> 0` always said honest. Official argmax mean 0.53 is chance. Folds on n_hold=6 swing 0.17–0.83. Train topic still readable (0.79). Not a camera. Do not fill $D$.

## Activation patch generate — 2026-09-21 02:57

mean_m_clean=-1.328 mean_m_patch=-1.227 bleed=0.00 n=12. Do not fill $D$.

## Verbal oracle coincidence slice — 2026-09-21 02:45

plan 0.54 topic 0.71 miss-slice 0.43 n_miss=7. Chance.

## Reply mutate mid-walk — 2026-09-21 02:41

tail_plan 0.46 tail_topic 0.46 bleed 0.08 LOTO 0.58. Confusion.

## Overnight / residual / heads / CPU

In-sample lstsq topic acc 1.00 can memorize. Hold-out head gap 0.04. Inspector moves the whole blob. Do not train the hinge.
