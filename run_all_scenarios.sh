#!/usr/bin/env bash
# Night run of every Phase 1 scenario file. Not the old bank. Not Phase 2.
# Public YES asserts the proposition. A field pass is not a handover.
# Empty walks stay out. Do not fill D. Do not freeze r. Do not run PPO.
set -u
cd "$(dirname "$0")"
DATA="${DATA:-data/scenarios_all.jsonl}"
STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/tests-all-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG data=$DATA"
echo "night run. not Phase 2. not a voter. not handoverPass. Do not fill D."
echo "start $(date -Iseconds)"

QWEN="${QWEN:-models/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL:-models/Mistral-7B-Instruct-v0.3}"
if [ ! -f "$QWEN/config.json" ]; then
  QWEN=/media/pauli/datapata/hf/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28
fi
if [ ! -f "$MISTRAL/config.json" ]; then
  MISTRAL=/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71
fi

declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]=models/aya-expanse-8b
  [gemma]=models/gemma-3-4b-it
  [falcon]=models/Falcon3-7B-Instruct
  [granite]=models/granite-4.2-8b
  [qwen35]=models/Qwen3.5-9B
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
  echo "=== $name $(date -Iseconds) ==="
  if ! python3 run_scenario.py --model "$path" --data "$DATA" \
      --dump "results/scenario_${name}_${STAMP}.jsonl"; then
    echo "fail $name exit=$?"
  fi
done
echo "done $(date -Iseconds). not a camera. not handoverPass."
