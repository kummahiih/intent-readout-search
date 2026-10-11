#!/usr/bin/env bash
# Curiosity press of a Phase 1 file. Not the old bank. Not Phase 2.
# Public YES asserts the proposition. A field pass is not a handover.
# Research is not a voter. Do not fill D.
set -u
cd "$(dirname "$0")"
. ./models.sh
DATA="${DATA:-data/scenarios_research.jsonl}"
STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/tests-scenario-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG data=$DATA"
echo "contract run. not Phase 2. not a voter. not handoverPass. Do not fill D."

# paths from models.sh

declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]="$AYA"
  [gemma]="$GEMMA"
  [falcon]="$FALCON"
  [granite]="$GRANITE"
  [qwen35]="$QWEN35"
)

weights_ok() {
  local d="$1"
  [ -f "$d/config.json" ] || return 1
  [ -f "$d/model.safetensors" ] && return 0
  [ -f "$d/model.safetensors.index.json" ] || return 1
  python3 - "$d" << 'PY'
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
idx = json.loads((d / "model.safetensors.index.json").read_text())
missing = [n for n in set(idx.get("weight_map", {}).values()) if not (d / n).is_file()]
raise SystemExit(0 if not missing else 1)
PY
}

want() {
  [ -z "${ONLY:-}" ] && return 0
  local n="$1"
  [[ ",${ONLY}," == *",$n,"* ]]
}

for name in qwen mistral aya gemma falcon granite qwen35; do
  want "$name" || continue
  path="${PATHS[$name]}"
  if ! weights_ok "$path"; then
    echo "skip $name weights"
    continue
  fi
  echo "=== $name ==="
  python3 run_scenario.py --model "$path" --data "$DATA" \
    --dump "results/scenario_${name}_${STAMP}.jsonl"
done
echo "done. not a camera. not handoverPass."
