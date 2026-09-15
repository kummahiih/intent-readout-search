# Protocol

Goal: a readout \(r\) such that proximity to a bank (or a pair gap) tracks **strategy**, not topic.

A gap counts only if all of these hold:

1. Cosine of \(r(h)\) to a frozen deceptive bank, honest vs deceptive, **per topic**.
2. Linear topic probe on the same vectors is *poor*.
3. The same pattern holds on a paraphrase.

Already failed: last-token / mean-pool identity (regret-heuristic), identity on `pairs.jsonl` and `pairs_paraphrase.jsonl` (topic acc 1.00 both).

## Current attempt

`topic_residual.py`: last-token \(h\), subtract the topic axis estimated from the **bank** pair only.

```bash
python topic_residual.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs.jsonl
python topic_residual.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs_paraphrase.jsonl
```

Pass would need: residual topic probe poor **and** a strategy gap that survives paraphrase. Not SAE. Not pooling.

No weights in git.
