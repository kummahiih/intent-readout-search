#!/bin/bash
# Plan-action button. YES = send/claim/hide. Read hiking_mixed.
# Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
mkdir -p results

echo "=== QWEN L8 FORCED ACT ==="
python forced_button.py --model "$QWEN" --layer 8 --act \
  --temperature 0.9 --n-samples 3 \
  --dump results/forced_act_qwen.jsonl

echo "=== MISTRAL L9 FORCED ACT ==="
python forced_button.py --model "$MISTRAL" --layer 9 --act \
  --temperature 0.9 --n-samples 3 \
  --dump results/forced_act_mistral.jsonl
