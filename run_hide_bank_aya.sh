#!/usr/bin/env bash
# Branch 2: Aya-expanse-8B on the crossed hide bank only.
# Need hide_on_hiking and frac_yes on HIDE vs NAME. Fourth bar, not a freeze.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
LOG="results/tests-hide-bank-aya-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

AYA="${AYA_MODEL:-models/aya-expanse-8b}"
if [[ ! -d "$AYA" ]]; then
  echo "ERROR: missing $AYA. Accept https://huggingface.co/CohereLabs/aya-expanse-8b"
  exit 1
fi
if [[ ! -f "$AYA/tokenizer.json" ]]; then
  echo "ERROR: $AYA/tokenizer.json missing. Re-download after Hub agree."
  exit 1
fi

run hide_bank.py --model "$AYA" --arm both --n-samples 2 \
  --dump results/hide_bank_aya.jsonl
run note_act.py --model "$AYA" --layer 10 \
  --from-dump results/hide_bank_aya.jsonl --arm hide

echo "log=$LOG"
echo "Bar is HIDE frac_yes vs NAME refuse. Not honesty. Do not fill D."
