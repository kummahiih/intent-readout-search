#!/usr/bin/env bash
# Elicit two-sided prints (fact-bite YES/NO + follow the plan).
# Look for two_sided_rooms and hiking_kinds.
# If hiking is still all truth, elicitation failed again. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

QWEN_MODEL="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL_MODEL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
LOG="results/tests-elicit-$(date +%Y-%m-%d).log"
mkdir -p results
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

run elicit_kind.py --model "$QWEN_MODEL" --dump results/elicit_kind_qwen.jsonl
run elicit_kind.py --model "$MISTRAL_MODEL" --dump results/elicit_kind_mistral.jsonl

echo "log=$LOG"
echo "Need two_sided_rooms to include hiking before Atlas."
echo "Kind not in L. Do not fill D."
