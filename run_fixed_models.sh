#!/usr/bin/env bash
# run_fixed_models.sh — PROVISIONAL rerun of only the 4 models whose runs failed on 2026-11-02:
#   granite-4.2-8b, Qwen3.5-9B (no-think template + reasoning-stripping parser),
#   Phi-4-mini-instruct (native load fallback), LFM2.5-8B-A1B (fp32 CPU-offload fallback).
# DOES: on each model, isolated (one failure does not stop the rest):
#   - provisional defect bank, --incentive-in-user (as gap_filler)
#   - framed original banks: user_says (--role-frame user-says), agent_stakes (--role-frame agent-stakes)
#   - text baselines per dump when sklearn is present.
#   A 1-scenario smoke per model first; if the smoke has 0 valid YES/NO buttons, that model is skipped (logged).
# Env: NEW_TOKENS (default 256, room for a final answer if a template ignores no-think),
#      RH_GPU_MAX_MEM (default 10GiB), RH_CPU_MAX_MEM (default 48GiB) for the offload fallback.
# DOES NOT: change banks or contract semantics, fit readouts, claim a camera or handoverPass,
#   fill D, freeze r, change the negative handover, or commit.
# Banks are provisional, not the confirmatory bank. GPU path untested at commit time.
set -uo pipefail
cd "$(dirname "$0")"
OUT=results/fixed_models_$(date +%Y%m%d_%H%M); mkdir -p "$OUT"; LOG=$OUT/run.log
exec > >(tee -a "$LOG") 2>&1
NEW_TOKENS=${NEW_TOKENS:-256}
# Remote-code modules need a writable cache; 2026-11-02 Phi-4 failed on an unwritable /media/pauli/datapata.
export HF_MODULES_CACHE=${HF_MODULES_CACHE:-$PWD/.hf_modules_cache}; mkdir -p "$HF_MODULES_CACHE"
WANT_FILTER=${WANT_FILTER:-.}
echo "HF_MODULES_CACHE=$HF_MODULES_CACHE WANT_FILTER=$WANT_FILTER"
echo "=== start $(date -Is) $(git rev-parse --short HEAD 2>/dev/null) NEW_TOKENS=$NEW_TOKENS ==="
python -c "import torch,transformers;print('torch',torch.__version__,'transformers',transformers.__version__,'cuda',torch.cuda.is_available())" || { echo "FAIL deps"; exit 2; }
python -c "import sklearn" 2>/dev/null && HAS_SK=1 || { HAS_SK=0; echo "WARN sklearn missing: baselines skipped"; }
python tests/test_final_button.py >/dev/null || { echo "FAIL parser tests"; exit 2; }
declare -A BANK=([defect]=data/prereg/scenarios_defect_bank_provisional.jsonl
                 [user_says]=data/prereg/scenarios_original_user_says.jsonl
                 [agent_stakes]=data/prereg/scenarios_original_agent_stakes.jsonl)
declare -A ARGS=([defect]="--incentive-in-user" [user_says]="--role-frame user-says" [agent_stakes]="--role-frame agent-stakes")
for k in defect user_says agent_stakes; do [[ -s ${BANK[$k]} ]] || { echo "FAIL missing ${BANK[$k]}"; exit 2; }; done
WANT=(granite-4.2-8b Qwen3.5-9B Phi-4-mini-instruct LFM2.5-8B-A1B)
ST=()
for name in "${WANT[@]}"; do
  [[ $name =~ $WANT_FILTER ]] || continue
  dir=""; for base in models ../regret-heuristic/models; do [[ -f $base/$name/config.json ]] && { dir=$base/$name; break; }; done
  [[ -n $dir ]] || { echo "SKIP $name: not found"; ST+=("$name: NOT FOUND"); continue; }
  sb=$OUT/smoke_${name}_bank.jsonl
  python -c "import json;[print(l,end='') for l in open('${BANK[defect]}') if json.loads(l)['scenario_id']=='defect-001']" > "$sb"
  echo "--- smoke $name ($(date -Is))"
  if ! python run_scenario.py --model "$dir" --data "$sb" --dump "$OUT/smoke_${name}.jsonl" --incentive-in-user --new-tokens "$NEW_TOKENS" > "$OUT/smoke_${name}.txt" 2>&1; then
    tail -3 "$OUT/smoke_${name}.txt"; echo "FAIL smoke $name (skipping model)"; ST+=("$name: SMOKE FAIL"); continue
  fi
  grep -E "load_attempt|load_failed|load_fallback|loaded=" "$OUT/smoke_${name}.txt" || true
  nvalid=$(python -c "import json;print(sum(json.loads(l)['button'] in('YES','NO') for l in open('$OUT/smoke_${name}.jsonl')))")
  echo "smoke $name valid buttons: $nvalid/18"
  [[ $nvalid -gt 0 ]] || { echo "SKIP $name: smoke all 'other' (no-think not honoured?)"; ST+=("$name: SMOKE ALL OTHER"); continue; }
  for k in defect user_says agent_stakes; do
    tag=${name}__$k; echo "--- $tag ($(date -Is))"
    # shellcheck disable=SC2086
    if python run_scenario.py --model "$dir" --data "${BANK[$k]}" --dump "$OUT/$tag.jsonl" ${ARGS[$k]} --new-tokens "$NEW_TOKENS" > "$OUT/${tag}_summary.txt" 2>&1; then
      tail -4 "$OUT/${tag}_summary.txt"
      [[ $HAS_SK -eq 1 ]] && { python scripts/text_baselines.py --dump "$OUT/$tag.jsonl" --bank "${BANK[$k]}" --out "$OUT/${tag}_text_baselines.json" >/dev/null || echo "WARN baselines failed $tag"; }
      ST+=("$tag: OK")
    else tail -3 "$OUT/${tag}_summary.txt"; echo "FAIL $tag (continuing)"; ST+=("$tag: FAIL"); fi
  done
done
echo "=== done $(date -Is) ==="; for s in "${ST[@]}"; do echo "  $s"; done
echo "Provisional banks, not confirmatory. Not a camera. Not handoverPass. D not filled. r not frozen. Negative handover unchanged."
