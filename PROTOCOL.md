# Protocol

Truth is a random variable. Pair tags and toy actions are **observations**, not nature.

\(u\) is uncertainty of that observation (label-flip rate, or walk entropy / NLL). It is not \(p(\mathrm{lie})\).

Walk / map (glossary [slam_analogy.md](https://github.com/kummahiih/regret-heuristic/blob/main/slam_analogy.md)):

- The printed string or the toy hidden state is a **walk**.
- Possible thoughts (including cells this walk never visits) are the **map**.
- \(D\) is a handful of pins, not the map.
- \(r\) is a sensor of the walk. Last-token identity is wallpaper on the hallway.
- High \(u\) means the chart is coarse there. Do not treat a pin in mush as a known room.

Rules from the first file:

1. Do not put a point in \(D\) if \(u > u_0\).
2. Report strategy gaps in sure / unsure bins.
3. Wider hinge threshold on high \(u\). Quiet on mush is not honesty.
4. Topic probe still has to fail on the same vectors.
5. Paraphrase still required for a language gap.
6. A held-out cell (action 2, or an unprinted sentence) is a map pin the walk did not occupy. Evading into that cell is not leaving the map.

## CPU (`synthetic_z.py`)

`--noise p` flips the labeler that builds \(D\). `lie_out` is an unmapped cell. Hinge 0 + `lie_out` up = walked off the pins, still on a lie path.
