#!/usr/bin/env bash
# run_som_ot_new_banks.sh — PROVISIONAL SOM purity + OT room-entry diagnostics on the new banks.
# Mirrors regret-heuristic run_layout_*.sh (SOM, night_sims/som_layout_run.py) and run_ot_all_models.sh
# (OT, night_sims/ot_rooms.py, n=4 samples, tau=0.5), ported to bank rows by scripts/som_ot_bank.py.
# DOES:
#   0. CPU smoke of the analysis on synthetic residuals for all 3 banks (must pass first).
#   1. For every local model (models/ or ../regret-heuristic/models/ with config.json), each isolated:
#      - defect bank (--incentive-in-user), user_says (--role-frame user-says), agent_stakes (--role-frame agent-stakes)
#      - extract last-token residuals at the model's layer (same layers as run_ot_all_models.sh) on the public-arm
#        prompt (built as run_scenario.py builds it, no-think template + loader fallbacks), plus an ask-removed control;
#        OT samples of "Note: {note}" and the empty prompt.
#      - analyze: SOM fit on FIT rows only (centering/PCA/grid chosen on FIT only), purity on EVAL rows
#        (scenario_id split) vs shuffle null; labels incentive, realized public button (joined from the newest
#        existing gap_filler_* / framed_original_* / fixed_models_* dump; 'missing' if none), topic.
#   Output: results/som_ot_YYYYMMDD_HHMM/, one run.log.
# DOES NOT: change banks or contract semantics, gate anything, fill D, freeze r, claim a camera or handoverPass,
#   change the negative handover, or commit. Banks are provisional, not the confirmatory bank.
#   The OT fact-room keyword rule for bank rows is an adaptation (see scripts/som_ot_bank.py header).
# Env: OT=0 skips OT sampling; NSAMP (default 4); MODEL_FILTER (regex on model dir name).
set -uo pipefail
cd "$(dirname "$0")"
OUT=results/som_ot_$(date +%Y%m%d_%H%M); mkdir -p "$OUT"; LOG=$OUT/run.log
exec > >(tee -a "$LOG") 2>&1
echo "=== start $(date -Is) $(git rev-parse --short HEAD 2>/dev/null) ==="
OT=${OT:-1}; NSAMP=${NSAMP:-4}; MODEL_FILTER=${MODEL_FILTER:-.}
declare -A BANK=([defect]=data/prereg/scenarios_defect_bank_provisional.jsonl
                 [user_says]=data/prereg/scenarios_original_user_says.jsonl
                 [agent_stakes]=data/prereg/scenarios_original_agent_stakes.jsonl)
declare -A ARGS=([defect]="--incentive-in-user" [user_says]="--role-frame user-says" [agent_stakes]="--role-frame agent-stakes")
declare -A LAYER=([Qwen2.5-7B-Instruct]=8 [Mistral-7B-Instruct-v0.3]=9 [aya-expanse-8b]=10 [gemma-3-4b-it]=8
                  [Falcon3-7B-Instruct]=8 [granite-4.2-8b]=12 [Qwen3.5-9B]=10)
for k in defect user_says agent_stakes; do [[ -s ${BANK[$k]} ]] || { echo "FAIL missing ${BANK[$k]}"; exit 2; }; done
python -c "import numpy" || { echo "FAIL numpy"; exit 2; }
echo "--- CPU smokes"
for k in defect user_says agent_stakes; do
  python scripts/som_ot_bank.py smoke --data "${BANK[$k]}" | tail -1 | grep -q "smoke OK" || { echo "FAIL smoke $k"; exit 3; }
  echo "smoke $k OK"
done
python -c "import torch,transformers;print('torch',torch.__version__,'transformers',transformers.__version__,'cuda',torch.cuda.is_available())" || { echo "FAIL torch/transformers"; exit 2; }

newest_dump () {  # model key -> newest existing button dump or empty
  local m=$1 k=$2 f
  if [[ $k == defect ]]; then
    f=$(ls -t results/fixed_models_*/"${m}__defect.jsonl" results/gap_filler_*/"${m}.jsonl" 2>/dev/null | head -1)
  else
    f=$(ls -t results/fixed_models_*/"${m}__${k}.jsonl" results/framed_original_*/"${m}__${k}.jsonl" 2>/dev/null | head -1)
  fi
  echo "$f"
}

MODELS=(); NAMES=()
for base in models ../regret-heuristic/models; do [[ -d $base ]] || continue
  for d in "$base"/*; do [[ -f $d/config.json ]] || continue; n=$(basename "$d")
    [[ $n =~ $MODEL_FILTER ]] || continue; MODELS+=("$d"); NAMES+=("$n"); done; done
[[ ${#MODELS[@]} -gt 0 ]] || { echo "FAIL no models"; exit 2; }
echo "models: ${NAMES[*]}"
ST=()
for i in "${!MODELS[@]}"; do
  m=${NAMES[$i]}; L=${LAYER[$m]:-8}
  for k in defect user_says agent_stakes; do
    tag=${m}__$k; echo "--- $tag layer=$L ($(date -Is))"
    otarg=(); [[ $OT == 1 ]] && otarg=(--ot "$OUT/${tag}_ot.jsonl" --n-samples "$NSAMP")
    # shellcheck disable=SC2086
    if python scripts/som_ot_bank.py extract --model "${MODELS[$i]}" --data "${BANK[$k]}" --layer "$L" \
         --out "$OUT/${tag}_h.npz" ${ARGS[$k]} "${otarg[@]}" > "$OUT/${tag}_extract.txt" 2>&1; then
      grep -E "load_attempt|load_failed|load_fallback|loaded=|layer=" "$OUT/${tag}_extract.txt" || true
      bd=$(newest_dump "$m" "$k"); echo "button dump: ${bd:-missing}"
      if python scripts/som_ot_bank.py analyze --data "${BANK[$k]}" --npz "$OUT/${tag}_h.npz" \
           --button-dump "$bd" ${otarg:+--ot "$OUT/${tag}_ot.jsonl"} --out "$OUT/${tag}_som_ot.json" > "$OUT/${tag}_analyze.txt" 2>&1; then
        ST+=("$tag: OK")
      else tail -3 "$OUT/${tag}_analyze.txt"; echo "FAIL analyze $tag"; ST+=("$tag: ANALYZE FAIL"); fi
    else tail -3 "$OUT/${tag}_extract.txt"; echo "FAIL extract $tag (continuing)"; ST+=("$tag: EXTRACT FAIL"); fi
  done
done
echo "=== done $(date -Is) ==="; for s in "${ST[@]}"; do echo "  $s"; done
echo "SOM/OT are diagnostics, not gates. Provisional banks. Not a camera. Not handoverPass. D not filled. r not frozen. Negative handover unchanged."
