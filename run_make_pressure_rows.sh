#!/usr/bin/env bash
# Ask each local Transformers walk for 100 pressure-bank rows.
# Items, not buttons. Not honesty. Do not fill D.
set -u
cd "$(dirname "$0")"
LOG="results/tests-pressure-rows-$(date +%F-%H%M).log"
mkdir -p results data
ONLY="${ONLY:-}"
want() { [ -z "$ONLY" ] || [[ ",${ONLY}," == *",$1,"* ]]; }
first_dir() {
  local a="$1" b="$2"
  if [ -d "$a" ]; then echo "$a"; elif [ -d "$b" ]; then echo "$b"; else echo "$a"; fi
}
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
run() { python "$@" 2>&1 | tee -a "$LOG"; return "${PIPESTATUS[0]}"; }
QWEN=$(first_dir models/Qwen2.5-7B-Instruct /media/pauli/datapata/hf/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28)
MISTRAL=$(first_dir models/Mistral-7B-Instruct-v0.3 /media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71)
declare -A PATHS=(
  [qwen]="$QWEN"
  [mistral]="$MISTRAL"
  [aya]=models/aya-expanse-8b
  [gemma]=models/gemma-3-4b-it
  [falcon]=models/Falcon3-7B-Instruct
  [phi4]=models/Phi-4-mini-instruct
  [granite]=models/granite-4.2-8b
  [qwen35]=models/Qwen3.5-9B
  [nimble]=models/Bespoke-Nimble-9B
)
for name in qwen mistral aya gemma falcon phi4 granite qwen35 nimble; do
  want "$name" || continue
  path="${PATHS[$name]}"
  if ! weights_ok "$path"; then
    echo "SKIP $name: incomplete weights at $path" | tee -a "$LOG"
    continue
  fi
  echo "USE $name path=$path" | tee -a "$LOG"
  run make_pressure_rows.py --model "$path" --n 100 --source "$name" \
    --dump "data/pressure_rows_${name}.jsonl" || echo "FAIL $name" | tee -a "$LOG"
done
echo "Hand rows are data/pressure_rows_hand.jsonl. External prompt is prompts/pressure_rows_external.md." | tee -a "$LOG"
echo "Not a button score. Do not fill D." | tee -a "$LOG"
