#!/bin/bash
# In-room last-token: v_T from T, score travel/neighbors voice.
# Qwen L8 pinned. Mistral via MISTRAL_MODEL.
set -euo pipefail
cd "$(dirname "$0")"

QWEN="Qwen/Qwen2.5-7B-Instruct"
MISTRAL="${MISTRAL_MODEL:-mistralai/Mistral-7B-Instruct-v0.3}"

run () {
  local model="$1" layer="$2" tag="$3" topic="$4"
  echo "=== $tag INROOM VOICE-LOUD topic=$topic ==="
  python pair_contrast.py --model "$model" --layer "$layer" --pool last \
    --in-room --only-topics "$topic" --permute 20000 \
    --data data/pairs_wide.jsonl --transfer data/pairs_voice_loud.jsonl
}

for T in travel neighbors; do
  run "$QWEN" 8 QWEN "$T"
done
for T in travel neighbors; do
  run "$MISTRAL" 9 MISTRAL "$T"
done
