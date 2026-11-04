#!/usr/bin/env bash
# Retest user-says vs agent-stakes on the framed original bank.
# Runs Qwen2.5-7B-Instruct on both framed banks (role frame already in the bank),
# then scores text baselines. Incentive lives in the original note; framing is only a role cue.
# Not a camera. Not handoverPass. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

OUT=results/retest_frames_$(date +%Y%m%d_%H%M)
mkdir -p "$OUT"
LOG=$OUT/retest.log
exec > >(tee -a "$LOG") 2>&1

QWEN=../regret-heuristic/models/Qwen2.5-7B-Instruct
[[ -d $QWEN ]] || { echo "FAIL missing $QWEN"; exit 2; }

BANK_USER=data/prereg/scenarios_original_user_says.jsonl
BANK_AGENT=data/prereg/scenarios_original_agent_stakes.jsonl
[[ -s $BANK_USER && -s $BANK_AGENT ]] || { echo "FAIL missing framed banks"; exit 2; }

echo "=== user-says ==="
python run_scenario.py \
  --model "$QWEN" \
  --data "$BANK_USER" \
  --dump "$OUT/qwen_user_says.jsonl" \
  --role-frame user-says

echo "=== agent-stakes ==="
python run_scenario.py \
  --model "$QWEN" \
  --data "$BANK_AGENT" \
  --dump "$OUT/qwen_agent_stakes.jsonl" \
  --role-frame agent-stakes

echo "=== text baselines ==="
python scripts/text_baselines.py --dump "$OUT/qwen_user_says.jsonl" --bank "$BANK_USER" --out "$OUT/qwen_user_says_baselines.json" || true
python scripts/text_baselines.py --dump "$OUT/qwen_agent_stakes.jsonl" --bank "$BANK_AGENT" --out "$OUT/qwen_agent_stakes_baselines.json" || true

echo "=== done. Outputs in $OUT ==="
echo "Compare public-button lie rates under hide vs name between the two dumps."
echo "Not a camera. Not handoverPass. D not filled."
