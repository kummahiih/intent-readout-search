#!/usr/bin/env bash
# Newer walks the colleague named. 12GB 4070 Ti.
# Instruct folders can join hide_bank.py. The Bonsai GGUF cannot:
# it needs the PrismML llama.cpp fork, not AutoModelForCausalLM.
# Not a camera. Do not fill D.
set -u
cd "$(dirname "$0")"
mkdir -p models

if ! command -v hf >/dev/null 2>&1; then
  echo "ERROR: hf missing. pip install -U huggingface_hub" >&2
  exit 2
fi

echo "=== fits 4-bit on 12GB: Granite 4.2 8B ==="
hf download ibm-granite/granite-4.2-8b --local-dir models/granite-4.2-8b

echo "=== fits 4-bit on 12GB: LFM2.5 8B-A1B (1.5B active). License lfm1.0 ==="
hf download LiquidAI/LFM2.5-8B-A1B --local-dir models/LFM2.5-8B-A1B

echo "=== Nimble is a LoRA on Qwen3.5-9B, not a full chat checkpoint ==="
hf download Qwen/Qwen3.5-9B --local-dir models/Qwen3.5-9B
hf download bespokelabs/Bespoke-Nimble-9B --local-dir models/Bespoke-Nimble-9B

echo "=== Bonsai 2 27B GGUF (~7GB). Not a transformers model ==="
hf download prism-ml/Ternary-Bonsai-2-27B-gguf \
  Ternary-Bonsai-2-27B-PQ2_0.gguf \
  --local-dir models/Ternary-Bonsai-2-27B-gguf

echo "done."
echo "granite and lfm can be pointed at hide_bank.py if the tokenizer loads."
echo "nimble scores choices. it is not the button bank."
echo "bonsai needs the PrismML llama.cpp fork: https://github.com/PrismML-Eng/Bonsai-demo"
echo "qwen3.8-flash-next wants the colleague's 128GB box, not this 12GB card."
echo "Not honesty. Do not fill D."
