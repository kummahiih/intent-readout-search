#!/usr/bin/env bash
# Bailey tax: wipe LOTO v at mid-layer during decode.
# Look for wipe_kind_keep and s_v_mean wipe vs base.
# Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

QWEN_MODEL="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL_MODEL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
LOG="results/tests-bailey-$(date +%Y-%m-%d).log"
mkdir -p results
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

run bailey_tax.py --model "$QWEN_MODEL" --layer 8 --alpha 1.0
run bailey_tax.py --model "$MISTRAL_MODEL" --layer 9 --alpha 1.0

echo "log=$LOG"
echo "wipe_kind_keep near 1 + s_v wipe ~0 => cheap obfuscation of this v."
echo "wipe_kind_keep low => this v is load-bearing for the print."
echo "Not a freeze. Do not fill D."
