#!/usr/bin/env bash
# Score note-only and note+public_ask text baselines on existing button dumps.
# Not a camera. Not handoverPass. Do not fill D.
set -euo pipefail
cd "$(dirname "$0")"

OUT=results/text_baselines_$(date +%Y%m%d)
mkdir -p "$OUT"
LOG=$OUT/baselines.log
exec > >(tee -a "$LOG") 2>&1

python -c "import sklearn" 2>/dev/null || { echo "FAIL: pip install scikit-learn"; exit 2; }

BANK_DEFECT=data/prereg/scenarios_defect_bank_provisional.jsonl
BANK_ORIG=data/scenarios_all.jsonl

score () {  # dump bank label
  local dump=$1 bank=$2 label=$3
  [[ -s $dump ]] || { echo "SKIP $label: $dump missing"; return 0; }
  echo "=== $label ==="
  python scripts/text_baselines.py --dump "$dump" --bank "$bank" --out "$OUT/${label}.json"
}

# Defect bank dumps
score results/gap_filler_20261102_0141/Qwen2.5-7B-Instruct.jsonl "$BANK_DEFECT" qwen25_defect
score results/gap_filler_20261102_0141/Qwen3.5-9B.jsonl "$BANK_DEFECT" qwen35_defect
score results/overnight_20261102/qwen.jsonl "$BANK_DEFECT" qwen_overnight_defect

# Original / framed dumps (if present)
for d in results/framed_original_*/*user_says*.jsonl results/framed_original_*/*agent_stakes*.jsonl; do
  [[ -s $d ]] || continue
  label=$(basename "$d" .jsonl | tr / _)
  score "$d" "$BANK_ORIG" "$label"
done

echo "=== done. Outputs in $OUT ==="
echo "Not a camera. Not handoverPass. D not filled."
