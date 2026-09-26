#!/bin/bash
# Qwen2.5-7B layer 8: K-step settle. Ignores leftover MODEL= from Mistral.
# Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

MODEL="Qwen/Qwen2.5-7B-Instruct"
LAYER="${LAYER:-8}"
K="${KSTEP_K:-8}"

echo "model=$MODEL layer=$LAYER kstep_k=$K"

run () {
  echo "=== QWEN KSTEP $* ==="
  python pair_contrast.py --model "$MODEL" --layer "$LAYER" --pool kstep \
    --kstep-k "$K" --permute 20000 --data data/pairs_wide.jsonl "$@"
}

run --transfer data/pairs_paraphrase.jsonl
run --transfer data/pairs_paraphrase.jsonl --hold-topics travel,neighbors
run --transfer data/pairs_voice.jsonl --hold-topics hiking,invoices

echo "=== QWEN KSTEP last-layer control ==="
python pair_contrast.py --model "$MODEL" --layer -1 --pool kstep \
  --kstep-k "$K" --permute 20000 \
  --data data/pairs_wide.jsonl --transfer data/pairs_paraphrase.jsonl
