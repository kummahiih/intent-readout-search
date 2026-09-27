#!/bin/bash
# Many room cameras. Read many_r_oracle_held vs many_r_shared_loto.
# Diagonal of the matrix is r_T on its own room. Not r_strat. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"

echo "=== QWEN L8 MANY-R ==="
python pair_many_r.py --model "$QWEN" --layer 8 --permute 20000 \
  --data data/pairs_wide.jsonl --transfer data/pairs_paraphrase.jsonl

echo "=== MISTRAL L9 MANY-R ==="
python pair_many_r.py --model "$MISTRAL" --layer 9 --permute 20000 \
  --data data/pairs_wide.jsonl --transfer data/pairs_paraphrase.jsonl
