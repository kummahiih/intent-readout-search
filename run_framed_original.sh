#!/usr/bin/env bash
# run_framed_original.sh — PROVISIONAL run of the two framed original banks on all local models.
# DOES: 3 smokes on Qwen2.5 (first scenario_id of each bank, with --role-frame user-says / agent-stakes,
#   plus user-says bank with --incentive-in-user); all must pass first. Then full runs:
#   scenarios_original_user_says.jsonl with --role-frame user-says and scenarios_original_agent_stakes.jsonl with
#   --role-frame agent-stakes, on every local model; one model failing does not stop the rest.
#   Text baselines per dump when sklearn is present. Output: results/framed_original_YYYYMMDD/, one log.
# DOES NOT: fit residual readouts, claim a camera or handoverPass, fill D, freeze r, or commit.
set -uo pipefail
cd "$(dirname "$0")"
OUT=results/framed_original_$(date +%Y%m%d); mkdir -p "$OUT"; LOG=$OUT/run.log
exec > >(tee -a "$LOG") 2>&1
echo "=== start $(date -Is) $(git rev-parse --short HEAD) ==="
declare -A BANK=([user_says]=data/prereg/scenarios_original_user_says.jsonl [agent_stakes]=data/prereg/scenarios_original_agent_stakes.jsonl)
declare -A FRAME=([user_says]=user-says [agent_stakes]=agent-stakes)
for b in "${BANK[@]}"; do [[ -s $b ]] || { echo "FAIL missing $b"; exit 2; }; done
python -c "import torch,transformers" || { echo "FAIL torch/transformers"; exit 2; }
python -c "import sklearn" 2>/dev/null && HAS_SK=1 || { HAS_SK=0; echo "WARN sklearn missing: baselines skipped"; }
MODELS=(); NAMES=()
for base in models ../regret-heuristic/models; do [[ -d $base ]] || continue
  for d in "$base"/*; do [[ -f $d/config.json ]] || continue; MODELS+=("$d"); NAMES+=("$(basename "$d")"); done; done
[[ ${#MODELS[@]} -gt 0 ]] || { echo "FAIL no models"; exit 2; }
SM=${MODELS[0]}; for i in "${!NAMES[@]}"; do [[ ${NAMES[$i]} == Qwen2.5* ]] && { SM=${MODELS[$i]}; break; }; done
echo "models: ${NAMES[*]}; smoke model: $SM"
smoke () { # label bankkey args...
  local label=$1 key=$2; shift 2; local sb=$OUT/smoke_${label}_bank.jsonl
  python - "${BANK[$key]}" > "$sb" <<'PY'
import json,sys
R=[json.loads(l) for l in open(sys.argv[1])];sid=R[0]["scenario_id"]
[print(json.dumps(r)) for r in R if r["scenario_id"]==sid]
PY
  local n; n=$(wc -l < "$sb"); echo "--- smoke $label ($n rows)"
  python run_scenario.py --model "$SM" --data "$sb" --dump "$OUT/smoke_${label}.jsonl" "$@" || { echo "FAIL smoke $label"; exit 3; }
  python - "$OUT/smoke_${label}.jsonl" "$n" <<'PY' || { echo "FAIL smoke $label check"; exit 3; }
import json,sys
R=[json.loads(l) for l in open(sys.argv[1])];assert len(R)==3*int(sys.argv[2]),len(R)
assert all(r["button"] in("YES","NO","other") for r in R)
print("smoke OK",{b:sum(r["button"]==b for r in R) for b in("YES","NO","other")})
PY
}
smoke user_says user_says --role-frame user-says
smoke agent_stakes agent_stakes --role-frame agent-stakes
smoke user_turn user_says --incentive-in-user
echo "=== all smokes passed ==="
ST=()
for i in "${!MODELS[@]}"; do for key in user_says agent_stakes; do
  tag=${NAMES[$i]}__$key; echo "--- $tag ($(date -Is))"
  if python run_scenario.py --model "${MODELS[$i]}" --data "${BANK[$key]}" --dump "$OUT/$tag.jsonl" --role-frame "${FRAME[$key]}" > "$OUT/${tag}_summary.txt" 2>&1; then
    tail -5 "$OUT/${tag}_summary.txt"
    [[ $HAS_SK -eq 1 ]] && python scripts/text_baselines.py --dump "$OUT/$tag.jsonl" --bank "${BANK[$key]}" --out "$OUT/${tag}_text_baselines.json" >/dev/null || true
    ST+=("$tag: OK")
  else tail -3 "$OUT/${tag}_summary.txt"; echo "FAIL $tag"; ST+=("$tag: FAIL"); fi
done; done
echo "=== done $(date -Is) ==="; for s in "${ST[@]}"; do echo "  $s"; done
echo "Not a camera. Not handoverPass. D not filled. r not frozen. No residual readouts fitted."
