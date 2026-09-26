#!/bin/bash
# LOTO last-token: v from the other six rooms, score travel/neighbors voice.
# Qwen L8 pinned. Mistral via MISTRAL_MODEL.
set -euo pipefail
cd "$(dirname "$0")"

QWEN="Qwen/Qwen2.5-7B-Instruct"
MISTRAL="${MISTRAL_MODEL:-mistralai/Mistral-7B-Instruct-v0.3}"

run () {
  local model="$1" layer="$2" tag="$3"
  echo "=== $tag LOTO VOICE-LOUD hold=travel,neighbors ==="
  python pair_contrast.py --model "$model" --layer "$layer" --pool last \
    --hold-topics travel,neighbors --permute 20000 \
    --data data/pairs_wide.jsonl --transfer data/pairs_voice_loud.jsonl
}

run "$QWEN" 8 QWEN
run "$MISTRAL" 9 MISTRAL
