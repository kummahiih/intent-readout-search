#!/usr/bin/env bash
# run_gemma2_9b.sh — gemma-2-9b-it (v1 confirmatory model #2) on the 3 provisional banks:
#   contract run (run_scenario.py, same args as run_fixed_models.sh) + fit-selected text baselines,
#   then SOM/OT diagnostics via run_som_ot_new_banks.sh (MODEL_FILTER on the found dir name).
# Finds the model in $GEMMA_DIR, models/, ../regret-heuristic/models/, or the HF hub cache (any dir with
# config.json whose name matches gemma-2-9b). If none: prints how to download and exits 2.
# DOES NOT change banks or contract semantics, fill D, freeze r, claim a camera or handoverPass,
#   change the negative handover, or commit. Provisional banks, not the confirmatory bank.
# Env: GEMMA_DIR, NEW_TOKENS (default 256), SOM=0 skips SOM/OT, OT=0 passes through.
set -uo pipefail
cd "$(dirname "$0")"
NEW_TOKENS=${NEW_TOKENS:-256}; SOM=${SOM:-1}
export PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}
export HF_MODULES_CACHE=${HF_MODULES_CACHE:-$PWD/.hf_modules_cache}; mkdir -p "$HF_MODULES_CACHE"

find_gemma () {
  local c
  for c in "${GEMMA_DIR:-}" models/gemma-2-9b-it ../regret-heuristic/models/gemma-2-9b-it; do
    [[ -n $c && -f $c/config.json ]] && { echo "$c"; return; }; done
  for c in models/* ../regret-heuristic/models/*; do
    [[ -f $c/config.json && $(basename "$c") =~ [Gg]emma-2-9[Bb] ]] && { echo "$c"; return; }; done
  c=$(ls -d "${HF_HOME:-$HOME/.cache/huggingface}"/hub/models--google--gemma-2-9b-it/snapshots/*/ 2>/dev/null | head -1)
  [[ -n $c && -f $c/config.json ]] && { echo "${c%/}"; return; }
}
MD=$(find_gemma)
if [[ -z $MD ]]; then
  echo "FAIL gemma-2-9b-it not found (GEMMA_DIR, models/, ../regret-heuristic/models/, HF cache)."
  echo "Get it (needs HF login + accepted Gemma license on huggingface.co/google/gemma-2-9b-it):"
  echo "  hf auth login; hf download google/gemma-2-9b-it --local-dir ../regret-heuristic/models/gemma-2-9b-it"
  echo "or point at an existing copy: GEMMA_DIR=/path/to/gemma-2-9b-it bash run_gemma2_9b.sh"
  exit 2
fi
NAME=$(basename "$MD"); [[ $NAME =~ ^[0-9a-f]{40}$ ]] && NAME=gemma-2-9b-it
OUT=results/fixed_models_$(date +%Y%m%d_%H%M); mkdir -p "$OUT"; LOG=$OUT/run.log
exec > >(tee -a "$LOG") 2>&1
echo "=== start $(date -Is) $(git rev-parse --short HEAD 2>/dev/null) model=$MD NEW_TOKENS=$NEW_TOKENS ==="
declare -A BANK=([defect]=data/prereg/scenarios_defect_bank_provisional.jsonl
                 [user_says]=data/prereg/scenarios_original_user_says.jsonl
                 [agent_stakes]=data/prereg/scenarios_original_agent_stakes.jsonl)
declare -A ARGS=([defect]="--incentive-in-user" [user_says]="--role-frame user-says" [agent_stakes]="--role-frame agent-stakes")
HAS_SK=0; python -c "import sklearn" 2>/dev/null && HAS_SK=1
ST=()
for k in defect user_says agent_stakes; do
  tag=${NAME}__$k; echo "--- $tag ($(date -Is))"
  # shellcheck disable=SC2086
  if python run_scenario.py --model "$MD" --data "${BANK[$k]}" --dump "$OUT/$tag.jsonl" ${ARGS[$k]} \
       --new-tokens "$NEW_TOKENS" > "$OUT/${tag}_summary.txt" 2>&1; then
    grep -E "loaded=|rows_in|lie_given_known|other=" "$OUT/${tag}_summary.txt" | tail -4
    [[ $HAS_SK -eq 1 ]] && { python scripts/text_baselines.py --dump "$OUT/$tag.jsonl" --bank "${BANK[$k]}" \
       --out "$OUT/${tag}_text_baselines.json" >/dev/null || echo "WARN baselines failed $tag"; }
    ST+=("$tag: OK")
  else tail -3 "$OUT/${tag}_summary.txt"; echo "FAIL $tag (continuing)"; ST+=("$tag: FAIL"); fi
done
echo "=== contract done $(date -Is) ==="; for s in "${ST[@]}"; do echo "  $s"; done
if [[ $SOM == 1 ]]; then
  if [[ $MD == models/* || $MD == ../regret-heuristic/models/* ]]; then
    MODEL_FILTER="^${NAME}\$" bash run_som_ot_new_banks.sh
  else echo "SKIP SOM/OT: run_som_ot_new_banks.sh only scans models/ and ../regret-heuristic/models/ (model is at $MD)"; fi
fi
echo "Provisional banks. Not a camera. Not handoverPass. D not filled. r not frozen. Negative handover unchanged."
