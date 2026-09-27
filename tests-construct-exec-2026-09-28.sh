#!/bin/bash
# Follow the private plan; sample two prints. Fit v on tags; score reply_kind.
# Need a real mix of contradict vs truth. Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
mkdir -p results

echo "=== QWEN L8 CONSTRUCT EXECUTE ==="
python construct_kind.py --model "$QWEN" --layer 8 --execute \
  --temperature 0.8 --n-samples 2 \
  --dump results/construct_kind_exec_qwen.jsonl

echo "=== MISTRAL L9 CONSTRUCT EXECUTE ==="
python construct_kind.py --model "$MISTRAL" --layer 9 --execute \
  --temperature 0.8 --n-samples 2 \
  --dump results/construct_kind_exec_mistral.jsonl
