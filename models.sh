# Model locations. Source this from runners.
# A clone sets MODEL_DIR (or the individual variables) and does not need the author's paths.
#
#   export MODEL_DIR=/path/to/your/models
#   source models.sh
#
# Optional: models.local.sh (gitignored) can set MODEL_DIR or the individual names
# for the machine that owns the weights.

if [ -f "$(dirname "${BASH_SOURCE[0]}")/models.local.sh" ]; then
  # shellcheck disable=SC1091
  source "$(dirname "${BASH_SOURCE[0]}")/models.local.sh"
fi

: "${MODEL_DIR:=models}"

export QWEN="${QWEN:-$MODEL_DIR/Qwen2.5-7B-Instruct}"
export MISTRAL="${MISTRAL:-$MODEL_DIR/Mistral-7B-Instruct-v0.3}"
export AYA="${AYA:-$MODEL_DIR/aya-expanse-8b}"
export GEMMA="${GEMMA:-$MODEL_DIR/gemma-3-4b-it}"
export FALCON="${FALCON:-$MODEL_DIR/Falcon3-7B-Instruct}"
export GRANITE="${GRANITE:-$MODEL_DIR/granite-4.2-8b}"
export QWEN35="${QWEN35:-$MODEL_DIR/Qwen3.5-9B}"
