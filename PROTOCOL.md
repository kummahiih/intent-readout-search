# Protocol

Goal: a readout \(r\) such that proximity to a bank (or a pair gap) tracks **strategy**, not topic.

A gap counts only if all of these hold:

1. Cosine of \(r(h)\) to a frozen deceptive bank, honest vs deceptive, **per topic**.
2. Linear topic probe on the same vectors is *poor* (sensor is not a topic classifier).
3. The same pattern holds on a **paraphrase** of the pair (new wording, same strategy). Clean gap that dies under rewording is the style-shift failure in Kumar 2026.

Walk NLL is observation only.

\(\max_k\cos(h,d_k)\) with tiny \(K\) is the single-direction geometry that paper rejects. Do not treat a large gap on one wording as a pass.

Already failed: last-token and mean-pool identity (regret-heuristic §2 / §6) and identity on `data/pairs.jsonl` (results ledger: topic acc 1.00, gap 0.01).

Do not treat more SGD on identity, more copies of \(I\), or pooling the printed walk as a new sensor.

## Next attempt

1. Paraphrase `pairs.jsonl` (same two topics, same strategies, new sentences). Run `pair_metrics.py` on that file. If topic acc stays ~1 and |gap| stays tiny, identity is dead under shift too.
2. After that: a small linear \(r\) trained with a topic adversary on last-token \(h\) (not SAE, not mean-pool).
3. A detector the hinge never saw, and evasion, only after (1)–(2) pass.

No weights in git.
