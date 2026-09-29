#!/usr/bin/env bash
# Fixed Bailey pass. In-place wipe on stored hidden_states[layer].
# Require instrument=ok (s_wipe collapsed) before reading wipe_kind_keep.
# Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

QWEN_MODEL="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL_MODEL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
LOG="results/tests-bailey-fix-$(date +%Y-%m-%d).log"
mkdir -p results
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

run bailey_tax.py --model "$QWEN_MODEL" --layer 8 --alpha 1.0
run bailey_tax.py --model "$MISTRAL_MODEL" --layer 9 --alpha 1.0

echo "log=$LOG"
echo "Need instrument=ok on both models."
echo "Then wipe_kind_keep / hiking_wipe_keep / s_v_mean wipe."
echo "Not a freeze. Do not fill D."
