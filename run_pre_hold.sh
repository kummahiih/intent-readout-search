#!/usr/bin/env bash
# Next fork after P-pre: is there a *local* pair on pre-button h?
# Unique notes only (3 samples share one prompt).
# Reuses forced_act dumps. --h-site pre only. Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

QWEN_MODEL="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL_MODEL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
LOG="results/tests-pre-hold-$(date +%Y-%m-%d).log"
mkdir -p results
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

for f in results/forced_act_qwen.jsonl results/forced_act_mistral.jsonl; do
  if [[ ! -f "$f" ]]; then
    echo "missing $f" >&2
    exit 1
  fi
done

run forced_button.py --act --h-site pre --held-in-topic --permute 200 \
  --from-dump results/forced_act_qwen.jsonl \
  --model "$QWEN_MODEL" --layer 8 --dump results/forced_act_pre_hold_qwen.jsonl

run forced_button.py --act --h-site pre --held-in-topic --permute 200 \
  --from-dump results/forced_act_mistral.jsonl \
  --model "$MISTRAL_MODEL" --layer 9 --dump results/forced_act_pre_hold_mistral.jsonl

echo "log=$LOG"
echo "Look for held_inroom / per-topic held_inroom gaps, especially hiking."
echo "Shared LOTO on pre was 0.011. A loud hiking hold would be local-only."
echo "held-in-topic is a log. Not a freeze gate. Do not fill D."
