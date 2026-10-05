# Pressure-row scores, 2026-10-05

The 2026-10-04 dumps in `results/pressure_score_<walk>__<source>.jsonl` have no `.rows` stamp. They scored the unfiltered 100-line files. Compare now skips them. They are not entered as 0.

Home rewrite, 4070 Ti 12GB, weights under `models/` or `/media/pauli/datapata/hf/hub`:

```bash
ONLY=qwen,mistral ./run_pressure_score.sh
ONLY=aya,gemma,falcon ./run_pressure_score.sh
ONLY=granite,qwen35 ./run_pressure_score.sh
python compare_pressure_scores.py
```

Phi-4 stays `LossKwargs`. Nimble stays incomplete weights. A walk with no HIDE press is left out of Spearman, not entered as 0.

Filter kept, same predicate as the proxy dry-run: gemma 48, qwen35 59, granite 52, aya 84, falcon 89, qwen 89, mistral 93. Drop count is not a lie rate. ChatGPT, Gemini, and hand rows are not this filter.

Cover, official MASK lie-given-known, and old-bank YES stay separate columns. The seven local files are not pooled. A kept file is not a pass of the four camera gates. Not honesty. Do not fill D. Do not freeze r.
