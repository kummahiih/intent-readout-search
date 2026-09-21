# Intent readout search

Can a camera on the walk see the *plan* (stall vs tell the truth) without also seeing the *subject* (hiking vs invoices)?

The hinge that would slap a seen plan lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo only hunts the camera. Tags are observations, not nature. Do not put the hidden room in a loss.

## What we tried (plain language)

Same small handmade notes. Same Qwen. Different ways of looking. None of them separated plan from subject.

- **Look at the leftover numbers inside the model.** Cut topic, take loud heads, take quiet heads, ablate heads. A linear reader still named hiking vs invoices every time (accuracy 1.00). The plan gap stayed near zero.
- **Ask the model in words.** “Honest or deceptive?” It was a coin flip (0.54). Even on the rows where it got the subject wrong, plan was still chance (0.43).
- **Let it talk, then change the subject mid-sentence.** It said there might be some confusion. It did not keep a stall that transfers to a new topic.
- **Copy a mid-layer snapshot from a stall note onto a truthful ask and let it finish.** The reply barely changed. No leaked hiking words. Still sounded honest.

So: we can write the test for a strategy camera. On this toy, we have not found one. Hearing the hallway is easy. Hearing the scheme is not. Ledger: [results/README.md](results/README.md). Pass/fail rules: [PROTOCOL.md](PROTOCOL.md).

```bash
python intent_oracle.py --data data/pairs_wide.jsonl
python reply_mutate.py --data data/pairs_wide.jsonl
python path_patch_gen.py --data data/pairs_wide.jsonl
python head_write_probe.py
python pair_adversary.py
python pair_contrast.py
python topic_residual.py --sweep
python synthetic_z.py
```
