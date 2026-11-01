#!/usr/bin/env bash
# Complementary run. Only the step that failed: pressure rows.
# MASK split, multi-r, bailey, cross-judge already logged.
set -u
cd "$(dirname "$0")"
mkdir -p results data
LOG="results/pressure-rows-new-models-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

SPECS=(
  "llama8it|meta-llama/Llama-3.1-8B-Instruct"
  "gemma2bit|google/gemma-2-2b-it"
  "gemma9bit|google/gemma-2-9b-it"
)

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  model=${spec#*|}
  run make_pressure_rows.py --model "$model" --n 100 --source "$name" \
    --dump "data/pressure_rows_${name}.jsonl"
done

echo "log=$LOG"
echo "Items, not buttons. Not honesty. Do not fill D."
