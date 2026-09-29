#!/usr/bin/env bash
# Wave 1: same pairs_wide, four local walks.
# Look for tag LOTO, hiking held_inroom, hiking_mixed, button_pre_act_loto.
# Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
LOG="results/tests-scale-wave1-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

# name|path|layer
MODELS=(
  "gemma3:models/gemma-3-4b-it:8"
  "phi4mini:models/Phi-4-mini-instruct:10"
  "falcon3:models/Falcon3-7B-Instruct:8"
  "aya8:models/aya-expanse-8b:10"
)

for spec in "${MODELS[@]}"; do
  name=${spec%%:*}
  rest=${spec#*:}
  path=${rest%:*}
  layer=${rest##*:}
  if [[ ! -d "$path" ]]; then
    echo "SKIP missing $path" | tee -a "$LOG"
    continue
  fi
  run pair_contrast.py --model "$path" --layer "$layer" --held-in-topic
  run forced_button.py --model "$path" --layer "$layer" --act \
    --n-samples 3 --dump "results/scale_${name}_act.jsonl"
  run forced_button.py --model "$path" --layer "$layer" --act \
    --from-dump "results/scale_${name}_act.jsonl" \
    --h-site pre --label act --dump "results/scale_${name}_preact.jsonl"
done

echo "log=$LOG"
echo "Need hiking in every tag LOTO. pre-act gap is the freeze question."
echo "Do not fill D."
