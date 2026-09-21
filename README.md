# Intent readout search

Can a camera on the walk see the *plan* (stall vs tell the truth) without also seeing the *subject* (hiking vs invoices)?

The hinge that would slap a seen plan lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo only hunts the camera. Tags are observations, not nature. Do not put the hidden room in a loss.

## What we tried (plain language)

Same small handmade notes. Same Qwen. Different ways of looking. These runs are **exploratory**. They do not yet prove the leftovers contain no plan.

- **Look at numbers inside the model.** A least-squares topic fit on the same rows can hit 1.00 even on random labels. That number alone is not a fail. Leave-one-out topic on heads was nearer chance-to-moderate. Strategy gaps stayed small.
- **Train a tiny adversary and hold out a topic.** After fixing the scorer (`argmax`, not `logit > 0`), hold strategy acc is **0.53**. The old 0.50 every fold was a broken threshold. Still not a camera.
- **Ask the model in words.** “Honest or deceptive?” was a coin flip (0.54), including on rows where the subject was wrong (0.43). Same model talks and grades — a walk, not a fact check.
- **Change the subject mid-sentence / copy a mid-layer snapshot.** Confusion, or the same honest sentence. No transferred stall.

Official topic gate should be leave-one-out or held-out, not in-sample least squares. Ledger: [results/README.md](results/README.md). Pass/fail: [PROTOCOL.md](PROTOCOL.md).

```bash
python pair_adversary.py --data data/pairs_wide.jsonl
python intent_oracle.py --data data/pairs_wide.jsonl
python reply_mutate.py --data data/pairs_wide.jsonl
python path_patch_gen.py --data data/pairs_wide.jsonl
python head_write_probe.py
python pair_contrast.py
python topic_residual.py --sweep
python synthetic_z.py
```
