#!/usr/bin/env bash
# Resume the all-model user-says vs agent-stakes retest.
# Skips any model/frame that already has a non-empty dump in the partial directory.
# Continues to the next model if one fails.
# Not a camera. Not handoverPass. Do not fill D.
set -uo pipefail
cd "$(dirname "$0")"

PARTIAL=results/retest_frames_all_20261104_1732
OUT=$PARTIAL
[[ -d $OUT ]] || { echo "FAIL missing $OUT"; exit 2; }
LOG=$OUT/retest_resume.log
exec > >(tee -a "$LOG") 2>&1

BANK_USER=data/prereg/scenarios_original_user_says.jsonl
BANK_AGENT=data/prereg/scenarios_original_agent_stakes.jsonl
[[ -s $BANK_USER && -s $BANK_AGENT ]] || { echo "FAIL missing framed banks"; exit 2; }

MODELS=()
NAMES=()
for base in models ../regret-heuristic/models; do
  [[ -d $base ]] || continue
  for d in "$base"/*; do
    [[ -d $d && -f $d/config.json ]] || continue
    MODELS+=("$d")
    NAMES+=("$(basename "$d")")
  done
done
[[ ${#MODELS[@]} -gt 0 ]] || { echo "FAIL no models found"; exit 2; }
echo "models: ${NAMES[*]}"

run_one () {
  local name=$1 dir=$2 frame=$3 bank=$4
  local dump="$OUT/${name}__${frame}.jsonl"
  if [[ -s $dump ]]; then
    echo "SKIP $name $frame (dump exists)"
    return 0
  fi
  echo "=== $name $frame ==="
  if python run_scenario.py \
       --model "$dir" \
       --data "$bank" \
       --dump "$dump" \
       --role-frame "$frame"; then
    python scripts/text_baselines.py \
      --dump "$dump" \
      --bank "$bank" \
      --out "$OUT/${name}__${frame}_baselines.json" || echo "baseline failed for $name $frame"
    echo "OK $name $frame"
  else
    echo "FAIL $name $frame (continuing)"
  fi
}

for i in "${!MODELS[@]}"; do
  run_one "${NAMES[$i]}" "${MODELS[$i]}" user-says "$BANK_USER"
  run_one "${NAMES[$i]}" "${MODELS[$i]}" agent-stakes "$BANK_AGENT"
done

echo "=== done. Outputs in $OUT ==="
echo "Not a camera. Not handoverPass. D not filled."
