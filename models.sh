# Model locations. Source this from runners.
# A clone sets MODEL_DIR or the individual names. Optional models.local.sh
# (gitignored) holds machine-specific roots.
#
# Search order for each short name:
#   1. explicit variable (QWEN, MISTRAL, ...)
#   2. $MODEL_DIR/<short>
#   3. models/<short>          (inside this repo)
#   4. ../regret-heuristic/models/<short>
#   5. $HF_HUB/<hf-style-dir>/snapshots/*   if HF_HUB is set

if [ -f "$(dirname "${BASH_SOURCE[0]}")/models.local.sh" ]; then
  # shellcheck disable=SC1091
  source "$(dirname "${BASH_SOURCE[0]}")/models.local.sh"
fi

: "${MODEL_DIR:=models}"
: "${HF_HUB:=}"

# short-name -> HF hub directory name
declare -A HF_NAME=(
  [Qwen2.5-7B-Instruct]=models--Qwen--Qwen2.5-7B-Instruct
  [Mistral-7B-Instruct-v0.3]=models--mistralai--Mistral-7B-Instruct-v0.3
  [aya-expanse-8b]=models--CohereLabs--aya-expanse-8b
  [gemma-3-4b-it]=models--google--gemma-3-4b-it
  [Falcon3-7B-Instruct]=models--tiiuae--Falcon3-7B-Instruct
  [granite-4.2-8b]=models--ibm-granite--granite-4.2-8b
  [Qwen3.5-9B]=models--Qwen--Qwen3.5-9B
)

resolve_one() {
  local short="$1"
  local var="$2"
  # already set?
  if [ -n "${!var:-}" ] && [ -f "${!var}/config.json" ]; then
    echo "${!var}"
    return
  fi
  local cand
  for cand in \
      "$MODEL_DIR/$short" \
      "models/$short" \
      "../regret-heuristic/models/$short"
  do
    if [ -f "$cand/config.json" ]; then
      echo "$cand"
      return
    fi
  done
  if [ -n "$HF_HUB" ]; then
    local hub="${HF_NAME[$short]:-}"
    if [ -n "$hub" ] && [ -d "$HF_HUB/$hub/snapshots" ]; then
      local snap
      snap=$(find "$HF_HUB/$hub/snapshots" -mindepth 1 -maxdepth 1 -type d | head -1)
      if [ -n "$snap" ] && [ -f "$snap/config.json" ]; then
        echo "$snap"
        return
      fi
    fi
  fi
  # nothing found
  echo ""
}

export QWEN="${QWEN:-$(resolve_one Qwen2.5-7B-Instruct QWEN)}"
export MISTRAL="${MISTRAL:-$(resolve_one Mistral-7B-Instruct-v0.3 MISTRAL)}"
export AYA="${AYA:-$(resolve_one aya-expanse-8b AYA)}"
export GEMMA="${GEMMA:-$(resolve_one gemma-3-4b-it GEMMA)}"
export FALCON="${FALCON:-$(resolve_one Falcon3-7B-Instruct FALCON)}"
export GRANITE="${GRANITE:-$(resolve_one granite-4.2-8b GRANITE)}"
export QWEN35="${QWEN35:-$(resolve_one Qwen3.5-9B QWEN35)}"
