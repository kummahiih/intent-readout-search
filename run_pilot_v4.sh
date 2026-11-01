#!/usr/bin/env bash
# Small pilot on the v4 provisional subset (stronger wording-matched stakes).
# Extracts the same 3 geography IDs used in the v3 pilot, runs the scenario presser,
# and tees everything to a log so nothing has to be pasted.
# Not a camera. Not handoverPass. Do not fill D.

set -euo pipefail

mkdir -p results data/prereg

SUBSET=data/prereg/pilot_v4_subset.jsonl
LOG=results/pilot_v4.log

# Extract the same three geography IDs
jq -c 'select(.id | test("geo-krasnodar-01|geo-krasnodar-02|geo-baku-01"))' \
  data/prereg/scenarios_prereg_candidates_v4.jsonl \
  > "$SUBSET"

echo "Subset rows: $(wc -l < "$SUBSET")" | tee -a "$LOG"

echo "=== Qwen2.5-7B-Instruct (local) ===" | tee -a "$LOG"
python run_scenario.py \
  --model ../regret-heuristic/models/Qwen2.5-7B-Instruct \
  --data "$SUBSET" \
  --dump results/pilot_v4_qwen.jsonl \
  2>&1 | tee -a "$LOG"

# Optional Gemma: uncomment and adjust path if present
# echo "=== gemma-2-9b-it (local) ===" | tee -a "$LOG"
# python run_scenario.py \
#   --model ../regret-heuristic/models/gemma-2-9b-it \
#   --data "$SUBSET" \
#   --dump results/pilot_v4_gemma9b.jsonl \
#   2>&1 | tee -a "$LOG"

echo "Pilot finished. Log: $LOG" | tee -a "$LOG"
echo "Dump: results/pilot_v4_qwen.jsonl" | tee -a "$LOG"
