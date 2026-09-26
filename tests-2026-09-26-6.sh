#!/bin/bash
# All related layer-8 gates, last-token then SIREN f(1).
# theta not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

run_last () {
  echo "=== LAST $* ==="
  python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
    --permute 20000 "$@"
}

run_siren () {
  echo "=== SIREN $* ==="
  python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool siren \
    --siren-t 1.0 --siren-steps 80 --permute 20000 "$@"
}

run_last --transfer data/pairs_paraphrase.jsonl
run_last --transfer data/pairs_paraphrase.jsonl --hold-topics travel,neighbors
run_last --transfer data/pairs_voice.jsonl --hold-topics hiking,invoices

run_siren --transfer data/pairs_paraphrase.jsonl
run_siren --transfer data/pairs_paraphrase.jsonl --hold-topics travel,neighbors
run_siren --transfer data/pairs_voice.jsonl --hold-topics hiking,invoices

echo "=== SIREN last-layer control ==="
python pair_contrast.py --data data/pairs_wide.jsonl --layer -1 --pool siren \
  --siren-t 1.0 --siren-steps 80 --permute 20000 \
  --transfer data/pairs_paraphrase.jsonl
