#!/usr/bin/env bash
# Intentional-absence check: original bank vs reworded compression control.
# Diagnostic only. Not a camera. Do not fill D. Do not freeze r.
set -u
cd "$(dirname "$0")"

STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/intentional-absence-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1

echo "log=$LOG"
echo "intentional absence check. not a camera. Do not fill D."
echo

python3 intentional_absence_check.py \
  --data data/scenarios_all.jsonl \
  --control data/scenarios_reworded_control.jsonl

echo
echo "done. diagnostic only. not a camera. not handoverPass. Do not fill D."
