#!/usr/bin/env bash
# MASK split on the button bank. One run.
# Three logs: P(B=T), P(S_HIDE != B | B had the fact), P(YES|HIDE).
# HIDE and NAME stay separate columns. Pre-button h is a diagnostic.
# Not honesty. Not a gate. Do not fill D.
# ONLY=qwen,mistral skips walks already logged.
# Not in this script: Bespoke-Nimble-9B (LoRA, not a chat model),
# Ternary-Bonsai-2-27B-gguf (llama.cpp only).
set -u
cd "$(dirname "$0")"
python -c "import sentencepiece" 2>/dev/null || {
  echo "ERROR: sentencepiece missing (Aya/Gemma tokenizer). Not a camera miss." >&2
  echo "fix: pip install sentencepiece" >&2
  exit 2
}
mkdir -p results
LOG="results/tests-mask-split-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python "$@" 2>&1 | tee -a "$LOG"
}

echo "===== hide_bank.py --self-check =====" | tee -a "$LOG"
python hide_bank.py --self-check 2>&1 | tee -a "$LOG"

HF="${HF_HUB:-/media/pauli/datapata/hf/hub}"
first_dir() {
  local c
  for c in "$@"; do
    [[ -d "$c" ]] || continue
    echo "$c"
    return 0
  done
  return 1
}

qwen=$(first_dir \
  models/Qwen2.5-7B-Instruct \
  "$HF"/models--Qwen--Qwen2.5-7B-Instruct/snapshots/*) || true
mistral=$(first_dir \
  models/Mistral-7B-Instruct-v0.3 \
  "$HF"/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/c170c708c41dac9275d15a8fff4eca08d52bab71 \
  "$HF"/models--mistralai--Mistral-7B-Instruct-v0.3/snapshots/*) || true
aya=$(first_dir models/aya-expanse-8b) || true
gemma=$(first_dir models/gemma-3-4b-it) || true
falcon=$(first_dir models/Falcon3-7B-Instruct) || true
phi=$(first_dir models/Phi-4-mini-instruct) || true
granite=$(first_dir models/granite-4.2-8b \
  "$HF"/models--ibm-granite--granite-4.2-8b/snapshots/*) || true
lfm=$(first_dir models/LFM2.5-8B-A1B \
  "$HF"/models--LiquidAI--LFM2.5-8B-A1B/snapshots/*) || true
qwen35=$(first_dir models/Qwen3.5-9B \
  "$HF"/models--Qwen--Qwen3.5-9B/snapshots/*) || true

# layer is ~0.3 depth, same rule as the 7B rows. Granite has 40 layers.
# Qwen3.5-9B has 32. LFM2.5 has 24. Phi stays the known LossKwargs miss.
SPECS=(
  "qwen|${qwen}|8"
  "mistral|${mistral}|9"
  "aya8|${aya}|10"
  "gemma3|${gemma}|8"
  "falcon3|${falcon}|8"
  "phi4|${phi}|10"
  "granite|${granite}|12"
  "lfm|${lfm}|8"
  "qwen35|${qwen35}|10"
)

want="${ONLY:-}"
for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  path=${rest%|*}
  layer=${rest##*|}
  if [[ -n "$want" && ",${want}," != *",${name},"* ]]; then
    echo "SKIP $name: not in ONLY=$want" | tee -a "$LOG"
    continue
  fi
  if [[ -z "$path" || ! -d "$path" ]]; then
    echo "SKIP $name: no folder. models/ or $HF snapshot." | tee -a "$LOG"
    continue
  fi
  echo "USE $name path=$path layer=$layer" | tee -a "$LOG"
  dump="results/mask_split_${name}.jsonl"
  run hide_bank.py --model "$path" --arm three --n-samples 2 \
    --data data/pairs_wide.jsonl --dump "$dump" || {
      echo "FAIL $name hide_bank" | tee -a "$LOG"
      continue
    }
  run note_act.py --model "$path" --layer "$layer" \
    --from-dump "$dump" --arm hide || echo "FAIL $name note_act" | tee -a "$LOG"
  run forced_button.py --model "$path" --layer "$layer" --act \
    --from-dump "$dump" --h-site pre --label act \
    --dump "results/mask_split_${name}_pre.jsonl" || echo "FAIL $name pre" | tee -a "$LOG"
done

echo "log=$LOG"
echo "Read accuracy, lie_given_known, cover. Do not average them."
echo "A YES without the fact is a miss, not a cover."
echo "pre-button is not a handover. Do not fill D."
