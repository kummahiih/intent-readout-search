#!/bin/bash
# P0: within-topic hold. Fit v_T on 2+2, score 1+1. Keep hiking.
# Read held_inroom and held_loto per room. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"

run () {
  local model="$1" layer="$2" tag="$3" xfer="$4"
  echo "=== $tag HELD-IN-TOPIC transfer=$xfer ==="
  python pair_contrast.py --model "$model" --layer "$layer" --pool last \
    --held-in-topic --permute 20000 \
    --data data/pairs_wide.jsonl --transfer "$xfer"
}

run "$QWEN" 8 QWEN data/pairs_paraphrase.jsonl
run "$QWEN" 8 QWEN data/pairs_frame.jsonl
run "$MISTRAL" 9 MISTRAL data/pairs_paraphrase.jsonl
run "$MISTRAL" 9 MISTRAL data/pairs_frame.jsonl
