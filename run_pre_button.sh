#!/usr/bin/env bash
# Pre-button h: last token of the prompt, not the YES/NO cell.
# Reuses results/forced_act_{qwen,mistral}.jsonl. Does not generate buttons.
# Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

QWEN_MODEL="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL_MODEL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
LOG="results/tests-pre-button-$(date +%Y-%m-%d).log"
mkdir -p results
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

if [[ ! -f results/forced_act_qwen.jsonl ]]; then
  echo "missing results/forced_act_qwen.jsonl" >&2
  exit 1
fi
if [[ ! -f results/forced_act_mistral.jsonl ]]; then
  echo "missing results/forced_act_mistral.jsonl" >&2
  exit 1
fi

run forced_button.py --act --h-site both --from-dump results/forced_act_qwen.jsonl \
  --model "$QWEN_MODEL" --layer 8 --dump results/forced_act_pre_qwen.jsonl

run forced_button.py --act --h-site both --from-dump results/forced_act_mistral.jsonl \
  --model "$MISTRAL_MODEL" --layer 9 --dump results/forced_act_pre_mistral.jsonl

echo "log=$LOG"
echo "Look for button_pre_tag_loto and button_pre_kind_loto vs button_print_*."
echo "pre is plan-plus-question. print is the pressed token. Not a camera."
