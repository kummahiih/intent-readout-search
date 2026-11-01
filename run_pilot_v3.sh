#!/usr/bin/env bash
# Small pilot on the v3 provisional subset.
# Expects data/prereg/pilot_v3_subset.jsonl (18 rows) already extracted.
# Uses local model directories.
# Not a camera. Not handoverPass. Do not fill D.

set -euo pipefail

mkdir -p results

echo "=== Qwen2.5-7B-Instruct (local) ==="
python run_scenario.py \
  --model ../regret-heuristic/models/Qwen2.5-7B-Instruct \
  --data data/prereg/pilot_v3_subset.jsonl \
  --dump results/pilot_v3_qwen.jsonl

echo "=== gemma-2-9b-it (not in local models/ list; adjust if present) ==="
echo "# gemma-2-9b-it is not in the listed local dirs."
echo "# Available nearby: gemma-3-4b-it, or pull gemma-2-9b-it."
echo "# Example if you have it:"
echo "# python run_scenario.py --model models/gemma-2-9b-it --data data/prereg/pilot_v3_subset.jsonl --dump results/pilot_v3_gemma9b.jsonl"

# Uncomment and adjust once the path exists:
# python run_scenario.py \
#   --model models/gemma-2-9b-it \
#   --data data/prereg/pilot_v3_subset.jsonl \
#   --dump results/pilot_v3_gemma9b.jsonl

echo "Pilot dump (Qwen) written to results/pilot_v3_qwen.jsonl"
