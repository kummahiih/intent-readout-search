#!/usr/bin/env bash
# Two-arm pilot on the v4 provisional subset with explicit role framing.
# Extracts the same 3 geography IDs, runs user-says and agent-stakes,
# and tees everything to a log.
# Not a camera. Not handoverPass. Do not fill D.

set -euo pipefail

mkdir -p results data/prereg

SUBSET=data/prereg/pilot_v4_subset.jsonl
LOG=results/pilot_v4_roles.log

# Extract the same three geography IDs (field is scenario_id)
jq -c 'select(.scenario_id | test("geo-krasnodar-01|geo-krasnodar-02|geo-baku-01"))' \
  data/prereg/scenarios_prereg_candidates_v4.jsonl \
  > "$SUBSET"

echo "Subset rows: $(wc -l < "$SUBSET")" | tee -a "$LOG"

echo "=== user-says framing ===" | tee -a "$LOG"
python run_scenario.py \
  --model ../regret-heuristic/models/Qwen2.5-7B-Instruct \
  --data "$SUBSET" \
  --dump results/pilot_v4_user_says_qwen.jsonl \
  --role-frame user-says \
  2>&1 | tee -a "$LOG"

echo "=== agent-stakes framing ===" | tee -a "$LOG"
python run_scenario.py \
  --model ../regret-heuristic/models/Qwen2.5-7B-Instruct \
  --data "$SUBSET" \
  --dump results/pilot_v4_agent_stakes_qwen.jsonl \
  --role-frame agent-stakes \
  2>&1 | tee -a "$LOG"

echo "Pilot finished. Log: $LOG" | tee -a "$LOG"
echo "Dumps: results/pilot_v4_user_says_qwen.jsonl results/pilot_v4_agent_stakes_qwen.jsonl" | tee -a "$LOG"
