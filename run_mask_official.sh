#!/usr/bin/env bash
# Official MASK public rows, belief vs pressure, every local Transformers walk.
# Not the paper judge. Not a cover rate. Not a camera. Do not fill D.
# Skips: Bespoke-Nimble (adapter), Bonsai GGUF, LFM2.5 (12GB 4-bit miss).
# ONLY=qwen,mistral skips the rest. FORCE=1 reruns a finished dump.
set -u
cd "$(dirname "$0")"
mkdir -p results
LOG="results/tests-mask-official-$(date +%Y-%m-%d-%H%M).log"
: >"$LOG"
HF="${HF_HUB:-/media/pauli/datapata/hf/hub}"
DATA="${MASK_DATA:-datasets/MASK}"
LIMIT="${LIMIT:-1000}"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
  return "${PIPESTATUS[0]}"
}

first_dir() {
  local c
  for c in "$@"; do
    [[ -d "$c" ]] || continue
    echo "$c"
    return 0
  done
  return 1
}

qwen=$(first_dir models/Qwen2.5-7B-Instruct \
  "$HF"/models--Qwen--Qwen2.5-7B-Instruct/snapshots/*) || true
mistral=$(first_dir models/Mistral-7B-Instruct-v0.3 \
  "$HF"/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/*) || true
aya=$(first_dir models/aya-expanse-8b) || true
gemma=$(first_dir models/gemma-3-4b-it) || true
falcon=$(first_dir models/Falcon3-7B-Instruct) || true
phi=$(first_dir models/Phi-4-mini-instruct) || true
granite=$(first_dir models/granite-4.2-8b) || true
qwen35=$(first_dir models/Qwen3.5-9B) || true

SPECS=(
  "qwen|${qwen}"
  "mistral|${mistral}"
  "aya8|${aya}"
  "gemma3|${gemma}"
  "falcon3|${falcon}"
  "phi4|${phi}"
  "granite|${granite}"
  "qwen35|${qwen35}"
)

want="${ONLY:-}"
for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  path=${spec#*|}
  if [[ -n "$want" && ",${want}," != *",${name},"* ]]; then
    echo "SKIP $name: not in ONLY=$want" | tee -a "$LOG"
    continue
  fi
  dump="results/mask_official_${name}.jsonl"
  if [[ -s "$dump" && "${FORCE:-}" != "1" ]]; then
    echo "SKIP $name: $dump exists. FORCE=1 to rerun." | tee -a "$LOG"
    continue
  fi
  if [[ -z "$path" || ! -d "$path" ]]; then
    echo "SKIP $name: no folder" | tee -a "$LOG"
    continue
  fi
  echo "USE $name path=$path" | tee -a "$LOG"
  run mask_official.py --model "$path" --data "$DATA" --limit "$LIMIT" \
    --dump "$dump" || echo "FAIL $name" | tee -a "$LOG"
done

python mask_official_chart.py | tee -a "$LOG" || true
echo "log=$LOG"
echo "Read accuracy and lie_given_known. Not the paper P(Lie). Do not fill D."
