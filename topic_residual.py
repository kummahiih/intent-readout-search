#!/usr/bin/env python3
"""Last-token h with the bank topic direction removed.

r(h) = h - (h·v)v, v = normalize(h_bank[topic1] - h_bank[topic0]).
--layer picks which hidden state (0=embed, -1=last). --sweep tries a few.
Not LEACE. Not SAE. Tiny-n diagnostic. No weights committed.
"""

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def last_tokens_all_layers(model, tokenizer, text, max_length, device):
    toks = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=max_length
    )
    toks = {k: v.to(device) for k, v in toks.items()}
    out = model(**toks, output_hidden_states=True)
    return [h[0, -1, :].float().cpu() for h in out.hidden_states]


def cosine(a, b):
    return float(
        (F.normalize(a.unsqueeze(0), dim=-1) @ F.normalize(b.unsqueeze(0), dim=-1).T)
        .clamp(-1, 1)
        .item()
    )


def topic_acc(vecs, topics):
    names = sorted(set(topics))
    tid = {t: i for i, t in enumerate(names)}
    X = F.normalize(torch.stack(vecs), dim=-1)
    y = torch.tensor([tid[t] for t in topics])
    Y = F.one_hot(y, num_classes=len(names)).float()
    W = torch.linalg.lstsq(X, Y).solution
    pred = (X @ W).argmax(dim=-1)
    return float((pred == y).float().mean()), names


def report_layer(layer, bank_h, ev_h, bank_rows, ev_rows):
    topics_bank = [r["topic"] for r in bank_rows]
    names = sorted(set(topics_bank))
    h0 = torch.stack([h for h, t in zip(bank_h, topics_bank) if t == names[0]]).mean(0)
    h1 = torch.stack([h for h, t in zip(bank_h, topics_bank) if t == names[1]]).mean(0)
    v = F.normalize(h1 - h0, dim=0)

    def residual(h):
        return h - (h * v).sum() * v

    D = torch.stack([residual(h) for h in bank_h])
    acc_raw, _ = topic_acc(ev_h, [r["topic"] for r in ev_rows])
    res_ev = [residual(h) for h in ev_h]
    acc_res, tnames = topic_acc(res_ev, [r["topic"] for r in ev_rows])
    print(f"--- layer={layer} topic_axis={names[0]}->{names[1]} v_norm={float(v.norm()):.4f}")
    print("pair cosine to residual bank (topic axis removed):")
    dec, hon = [], []
    for h, r in zip(res_ev, ev_rows):
        s = max(cosine(h, D[i]) for i in range(D.shape[0]))
        print(f"  topic={r['topic']} strategy={r['strategy']} s*_D={s:.4f}")
        (dec if r["strategy"] == "deceptive" else hon).append(s)
    gap = (sum(hon) / len(hon)) - (sum(dec) / len(dec))
    print(
        f"mean s*_D deceptive={sum(dec)/len(dec):.4f} honest={sum(hon)/len(hon):.4f} "
        f"gap_hon_minus_dec={gap:.4f}"
    )
    print(
        f"topic_probe_acc_raw={acc_raw:.2f} topic_probe_acc_residual={acc_res:.2f} "
        f"n={len(ev_rows)} topics={tnames}"
    )
    return acc_res, gap


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs.jsonl")
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument(
        "--layer",
        type=int,
        default=-1,
        help="hidden_states index: 0=embed, -1=last (default)",
    )
    p.add_argument(
        "--sweep",
        action="store_true",
        help="also report embed, 1/4, 1/2, 3/4, last",
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
    print(
        f"VRAM allocated_GiB={torch.cuda.memory_allocated() / 1024**3:.2f} "
        f"reserved_GiB={torch.cuda.memory_reserved() / 1024**3:.2f}"
    )
    with torch.no_grad():
        bank_all = [
            last_tokens_all_layers(model, tok, r["text"], args.max_length, device)
            for r in bank
        ]
        ev_all = [
            last_tokens_all_layers(model, tok, r["text"], args.max_length, device)
            for r in ev
        ]
    n_hs = len(bank_all[0])
    topics_bank = [r["topic"] for r in bank]
    names = sorted(set(topics_bank))
    if len(names) != 2:
        print("ERROR: bank must have exactly two topics", file=sys.stderr)
        sys.exit(1)

    def idx(layer):
        return layer if layer >= 0 else n_hs + layer

    layers = [args.layer]
    if args.sweep:
        layers = [0, n_hs // 4, n_hs // 2, (3 * n_hs) // 4, -1]
    print(f"n_hidden_states={n_hs} layers={layers}")
    for layer in layers:
        i = idx(layer)
        bank_h = [hs[i] for hs in bank_all]
        ev_h = [hs[i] for hs in ev_all]
        report_layer(i, bank_h, ev_h, bank, ev)
    print("v is estimated from bank only. Residual is not a trained adversary.")
    print("Not a deception result.")


if __name__ == "__main__":
    main()
