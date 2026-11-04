#!/usr/bin/env bash
# run_fix_rerun.sh — rerun after the 2026-11-03 audit fixes and second review (results/audit_2026-11-03.md).
# Run from the repo root:  bash run_fix_rerun.sh
#   pre. Hard fail (exit 2) when: HF_HOME is missing, $GEMMA config.json is missing (unless SKIP_GEMMA=1),
#        no requested model is found, or torch/transformers is not importable.
#   0. CPU tests (tests/*.py) + SOM smokes. Any failure stops the run (exit 3).
#   1. Tokenizer-only double-BOS check. With AUTO_RERUN_BOS=1 (the default), any non-gemma model flagged
#      DOUBLE_BOS_BEFORE_FIX gets its contract rerun automatically. With AUTO_RERUN_BOS=0 and
#      RERUN_CONTRACT=0, a flagged model is a failure.
#   2. $GEMMA contract rerun on the 3 banks + text baselines (incl. order-sensitive word 1-5 / char_wb 3-6).
#   3. $GEMMA SOM/OT at GEMMA_LAYER, once per OT condition in OT_ASKS.
#   4. Other models (OTHER_MODELS): SOM/OT at each model's old layer, against the newest existing button
#      dump, or a fresh contract when rerun (RERUN_CONTRACT=1 or BOS-flagged); + text baselines.
# Exit status:
#   - Each failure (contract, extract, analyze, baseline, BOS check, missing dump, missing model) sets
#     FAIL=1; the run continues through the independent steps.
#   - A missing model is not a failure with ALLOW_MISSING=1.
#   - The run ends with "RUN FAILED: inspect <log>" (exit 1) or "RUN COMPLETED" (exit 0).
# Resumable: reuse OUT=results/fix_rerun_... ; finished steps leave .done markers and are skipped.
# OT conditions:
#   - OT_ASKS (default "yesno open"): yesno is the contract ask + "Answer with only YES or NO."; open
#     drops the YES/NO instruction and asks an open-ended question.
#   - The open condition is PROVISIONAL and not preregistered.
#   - OT_ASK (default '') is passed as --ot-ask (empty = each condition's default ask); ot_ask and
#     ot_format are recorded in each OT row.
#   - The YES/NO condition is not evidence of room-entry behaviour.
# DOES NOT: change banks or contract semantics, fill D, freeze r, claim a camera or handoverPass,
#   change the negative handover, or commit. Provisional banks.
# Env:
#   - Paths: HF_HOME (default /run/media/pauli/datapata/hf).
#     MODEL_DIRS: search path, default "models ../regret-heuristic/models", the same order as
#     run_som_ot_new_banks.sh. Each model resolves to the first dir that has <name>/config.json.
#     MODELS_DIR (old, one dir) is used alone when it is set and MODEL_DIRS is not.
#   - Gemma: GEMMA (default gemma-2-9b-it), GEMMA_LAYER (24).
#   - Generation: NEW_TOKENS (256), NSAMP (4).
#   - OT: OT=0 skips OT; OT_ASKS; OT_ASK; OT_COMPARE_NOTE=1 adds a note-only OT extract.
#   - Model selection: SKIP_GEMMA=1, SKIP_OTHERS=1, OTHER_MODELS (space list), MODEL_FILTER (regex on names).
#   - RESOLVE_ONLY=1: print the resolved model paths and exit.
#   - Reruns: RERUN_CONTRACT (0), AUTO_RERUN_BOS (1), ALLOW_MISSING (0), OUT.
set -uo pipefail
[[ -f run_scenario.py && -f scripts/som_ot_bank.py && -f prompt_text.py ]] || { echo "FAIL run from the intent-readout-search repo root"; exit 2; }
export HF_HOME=${HF_HOME:-/run/media/pauli/datapata/hf}
export PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}
if [[ -n ${MODEL_DIRS:-} ]]; then :; elif [[ -n ${MODELS_DIR:-} ]]; then MODEL_DIRS=$MODELS_DIR; else MODEL_DIRS="models ../regret-heuristic/models"; fi
declare -A MPATH=()
resolve () { local d; for d in $MODEL_DIRS; do [[ -f $d/$1/config.json ]] && { MPATH[$1]=$d/$1; return 0; }; done; return 1; }
GEMMA=${GEMMA:-gemma-2-9b-it}; GEMMA_LAYER=${GEMMA_LAYER:-24}; NEW_TOKENS=${NEW_TOKENS:-256}; NSAMP=${NSAMP:-4}
OT=${OT:-1}; OT_COMPARE_NOTE=${OT_COMPARE_NOTE:-0}; SKIP_GEMMA=${SKIP_GEMMA:-0}; SKIP_OTHERS=${SKIP_OTHERS:-0}
OT_ASKS=${OT_ASKS:-"yesno open"}; OT_ASK=${OT_ASK:-}
RERUN_CONTRACT=${RERUN_CONTRACT:-0}; AUTO_RERUN_BOS=${AUTO_RERUN_BOS:-1}; ALLOW_MISSING=${ALLOW_MISSING:-0}; MODEL_FILTER=${MODEL_FILTER:-.}
OTHER_MODELS=${OTHER_MODELS:-"granite-4.2-8b Qwen3.5-9B Phi-4-mini-instruct LFM2.5-8B-A1B Qwen2.5-7B-Instruct Mistral-7B-Instruct-v0.3 aya-expanse-8b gemma-3-4b-it Falcon3-7B-Instruct"}
for c in $OT_ASKS; do [[ $c == yesno || $c == open ]] || { echo "FAIL OT_ASKS: unknown condition '$c' (yesno|open)"; exit 2; }; done

# --- preflight: hard failures before anything is written
[[ -d $HF_HOME ]] || { echo "FAIL HF_HOME $HF_HOME does not exist (drive not mounted?)"; exit 2; }
if [[ $SKIP_GEMMA != 1 ]] && ! resolve "$GEMMA"; then
  echo "FAIL $GEMMA missing: no $GEMMA/config.json in MODEL_DIRS='$MODEL_DIRS' (set MODEL_DIRS, or SKIP_GEMMA=1)"; exit 2; fi
ALL=(); MISSING=(); OTHERS=()
[[ $SKIP_GEMMA != 1 ]] && ALL+=("${MPATH[$GEMMA]}")
if [[ $SKIP_OTHERS != 1 ]]; then
  for m in $OTHER_MODELS; do
    [[ $m =~ $MODEL_FILTER ]] || continue
    if resolve "$m"; then ALL+=("${MPATH[$m]}"); OTHERS+=("$m"); else MISSING+=("$m"); fi
  done
fi
(( ${#ALL[@]} > 0 )) || { echo "FAIL no requested model found in MODEL_DIRS='$MODEL_DIRS' (missing: ${MISSING[*]:-none requested})"; exit 2; }
if [[ ${RESOLVE_ONLY:-0} == 1 ]]; then  # print model resolution and stop (for tests and checks)
  for n in "${!MPATH[@]}"; do echo "model $n -> ${MPATH[$n]}"; done; for n in "${MISSING[@]}"; do echo "missing $n"; done; exit 0; fi
python -c "import torch,transformers" 2>/dev/null || { echo "FAIL torch/transformers not importable"; exit 2; }

export HF_MODULES_CACHE=${HF_MODULES_CACHE:-$PWD/.hf_modules_cache}; mkdir -p "$HF_MODULES_CACHE"
OUT=${OUT:-results/fix_rerun_$(date +%Y%m%d_%H%M)}; mkdir -p "$OUT"; LOG=$OUT/run.log
exec > >(tee -a "$LOG") 2>&1
echo "=== start $(date -Is) $(git rev-parse --short HEAD 2>/dev/null) dirty=$(git status --porcelain 2>/dev/null | wc -l) OUT=$OUT HF_HOME=$HF_HOME OT_ASKS='$OT_ASKS' OT_ASK='$OT_ASK' ==="
for n in "${!MPATH[@]}"; do echo "model $n -> ${MPATH[$n]}"; done
python -c "import torch,transformers;print('torch',torch.__version__,'transformers',transformers.__version__,'cuda',torch.cuda.is_available())"
FAIL=0; ST=()
ok_ () { ST+=("$1: OK"); }
bad () { ST+=("$1"); FAIL=1; echo "FAIL $1"; }
for m in "${MISSING[@]}"; do
  if [[ $ALLOW_MISSING == 1 ]]; then ST+=("model $m: SKIPPED (missing, ALLOW_MISSING=1)"); echo "SKIP missing model $m (MODEL_DIRS='$MODEL_DIRS')"
  else bad "model $m: SKIPPED (no $m/config.json in MODEL_DIRS='$MODEL_DIRS')"; fi
done
declare -A BANK=([defect]=data/prereg/scenarios_defect_bank_provisional.jsonl
                 [user_says]=data/prereg/scenarios_original_user_says.jsonl
                 [agent_stakes]=data/prereg/scenarios_original_agent_stakes.jsonl)
declare -A ARGS=([defect]="--incentive-in-user" [user_says]="--role-frame user-says" [agent_stakes]="--role-frame agent-stakes")
declare -A LAYER=([Qwen2.5-7B-Instruct]=8 [Mistral-7B-Instruct-v0.3]=9 [aya-expanse-8b]=10 [gemma-3-4b-it]=8
                  [Falcon3-7B-Instruct]=8 [granite-4.2-8b]=12 [Qwen3.5-9B]=10)
done_ () { [[ -f $OUT/.done_$1 ]]; }
mark () { touch "$OUT/.done_$1"; }

echo "--- 0. CPU tests"
if ! done_ tests; then
  for t in tests/*.py; do
    python "$t" > "$OUT/test_$(basename "$t" .py).txt" 2>&1 || { tail -20 "$OUT/test_$(basename "$t" .py).txt"; echo "FAIL $t"; echo "RUN FAILED: inspect $LOG"; exit 3; }
    echo "PASS $t ($(grep -c '^PASS' "$OUT/test_$(basename "$t" .py).txt") checks)"
  done
  for k in defect user_says agent_stakes; do
    python scripts/som_ot_bank.py smoke --data "${BANK[$k]}" | tail -1 | grep -q "smoke OK" || { echo "FAIL smoke $k"; echo "RUN FAILED: inspect $LOG"; exit 3; }
  done; echo "smokes OK"; mark tests
else echo "skip (done)"; fi
HAS_SK=0; python -c "import sklearn" 2>/dev/null && HAS_SK=1
[[ $HAS_SK == 1 ]] || bad "sklearn missing: text baselines cannot run"

echo "--- 1. double-BOS check (tokenizer only)"
declare -A BOSRERUN=()
if python scripts/bos_check.py --model "${ALL[@]}" > "$OUT/bos_check.txt" 2>&1; then cat "$OUT/bos_check.txt"
else cat "$OUT/bos_check.txt"; bad "bos_check: script failed"; fi
grep -q "tokenizer load failed" "$OUT/bos_check.txt" && bad "bos_check: tokenizer load failed for $(grep 'tokenizer load failed' "$OUT/bos_check.txt" | cut -d: -f1 | sed 's/bos_check //' | tr '\n' ' ')"
for m in "${OTHERS[@]}"; do
  if grep -q "^bos_check $m: .*DOUBLE_BOS_BEFORE_FIX" "$OUT/bos_check.txt"; then
    if [[ $RERUN_CONTRACT == 1 || $AUTO_RERUN_BOS == 1 ]]; then BOSRERUN[$m]=1; echo "BOS: $m had double BOS before the fix -> contract rerun"
    else bad "BOS: $m had double BOS before the fix; old button dumps are inconsistent (set AUTO_RERUN_BOS=1 or RERUN_CONTRACT=1)"; fi
  fi
done

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
    grep -E "loaded=|rows_in|lie_given_known|other=" "$OUT/${tag}_summary.txt" | tail -4; mark "contract_$tag"; ok_ "contract $tag"
  else tail -3 "$OUT/${tag}_summary.txt"; bad "contract $tag (continuing)"; return 1; fi
}
baselines () {  # dump tag bank
  local d=$1 tag=$2 k=$3
  [[ $HAS_SK == 1 ]] || return 0   # already counted as a failure
  [[ -s $d ]] || { bad "baselines $tag: no button dump"; return 1; }
  done_ "tb_$tag" && return 0
  if python scripts/text_baselines.py --dump "$d" --bank "${BANK[$k]}" --out "$OUT/${tag}_text_baselines.json" > "$OUT/${tag}_text_baselines.txt" 2>&1; then
    mark "tb_$tag"; ok_ "baselines $tag"; echo "baselines $tag OK (dump $d)"
  else tail -3 "$OUT/${tag}_text_baselines.txt"; bad "baselines $tag"; return 1; fi
}
somot () {  # model_dir name bank layer dump otmode otcond
  local md=$1 m=$2 k=$3 L=$4 bd=$5 mode=${6:-chat} cond=${7:-yesno} tag=${2}__$3
  [[ $mode == note ]] && tag=${tag}__otnote
  [[ $cond == open ]] && tag=${tag}__otopen
  done_ "som_$tag" && { echo "skip som/ot $tag (done)"; return 0; }
  [[ -s $bd ]] || { bad "som/ot $tag: no button dump"; return 1; }
  echo "--- som/ot $tag layer=$L ot=$mode/$cond ask='${OT_ASK}' ($(date -Is)) dump=$bd"
  local otarg=(); [[ $OT == 1 ]] && otarg=(--ot "$OUT/${tag}_ot.jsonl" --n-samples "$NSAMP" --ot-mode "$mode" --ot-format "$cond" --ot-ask "$OT_ASK")
  local anarg=(); [[ $OT == 1 ]] && anarg=(--ot "$OUT/${tag}_ot.jsonl")
  # shellcheck disable=SC2086
  if python scripts/som_ot_bank.py extract --model "$md" --data "${BANK[$k]}" --layer "$L" --out "$OUT/${tag}_h.npz" \
       ${ARGS[$k]} "${otarg[@]}" > "$OUT/${tag}_extract.txt" 2>&1; then
    grep -E "load_failed|load_fallback|loaded=|layer=" "$OUT/${tag}_extract.txt" || true
    if python scripts/som_ot_bank.py analyze --data "${BANK[$k]}" --npz "$OUT/${tag}_h.npz" --button-dump "$bd" \
         "${anarg[@]}" --out "$OUT/${tag}_som_ot.json" > "$OUT/${tag}_analyze.txt" 2>&1; then
      mark "som_$tag"; ok_ "som/ot $tag"
    else tail -3 "$OUT/${tag}_analyze.txt"; bad "som/ot $tag: ANALYZE"; fi
  else tail -3 "$OUT/${tag}_extract.txt"; bad "som/ot $tag: EXTRACT (continuing)"; fi
}
conds () { [[ $OT == 1 ]] && echo "$OT_ASKS" || echo yesno; }

if [[ $SKIP_GEMMA != 1 ]]; then
  GD=${MPATH[$GEMMA]}
  echo "--- 2. $GEMMA contract rerun (BOS fix)"
  for k in defect user_says agent_stakes; do contract "$GD" "$GEMMA" "$k" && baselines "$OUT/${GEMMA}__$k.jsonl" "${GEMMA}__$k" "$k"; done
  echo "--- 3. $GEMMA SOM/OT at layer $GEMMA_LAYER"
  for k in defect user_says agent_stakes; do
    bd=$OUT/${GEMMA}__$k.jsonl
    if [[ ! -s $bd ]]; then bd=$(newest_dump "$GEMMA" "$k"); bad "som/ot ${GEMMA}__$k: fresh contract dump missing, using old dump ${bd:-none}"; fi
    for c in $(conds); do somot "$GD" "$GEMMA" "$k" "$GEMMA_LAYER" "$bd" chat "$c"; done
    [[ $OT_COMPARE_NOTE == 1 ]] && somot "$GD" "$GEMMA" "$k" "$GEMMA_LAYER" "$bd" note yesno
  done
fi

if [[ $SKIP_OTHERS != 1 ]]; then
  echo "--- 4. other models: chat-prompt OT + new baselines"
  for m in "${OTHERS[@]}"; do
    md=${MPATH[$m]}
    for k in defect user_says agent_stakes; do
      if [[ $RERUN_CONTRACT == 1 || -n ${BOSRERUN[$m]:-} ]]; then
        contract "$md" "$m" "$k" || continue   # failure recorded; no stale dump substituted
        bd=$OUT/${m}__$k.jsonl
      else bd=$(newest_dump "$m" "$k"); fi
      baselines "$bd" "${m}__$k" "$k"
      for c in $(conds); do somot "$md" "$m" "$k" "${LAYER[$m]:-8}" "$bd" chat "$c"; done
      [[ $OT_COMPARE_NOTE == 1 ]] && somot "$md" "$m" "$k" "${LAYER[$m]:-8}" "$bd" note yesno
    done
  done
fi
echo "--- OT identity check (user_says vs agent_stakes must differ now)"
# All-zero OT files (every row mass_note==0 and in_room false) are identical by construction: log them as
# uninformative instead of failing. Identical files with any non-zero row still fail.
ot_allzero() { python3 -c 'import json,sys
rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
sys.exit(0 if rows and all(float(r.get("mass_note") or 0)==0 and not r.get("in_room") for r in rows) else 1)' "$1"; }
ot_identity() { local f=$1 g=$2
  if ! cmp -s "$f" "$g"; then echo "differ $(basename "$f")"
  elif ot_allzero "$f"; then echo "OT uninformative (all-zero) $(basename "$f") vs agent_stakes"
  else bad "OT IDENTICAL $(basename "$f") vs agent_stakes"; fi; }
for f in "$OUT"/*__user_says_ot.jsonl "$OUT"/*__user_says__otopen_ot.jsonl; do [[ -f $f ]] || continue; g=${f/__user_says/__agent_stakes}
  [[ -f $g ]] && ot_identity "$f" "$g"; done
echo "=== done $(date -Is) ==="; for s in "${ST[@]}"; do echo "  $s"; done
echo "Provisional banks. SOM/OT are diagnostics, not gates. OT YES/NO is not evidence of room-entry behaviour."
echo "Not a camera. Not handoverPass. D not filled. r not frozen. Negative handover unchanged."
if (( FAIL )); then echo "RUN FAILED: inspect $LOG"; exit 1; fi
echo "RUN COMPLETED"; exit 0
