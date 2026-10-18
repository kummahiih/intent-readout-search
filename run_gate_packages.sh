#!/usr/bin/env bash
# Score the four statistical gates under packages A, B, and C.
# SCORES is a JSONL with scenario_id, topic, y, pred,
# and optional paraphrase_of, topic_pred, loto_pred, score.
# Not a camera. Do not fill D. Do not freeze r.
set -u
cd "$(dirname "$0")"

SCORES="${SCORES:?set SCORES to a probe-scores JSONL}"
STAMP="$(date +%Y-%m-%d-%H%M)"
LOG="results/gate-packages-${STAMP}.log"
mkdir -p results
exec > >(tee -a "$LOG") 2>&1

echo "log=$LOG scores=$SCORES"
echo "gate packages. not a camera. Do not fill D."
python3 gate_packages.py --scores "$SCORES"
echo "done. not a camera. not handoverPass. Do not fill D."
