#!/usr/bin/env bash
# run_overnight_paper_tests.sh — PROVISIONAL overnight run on the defect/recall bank.
#
# DOES:
#   0. Preflight: checks python deps (torch, transformers; sklearn optional), the bank file, and the Qwen model dir.
#   1. Smokes (all must pass before any full run):
#      - defect-001, user-turn
#      - defect-001, user-says framing
#      - defect-001, agent-stakes framing
#      Each is 6 rows / 18 generations, Qwen only. Exits non-zero on crash, wrong line count, or bad button.
#   2. Full bank (72 IDs, 432 rows, 1296 generations per model), incentive in the user turn:
#      Qwen2.5-7B-Instruct; then gemma-2-9b-it if ../regret-heuristic/models/gemma-2-9b-it exists, else a SKIP line.
#   3. Visible-text baselines per model (if sklearn is present): note-only and note+public_ask, against realized public button and
#      assigned incentive; model family selected on the fit split only, scored on eval.
#      If sklearn is missing, baselines are skipped with a log line (install with: pip install scikit-learn).
#   4. Everything under results/overnight_YYYYMMDD/, one tee'd log (overnight.log).
# DOES NOT:
#   fit residual-stream readouts, extract activations, claim a camera or handoverPass, fill D, freeze r,
#   change the negative handover, or commit anything.
set -euo pipefail
cd "$(dirname "$0")"
BANK=data/prereg/scenarios_defect_bank_provisional.jsonl
QWEN=../regret-heuristic/models/Qwen2.5-7B-Instruct
GEMMA=../regret-heuristic/models/gemma-2-9b-it
OUT=results/overnight_$(date +%Y%m%d)
mkdir -p "$OUT"; LOG=$OUT/overnight.log
exec > >(tee -a "$LOG") 2>&1
echo "=== start $(date -Is) ==="; git rev-parse HEAD || true

echo "--- preflight"
python -c "import torch,transformers;print('torch',torch.__version__,'cuda',torch.cuda.is_available())"
HAS_SKLEARN=1
python -c "import sklearn" 2>/dev/null || { echo "WARN: sklearn missing; text baselines will be skipped (pip install scikit-learn)"; HAS_SKLEARN=0; }
for f in "$BANK" run_scenario.py forced_button.py scripts/text_baselines.py; do [[ -s $f ]] || { echo "FAIL missing $f"; exit 2; }; done
[[ -d $QWEN ]] || { echo "FAIL missing model dir $QWEN"; exit 2; }
echo "bank rows: $(wc -l < "$BANK")"

smoke () {  # label extra-args
  local label=$1; shift
  echo "--- smoke: $label"
  local smoke_bank=$OUT/smoke_${label}_bank.jsonl
  python -c "import json,sys;[print(l,end='') for l in open('$BANK') if json.loads(l)['scenario_id']=='defect-001']" > "$smoke_bank"
  [[ $(wc -l < "$smoke_bank") -eq 6 ]] || { echo "FAIL smoke subset is not 6 rows"; exit 3; }
  python run_scenario.py --model "$QWEN" --data "$smoke_bank" --dump "$OUT/smoke_${label}_qwen.jsonl" "$@"
  python - "$OUT/smoke_${label}_qwen.jsonl" <<'PY'
import json,sys
R=[json.loads(l) for l in open(sys.argv[1])]
assert len(R)==18,f"smoke dump has {len(R)} lines, want 18"
assert all(r["button"] in("YES","NO","other") for r in R),"bad button value"
print("smoke OK; buttons:",{b:sum(r["button"]==b for r in R) for b in("YES","NO","other")})
PY
}

echo "=== all smokes before any full run ==="
smoke user_turn --incentive-in-user
smoke user_says --role-frame user-says
smoke agent_stakes --role-frame agent-stakes
echo "=== all smokes passed; starting full bank ==="

run_model () {  # name dir
  echo "--- full bank: $1 ($(date -Is))"
  python run_scenario.py --model "$2" --data "$BANK" --dump "$OUT/${1}.jsonl" --incentive-in-user | tee "$OUT/${1}_summary.txt"
  if [[ $HAS_SKLEARN -eq 1 ]]; then
    echo "--- text baselines: $1"
    python scripts/text_baselines.py --dump "$OUT/${1}.jsonl" --bank "$BANK" --out "$OUT/${1}_text_baselines.json"
  else
    echo "SKIP text baselines for $1 (sklearn missing)"
  fi
}
run_model qwen "$QWEN"
if [[ -d $GEMMA ]]; then run_model gemma9b "$GEMMA"; else echo "SKIP gemma-2-9b-it: $GEMMA not found"; fi
echo "=== done $(date -Is). Outputs in $OUT ==="
echo "Not a camera. Not handoverPass. D not filled. r not frozen. No residual readouts fitted."
