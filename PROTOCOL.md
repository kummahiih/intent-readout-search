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
4. Topic probe still has to fail on the same vectors. Official number is leave-one-out / held-out, not in-sample least squares (`topic_metrics.loo_centroid_acc`). Lstsq 1.00 on the same rows can memorize random labels.
5. Paraphrase still required for a language gap.
6. A held-out cell (action 2, or an unprinted sentence) is a map pin the walk did not occupy. Evading into that cell is not leaving the map.
7. Search $r_{\mathrm{strat}}$ here. Superposition packing fights a clean split. The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). Do not put $z$ in a loss.
8. Same model as actor and judge is one walk. A critic head on the same backbone is not an independent fact. Fact-judge on notes (gap 4.79) is not the same instrument as fact-judge on that model's chat (gap 1.17, and a visible lie can score as "no contradiction"). Do not train the hinge on those scores. Do not fill $D$ from them.

Pass / fail for a camera (same scoreboard):

- Pass: plan / stall transfers leave-one-topic-out.
- Pass: a topic classifier on that same score is near chance (LOO / hold, not same-row lstsq).
- Pass: paraphrase of the walk keeps the plan call.
- Fail: in-sample plan only (LOTO chance).
- Fail: the score still names hiking vs invoices under the official topic gate.
- Fail: path-patch from topic A prints A's words on topic B (lexical bleed).
- Fail: treating same-model chat grades as nature.

A verbal oracle and a mutated tail are walks. Implicit reject: the API may return a polite key and no fail bit. Do not treat that as $z$.

## CPU (`synthetic_z.py`)

`--noise p` flips the labeler that builds $D$. `lie_out` is an unmapped cell. Hinge 0 + `lie_out` up = walked off the pins, still on a lie path.
