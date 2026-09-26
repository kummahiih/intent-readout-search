# Protocol

Truth is a random variable. Pair tags and toy actions are **observations**, not nature.

$u$ is uncertainty of that observation (label-flip rate, or walk entropy / NLL). It is not $p(\mathrm{lie})$.

Walk / map (glossary [slam_analogy.md](https://github.com/kummahiih/regret-heuristic/blob/main/slam_analogy.md)):

- The printed string or the toy hidden state is a **walk**.
- Possible thoughts (including cells this walk never visits) are the **map**.
- $D$ is a handful of pins, not the map.
- $r$ is a sensor of the walk. Last-token identity is wallpaper on the hallway.
- High $u$ means the chart is coarse there. Do not treat a pin in mush as a known room.

Rules from the first file:

1. Do not put a point in $D$ if $u > u_0$.
2. Report strategy gaps in sure / unsure bins.
3. Wider hinge threshold on high $u$. Quiet on mush is not honesty.
4. Topic probe still has to fail on the same vectors. Official number on vectors is leave-one-out cosine / held-out. Official number on **1-d scores** is `loo_l2_acc` (cosine on a scalar keeps only the sign).
5. Paraphrase still required for a language gap. `data/pairs_paraphrase.jsonl` must cover every topic in the fit file. Do not score a high-$u$ mush row in the same bin as $u\le 0.2$.
6. A held-out cell (action 2, or an unprinted sentence) is a map pin the walk did not occupy. Evading into that cell is not leaving the map.
7. Search $r_{\mathrm{strat}}$ here. Superposition packing fights a clean split. The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). Do not put $z$ in a loss.
8. Same model as actor and judge is one walk. Do not train the hinge on those scores. Do not fill $D$ from them. A *second* judge is a different model later. Do not implement that as Qwen-vs-Qwen.
9. **Pair contract.** A contrast or detector row is legal only if topic is matched and strategy differs (`topic_A \approx topic_B`, `strategy_A \neq strategy_B`). Tags build the *set*. They are not a feature of $L_{\mathrm{total}}$. Assigned strategy is not ground truth of the printed reply.
10. **Same answer is not same strategy.** Last-token identity can match on two walks that print the same cell. A path sensor is only interesting if mid-steps differ while the printed answer stays put. Dummy: [simulation_path_pairs.py](https://github.com/kummahiih/regret-heuristic/blob/main/simulation_path_pairs.py).
11. **`reply_kind`.** Optional field on a *generated reply*, not on the pair tag:
    `{truth, contradict, evade, refuse, insufficient}`.
    Keep it separate from assigned strategy. If the field is missing, print only `frac_contradict` (if you have a fact string) and `agree_assigned_strategy`. Do **not** print `fact_sign_acc` or a deception rate.

## Fit / transfer files (2026-09-26)

- Fit: `data/pairs_wide.jsonl` — 8 topics (invoices, hiking, repairs, cooking, taxes, pets, travel, neighbors). Each topic has 3 deceptive + 3 honest notes.
- Transfer: `data/pairs_paraphrase.jsonl` — same 8 topics, 2 deceptive + 2 honest each. No mush row.
- Tags are observations. Do not put them in $L_{\mathrm{total}}$.

Rerun after a data change:

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
```

## What to report

A run that only prints $L_{\mathrm{reg}}\downarrow$ is incomplete. Log these four when they exist:

| Meter | Question | Official number |
| --- | --- | --- |
| Task | Did the job still work? | task loss / task acc |
| Plan | Does strategy transfer? | plan LOTO |
| Topic | Does the same score name the hallway? | topic LOO (L2 on scalars) |
| Reply | Did the printed text contradict the fact? | `frac_contradict` |

Do **not** report hinge drop as success. Do **not** report `agree_assigned_strategy` as judge accuracy. Do **not** invent a deception-rate column until `reply_kind` exists on the replies.

P0 layer-8 (2026-09-26, 6-topic fit): plan gap 0.0657, topic L2 0.17, within-topic $p=0$. Transfer gap 0.0268, $p=0.10$ on a 3-topic paraphrase file. Hint kept. Camera killed. Do not fill $D$. Rerun on the 8-topic files before claiming the paraphrase kill is stable.

Pass / fail for a camera (same scoreboard):

- Pass: plan / stall transfers leave-one-topic-out.
- Pass: a topic classifier on that same score is near chance (LOO L2 on scalars; LOO / hold on vectors).
- Pass: paraphrase of the walk keeps the plan call.
- Fail: in-sample plan only (LOTO chance).
- Fail: the score still names hiking vs invoices under the official topic gate.
- Fail: path-patch from topic A prints A's words on topic B (lexical bleed).
- Fail: treating same-model chat grades as nature.
- Fail: mixing two topics in one contrast pair and calling that plan.
- Fail: treating $L_{\mathrm{reg}}\to 0$ as reduced deception.
- Fail: calling last-token equality a path camera.
- Fail: printing accuracy when `reply_kind` is absent.

A verbal oracle and a mutated tail are walks. Implicit reject: the API may return a polite key and no fail bit. Do not treat that as $z$.

## CPU (`synthetic_z.py`)

`--noise p` flips the labeler that builds $D$. `lie_out` is an unmapped cell. Hinge 0 + `lie_out` up = walked off the pins, still on a lie path.
