#!/usr/bin/env bash
# run_fix_rerun.sh — rerun after the 2026-11-03 audit fixes (results/audit_2026-11-03.md).
# Run from the repo root:  bash run_fix_rerun.sh
#   0. CPU tests (tests/*.py) + SOM smokes. Any failure stops the run.
#   1. Tokenizer-only double-BOS check for gemma-2-9b-it and every other model found.
#   2. gemma-2-9b-it contract rerun on the 3 banks (run_scenario.py, BOS fix) + text baselines (new inputs).
#   3. gemma-2-9b-it SOM/OT at GEMMA_LAYER (default 24 of 42), OT on the chat prompt (--ot-mode chat).
#   4. Other models (OTHER_MODELS): SOM/OT extract with the chat-prompt OT at each model's old layer,
#      analyzed against the newest existing button dump, + text baselines (new inputs) on that dump (CPU).
#      RERUN_CONTRACT=1 also reruns their contract (BOS fix can change templates that start with BOS).
# Resumable: reuse OUT=results/fix_rerun_... ; finished steps leave .done markers and are skipped.
# Missing model dirs are skipped. One model process at a time (fits a 12 GB GPU via the usual loader).
# DOES NOT: change banks or contract semantics, fill D, freeze r, claim a camera or handoverPass,
#   change the negative handover, or commit. Provisional banks.
# Env: HF_HOME (default /run/media/pauli/datapata/hf), MODELS_DIR (default ../regret-heuristic/models),
#   GEMMA (default gemma-2-9b-it), GEMMA_LAYER (24), NEW_TOKENS (256), NSAMP (4), OT=0 skips OT,
#   OT_COMPARE_NOTE=1 adds a note-only OT extract for comparison, SKIP_GEMMA=1, SKIP_OTHERS=1,
#   OTHER_MODELS (space list), MODEL_FILTER (regex on names), RERUN_CONTRACT (0), OUT.
set -uo pipefail
[[ -f run_scenario.py && -f scripts/som_ot_bank.py && -f prompt_text.py ]] || { echo "FAIL run from the intent-readout-search repo root"; exit 2; }
export HF_HOME=${HF_HOME:-/run/media/pauli/datapata/hf}
export PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}
export HF_MODULES_CACHE=${HF_MODULES_CACHE:-$PWD/.hf_modules_cache}; mkdir -p "$HF_MODULES_CACHE"
MODELS_DIR=${MODELS_DIR:-../regret-heuristic/models}
GEMMA=${GEMMA:-gemma-2-9b-it}; GEMMA_LAYER=${GEMMA_LAYER:-24}; NEW_TOKENS=${NEW_TOKENS:-256}; NSAMP=${NSAMP:-4}
OT=${OT:-1}; OT_COMPARE_NOTE=${OT_COMPARE_NOTE:-0}; SKIP_GEMMA=${SKIP_GEMMA:-0}; SKIP_OTHERS=${SKIP_OTHERS:-0}
RERUN_CONTRACT=${RERUN_CONTRACT:-0}; MODEL_FILTER=${MODEL_FILTER:-.}
OTHER_MODELS=${OTHER_MODELS:-"granite-4.2-8b Qwen3.5-9B Phi-4-mini-instruct LFM2.5-8B-A1B Qwen2.5-7B-Instruct Mistral-7B-Instruct-v0.3 aya-expanse-8b gemma-3-4b-it Falcon3-7B-Instruct"}
OUT=${OUT:-results/fix_rerun_$(date +%Y%m%d_%H%M)}; mkdir -p "$OUT"; LOG=$OUT/run.log
exec > >(tee -a "$LOG") 2>&1
echo "=== start $(date -Is) $(git rev-parse --short HEAD 2>/dev/null) dirty=$(git status --porcelain 2>/dev/null | wc -l) OUT=$OUT HF_HOME=$HF_HOME ==="
[[ -d $HF_HOME ]] || echo "WARN HF_HOME $HF_HOME does not exist (drive not mounted?)"
declare -A BANK=([defect]=data/prereg/scenarios_defect_bank_provisional.jsonl
                 [user_says]=data/prereg/scenarios_original_user_says.jsonl
                 [agent_stakes]=data/prereg/scenarios_original_agent_stakes.jsonl)
declare -A ARGS=([defect]="--incentive-in-user" [user_says]="--role-frame user-says" [agent_stakes]="--role-frame agent-stakes")
declare -A LAYER=([Qwen2.5-7B-Instruct]=8 [Mistral-7B-Instruct-v0.3]=9 [aya-expanse-8b]=10 [gemma-3-4b-it]=8
                  [Falcon3-7B-Instruct]=8 [granite-4.2-8b]=12 [Qwen3.5-9B]=10)
ST=()
done_ () { [[ -f $OUT/.done_$1 ]]; }
mark () { touch "$OUT/.done_$1"; }

echo "--- 0. CPU tests"
if ! done_ tests; then
  for t in tests/*.py; do
    python "$t" > "$OUT/test_$(basename "$t" .py).txt" 2>&1 || { tail -20 "$OUT/test_$(basename "$t" .py).txt"; echo "FAIL $t"; exit 3; }
    echo "PASS $t ($(grep -c '^PASS' "$OUT/test_$(basename "$t" .py).txt") checks)"
  done
  for k in defect user_says agent_stakes; do
    python scripts/som_ot_bank.py smoke --data "${BANK[$k]}" | tail -1 | grep -q "smoke OK" || { echo "FAIL smoke $k"; exit 3; }
  done; echo "smokes OK"; mark tests
else echo "skip (done)"; fi
python -c "import torch,transformers;print('torch',torch.__version__,'transformers',transformers.__version__,'cuda',torch.cuda.is_available())" || { echo "FAIL torch/transformers"; exit 2; }
HAS_SK=0; python -c "import sklearn" 2>/dev/null && HAS_SK=1

ALL=()
for n in "$GEMMA" $OTHER_MODELS; do [[ -f $MODELS_DIR/$n/config.json ]] && ALL+=("$MODELS_DIR/$n") || echo "SKIP missing model $MODELS_DIR/$n"; done
echo "--- 1. double-BOS check (tokenizer only)"
if [[ ${#ALL[@]} -gt 0 ]]; then python scripts/bos_check.py --model "${ALL[@]}" | tee "$OUT/bos_check.txt"; fi

newest_dump () {  # old button dump for model $1 bank $2 (not from this OUT)
  local m=$1 k=$2
  if [[ $k == defect ]]; then ls -t results/fixed_models_*/"${m}__defect.jsonl" results/gap_filler_*/"${m}.jsonl" 2>/dev/null | head -1
  else ls -t results/fixed_models_*/"${m}__${k}.jsonl" results/framed_original_*/"${m}__${k}.jsonl" 2>/dev/null | head -1; fi
}
contract () {  # model_dir name bank
  local md=$1 m=$2 k=$3 tag=${2}__$3
  done_ "contract_$tag" && { echo "skip contract $tag (done)"; return 0; }
  echo "--- contract $tag ($(date -Is))"
  # shellcheck disable=SC2086
  if python run_scenario.py --model "$md" --data "${BANK[$k]}" --dump "$OUT/$tag.jsonl" ${ARGS[$k]} \
       --new-tokens "$NEW_TOKENS" > "$OUT/${tag}_summary.txt" 2>&1; then
    grep -E "loaded=|rows_in|lie_given_known|other=" "$OUT/${tag}_summary.txt" | tail -4; mark "contract_$tag"; ST+=("contract $tag: OK")
  else tail -3 "$OUT/${tag}_summary.txt"; echo "FAIL contract $tag (continuing)"; ST+=("contract $tag: FAIL"); return 1; fi
}
baselines () {  # dump tag bank
  local d=$1 tag=$2 k=$3
  [[ $HAS_SK == 1 && -s $d ]] || { echo "skip baselines $tag (no sklearn or no dump)"; return 0; }
  done_ "tb_$tag" && return 0
  python scripts/text_baselines.py --dump "$d" --bank "${BANK[$k]}" --out "$OUT/${tag}_text_baselines.json" >/dev/null \
    && { mark "tb_$tag"; echo "baselines $tag OK (dump $d)"; } || echo "WARN baselines failed $tag"
}
somot () {  # model_dir name bank layer dump [otmode]
  local md=$1 m=$2 k=$3 L=$4 bd=$5 mode=${6:-chat} tag=${2}__$3; [[ $mode == note ]] && tag=${tag}__otnote
  done_ "som_$tag" && { echo "skip som/ot $tag (done)"; return 0; }
  echo "--- som/ot $tag layer=$L ot=$mode ($(date -Is)) dump=${bd:-missing}"
  local otarg=(); [[ $OT == 1 ]] && otarg=(--ot "$OUT/${tag}_ot.jsonl" --n-samples "$NSAMP" --ot-mode "$mode")
  # shellcheck disable=SC2086
  if python scripts/som_ot_bank.py extract --model "$md" --data "${BANK[$k]}" --layer "$L" --out "$OUT/${tag}_h.npz" \
       ${ARGS[$k]} "${otarg[@]}" > "$OUT/${tag}_extract.txt" 2>&1; then
    grep -E "load_failed|load_fallback|loaded=|layer=" "$OUT/${tag}_extract.txt" || true
    if python scripts/som_ot_bank.py analyze --data "${BANK[$k]}" --npz "$OUT/${tag}_h.npz" --button-dump "$bd" \
         ${otarg:+--ot "$OUT/${tag}_ot.jsonl"} --out "$OUT/${tag}_som_ot.json" > "$OUT/${tag}_analyze.txt" 2>&1; then
      mark "som_$tag"; ST+=("som/ot $tag: OK")
    else tail -3 "$OUT/${tag}_analyze.txt"; ST+=("som/ot $tag: ANALYZE FAIL"); fi
  else tail -3 "$OUT/${tag}_extract.txt"; echo "FAIL extract $tag (continuing)"; ST+=("som/ot $tag: EXTRACT FAIL"); fi
}

if [[ $SKIP_GEMMA != 1 ]]; then
  GD=$MODELS_DIR/$GEMMA
  if [[ -f $GD/config.json ]]; then
    echo "--- 2. $GEMMA contract rerun (BOS fix)"
    for k in defect user_says agent_stakes; do contract "$GD" "$GEMMA" "$k" && baselines "$OUT/${GEMMA}__$k.jsonl" "${GEMMA}__$k" "$k"; done
    echo "--- 3. $GEMMA SOM/OT at layer $GEMMA_LAYER"
    for k in defect user_says agent_stakes; do
      bd=$OUT/${GEMMA}__$k.jsonl; [[ -s $bd ]] || bd=$(newest_dump "$GEMMA" "$k")
      somot "$GD" "$GEMMA" "$k" "$GEMMA_LAYER" "$bd"
      [[ $OT_COMPARE_NOTE == 1 ]] && somot "$GD" "$GEMMA" "$k" "$GEMMA_LAYER" "$bd" note
    done
  else echo "SKIP $GEMMA: not found at $GD"; fi
fi

if [[ $SKIP_OTHERS != 1 ]]; then
  echo "--- 4. other models: chat-prompt OT + new baselines"
  for m in $OTHER_MODELS; do
    [[ $m =~ $MODEL_FILTER ]] || continue
    md=$MODELS_DIR/$m; [[ -f $md/config.json ]] || { echo "SKIP missing model $md"; continue; }
    for k in defect user_says agent_stakes; do
      if [[ $RERUN_CONTRACT == 1 ]]; then contract "$md" "$m" "$k"; bd=$OUT/${m}__$k.jsonl; else bd=$(newest_dump "$m" "$k"); fi
      baselines "$bd" "${m}__$k" "$k"
      somot "$md" "$m" "$k" "${LAYER[$m]:-8}" "$bd"
      [[ $OT_COMPARE_NOTE == 1 ]] && somot "$md" "$m" "$k" "${LAYER[$m]:-8}" "$bd" note
    done
  done
fi
echo "--- OT identity check (user_says vs agent_stakes must differ now)"
for f in "$OUT"/*__user_says_ot.jsonl; do [[ -f $f ]] || continue; g=${f/__user_says_ot/__agent_stakes_ot}
  [[ -f $g ]] && { cmp -s "$f" "$g" && echo "IDENTICAL $(basename "$f") (unexpected)" || echo "differ $(basename "$f" _user_says_ot.jsonl)"; }; done
echo "=== done $(date -Is) ==="; for s in "${ST[@]}"; do echo "  $s"; done
echo "Provisional banks. SOM/OT are diagnostics, not gates. Not a camera. Not handoverPass. D not filled. r not frozen. Negative handover unchanged."
