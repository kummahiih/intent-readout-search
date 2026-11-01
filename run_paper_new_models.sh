#!/usr/bin/env bash
# Paper-depth meters on the newly granted models.
# hide-bank (HIDE/NAME), note->button, pre-button.
# Base (non-instruct) models have no chat template; skip them here.
# MASK official only if datasets/MASK exists.
# Continues on failure. No local paths. HF names only.
set -u
cd "$(dirname "$0")"
mkdir -p results

if [[ "${1:-}" == "--smoke" ]]; then
  echo "smoke: hide_bank self-check (no model)"
  python3 hide_bank.py --self-check || exit 1
  echo "smoke: chat-template probe on instruct models"
  python3 - << 'PY'
from transformers import AutoTokenizer
models = [
    "meta-llama/Llama-3.1-8B-Instruct",
    "google/gemma-2-2b-it",
    "google/gemma-2-9b-it",
]
for m in models:
    tok = AutoTokenizer.from_pretrained(m, trust_remote_code=True)
    tmpl = getattr(tok, "chat_template", None)
    print(f"  {m}: chat_template={'yes' if tmpl else 'NO'}")
    if not tmpl:
        raise SystemExit(1)
print("smoke ok — chat templates present, no weights loaded")
PY
  exit 0
fi

LOG="results/paper-new-models-$(date +%Y-%m-%d).log"
: >"$LOG"

run() {
  echo "===== $* =====" | tee -a "$LOG"
  python3 "$@" 2>&1 | tee -a "$LOG" || echo "FAILED $*" | tee -a "$LOG"
}

# name|hf-id|layer  (instruct / chat models only)
SPECS=(
  "llama8it|meta-llama/Llama-3.1-8B-Instruct|8"
  "gemma2bit|google/gemma-2-2b-it|8"
  "gemma9bit|google/gemma-2-9b-it|10"
)

for spec in "${SPECS[@]}"; do
  name=${spec%%|*}
  rest=${spec#*|}
  model=${rest%|*}
  layer=${rest##*|}
  dump="results/hide_bank_${name}.jsonl"
  echo "===== hide-bank $name $model layer=$layer =====" | tee -a "$LOG"
  if ! python3 hide_bank.py --model "$model" --arm both --n-samples 2 \
      --data data/pairs_wide.jsonl --dump "$dump" 2>&1 | tee -a "$LOG"; then
    echo "FAILED hide_bank $name" | tee -a "$LOG"
    continue
  fi
  run note_act.py --model "$model" --layer "$layer" \
    --from-dump "$dump" --arm hide
  run forced_button.py --model "$model" --layer "$layer" --act \
    --from-dump "$dump" --h-site pre --label act \
    --dump "results/hide_bank_${name}_pre.jsonl"
done

if [[ -d datasets/MASK ]]; then
  echo "===== MASK official =====" | tee -a "$LOG"
  for spec in "${SPECS[@]}"; do
    name=${spec%%|*}
    rest=${spec#*|}
    model=${rest%|*}
    dump="results/mask_official_${name}.jsonl"
    run mask_official.py --model "$model" --data datasets/MASK \
      --limit 1000 --dump "$dump"
  done
else
  echo "SKIP MASK official: datasets/MASK not present" | tee -a "$LOG"
fi

echo "log=$LOG"
echo "Read HIDE YES, NAME YES, note->button, pre->button. Do not average."
echo "A YES without the fact is a miss, not a cover."
echo "Not a camera. Not handoverPass. Do not fill D."
