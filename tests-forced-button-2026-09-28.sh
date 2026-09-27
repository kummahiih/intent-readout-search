#!/bin/bash
# Forced YES/NO. True button on this bank is NO. Grade the token.
# Read frac_yes and button_kind_loto vs button_tag_loto. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
mkdir -p results

echo "=== QWEN L8 FORCED BUTTON ==="
python forced_button.py --model "$QWEN" --layer 8 \
  --dump results/forced_button_qwen.jsonl

echo "=== MISTRAL L9 FORCED BUTTON ==="
python forced_button.py --model "$MISTRAL" --layer 9 \
  --dump results/forced_button_mistral.jsonl
