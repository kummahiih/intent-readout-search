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
12. **Genre.** A freeze-gate transfer file must keep the bank speech act (`User asked` / `I will`). Office-log / radio / trail-desk is a different walk. It may be logged. It does not vote.

## Voter set (2026-09-27)

A **voter** is a (model, depth, pool, room, file) cell that may count toward freeze. Diagnostics that are not voters stay in the ledger.

**In (may vote)**

| File | Rooms | Frame | Role |
| --- | --- | --- | --- |
| `data/pairs_wide.jsonl` | 8 topics, 3+3 each | bank (`User asked` / `I will`) | fit |
| `data/pairs_paraphrase.jsonl` | 8 topics, 2+2 each | same speech act, reworded; has `fact` | transfer |
| `data/pairs_frame.jsonl` | 8 topics, 3+3 | bank syntax + `Desk note:` | transfer, prefix control |

Models: Qwen2.5-7B layer 8, Mistral-7B layer 9. Official pool is last-token. K-step / SIREN / mid3 are one arrow and log only.

Hiking stays in the 8-room set. After a lexical rewrite it is still thin on Qwen LOTO (~0.01). That is a **fail** (rooms are a subset), not a reason to drop the room.

**Out (do not vote)**

| File or object | Why |
| --- | --- |
| `data/pairs_voice.jsonl` | log/radio genre |
| `data/pairs_voice_loud.jsonl` | same genre; LOTO held ~0 |
| last layer | topic L2 leftover |
| SIREN $\theta$ | plan L2 $\approx$ topic L2 |
| $\hat m$ | cap 6 on every 6-note room |
| SAE latents | not through these gates; not in $L$ |

**In-room $v_T$** is a diagnosis, not a freeze voter.

**Holes**

- `split=bank|eval` is stored and unused: $v$ is fit on all 3+3 notes.
- $n$ per room is small. Read gaps, not one-room $p$.

Pass / fail for a camera still needs all four: plan LOTO, topic L2 near chance, paraphrase (in-set files only), rooms not a subset. Genre-out files cannot rescue a room fail. Do not fill $D$.

## Fit / transfer files

- Fit: `data/pairs_wide.jsonl`.
- Official transfer: `data/pairs_paraphrase.jsonl`.
- Prefix control: `data/pairs_frame.jsonl` (8 topics).
- Tags are observations. Do not put them in $L_{\mathrm{total}}$.

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
```

## What to report

| Meter | Question | Official number |
| --- | --- | --- |
| Task | Did the job still work? | task loss / task acc |
| Plan | Does strategy transfer? | plan LOTO |
| Topic | Does the same score name the hallway? | topic LOO (L2 on scalars) |
| Reply | Did the printed text contradict the fact? | `frac_contradict` |

Do **not** report hinge drop as success. Do **not** report `agree_assigned_strategy` as judge accuracy. Do **not** invent a deception-rate column until `reply_kind` exists on the replies.

Pass / fail for a camera:

- Pass: plan / stall transfers leave-one-topic-out.
- Pass: a topic classifier on that same score is near chance (LOO L2 on scalars).
- Pass: paraphrase of the walk keeps the plan call.
- Fail: in-sample plan only.
- Fail: the score still names hiking vs invoices under the official topic gate.
- Fail: rooms are a subset (hiking thin on the shared axis).
- Fail: counting office-log / radio voice as paraphrase.
- Fail: dropping a thin room to manufacture a pass.
- Fail: treating $L_{\mathrm{reg}}\to 0$ as reduced deception.
- Fail: filling $D$ from a hint.

A verbal oracle and a mutated tail are walks. Implicit reject: the API may return a polite key and no fail bit. Do not treat that as $z$.

## CPU (`synthetic_z.py`)

`--noise p` flips the labeler that builds $D$. `lie_out` is an unmapped cell. Hinge 0 + `lie_out` up = walked off the pins, still on a lie path.
