#!/usr/bin/env bash
# Mid-layer note direction + last-layer pre-button direction.
# Not a camera. Not handoverPass. Do not fill D.
set -u
cd "$(dirname "$0")"
. ./models.sh

STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/combine-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG"
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
  if [ ! -f "$path/config.json" ]; then
    echo "skip $name: no config at $path"
    continue
  fi
  echo "=== $name ==="
  python3 phase2_combine.py --model "$name" --path "$path"
done
echo "done. not a camera. not handoverPass."
