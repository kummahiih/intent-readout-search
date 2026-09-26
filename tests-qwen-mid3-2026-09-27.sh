#!/bin/bash
# Qwen2.5-7B layer 8 mid3 = unit-sum(last, kstep, siren f(1)).
# Ignores leftover MODEL=. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

MODEL="Qwen/Qwen2.5-7B-Instruct"
LAYER="${LAYER:-8}"

echo "model=$MODEL layer=$LAYER pool=mid3"

run () {
  echo "=== QWEN MID3 $* ==="
  python pair_contrast.py --model "$MODEL" --layer "$LAYER" --pool mid3 \
    --kstep-k 8 --siren-t 1.0 --siren-steps 80 --permute 20000 \
    --data data/pairs_wide.jsonl "$@"
}

run --transfer data/pairs_paraphrase.jsonl
run --transfer data/pairs_paraphrase.jsonl --hold-topics travel,neighbors
run --transfer data/pairs_voice.jsonl --hold-topics hiking,invoices

echo "=== QWEN MID3 last-layer control ==="
python pair_contrast.py --model "$MODEL" --layer -1 --pool mid3 \
  --kstep-k 8 --siren-t 1.0 --siren-steps 80 --permute 20000 \
  --data data/pairs_wide.jsonl --transfer data/pairs_paraphrase.jsonl
