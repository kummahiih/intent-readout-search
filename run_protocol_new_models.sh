#!/usr/bin/env bash
# Protocol-paper meters on the newly granted models.
# Same files and meters as the 7B runs: pairs_wide + paraphrase transfer, last-token, LOTO.
# held-in-topic is a diagnostic, not a freeze gate.
# Continues on failure. No local paths.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
LOG="results/protocol-new-models-$(date +%Y-%m-%d).log"
: >"$LOG"

# model  layer  (mid-layer, ~0.25-0.3 depth)
# Llama-3.1-8B: 32 layers -> 8
# gemma-2-2b:   26 layers -> 8
# gemma-2-9b:   42 layers -> 10
MODELS=(
  "meta-llama/Llama-3.1-8B:8"
  "meta-llama/Llama-3.1-8B-Instruct:8"
  "google/gemma-2-2b:8"
  "google/gemma-2-2b-it:8"
  "google/gemma-2-9b-it:10"
)

run_one() {
  local spec="$1"
  local model="${spec%%:*}"
  local layer="${spec##*:}"
  echo "===== $model layer=$layer =====" | tee -a "$LOG"
  python3 pair_contrast.py \
    --model "$model" \
    --data data/pairs_wide.jsonl \
    --layer "$layer" \
    --pool last \
    --permute 20000 \
    --transfer data/pairs_paraphrase.jsonl \
    2>&1 | tee -a "$LOG" || echo "FAILED $model LOTO" | tee -a "$LOG"
  echo "===== $model layer=$layer held-in-topic =====" | tee -a "$LOG"
  python3 pair_contrast.py \
    --model "$model" \
    --data data/pairs_wide.jsonl \
    --layer "$layer" \
    --pool last \
    --held-in-topic \
    --permute 20000 \
    --transfer data/pairs_paraphrase.jsonl \
    2>&1 | tee -a "$LOG" || echo "FAILED $model held-in-topic" | tee -a "$LOG"
}

if [[ "${1:-}" == "--smoke" ]]; then
  echo "smoke: pair_contrast self-check" | tee -a "$LOG"
  python3 pair_contrast.py --self-check 2>&1 | tee -a "$LOG"
  echo "smoke ok — no model loaded" | tee -a "$LOG"
  exit 0
fi

for spec in "${MODELS[@]}"; do
  run_one "$spec"
done

echo "log=$LOG"
echo "held-in-topic is a diagnostic. Not a fifth freeze gate. Do not fill D."
echo "Not a camera. Not handoverPass."
