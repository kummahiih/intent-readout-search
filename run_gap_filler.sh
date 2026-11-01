#!/usr/bin/env bash
# run_gap_filler.sh — fill the gaps from the incomplete overnight run.
#
# Runs every model directory that contains config.json under models/ or
# ../regret-heuristic/models/. Continues to the next model if one fails.
# Smokes first (on Qwen if present). Full bank with incentive in the user turn.
# Text baselines if sklearn is available.
#
# Not a camera. Not handoverPass. Do not fill D. Do not freeze r.
set -uo pipefail
cd "$(dirname "$0")"
BANK=data/prereg/scenarios_defect_bank_provisional.jsonl
OUT=results/gap_filler_$(date +%Y%m%d_%H%M)
mkdir -p "$OUT"
LOG=$OUT/gap_filler.log
exec > >(tee -a "$LOG") 2>&1
echo "=== start $(date -Is) ==="; git rev-parse HEAD || true

echo "--- preflight"
python -c "import torch,transformers;print('torch',torch.__version__,'cuda',torch.cuda.is_available())" || { echo "FAIL deps"; exit 2; }
HAS_SKLEARN=1
python -c "import sklearn" 2>/dev/null || { echo "WARN: no sklearn, baselines skipped"; HAS_SKLEARN=0; }
[[ -s $BANK ]] || { echo "FAIL missing $BANK"; exit 2; }
[[ -s run_scenario.py && -s forced_button.py ]] || { echo "FAIL missing runner scripts"; exit 2; }

# Discover models
MODELS=()
NAMES=()
for base in models ../regret-heuristic/models; do
  [[ -d $base ]] || continue
  for d in "$base"/*; do
    [[ -d $d && -f $d/config.json ]] || continue
    MODELS+=("$d")
    NAMES+=("$(basename "$d")")
  done
done
[[ ${#MODELS[@]} -gt 0 ]] || { echo "FAIL no models found"; exit 2; }
echo "models: ${NAMES[*]}"

# Smoke on Qwen if present, else first
SMOKE_MODEL=${MODELS[0]}
SMOKE_NAME=${NAMES[0]}
for i in "${!NAMES[@]}"; do
  if [[ ${NAMES[$i]} == *Qwen2.5* ]]; then
    SMOKE_MODEL=${MODELS[$i]}
    SMOKE_NAME=${NAMES[$i]}
    break
  fi
done

smoke () {
  local label=$1; shift
  echo "--- smoke $label on $SMOKE_NAME"
  local sb=$OUT/smoke_${label}_bank.jsonl
  python -c "import json;[print(l,end='') for l in open('$BANK') if json.loads(l)['scenario_id']=='defect-001']" > "$sb"
  [[ $(wc -l < "$sb") -eq 6 ]] || { echo "FAIL smoke bank"; return 1; }
  python run_scenario.py --model "$SMOKE_MODEL" --data "$sb" --dump "$OUT/smoke_${label}.jsonl" "$@" || return 1
  python - "$OUT/smoke_${label}.jsonl" <<'PY'
import json,sys
R=[json.loads(l) for l in open(sys.argv[1])]
assert len(R)==18, f"got {len(R)}"
assert all(r["button"] in ("YES","NO","other") for r in R)
print("smoke OK", {b:sum(r["button"]==b for r in R) for b in ("YES","NO","other")})
PY
}

echo "=== smokes ==="
smoke user_turn --incentive-in-user || { echo "smoke user_turn failed"; exit 3; }
smoke user_says --role-frame user-says || { echo "smoke user_says failed"; exit 3; }
smoke agent_stakes --role-frame agent-stakes || { echo "smoke agent_stakes failed"; exit 3; }
echo "=== smokes passed ==="

run_one () {
  local name=$1 dir=$2
  echo "--- full: $name $(date -Is)"
  if python run_scenario.py --model "$dir" --data "$BANK" --dump "$OUT/${name}.jsonl" --incentive-in-user | tee "$OUT/${name}_summary.txt"; then
    if [[ $HAS_SKLEARN -eq 1 ]]; then
      python scripts/text_baselines.py --dump "$OUT/${name}.jsonl" --bank "$BANK" --out "$OUT/${name}_text_baselines.json" || echo "baseline failed for $name"
    fi
    echo "OK $name"
  else
    echo "FAIL $name (continuing)"
  fi
}

for i in "${!MODELS[@]}"; do
  run_one "${NAMES[$i]}" "${MODELS[$i]}"
done

echo "=== done $(date -Is) ==="
echo "Outputs in $OUT"
echo "Not a camera. Not handoverPass. D not filled. r not frozen."
