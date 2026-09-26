#!/bin/bash
# Layer-8 family. Do not fill D.
# 3: eight-topic LOTO + paraphrase (topic L2).
# 4: v without travel/neighbors.
# 5: v without hiking/invoices; score the rewritten voice file.
set -euo pipefail
cd "$(dirname "$0")"

echo "=== 3 eight-topic layer 8 ==="
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl

echo "=== 4 hold travel,neighbors ==="
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl \
  --hold-topics travel,neighbors

echo "=== 5 hold hiking,invoices; transfer pairs_voice ==="
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_voice.jsonl \
  --hold-topics hiking,invoices
