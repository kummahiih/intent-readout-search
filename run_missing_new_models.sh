#!/usr/bin/env bash
# Missing paper-depth meters on the three new instruct models.
# MASK split, pressure rows, cross-judge, multi-r, bailey wipe.
# Continues on failure. No local paths. HF names only.
set -u
cd "$(dirname "$0")"
mkdir -p results data
LOG="results/missing-new-models-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

# name|hf-id|layer
SPECS=(
  "llama8it|meta-llama/Llama-3.1-8B-Instruct|8"
  "gemma2bit|google/gemma-2-2b-it|8"
  "gemma9bit|google/gemma-2-9b-it|10"
)

echo "===== MASK split =====" | tee -a "$LOG"
for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  model=${rest%|*}
  layer=${rest##*|}
  dump="results/mask_split_${name}.jsonl"
  if ! python3 hide_bank.py --model "$model" --arm three --n-samples 2 \
      --data data/pairs_wide.jsonl --dump "$dump" 2>&1 | tee -a "$LOG"; then
    echo "FAILED hide_bank three $name" | tee -a "$LOG"
    continue
  fi
  run note_act.py --model "$model" --layer "$layer" \
    --from-dump "$dump" --arm hide
  run forced_button.py --model "$model" --layer "$layer" --act \
    --from-dump "$dump" --h-site pre --label act \
    --dump "results/mask_split_${name}_pre.jsonl"
done

echo "===== pressure rows =====" | tee -a "$LOG"
for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  model=${rest%|*}
  run make_pressure_rows.py --model "$model" --n 100 --source "$name" \
    --dump "data/pressure_rows_${name}.jsonl"
done

echo "===== multi-r =====" | tee -a "$LOG"
for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  model=${rest%|*}
  layer=${rest##*|}
  run pair_multi_r.py --model "$model" --layer "$layer" --data data/pairs_wide.jsonl
done

echo "===== bailey wipe =====" | tee -a "$LOG"
for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  model=${rest%|*}
  layer=${rest##*|}
  run bailey_tax.py --model "$model" --layer "$layer" --alpha 1.0
done

echo "===== cross-judge =====" | tee -a "$LOG"
# camera -> walk pairs among the three
run pair_cross_judge.py \
  --camera meta-llama/Llama-3.1-8B-Instruct --camera-layer 8 \
  --walk google/gemma-2-2b-it --walk-layer 8 \
  --data data/pairs_wide.jsonl --transfer data/pairs_paraphrase.jsonl --permute 20000
run pair_cross_judge.py \
  --camera meta-llama/Llama-3.1-8B-Instruct --camera-layer 8 \
  --walk google/gemma-2-9b-it --walk-layer 10 \
  --data data/pairs_wide.jsonl --transfer data/pairs_paraphrase.jsonl --permute 20000
run pair_cross_judge.py \
  --camera google/gemma-2-2b-it --camera-layer 8 \
  --walk google/gemma-2-9b-it --walk-layer 10 \
  --data data/pairs_wide.jsonl --transfer data/pairs_paraphrase.jsonl --permute 20000

echo "log=$LOG"
echo "Read accuracy, lie_given_known, cover. Do not average."
echo "Not a camera. Not handoverPass. Do not fill D."
