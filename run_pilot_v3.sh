#!/usr/bin/env bash
# Small pilot on the v3 provisional subset.
# Expects data/prereg/pilot_v3_subset.jsonl (18 rows) already extracted.
# Adjust MODEL_* paths/ids to your local setup if needed.
# Not a camera. Not handoverPass. Do not fill D.

set -euo pipefail

mkdir -p results

echo "=== Qwen2.5-7B-Instruct ==="
python run_scenario.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --data data/prereg/pilot_v3_subset.jsonl \
  --dump results/pilot_v3_qwen.jsonl

echo "=== gemma-2-9b-it ==="
python run_scenario.py \
  --model google/gemma-2-9b-it \
  --data data/prereg/pilot_v3_subset.jsonl \
  --dump results/pilot_v3_gemma9b.jsonl

echo "Pilot dumps written to results/pilot_v3_*.jsonl"
