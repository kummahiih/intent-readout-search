#!/usr/bin/env bash
# Noise press. 4 alphanumeric bytes before and after the proposition.
# Same handwritten and web cases. Not Phase 2. Do not fill D.
set -u
cd "$(dirname "$0")"
. ./models.sh

DATA="${DATA:-data/scenarios_noise.jsonl}"
STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/noise-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG data=$DATA"
echo "noise press. not Phase 2. not a voter. not handoverPass. Do not fill D."

declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]="$AYA"
  [gemma]="$GEMMA"
  [falcon]="$FALCON"
  [granite]="$GRANITE"
  [qwen35]="$QWEN35"
)

for name in qwen mistral aya gemma falcon granite qwen35; do
  path="${PATHS[$name]}"
  if [ ! -f "$path/config.json" ]; then
    echo "skip $name: no config at $path"
    continue
  fi
  echo "=== $name $(date -Iseconds) ==="
  python3 run_scenario.py --model "$path" --data "$DATA" \
    --out "results/scenario_${name}_${STAMP}.jsonl"
done
echo "done. not Phase 2. not handoverPass."
