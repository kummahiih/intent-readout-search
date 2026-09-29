#!/usr/bin/env python3
"""Shared tokenizer + 4bit walk load.

Aya and Gemma ship a SentencePiece tokenizer without a standalone
tokenizers.json that the fast path can eat. Missing sentencepiece
must not look like a camera failure. Fast conversion can still fail
when sentencepiece is present — try use_fast=False first.
"""

from __future__ import annotations

import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def load_tokenizer(name: str):
    last = None
    # Aya/Gemma: fast conversion fails even with sentencepiece installed.
    for use_fast in (False, True):
        try:
            tok = AutoTokenizer.from_pretrained(
                name, trust_remote_code=True, use_fast=use_fast
            )
            if tok.pad_token is None:
                tok.pad_token = tok.eos_token
            print(
                f"tokenizer name={name} fast={int(use_fast)} "
                f"class={type(tok).__name__}"
            )
            return tok
        except Exception as exc:
            last = exc
            print(f"tokenizer use_fast={int(use_fast)} failed: {exc}")
    print(
        "ERROR: tokenizer needs sentencepiece (Aya / Gemma) or tiktoken. "
        "Not a camera miss. Kind not in L.",
        file=sys.stderr,
    )
    print("fix: pip install sentencepiece", file=sys.stderr)
    raise SystemExit(2) from last


def text_n_layers(model) -> int | None:
    cfg = getattr(model, "config", None)
    if cfg is None:
        return None
    tc = getattr(cfg, "text_config", None)
    if tc is not None and getattr(tc, "num_hidden_layers", None):
        return int(tc.num_hidden_layers)
    n = getattr(cfg, "num_hidden_layers", None)
    return int(n) if n else None


def load_walk(name: str):
    tok = load_tokenizer(name)
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        name, quantization_config=bnb, device_map="auto", trust_remote_code=True
    )
    model.eval()
    n = text_n_layers(model)
    print(
        f"loaded={name} class={type(model).__name__} n_layers={n} "
        f"VRAM_GiB={torch.cuda.memory_allocated() / 1024**3:.2f}"
    )
    return tok, model
