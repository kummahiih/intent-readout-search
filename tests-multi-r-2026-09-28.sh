#!/bin/bash
# Three probes: label + topic adversary + corr^2. LOTO.
# Read ensemble hiking vs travel and mean_held_score_corr2.
# Not r_strat. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"

echo "=== QWEN L8 MULTI-R NOTES/TAGS ==="
python pair_multi_r.py --model "$QWEN" --layer 8 --data data/pairs_wide.jsonl

echo "=== QWEN L8 MULTI-R EXEC/KIND ==="
python pair_multi_r.py --model "$QWEN" --layer 8 \
  --from-jsonl results/construct_kind_exec_qwen.jsonl

echo "=== MISTRAL L9 MULTI-R NOTES/TAGS ==="
python pair_multi_r.py --model "$MISTRAL" --layer 9 --data data/pairs_wide.jsonl

echo "=== MISTRAL L9 MULTI-R EXEC/KIND ==="
python pair_multi_r.py --model "$MISTRAL" --layer 9 \
  --from-jsonl results/construct_kind_exec_mistral.jsonl
