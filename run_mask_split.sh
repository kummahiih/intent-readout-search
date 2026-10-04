#!/usr/bin/env bash
# MASK split on the button bank. One run.
# Three logs: P(B=T), P(S_HIDE != B | B had the fact), P(YES|HIDE).
# HIDE and NAME stay separate columns. Pre-button h is a diagnostic.
# Not honesty. Not a gate. Do not fill D.
set -euo pipefail
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

# name:path:layer. Skip a missing folder. Phi-4 stays out (LossKwargs).
MODELS=(
  "qwen:models/Qwen2.5-7B-Instruct:8"
  "mistral:models/Mistral-7B-Instruct-v0.3:9"
  "aya8:models/aya-expanse-8b:10"
  "gemma3:models/gemma-3-4b-it:8"
  "falcon3:models/Falcon3-7B-Instruct:8"
)

for spec in "${MODELS[@]}"; do
  name=${spec%%:*}
  rest=${spec#*:}
  path=${rest%:*}
  layer=${rest##*:}
  if [[ ! -d "$path" ]]; then
    echo "SKIP missing $path" | tee -a "$LOG"
    continue
  fi
  dump="results/mask_split_${name}.jsonl"
  run hide_bank.py --model "$path" --arm three --n-samples 2 \
    --data data/pairs_wide.jsonl --dump "$dump"
  run note_act.py --model "$path" --layer "$layer" \
    --from-dump "$dump" --arm hide
  run forced_button.py --model "$path" --layer "$layer" --act \
    --from-dump "$dump" --h-site pre --label act \
    --dump "results/mask_split_${name}_pre.jsonl"
done

echo "log=$LOG"
echo "Read accuracy, lie_given_known, cover. Do not average them."
echo "A YES without the fact is a miss, not a cover."
echo "pre-button is not a handover. Do not fill D."
