#!/bin/bash
# The 8-topic layer-8 gap/transfer is already logged from photos.
# This rerun exists only to print topic_loo_l2_on_scalar and m_hat_fit_*.
# Do not fill D.
set -euo pipefail
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
