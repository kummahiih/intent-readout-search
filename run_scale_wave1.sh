#!/usr/bin/env bash
# Wave 1: same pairs_wide, local walks that load on this venv.
# Phi-4-mini remote modeling_phi3.py wants LossKwargs; skip until stack matches.
# Gemma-3 needs a gated accept + sentencepiece.
# Look for tag LOTO, hiking held_inroom, hiking_mixed, button_pre_act_loto.
# Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
LOG="results/tests-scale-wave1-$(date +%Y-%m-%d).log"
# append; do not wipe a finished Gemma block
touch "$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

MODELS=(
  "gemma3:models/gemma-3-4b-it:8"
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
  run pair_contrast.py --model "$path" --layer "$layer" --held-in-topic \
    --data data/pairs_wide.jsonl
  run forced_button.py --model "$path" --layer "$layer" --act \
    --data data/pairs_wide.jsonl --n-samples 3 --dump "results/scale_${name}_act.jsonl"
  run forced_button.py --model "$path" --layer "$layer" --act \
    --from-dump "results/scale_${name}_act.jsonl" \
    --h-site pre --label act --dump "results/scale_${name}_preact.jsonl"
done

echo "log=$LOG"
echo "Need eight rooms in paired_topics. pre-act gap is the freeze question."
echo "Do not fill D."
