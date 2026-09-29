#!/usr/bin/env bash
# Wave 1 gates on one local walk. CUDA required.
# Usage: bash wave1_run.sh gemma|falcon|aya [layer]
set -euo pipefail
cd "$(dirname "$0")"

KIND=${1:-}
LAYER_OVERRIDE=${2:-}
DATE=$(date +%Y-%m-%d)

case "$KIND" in
  gemma)
    MODEL=models/gemma-3-4b-it
    LAYER=${LAYER_OVERRIDE:-10}
    TAG=gemma
    ;;
  falcon)
    MODEL=models/Falcon3-7B-Instruct
    LAYER=${LAYER_OVERRIDE:-8}
    TAG=falcon
    ;;
  aya)
    MODEL=models/aya-expanse-8b
    LAYER=${LAYER_OVERRIDE:-10}
    TAG=aya
    ;;
  *)
    echo "usage: bash wave1_run.sh gemma|falcon|aya [layer]" >&2
    exit 2
    ;;
esac

if [[ ! -d $MODEL ]]; then
  echo "ERROR: missing $MODEL (gitignored weights). Run get-models.sh on the walk box." >&2
  exit 1
fi

python wave1_layers.py
LOG=results/tests-wave1-${TAG}-L${LAYER}-${DATE}.log
DUMP=results/forced_act_${TAG}.jsonl

{
  echo "wave1 tag=$TAG model=$MODEL layer=$LAYER"
  echo "Do not freeze r. Do not fill D. Kind not in L. Keep hiking."
  echo "=== pair_contrast note last-token LOTO + held_inroom ==="
  python pair_contrast.py --model "$MODEL" --data data/pairs_wide.jsonl \
    --layer "$LAYER" --pool last --held-in-topic --permute 20000 \
    --transfer data/pairs_paraphrase.jsonl
  echo "=== forced_button --act generate ==="
  python forced_button.py --model "$MODEL" --data data/pairs_wide.jsonl \
    --layer "$LAYER" --act --h-site print --label tag \
    --dump "$DUMP"
  echo "=== forced_button pre --label act (reuse dump) ==="
  python forced_button.py --model "$MODEL" --data data/pairs_wide.jsonl \
    --layer "$LAYER" --act --from-dump "$DUMP" \
    --h-site pre --label act --held-in-topic --permute 20000 \
    --dump "results/pre_act_${TAG}.jsonl"
  echo "wave1 done tag=$TAG layer=$LAYER"
  echo "A 0.10 note gap is not a pass. Hiking must stay in the chart."
} 2>&1 | tee "$LOG"

echo "log=$LOG dump=$DUMP"
