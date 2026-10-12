#!/usr/bin/env bash
# Mid-layer note direction + last-layer pre-button direction.
# DUMP_STAMP selects the scenario dumps. Default is the night press.
# For the noise set: DUMP_STAMP=<noise stamp> bash run_combine.sh
# Not a camera. Not handoverPass. Do not fill D.
set -u
cd "$(dirname "$0")"
. ./models.sh

DUMP_STAMP="${DUMP_STAMP:-2026-10-12-0031}"
STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/combine-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG dump_stamp=$DUMP_STAMP"
echo "combine. mid-layer note + prebutton. not a camera. Do not fill D."

declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]="$AYA"
  [gemma]="$GEMMA"
  [falcon]="$FALCON"
)

for name in qwen mistral aya gemma falcon; do
  path="${PATHS[$name]}"
  dump="results/scenario_${name}_${DUMP_STAMP}.jsonl"
  if [ ! -f "$path/config.json" ]; then
    echo "skip $name: no config at $path"
    continue
  fi
  if [ ! -f "$dump" ]; then
    echo "skip $name: no dump $dump"
    continue
  fi
  echo "=== $name ==="
  python3 phase2_combine.py --model "$name" --path "$path" --dump "$dump"
done
echo "done. not a camera. not handoverPass."
