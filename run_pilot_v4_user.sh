#!/usr/bin/env bash
# Small pilot on the v4 provisional subset, with incentive_context in the user turn.
# Extracts the same 3 geography IDs, runs the scenario presser with --incentive-in-user,
# and tees everything to a log.
# Not a camera. Not handoverPass. Do not fill D.

set -euo pipefail

mkdir -p results data/prereg

SUBSET=data/prereg/pilot_v4_subset.jsonl
LOG=results/pilot_v4_user.log

# Extract the same three geography IDs (field is scenario_id)
jq -c 'select(.scenario_id | test("geo-krasnodar-01|geo-krasnodar-02|geo-baku-01"))' \
  data/prereg/scenarios_prereg_candidates_v4.jsonl \
  > "$SUBSET"

echo "Subset rows: $(wc -l < "$SUBSET")" | tee -a "$LOG"

echo "=== Qwen2.5-7B-Instruct (local, incentive in user turn) ===" | tee -a "$LOG"
python run_scenario.py \
  --model ../regret-heuristic/models/Qwen2.5-7B-Instruct \
  --data "$SUBSET" \
  --dump results/pilot_v4_user_qwen.jsonl \
  --incentive-in-user \
  2>&1 | tee -a "$LOG"

echo "Pilot finished. Log: $LOG" | tee -a "$LOG"
echo "Dump: results/pilot_v4_user_qwen.jsonl" | tee -a "$LOG"
