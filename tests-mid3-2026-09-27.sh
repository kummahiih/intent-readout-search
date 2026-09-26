#!/bin/bash
# mid3 = unit-sum(last, kstep, siren f(1)). Same gates, two models.
# Qwen is pinned. Mistral path must be set if not in the HF cache.
# Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

QWEN="Qwen/Qwen2.5-7B-Instruct"
MISTRAL="${MISTRAL_MODEL:-mistralai/Mistral-7B-Instruct-v0.3}"

run () {
  local model="$1" layer="$2" tag="$3"
  shift 3
  echo "=== mid3 $tag model=$model L$layer $* ==="
  python pair_contrast.py --model "$model" --layer "$layer" --pool mid3 \
    --kstep-k 8 --siren-t 1.0 --siren-steps 80 --permute 20000 \
    --data data/pairs_wide.jsonl "$@"
}

echo "Qwen=$QWEN"
echo "Mistral=$MISTRAL"

run "$QWEN" 8 qwen --transfer data/pairs_paraphrase.jsonl
run "$QWEN" 8 qwen --transfer data/pairs_paraphrase.jsonl --hold-topics travel,neighbors
run "$QWEN" 8 qwen --transfer data/pairs_voice.jsonl --hold-topics hiking,invoices
run "$QWEN" -1 qwen-last --transfer data/pairs_paraphrase.jsonl

run "$MISTRAL" 9 mistral --transfer data/pairs_paraphrase.jsonl
run "$MISTRAL" 9 mistral --transfer data/pairs_paraphrase.jsonl --hold-topics travel,neighbors
run "$MISTRAL" 9 mistral --transfer data/pairs_voice.jsonl --hold-topics hiking,invoices
run "$MISTRAL" -1 mistral-last --transfer data/pairs_paraphrase.jsonl
