#!/usr/bin/env python3
"""Rank mid-layer heads by strategy gap vs topic, then B0 the subset.

--holdout ranks on split=bank only and scores on split=eval.
Not Pandey path-patching. Not SAE. Not a frozen D. Tiny-n diagnostic.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
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


def strategy_gap(vecs, rows, pin_vecs):
    D = torch.stack(pin_vecs)
    dec, hon = [], []
    for vec, r in zip(vecs, rows):
        s = max(cosine(vec, D[i]) for i in range(D.shape[0]))
        (dec if r["strategy"] == "deceptive" else hon).append(s)
    if not dec or not hon:
        return 0.0, 0.0, 0.0
    md = sum(dec) / len(dec)
    mh = sum(hon) / len(hon)
    return md, mh, mh - md


def pack_all(heads):
    return torch.cat([heads[i] for i in range(heads.shape[0])], dim=0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs.jsonl")
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--layer", type=int, default=-1)
    p.add_argument("--k", type=int, default=4)
    p.add_argument(
        "--holdout",
        action="store_true",
        help="rank heads on bank; report B0 only on eval",
    )
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        sys.exit(1)
    rows = [json.loads(l) for l in Path(args.data).read_text().splitlines() if l.strip()]
    pin = [r for r in rows if r["split"] == "bank" and r["strategy"] == "deceptive"]
    rank_rows = [r for r in rows if r["split"] == "bank"] if args.holdout else None
    ev = [r for r in rows if r["split"] == "eval"]
    if len(pin) < 2 or not ev:
        print("ERROR: need >=2 deceptive bank rows and eval rows", file=sys.stderr)
        sys.exit(1)
    if args.holdout and len(rank_rows) < 2:
        print("ERROR: --holdout needs bank rows to rank on", file=sys.stderr)
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
    mode = "holdout" if args.holdout else "in_sample"
    print(f"n_layers={n_layers} layer={layer} k={args.k} mode={mode}")
    with torch.no_grad():
        pin_heads = [
            extract_one(model, tok, r["text"], layer, args.max_length, device)[0]
            for r in pin
        ]
        ev_heads = [
            extract_one(model, tok, r["text"], layer, args.max_length, device)[0]
            for r in ev
        ]
        if args.holdout:
            rank_heads = [
                extract_one(model, tok, r["text"], layer, args.max_length, device)[0]
                for r in rank_rows
            ]
        else:
            rank_rows = ev
            rank_heads = ev_heads
    n_heads = pin_heads[0].shape[0]
    rank_topics = [r["topic"] for r in rank_rows]
    ev_topics = [r["topic"] for r in ev]
    pin_alone = [[h[i] for h in pin_heads] for i in range(n_heads)]
    print(
        f"n_rank={len(rank_rows)} n_eval={len(ev)} n_pin={len(pin)} "
        f"rank_has_honest={any(r['strategy']=='honest' for r in rank_rows)}"
    )
    print("head topic_loo_rank |gap_rank| score")
    ranked = []
    for i in range(n_heads):
        alone_rank = [h[i] for h in rank_heads]
        t_rank = loo_centroid_acc(alone_rank, rank_topics)
        _, _, g_rank = strategy_gap(alone_rank, rank_rows, pin_alone[i])
        score = abs(g_rank) - t_rank
        ranked.append((score, i, t_rank, g_rank))
        print(f"{i:4d} {t_rank:.2f} {abs(g_rank):.4f} {score:.4f}")
    ranked.sort(reverse=True)
    picked = sorted(idx for _, idx, *_ in ranked[: min(args.k, len(ranked))])
    print("picked_heads=" + ",".join(str(i) for i in picked))

    def pack_k(heads):
        return torch.cat([heads[i] for i in picked], dim=0)

    ev_r = [pack_k(h) for h in ev_heads]
    pin_r = [pack_k(h) for h in pin_heads]
    acc_r, tnames = topic_acc(ev_r, ev_topics)
    t_loo = loo_centroid_acc(ev_r, ev_topics)
    md, mh, gap = strategy_gap(ev_r, ev, pin_r)
    print(
        f"eval topic_probe_acc={acc_r:.2f} topic_loo={t_loo:.2f} "
        f"mean s*_D dec={md:.4f} hon={mh:.4f} gap_hon_minus_dec={gap:.4f} "
        f"n={len(ev)} topics={tnames}"
    )
    print("Heads ranked off eval when --holdout. Topic acc 1.00 on r is a fail.")
    print("Not a deception result.")


if __name__ == "__main__":
    main()
