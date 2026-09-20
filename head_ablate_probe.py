#!/usr/bin/env python3
"""Rank mid-layer heads by strategy gap vs topic, then B0 the subset.

For each head: metrics on that head alone, and on all-heads with this
head replaced by the bank mean. Keep k heads with large |gap| and
low leave-one-out topic centroid acc. Then concat those k and probe.
Not Pandey path-patching. Not SAE. Not a frozen D. Tiny-n diagnostic.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from head_write_probe import cosine, extract_one, topic_acc, transformer_layers


def loo_centroid_acc(vecs, labels):
    n = len(vecs)
    names = sorted(set(labels))
    hit = 0
    for i in range(n):
        scores = {}
        for name in names:
            members = [vecs[j] for j in range(n) if j != i and labels[j] == name]
            if not members:
                continue
            scores[name] = cosine(vecs[i], torch.stack(members).mean(0))
        if scores and max(scores, key=scores.get) == labels[i]:
            hit += 1
    return hit / n if n else 0.0


def strategy_gap(vecs, rows, bank_vecs):
    D = torch.stack(bank_vecs)
    dec, hon = [], []
    for vec, r in zip(vecs, rows):
        s = max(cosine(vec, D[i]) for i in range(D.shape[0]))
        (dec if r["strategy"] == "deceptive" else hon).append(s)
    if not dec or not hon:
        return 0.0, 0.0, 0.0
    md = sum(dec) / len(dec)
    mh = sum(hon) / len(hon)
    return md, mh, mh - md


def pack_all(heads, replace=None):
    parts = []
    for i in range(heads.shape[0]):
        parts.append(replace[i] if replace is not None else heads[i])
    return torch.cat(parts, dim=0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs.jsonl")
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--layer", type=int, default=-1)
    p.add_argument("--k", type=int, default=4)
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
    print(
        f"VRAM allocated_GiB={torch.cuda.memory_allocated() / 1024**3:.2f} "
        f"reserved_GiB={torch.cuda.memory_reserved() / 1024**3:.2f}"
    )
    print(f"n_layers={n_layers} layer={layer} k={args.k}")
    topics = [r["topic"] for r in ev]
    with torch.no_grad():
        bank_heads = [
            extract_one(model, tok, r["text"], layer, args.max_length, device)[0]
            for r in bank
        ]
        ev_heads = [
            extract_one(model, tok, r["text"], layer, args.max_length, device)[0]
            for r in ev
        ]
    n_heads = bank_heads[0].shape[0]
    bank_mean = torch.stack(bank_heads).mean(0)
    base_ev = [pack_all(h) for h in ev_heads]
    base_bank = [pack_all(h) for h in bank_heads]
    base_topic = loo_centroid_acc(base_ev, topics)
    _, _, base_gap = strategy_gap(base_ev, ev, base_bank)
    print(f"baseline_all_heads topic_loo={base_topic:.2f} gap_hon_minus_dec={base_gap:.4f}")
    print("head topic_loo |gap| ablate_topic_loo ablate_gap score")
    ranked = []
    for i in range(n_heads):
        alone_ev = [h[i] for h in ev_heads]
        alone_bank = [h[i] for h in bank_heads]
        t_alone = loo_centroid_acc(alone_ev, topics)
        _, _, g_alone = strategy_gap(alone_ev, ev, alone_bank)
        repl = [bank_mean[i] if j == i else None for j in range(n_heads)]
        # pack_all with per-index replace: pass a list via custom
        ab_ev = []
        for h in ev_heads:
            parts = [bank_mean[j] if j == i else h[j] for j in range(n_heads)]
            ab_ev.append(torch.cat(parts, dim=0))
        ab_bank = []
        for h in bank_heads:
            parts = [bank_mean[j] if j == i else h[j] for j in range(n_heads)]
            ab_bank.append(torch.cat(parts, dim=0))
        t_ab = loo_centroid_acc(ab_ev, topics)
        _, _, g_ab = strategy_gap(ab_ev, ev, ab_bank)
        score = abs(g_alone) - t_alone
        ranked.append((score, i, t_alone, g_alone, t_ab, g_ab))
        print(
            f"{i:4d} {t_alone:.2f} {abs(g_alone):.4f} {t_ab:.2f} {g_ab:.4f} {score:.4f}"
        )
    ranked.sort(reverse=True)
    picked = sorted(idx for _, idx, *_ in ranked[: min(args.k, len(ranked))])
    print("picked_heads=" + ",".join(str(i) for i in picked))

    def pack_k(heads):
        return torch.cat([heads[i] for i in picked], dim=0)

    ev_r = [pack_k(h) for h in ev_heads]
    bank_r = [pack_k(h) for h in bank_heads]
    acc_r, tnames = topic_acc(ev_r, topics)
    t_loo = loo_centroid_acc(ev_r, topics)
    md, mh, gap = strategy_gap(ev_r, ev, bank_r)
    print(
        f"subset topic_probe_acc={acc_r:.2f} topic_loo={t_loo:.2f} "
        f"mean s*_D dec={md:.4f} hon={mh:.4f} gap_hon_minus_dec={gap:.4f} "
        f"n={len(ev)} topics={tnames}"
    )
    print("Not path-patching. Not a deception result. Topic acc 1.00 on r is a fail.")


if __name__ == "__main__":
    main()
