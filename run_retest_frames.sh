#!/usr/bin/env bash
# Retest user-says vs agent-stakes on the framed original bank, on every local model.
# Discovers models under models/ and ../regret-heuristic/models/ (must contain config.json).
# Continues to the next model if one fails. Incentive lives in the original note;
# framing is only a role cue.
# Not a camera. Not handoverPass. Do not fill D.
set -uo pipefail
cd "$(dirname "$0")"

OUT=results/retest_frames_all_$(date +%Y%m%d_%H%M)
mkdir -p "$OUT"
LOG=$OUT/retest.log
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
  echo "=== $name $frame ==="
  if python run_scenario.py \
       --model "$dir" \
       --data "$bank" \
       --dump "$OUT/${name}__${frame}.jsonl" \
       --role-frame "$frame"; then
    python scripts/text_baselines.py \
      --dump "$OUT/${name}__${frame}.jsonl" \
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
echo "Compare public-button lie rates under hide vs name between user-says and agent-stakes for each model."
echo "Not a camera. Not handoverPass. D not filled."
