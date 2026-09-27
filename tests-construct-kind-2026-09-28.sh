#!/bin/bash
# Fit v on assigned tags. Score generated reply_kind.
# Read construct_kind_loto vs construct_tag_loto. Kind is not in L.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
mkdir -p results

echo "=== QWEN L8 CONSTRUCT KIND ==="
python construct_kind.py --model "$QWEN" --layer 8 \
  --dump results/construct_kind_qwen.jsonl

echo "=== MISTRAL L9 CONSTRUCT KIND ==="
python construct_kind.py --model "$MISTRAL" --layer 9 \
  --dump results/construct_kind_mistral.jsonl
