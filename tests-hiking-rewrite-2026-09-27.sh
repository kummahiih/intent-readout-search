#!/bin/bash
# Hiking notes rewritten: less shared trail nouns.
# Fit wide, transfer paraphrase and 8-topic frame. Qwen L8 / Mistral L9 last-token.
# Read hiking LOTO gap, 8-way transfer, topic L2. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="Qwen/Qwen2.5-7B-Instruct"
MISTRAL="${MISTRAL_MODEL:-mistralai/Mistral-7B-Instruct-v0.3}"

run () {
  local model="$1" layer="$2" tag="$3" xfer="$4"
  echo "=== $tag HIKING-REWRITE transfer=$xfer ==="
  python pair_contrast.py --model "$model" --layer "$layer" --pool last \
    --permute 20000 --data data/pairs_wide.jsonl --transfer "$xfer"
}

run "$QWEN" 8 QWEN data/pairs_paraphrase.jsonl
run "$QWEN" 8 QWEN data/pairs_frame.jsonl
run "$MISTRAL" 9 MISTRAL data/pairs_paraphrase.jsonl
run "$MISTRAL" 9 MISTRAL data/pairs_frame.jsonl
