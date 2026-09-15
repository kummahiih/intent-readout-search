# Protocol

Goal: a readout \(r\) such that proximity to a bank (or a pair gap) tracks **strategy**, not topic.

Report:

1. Cosine of \(r(h)\) to a frozen deceptive bank, honest vs deceptive, **per topic**.
2. Linear topic probe on the same vectors. If topic accuracy is high and the strategy gap is ~0, the sensor failed.
3. Walk NLL (observation only).

Baselines already failed: last-token and mean-pool identity in regret-heuristic §2 / §6.

Do not treat more SGD on identity last-token, more copies of \(I\), or pooling more of the printed walk as a new sensor.

Next sensors to try after the identity control: contrast on pairs; a topic adversary on \(r\); a question the prompt did not ask to print.

Evasion tests come after a sensor that passes (1)–(2). No weights in git.
