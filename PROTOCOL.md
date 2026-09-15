# Protocol

Goal: a readout \(r\) such that proximity to a bank (or a pair gap) tracks **strategy**, not topic.

Metric, in words: gap honest vs deceptive **conditional on topic**, plus a topic probe on \(r\) that should *fail*.

## Try 1 (not run in this file)

Data: paired items. Same task sentence frame. Two strategies (honest plan vs deceptive plan). Same topic words on purpose.

Report:

1. Cosine or hinge of \(r(h)\) to a frozen deceptive bank, honest vs deceptive.
2. A linear topic probe on \(r(h)\). If it works and the strategy gap dies, the sensor failed.
3. NLL / entropy of the walk (observation uncertainty only).

Kill: last-token and mean-pool identity already failed on this pattern in regret-heuristic §2 / §6. They are baselines, not try 2.

Forbidden as the next try: more SGD on identity last-token; more heads of \(I\); pooling more of the printed walk.

Allowed as try 2: contrast pairs; a topic adversary on \(r\); a question the prompt did not ask to print.

Evasion (\(L_{\mathrm{reg}}\downarrow\) with deceptive behavior flat) is a later try, after a sensor that passes (1)–(2).

No \(q_\phi \approx P(Y_D=1\mid z)\) until pairs exist. No weights in git.
