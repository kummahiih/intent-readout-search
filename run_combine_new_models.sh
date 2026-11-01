#!/usr/bin/env bash
# Combination probe for the November models.
# Presses the bank, extracts prebutton, then fits mid-layer note + pre-button.
# Not a camera. Not handoverPass. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/combine-new-models-$(date +%Y-%m-%d).log"
: >"$LOG"

MODELS_ROOTS=(
  "$HOME/dockers/regret-heuristic/models"
  "$HOME/dockers/intent-readout-search/models"
)

# name|localdir|hfid|mid_layer
SPECS=(
  "llama8it|meta-llama/Llama-3.1-8B-Instruct|meta-llama/Llama-3.1-8B-Instruct|8"
  "gemma2bit|google/gemma-2-2b-it|google/gemma-2-2b-it|8"
  "gemma9bit|google/gemma-2-9b-it|google/gemma-2-9b-it|8"
)

weights_ok() {
  local d="$1"
  [[ -d "$d" ]] || return 1
  python3 - "$d" << 'PY'
import json, sys
from pathlib import Path
d = Path(sys.argv[1])
idx = d / "model.safetensors.index.json"
if idx.is_file():
    shards = set(json.loads(idx.read_text()).get("weight_map", {}).values())
    missing = [s for s in shards if not (d / s).is_file()]
    sys.exit(1 if missing else 0)
sys.exit(0 if list(d.glob("*.safetensors")) or list(d.glob("*.bin")) else 1)
PY
}

first_dir() {
  local c
  for c in "$@"; do
    weights_ok "$c" || continue
    echo "$c"
    return 0
  done
  return 1
}

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  localdir=${rest%%|*}
  rest2=${rest#*|}
  hfid=${rest2%%|*}
  mid=${rest2##*|}

  path=""
  for root in "${MODELS_ROOTS[@]}"; do
    cand="$root/$localdir"
    echo "  check $cand" | tee -a "$LOG"
    path=$(first_dir "$cand") || true
    [[ -n "$path" ]] && break
  done
  if [[ -z "$path" ]]; then
    path="$hfid"
    echo "USE $name hf=$hfid (no local weights)" | tee -a "$LOG"
  else
    echo "USE $name path=$path" | tee -a "$LOG"
  fi

  dump="results/scenario_${name}_$(date +%Y-%m-%d).jsonl"
  run run_scenario.py --model "$path" --data data/scenarios_research.jsonl --dump "$dump"
  run phase2_prebutton.py --model "$name" --path "$path" --dump "$dump" --layer -1
  run phase2_combine.py --model "$name" --path "$path" --dump "$dump" --mid "$mid"
done

echo "log=$LOG"
echo "Read joint vs note-text. Do not average."
echo "Not a camera. Not handoverPass. Do not fill D."
