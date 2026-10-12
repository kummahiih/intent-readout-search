#!/usr/bin/env bash
# Noise press, then pre-button residual, then the combine.
# Same stamp throughout. Not Phase 2. Not a camera. Do not fill D.
set -u
cd "$(dirname "$0")"
. ./models.sh

DATA="${DATA:-data/scenarios_noise.jsonl}"
STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/noise-combine-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG data=$DATA stamp=$STAMP"
echo "noise press then combine. not Phase 2. not a camera. Do not fill D."

declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]="$AYA"
  [gemma]="$GEMMA"
  [falcon]="$FALCON"
  [granite]="$GRANITE"
  [qwen35]="$QWEN35"
)

echo "=== press ==="
for name in qwen mistral aya gemma falcon granite qwen35; do
  path="${PATHS[$name]}"
  if [ ! -f "$path/config.json" ]; then
    echo "skip $name: no config"
    continue
  fi
  echo "=== press $name $(date -Iseconds) ==="
  python3 run_scenario.py --model "$path" --data "$DATA" \
    --dump "results/scenario_${name}_${STAMP}.jsonl"
done

echo "=== prebutton ==="
for name in qwen mistral aya gemma falcon; do
  path="${PATHS[$name]}"
  dump="results/scenario_${name}_${STAMP}.jsonl"
  if [ ! -f "$dump" ]; then
    echo "skip $name: no dump"
    continue
  fi
  echo "=== prebutton $name ==="
  python3 phase2_prebutton.py --model "$name" --path "$path" --dump "$dump"
done

echo "=== combine ==="
for name in qwen mistral aya gemma falcon; do
  path="${PATHS[$name]}"
  dump="results/scenario_${name}_${STAMP}.jsonl"
  if [ ! -f "$dump" ]; then
    echo "skip $name: no dump"
    continue
  fi
  echo "=== combine $name ==="
  python3 phase2_combine.py --model "$name" --path "$path" --dump "$dump"
done
echo "done stamp=$STAMP. not Phase 2. not a camera. Do not fill D."
