#!/usr/bin/env python3
"""Topic probe on a handful of mid-layer attention-head writes.

r = concat of k last-token head writes before o_proj.
Heads picked by mean L2 write-norm on the bank, not by AUROC.
--quiet picks the smallest norms instead of the largest.
Control: last-token residual at the same layer.
Official topic gate is LOO centroid, not in-sample lstsq.
Not Pandey path-patching. Not SAE. Not a frozen D. Tiny-n diagnostic.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from topic_metrics import cosine, loo_centroid_acc, topic_acc


def transformer_layers(model):
    base = model
    if hasattr(base, "model"):
        base = base.model
    if hasattr(base, "model") and hasattr(base.model, "layers"):
        base = base.model
    if not hasattr(base, "layers"):
        raise SystemExit("ERROR: could not find model.layers")
    return base.layers


def extract_one(model, tokenizer, text, layer, max_length, device):
    layers = transformer_layers(model)
    attn = layers[layer].self_attn
    captured = {}

    def pre_hook(mod, args):
        captured["x"] = args[0].detach()

    handle = attn.o_proj.register_forward_pre_hook(pre_hook)
    toks = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=max_length
    )
    toks = {k: v.to(device) for k, v in toks.items()}
    try:
        out = model(**toks, output_hidden_states=True)
    finally:
        handle.remove()
    if "x" not in captured:
        raise SystemExit("ERROR: o_proj hook missed")
    x = captured["x"][0, -1, :].float().cpu()
    n_heads = int(model.config.num_attention_heads)
    if x.numel() % n_heads != 0:
        raise SystemExit(f"ERROR: last-dim {x.numel()} not divisible by heads {n_heads}")
    head_dim = x.numel() // n_heads
    heads = x.view(n_heads, head_dim)
    residual = out.hidden_states[layer + 1][0, -1, :].float().cpu()
    return heads, residual


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs.jsonl")
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--layer", type=int, default=-1, help="transformer block; default mid")
    p.add_argument("--k", type=int, default=4, help="how many heads to keep")
    p.add_argument(
        "--quiet",
        action="store_true",
        help="pick smallest bank write-norm heads instead of largest",
    )
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        sys.exit(1)
    rows = [json.loads(l) for l in Path(args.data).read_text().splitlines() if l.strip()]
    bank = [r for r in rows if r["split"] == "bank" and r["strategy"] == "deceptive"]
    ev = [r for r in rows if r["split"] == "eval"]
    if len(bank) < 2 or not ev:
        print("ERROR: need >=2 bank topics and eval rows", file=sys.stderr)
        sys.exit(1)
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.model, quantization_config=bnb, device_map="auto", trust_remote_code=True
    )
    model.eval()
    device = model.device
    n_layers = len(transformer_layers(model))
    layer = args.layer if args.layer >= 0 else n_layers // 2
    if layer >= n_layers:
        print(f"ERROR: layer {layer} >= n_layers {n_layers}", file=sys.stderr)
        sys.exit(1)
    print(
        f"VRAM allocated_GiB={torch.cuda.memory_allocated() / 1024**3:.2f} "
        f"reserved_GiB={torch.cuda.memory_reserved() / 1024**3:.2f}"
    )
    mode = "quiet" if args.quiet else "loud"
    print(f"n_layers={n_layers} layer={layer} k={args.k} mode={mode}")
    with torch.no_grad():
        bank_heads = []
        bank_h = []
        for r in bank:
            heads, residual = extract_one(
                model, tok, r["text"], layer, args.max_length, device
            )
            bank_heads.append(heads)
            bank_h.append(residual)
        ev_heads = []
        ev_h = []
        for r in ev:
            heads, residual = extract_one(
                model, tok, r["text"], layer, args.max_length, device
            )
            ev_heads.append(heads)
            ev_h.append(residual)
    norms = torch.stack([h.norm(dim=-1) for h in bank_heads]).mean(0)
    k = min(args.k, norms.numel())
    score = -norms if args.quiet else norms
    picked = torch.topk(score, k).indices.tolist()
    picked_sorted = sorted(picked)
    print(
        "picked_heads="
        + ",".join(str(i) for i in picked_sorted)
        + " write_norm="
        + ",".join(f"{float(norms[i]):.4f}" for i in picked_sorted)
    )

    def pack(heads):
        return torch.cat([heads[i] for i in picked_sorted], dim=0)

    bank_r = [pack(h) for h in bank_heads]
    ev_r = [pack(h) for h in ev_heads]
    ev_topics = [r["topic"] for r in ev]
    acc_r, tnames = topic_acc(ev_r, ev_topics)
    acc_h, _ = topic_acc(ev_h, ev_topics)
    loo_r = loo_centroid_acc(ev_r, ev_topics)
    loo_h = loo_centroid_acc(ev_h, ev_topics)
    D = torch.stack(bank_r)
    dec, hon = [], []
    print("pair cosine of r to bank-deceptive head-writes:")
    for vec, r in zip(ev_r, ev):
        s = max(cosine(vec, D[i]) for i in range(D.shape[0]))
        print(f"  topic={r['topic']} strategy={r['strategy']} s*_D={s:.4f}")
        (dec if r["strategy"] == "deceptive" else hon).append(s)
    gap = (sum(hon) / len(hon)) - (sum(dec) / len(dec))
    print(
        f"mean s*_D deceptive={sum(dec)/len(dec):.4f} honest={sum(hon)/len(hon):.4f} "
        f"gap_hon_minus_dec={gap:.4f}"
    )
    print(
        f"topic_lstsq_head_r={acc_r:.2f} topic_lstsq_layer_h={acc_h:.2f} "
        f"topic_loo_head_r={loo_r:.2f} topic_loo_layer_h={loo_h:.2f} "
        f"n={len(ev)} topics={tnames}"
    )
    print("Official topic gate is topic_loo_*. topic_lstsq_* can memorize.")
    print("Heads picked on bank write-norm only. Not a deception result.")


if __name__ == "__main__":
    main()
