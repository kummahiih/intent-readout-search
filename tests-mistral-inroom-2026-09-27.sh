#!/bin/bash
# In-room last-token: v_T from T, score T. Not LOTO.
# Mistral layer 9. Set MISTRAL_MODEL to the snapshot.
set -euo pipefail
cd "$(dirname "$0")"

MODEL="${MISTRAL_MODEL:-mistralai/Mistral-7B-Instruct-v0.3}"
LAYER=9

run () {
  local topic="$1" xfer="$2"
  echo "=== MISTRAL INROOM topic=$topic transfer=$xfer ==="
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
