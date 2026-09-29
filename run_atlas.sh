#!/usr/bin/env bash
# Atlas: note last-token h, free-text reply_kind as the label.
# Reuses construct_kind_exec dumps. No new generation.
# Kind not in L. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

QWEN_MODEL="${QWEN_MODEL:-Qwen/Qwen2.5-7B-Instruct}"
MISTRAL_MODEL="${MISTRAL_MODEL:-/media/pauli/datapata/hf/hub/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71}"
LOG="results/tests-atlas-$(date +%Y-%m-%d).log"
mkdir -p results
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

for f in results/construct_kind_exec_qwen.jsonl results/construct_kind_exec_mistral.jsonl; do
  if [[ ! -f "$f" ]]; then
    echo "missing $f — run construct_kind --execute first" >&2
    exit 1
  fi
done

run construct_atlas.py --from-jsonl results/construct_kind_exec_qwen.jsonl \
  --model "$QWEN_MODEL" --layer 8 --permute 200

run construct_atlas.py --from-jsonl results/construct_kind_exec_mistral.jsonl \
  --model "$MISTRAL_MODEL" --layer 9 --permute 200

echo "log=$LOG"
echo "Look for atlas_tag_loto vs atlas_kind_loto and hiking_kinds."
echo "Kind-fit rooms skip if a topic has no truth/contradict pair."
echo "Not a freeze gate. Do not fill D."
