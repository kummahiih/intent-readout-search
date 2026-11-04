#!/usr/bin/env bash
# Run the user-says vs agent-stakes retest on one named model.
# Usage: ./run_retest_frames_one.sh <model-name>
# Example: ./run_retest_frames_one.sh Qwen2.5-7B-Instruct
# Looks for the model under models/ then ../regret-heuristic/models/.
# Not a camera. Not handoverPass. Do not fill D.
set -uo pipefail
cd "$(dirname "$0")"

NAME=${1:?usage: $0 <model-name>}

OUT=results/retest_frames_one_${NAME}_$(date +%Y%m%d_%H%M)
mkdir -p "$OUT"
LOG=$OUT/retest.log
exec > >(tee -a "$LOG") 2>&1

BANK_USER=data/prereg/scenarios_original_user_says.jsonl
BANK_AGENT=data/prereg/scenarios_original_agent_stakes.jsonl
[[ -s $BANK_USER && -s $BANK_AGENT ]] || { echo "FAIL missing framed banks"; exit 2; }

DIR=""
for base in models ../regret-heuristic/models; do
  [[ -d $base/$NAME ]] && DIR=$base/$NAME && break
done
[[ -n $DIR && -f $DIR/config.json ]] || { echo "FAIL model not found: $NAME"; exit 2; }
echo "model=$NAME dir=$DIR"

run_one () {
  local frame=$1 bank=$2
  echo "=== $NAME $frame ==="
  if python run_scenario.py \
       --model "$DIR" \
       --data "$bank" \
       --dump "$OUT/${NAME}__${frame}.jsonl" \
       --role-frame "$frame"; then
    python scripts/text_baselines.py \
      --dump "$OUT/${NAME}__${frame}.jsonl" \
      --bank "$bank" \
      --out "$OUT/${NAME}__${frame}_baselines.json" || echo "baseline failed for $frame"
    echo "OK $NAME $frame"
  else
    echo "FAIL $NAME $frame"
  fi
}

run_one user-says "$BANK_USER"
run_one agent-stakes "$BANK_AGENT"

echo "=== done. Outputs in $OUT ==="
echo "Not a camera. Not handoverPass. D not filled."
