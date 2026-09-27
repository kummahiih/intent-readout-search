#!/bin/bash
# Cross-model judge. Camera owns v. Walk owns h. Linear map is LOTO.
# Read cross_loto hiking vs travel. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"

run () {
  local cam="$1" cl="$2" wk="$3" wl="$4" tag="$5" xfer="$6"
  echo "=== $tag CROSS-JUDGE transfer=$xfer ==="
  python pair_cross_judge.py \
    --camera "$cam" --camera-layer "$cl" \
    --walk "$wk" --walk-layer "$wl" \
    --permute 20000 \
    --data data/pairs_wide.jsonl --transfer "$xfer"
}

run "$QWEN" 8 "$MISTRAL" 9 QWEN-cam/MISTRAL-walk data/pairs_paraphrase.jsonl
run "$MISTRAL" 9 "$QWEN" 8 MISTRAL-cam/QWEN-walk data/pairs_paraphrase.jsonl
