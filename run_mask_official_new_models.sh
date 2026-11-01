#!/usr/bin/env bash
# Official MASK public rows on the three new instruct models.
# Needs datasets/MASK and pandas. Continues on failure.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/mask-official-new-models-$(date +%Y-%m-%d).log"
: >"$LOG"

if [[ ! -d datasets/MASK ]]; then
  echo "SKIP: datasets/MASK not present" | tee -a "$LOG"
  exit 1
fi

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

run mask_official.py --model meta-llama/Llama-3.1-8B-Instruct \
  --data datasets/MASK --limit 1000 \
  --dump results/mask_official_llama8it.jsonl

run mask_official.py --model google/gemma-2-2b-it \
  --data datasets/MASK --limit 1000 \
  --dump results/mask_official_gemma2bit.jsonl

run mask_official.py --model google/gemma-2-9b-it \
  --data datasets/MASK --limit 1000 \
  --dump results/mask_official_gemma9bit.jsonl

echo "log=$LOG"
echo "Read accuracy and lie_given_known. Not the paper P(Lie). Do not fill D."
