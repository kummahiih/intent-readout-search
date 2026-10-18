#!/usr/bin/env bash
# Press the reversed-polarity files, then run the combination probe on them.
# Bias control only. Not a voter. Not a camera. Do not fill D. Do not freeze r.
set -u
cd "$(dirname "$0")"
. ./models.sh

STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/reverted-combine-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG"
echo "reversed polarity bias control. not a camera. Do not fill D."

# Concatenate the two reversed files for a single press.
CAT="results/scenarios_reverted_${STAMP}.jsonl"
cat data/scenarios_reverted_handwritten.jsonl data/scenarios_reverted_documented.jsonl > "$CAT"
echo "scenarios=$CAT rows=$(wc -l < "$CAT")"

declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]="$AYA"
  [gemma]="$GEMMA"
  [falcon]="$FALCON"
)

for name in qwen mistral aya gemma falcon; do
  path="${PATHS[$name]}"
  if [ ! -f "$path/config.json" ]; then
    echo "skip $name: no config at $path"
    continue
  fi
  dump="results/scenario_${name}_reverted_${STAMP}.jsonl"
  echo "=== press $name ==="
  if ! python3 run_scenario.py --model "$path" --data "$CAT" --dump "$dump"; then
    echo "fail press $name"
    continue
  fi
  echo "=== combine $name ==="
  python3 phase2_combine_reverted.py \
    --model "$name" \
    --path "$path" \
    --scenarios "$CAT" \
    --dump "$dump"
done

echo "done. bias control. not a camera. not handoverPass. Do not fill D."
