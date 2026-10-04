#!/usr/bin/env bash
# Matched pre-button patch. Qwen L8 and Mistral L9 only.
# delta P(YES) on the HIDE arm. Hiking stays in. Not a handover. Do not fill D.
set -u
cd "$(dirname "$0")"
LOG="results/tests-pre-patch-$(date +%Y-%m-%d-%H%M).log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1
echo "log=$LOG"

QWEN="${QWEN:-models/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL:-models/Mistral-7B-Instruct-v0.3}"
if [ ! -f "$QWEN/config.json" ]; then
  QWEN=/media/pauli/datapata/hf/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/a09a35458c702b33eeacc393d103063234e8bc28
fi
if [ ! -f "$MISTRAL/config.json" ]; then
  MISTRAL=/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71
fi

python pre_patch.py --model "$QWEN" --layer 8 --dump results/pre_patch_qwen.jsonl \
  || echo "FAIL qwen"
python pre_patch.py --model "$MISTRAL" --layer 9 --dump results/pre_patch_mistral.jsonl \
  || echo "FAIL mistral"
echo "Near-zero delta is not a handover. Do not fill D."
