#!/usr/bin/env bash
# Score the generated pressure-row files with the button bank.
# Three arms: belief, hide, name. One sample. Temperature 0.
# Items in, buttons out. Not honesty. Do not fill D.
# A YES without the fact is a miss, not a cover.
set -u
cd "$(dirname "$0")"
LOG="results/tests-pressure-score-$(date +%Y-%m-%d-%H%M).log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG"
echo "S=button. Tag is not S. Kind not in L. Do not fill D."

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
  [phi4]=models/Phi-4-mini-instruct
  [granite]=models/granite-4.2-8b
  [qwen35]=models/Qwen3.5-9B
  [nimble]=models/Bespoke-Nimble-9B
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

SOURCES=(qwen mistral aya gemma falcon granite qwen35 chatgpt gemini hand)
for name in qwen mistral aya gemma falcon phi4 granite qwen35 nimble; do
  want "$name" || continue
  path="${PATHS[$name]}"
  if ! weights_ok "$path"; then
    echo "SKIP $name: incomplete weights at $path"
    continue
  fi
  for src in "${SOURCES[@]}"; do
    data="data/pressure_rows_${src}.jsonl"
    [ -f "$data" ] || continue
    dump="results/pressure_score_${name}__${src}.jsonl"
    if [ -f "$dump" ] && [ "$(wc -l < "$dump")" -ge 200 ]; then
      echo "SKIP $name on $src: have $dump"
      continue
    fi
    echo "===== $name on $src ====="
    python hide_bank.py --model "$path" --data "$data" --arm three \
      --n-samples 1 --temperature 0 --new-tokens 8 --dump "$dump" \
      || echo "FAIL $name on $src"
  done
done
echo "score dumps in results/pressure_score_*__*.jsonl"
echo "Then: python compare_pressure_scores.py"
echo "Not honesty. Do not fill D."
