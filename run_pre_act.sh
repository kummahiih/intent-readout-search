#!/usr/bin/env bash
# Fit v on pressed YES/NO. Score pre-button h. LOTO rooms.
# Reuse P-act dumps. Look for button_pre_act_loto and hiking gap.
# Qwen hiking may skip (all NO). Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

QWEN_MODEL="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL_MODEL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
LOG="results/tests-pre-act-$(date +%Y-%m-%d).log"
mkdir -p results
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

run forced_button.py --from-dump results/forced_act_qwen.jsonl \
  --model "$QWEN_MODEL" --layer 8 --h-site pre --label act --act \
  --dump results/pre_act_qwen.jsonl

run forced_button.py --from-dump results/forced_act_mistral.jsonl \
  --model "$MISTRAL_MODEL" --layer 9 --h-site pre --label act --act \
  --dump results/pre_act_mistral.jsonl

echo "log=$LOG"
echo "Need button_pre_act_loto gap_yes_minus_no and per-topic hiking."
echo "Not a freeze. Do not fill D."
