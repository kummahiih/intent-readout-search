# Install notes

Pip lines are in `requirements.txt`. This file is the why. Do not run `pip install -r requirements.txt` blindly: two of the kernel packages must be installed with `--no-deps`, and `causal-conv1d` is a local build.

The venv used for these runs is `/media/pauli/datapata/rh-venv`.

## Qwen3.5 and Granite kernels

Qwen3.5-9B and Granite 4.2-8B use a gated-delta layer and a causal convolution. Without the kernels, Transformers falls back to a slow PyTorch reference and a 100-row generation is not practical.

Compiled on this machine for those two walks, 2026-10-04:

- `flash-linear-attention==0.5.2` and `fla-core==0.5.2`, installed with `--no-deps`. `fla-core` holds `fla.ops`. The top package alone is a namespace and `from fla.ops.gated_delta_rule import chunk_gated_delta_rule` fails.
- `causal-conv1d`, built locally. There is no wheel for Torch `2.14.0+cu130`, Python 3.12, C++11 ABI. The system `nvcc` was CUDA 12.0 and this Torch was built with CUDA 13.0, so a plain `pip install causal-conv1d` fails the version check.

Build that worked:

```bash
source /media/pauli/datapata/rh-venv/bin/activate
export CUDA_HOME=/usr/local/cuda-13.0
export PATH="$CUDA_HOME/bin:$PATH"
# nvcc must print release 13.0. Do not apt install cuda. That can replace the driver.
TORCH_CUDA_ARCH_LIST=8.9 \
CAUSAL_CONV1D_FORCE_BUILD=TRUE \
CAUSAL_CONV1D_FORCE_CXX11_ABI=TRUE \
pip install causal-conv1d --no-build-isolation --no-cache-dir
```

`8.9` is the 4070 Ti. The running process does not pick up a kernel installed after it started.

Do not install `flash-linear-attention[cuda]`. That extra can replace Torch.

## Other requirements

- `sentencepiece` is required for the Gemma tokenizer. Without it, `AutoTokenizer` raises the slow-tokenizer error.
- Phi-4-mini still fails in this venv: its remote modeling file imports `LossKwargs` from `transformers.utils`, and this Transformers build does not export that name. Skip it. Do not downgrade Transformers for one walk.
- Loads are 4-bit NF4 through `bitsandbytes`. A model directory needs `config.json` and a complete `model.safetensors` set. An index without its shards is an incomplete weight and the runner skips it.
- Model weights and the MASK dataset stay out of git. Paths are local `models/<name>` or a Hugging Face snapshot.
- LFM2.5 and the Bonsai GGUF are not in the Transformers row generator. Bonsai needs the llama.cpp server.
- Row generation is items, not buttons. A file of 100 lines can still be templates. A `...` fact is not an item.
