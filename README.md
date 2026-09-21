# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss.

## What we tried (plain language)

Same handmade notes. Same Qwen. These runs are exploratory. Official topic gate is leave-one-out, not same-row least squares.

- **Numbers inside the model.** Lstsq topic can hit 1.00 on the same rows (and on random labels). Official LOO: loud heads **0.79**, full layer **0.62**. Six-way chance is ~0.17, so topic is still there. Strategy gap ~0.
- **Adversary, hold out a topic.** After fixing `argmax`, hold strategy acc is **0.53**. The old 0.50 every fold was `logit > 0` on huge-negative class-1 scores.
- **Contrast direction $v$.** Topic on the scalar $s=h\cdot v$ is **0.17** (chance). The old 0.81 used fold-identified $(h\cdot v)v$. Plan gap **0.03**. Topic-blind and plan-blind.
- **Ask in words.** Honest/deceptive was a coin flip (0.54).
- **Fact vs note.** Same model, different question: does this note fight a known fact? Gap **4.79**, sign acc **0.79**. The judge can read a written scheme.
- **Fact vs generated reply.** Gap **1.17**, sign acc **0.46**. The actor often refuses or narrates. A visible lie can still score as "no contradiction." Same-model chat grades are not nature.
- **Mutate mid-walk, grade the tail only.** Plan **0.50**, topic after swap **0.62**, old subject **0.08**, LOTO **0.38**. Confusion, not a transferred stall.
- **Copy a mid-layer snapshot into a truthful ask.** Bleed 0. Margins unchanged.

Ledger: [results/README.md](results/README.md). Rules: [PROTOCOL.md](PROTOCOL.md).

```bash
python fact_grade.py --data data/pairs_wide.jsonl
python generate_fact_grade.py --data data/pairs_wide.jsonl
python pair_adversary.py --data data/pairs_wide.jsonl
python pair_contrast.py --data data/pairs_wide.jsonl
python head_write_probe.py --data data/pairs_wide.jsonl
python reply_mutate.py --data data/pairs_wide.jsonl
```
