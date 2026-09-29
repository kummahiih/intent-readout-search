#!/usr/bin/env bash
# Independent S = hide button on --act dumps. h = desk-note last token.
# Look for note_act_loto gap_yes_minus_no and topic=hiking.
# Qwen hiking may skip (no YES). Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
LOG="results/tests-note-act-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

QWEN="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"

[[ -f results/forced_act_qwen.jsonl ]] && run note_act.py --model "$QWEN" --layer 8 --from-dump results/forced_act_qwen.jsonl
[[ -f results/forced_act_mistral.jsonl ]] && run note_act.py --model "$MISTRAL" --layer 9 --from-dump results/forced_act_mistral.jsonl
[[ -f results/forced_act_gemma.jsonl ]] && run note_act.py --model models/gemma-3-4b-it --layer 10 --from-dump results/forced_act_gemma.jsonl
[[ -f results/forced_act_falcon.jsonl ]] && run note_act.py --model models/Falcon3-7B-Instruct --layer 8 --from-dump results/forced_act_falcon.jsonl

echo "log=$LOG"
echo "S is the button. Hiking must appear or be skipped explicitly."
echo "Do not fill D."
