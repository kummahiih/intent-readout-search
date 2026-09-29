#!/usr/bin/env bash
# New hide-print bank. S is the button under a HIDE instruction, not the pair tag.
# First look at hide_on_hiking=1. If 0, stop — bank is empty.
# Then note_act on the HIDE arm only.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
LOG="results/tests-hide-bank-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"

run hide_bank.py --model "$QWEN" --arm both --n-samples 2 \
  --dump results/hide_bank_qwen.jsonl
run note_act.py --model "$QWEN" --layer 8 \
  --from-dump results/hide_bank_qwen.jsonl --arm hide

run hide_bank.py --model "$MISTRAL" --arm both --n-samples 2 \
  --dump results/hide_bank_mistral.jsonl
run note_act.py --model "$MISTRAL" --layer 9 \
  --from-dump results/hide_bank_mistral.jsonl --arm hide

if [[ -d models/gemma-3-4b-it ]]; then
  run hide_bank.py --model models/gemma-3-4b-it --arm both --n-samples 2 \
    --dump results/hide_bank_gemma.jsonl
  run note_act.py --model models/gemma-3-4b-it --layer 10 \
    --from-dump results/hide_bank_gemma.jsonl --arm hide
fi

echo "log=$LOG"
echo "Need hide_on_hiking=1 on HIDE arm. Low agree_assigned is the point."
echo "Do not fill D."
