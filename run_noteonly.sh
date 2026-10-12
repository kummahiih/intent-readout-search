#!/usr/bin/env bash
# Note-only residual on the five live walks.
# No ask. No YES/NO instruction. Prompt is the private note.
# Not a camera. Not handoverPass. Do not fill D.
set -u
cd "$(dirname "$0")"
. ./models.sh

LAYER="${LAYER:--1}"
STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/noteonly-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG layer=$LAYER"
echo "noteonly. no ask. not a camera. not handoverPass. Do not fill D."

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
  python3 phase2_noteonly.py --model "$name" --path "$path" --layer "$LAYER"
done
echo "done. not a camera. not handoverPass."
