#!/usr/bin/env bash
# Extract pre-button residuals on npp dumps, then run the note-plus-prebutton probe.
# Needs local weights. Not a camera. Do not fill D. Do not freeze r.
#
# Usage
#   STAMP=2026-10-18-1328 bash run_npp_extract_and_probe.sh
#   STAMP=2026-10-18-1330 bash run_npp_extract_and_probe.sh
set -u
cd "$(dirname "$0")"
. ./models.sh

STAMP="${STAMP:?set STAMP to the npp dump stamp, e.g. 2026-10-18-1328}"
LOG="results/npp-extract-probe-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1

echo "log=$LOG stamp=$STAMP"
echo "extract prebutton then probe. not a camera. Do not fill D."

declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]="$AYA"
  [gemma]="$GEMMA"
  [falcon]="$FALCON"
)

for name in qwen mistral aya gemma falcon; do
  path="${PATHS[$name]}"
  dump="results/scenario_${name}_npp_${STAMP}.jsonl"
  if [ ! -f "$path/config.json" ]; then
    echo "skip $name: no config"
    continue
  fi
  if [ ! -f "$dump" ]; then
    echo "skip $name: no dump $dump"
    continue
  fi
  echo "=== extract prebutton $name ==="
  python3 phase2_prebutton.py --model "$name" --path "$path" --dump "$dump" --layer -1 || {
    echo "fail extract $name"
    continue
  }
  echo "=== probe $name ==="
  python3 phase2_combine.py --model "$name" --path "$path" --dump "$dump" || echo "fail probe $name"
done

echo "done. not a camera. not handoverPass. Do not fill D."
