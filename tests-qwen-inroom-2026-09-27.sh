#!/bin/bash
# In-room last-token: v_T from T, score T. Not LOTO.
# Hiking/invoices vs travel/neighbors. Qwen layer 8 pinned.
set -euo pipefail
cd "$(dirname "$0")"

MODEL="Qwen/Qwen2.5-7B-Instruct"
LAYER=8

run () {
  local topic="$1" xfer="$2"
  echo "=== QWEN INROOM topic=$topic transfer=$xfer ==="
  python pair_contrast.py --model "$MODEL" --layer "$LAYER" --pool last \
    --in-room --only-topics "$topic" --permute 20000 \
    --data data/pairs_wide.jsonl --transfer "$xfer"
}

for T in hiking invoices travel neighbors; do
  run "$T" data/pairs_paraphrase.jsonl
done
for T in hiking invoices; do
  run "$T" data/pairs_voice.jsonl
done
