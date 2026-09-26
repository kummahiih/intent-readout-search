#!/bin/bash
# Fit v on the six older rooms. Score travel/neighbors as OOD.
# Do not fill D.
set -euo pipefail
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl \
  --hold-topics travel,neighbors
