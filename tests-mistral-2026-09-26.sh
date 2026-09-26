#!/bin/bash
# Mistral-7B-Instruct-v0.3. Layer 9 ~ Qwen layer 8 depth (9/32 vs 8/28).
# last, kstep (settle), siren f(1). Same files. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

MODEL="${MODEL:-mistralai/Mistral-7B-Instruct-v0.3}"
LAYER="${LAYER:-9}"
K="${KSTEP_K:-8}"

echo "model=$MODEL layer=$LAYER kstep_k=$K"

run () {
  local pool="$1"
  shift
  echo "=== $MODEL L$LAYER pool=$pool $* ==="
  python pair_contrast.py --model "$MODEL" --layer "$LAYER" --pool "$pool" \
    --kstep-k "$K" --siren-t 1.0 --siren-steps 80 --permute 20000 \
    --data data/pairs_wide.jsonl "$@"
}

for POOL in last kstep siren; do
  run "$POOL" --transfer data/pairs_paraphrase.jsonl
  run "$POOL" --transfer data/pairs_paraphrase.jsonl --hold-topics travel,neighbors
  run "$POOL" --transfer data/pairs_voice.jsonl --hold-topics hiking,invoices
done

echo "=== last-layer controls ==="
for POOL in last kstep siren; do
  python pair_contrast.py --model "$MODEL" --layer -1 --pool "$POOL" \
    --kstep-k "$K" --siren-t 1.0 --siren-steps 80 --permute 20000 \
    --data data/pairs_wide.jsonl --transfer data/pairs_paraphrase.jsonl
done
