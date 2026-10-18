#!/usr/bin/env bash
# Note-plus-prebutton probe.
# Mid-layer note direction + last-layer pre-button residual, logistic on the pair.
# Same procedure as phase2_combine.py. Diagnostic only.
# Not a camera. Not handoverPass. Do not fill D. Do not freeze r.
#
# Usage
#   bash run_note_plus_prebutton.sh
#   DUMP_STAMP=2026-10-12-0031 bash run_note_plus_prebutton.sh
#   DATA=data/scenarios_simulated.jsonl bash run_note_plus_prebutton.sh
#
# If DATA is set, the script presses that file first, then runs the probe.
# If DATA is unset, it uses existing dumps selected by DUMP_STAMP.
set -u
cd "$(dirname "$0")"
. ./models.sh

DUMP_STAMP="${DUMP_STAMP:-2026-10-12-0031}"
DATA="${DATA:-}"
STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/note-plus-prebutton-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1

echo "log=$LOG"
echo "note-plus-prebutton probe. not a camera. Do not fill D."

declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]="$AYA"
  [gemma]="$GEMMA"
  [falcon]="$FALCON"
)

if [ -n "$DATA" ]; then
  echo "pressing $DATA"
  for name in qwen mistral aya gemma falcon; do
    path="${PATHS[$name]}"
    if [ ! -f "$path/config.json" ]; then
      echo "skip press $name: no config"
      continue
    fi
    dump="results/scenario_${name}_npp_${STAMP}.jsonl"
    echo "=== press $name ==="
    python3 run_scenario.py --model "$path" --data "$DATA" --dump "$dump" || echo "fail press $name"
  done
  DUMP_GLOB="results/scenario_*_npp_${STAMP}.jsonl"
else
  DUMP_GLOB="results/scenario_*_${DUMP_STAMP}.jsonl"
fi

echo "probe stamp=$DUMP_STAMP data=${DATA:-existing dumps}"
for name in qwen mistral aya gemma falcon; do
  path="${PATHS[$name]}"
  if [ -n "$DATA" ]; then
    dump="results/scenario_${name}_npp_${STAMP}.jsonl"
  else
    dump="results/scenario_${name}_${DUMP_STAMP}.jsonl"
  fi
  if [ ! -f "$path/config.json" ]; then
    echo "skip $name: no config at $path"
    continue
  fi
  if [ ! -f "$dump" ]; then
    echo "skip $name: no dump $dump"
    continue
  fi
  echo "=== probe $name ==="
  python3 phase2_combine.py --model "$name" --path "$path" --dump "$dump"
done

echo "done. note-plus-prebutton. not a camera. not handoverPass. Do not fill D."
