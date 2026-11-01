#!/usr/bin/env bash
# Paper-depth meters on the newly granted models.
# hide-bank (HIDE/NAME), note->button, pre-button.
# MASK official only if datasets/MASK exists.
# Continues on failure. No local paths. HF names only.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/paper-new-models-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

# name|hf-id|layer
SPECS=(
  "llama8|meta-llama/Llama-3.1-8B|8"
  "llama8it|meta-llama/Llama-3.1-8B-Instruct|8"
  "gemma2b|google/gemma-2-2b|8"
  "gemma2bit|google/gemma-2-2b-it|8"
  "gemma9bit|google/gemma-2-9b-it|10"
)

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  model=${rest%|*}
  layer=${rest##*|}
  dump="results/hide_bank_${name}.jsonl"
  echo "===== hide-bank $name $model layer=$layer =====" | tee -a "$LOG"
  run hide_bank.py --model "$model" --arm both --n-samples 2 \
    --data data/pairs_wide.jsonl --dump "$dump" || continue
  run note_act.py --model "$model" --layer "$layer" \
    --from-dump "$dump" --arm hide
  run forced_button.py --model "$model" --layer "$layer" --act \
    --from-dump "$dump" --h-site pre --label act \
    --dump "results/hide_bank_${name}_pre.jsonl"
done

if [[ -d datasets/MASK ]]; then
  echo "===== MASK official =====" | tee -a "$LOG"
  for spec in "${SPECS[@]}"; do
    name=${spec%%|*}
    rest=${spec#*|}
    model=${rest%|*}
    dump="results/mask_official_${name}.jsonl"
    run mask_official.py --model "$model" --data datasets/MASK \
      --limit 1000 --dump "$dump"
  done
else
  echo "SKIP MASK official: datasets/MASK not present" | tee -a "$LOG"
fi

echo "log=$LOG"
echo "Read HIDE YES, NAME YES, note->button, pre->button. Do not average."
echo "A YES without the fact is a miss, not a cover."
echo "Not a camera. Not handoverPass. Do not fill D."
