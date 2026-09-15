#!/usr/bin/env python3
"""Strategy gap vs topic probe on last-token identity.

Control, not a detector. Identity is expected to encode topic.
No weights committed. 4070 Ti 4-bit load.
"""

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def last_hidden(model, tokenizer, text, max_length, device):
    toks = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=max_length
    )
    toks = {k: v.to(device) for k, v in toks.items()}
    out = model(**toks, output_hidden_states=True)
    return out.hidden_states[-1][0, -1, :].float().cpu()


def cosine(a, b):
    return float(
        (F.normalize(a.unsqueeze(0), dim=-1) @ F.normalize(b.unsqueeze(0), dim=-1).T)
        .clamp(-1, 1)
        .item()
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs.jsonl")
    p.add_argument("--max-length", type=int, default=256)
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        sys.exit(1)
    rows = [json.loads(l) for l in Path(args.data).read_text().splitlines() if l.strip()]
    bank = [r for r in rows if r["split"] == "bank" and r["strategy"] == "deceptive"]
    ev = [r for r in rows if r["split"] == "eval"]
    if not bank or not ev:
        print("ERROR: need bank deceptive and eval rows", file=sys.stderr)
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
    print(
        f"VRAM allocated_GiB={torch.cuda.memory_allocated() / 1024**3:.2f} "
        f"reserved_GiB={torch.cuda.memory_reserved() / 1024**3:.2f}"
    )
    with torch.no_grad():
        D = torch.stack(
            [last_hidden(model, tok, r["text"], args.max_length, device) for r in bank]
        )
        feats = []
        for r in ev:
            h = last_hidden(model, tok, r["text"], args.max_length, device)
            s = max(cosine(h, D[i]) for i in range(D.shape[0]))
            feats.append((h, s, r["topic"], r["strategy"]))
    print("pair cosine to deceptive bank (last-token identity):")
    for h, s, topic, strat in feats:
        print(f"  topic={topic} strategy={strat} s*_D={s:.4f}")
    topics = sorted({t for _, _, t, _ in feats})
    topic_id = {t: i for i, t in enumerate(topics)}
    X = torch.stack([h for h, _, _, _ in feats])
    y = torch.tensor([topic_id[t] for _, _, t, _ in feats])
    # closed-form least-squares topic probe on this tiny eval set (diagnostic only)
    Xn = F.normalize(X, dim=-1)
    Y = F.one_hot(y, num_classes=len(topics)).float()
    W = torch.linalg.lstsq(Xn, Y).solution
    pred = (Xn @ W).argmax(dim=-1)
    acc = float((pred == y).float().mean())
    dec = [s for _, s, _, st in feats if st == "deceptive"]
    hon = [s for _, s, _, st in feats if st == "honest"]
    print(
        f"mean s*_D deceptive={sum(dec)/len(dec):.4f} honest={sum(hon)/len(hon):.4f} "
        f"gap_hon_minus_dec={(sum(hon)/len(hon))-(sum(dec)/len(dec)):.4f}"
    )
    print(f"topic_probe_acc={acc:.2f} n={len(feats)} topics={topics}")
    print("If topic_probe_acc is high and |gap| is tiny, identity failed the topic test.")
    print("Not a deception result.")


if __name__ == "__main__":
    main()
