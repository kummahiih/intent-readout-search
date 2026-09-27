#!/usr/bin/env python3
"""M linear probes on frozen last-token h.

Each r_i is trained to: hit a binary label, fool a topic head on its
score, and disagree with the other r_j scores.
Labels are assigned tags on notes, or reply_kind on --from-jsonl.
Not r_strat. Do not fill D. Kind is not in L_total.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from pair_contrast import cosine, hidden_path, load_rows, per_topic_gaps, pooled_from_path, report_gap


def kind_side(k: str):
    if k == "contradict":
        return "deceptive"
    if k == "truth":
        return "honest"
    return None


def load_model(name):
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    tok = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        name, quantization_config=bnb, device_map="auto", trust_remote_code=True
    )
    model.eval()
    print(f"loaded={name} VRAM_GiB={torch.cuda.memory_allocated() / 1024**3:.2f}")
    return tok, model


def corr2(a, b):
    a = a - a.mean()
    b = b - b.mean()
    da = float(a.norm())
    db = float(b.norm())
    if da < 1e-6 or db < 1e-6:
        return a.new_zeros(())
    c = (a * b).sum() / (a.norm() * b.norm())
    return c * c


def gap_pairs(pairs):
    dec = [s for lab, s in pairs if lab == "deceptive"]
    hon = [s for lab, s in pairs if lab == "honest"]
    if not dec or not hon:
        return None
    return sum(dec) / len(dec) - sum(hon) / len(hon)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs_wide.jsonl")
    p.add_argument("--from-jsonl", default="", help="construct dumps: score reply text, label=kind")
    p.add_argument("--layer", type=int, default=8)
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--heads", type=int, default=3)
    p.add_argument("--steps", type=int, default=400)
    p.add_argument("--lr", type=float, default=5e-3)
    p.add_argument("--beta", type=float, default=0.5, help="topic adversary weight")
    p.add_argument("--lam", type=float, default=1.0, help="score corr^2 weight")
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        return 1

    print(
        f"multi-r heads={args.heads} beta={args.beta} lam={args.lam} "
        f"layer={args.layer}"
    )
    print("behavior + fool topic + decorrelate scores. Not a freeze. Do not fill D.")

    items = []
    if args.from_jsonl:
        raw = [json.loads(l) for l in Path(args.from_jsonl).read_text().splitlines() if l.strip()]
        for r in raw:
            side = kind_side(r.get("reply_kind", ""))
            if side is None:
                continue
            items.append(
                {
                    "text": r["reply"],
                    "topic": r["topic"],
                    "y": side,
                    "source": "kind",
                }
            )
        print(f"from_jsonl={args.from_jsonl} kept_truth_or_contradict={len(items)}")
    else:
        for r in load_rows(args.data):
            if r.get("strategy") not in ("deceptive", "honest"):
                continue
            items.append(
                {
                    "text": r["text"],
                    "topic": r["topic"],
                    "y": r["strategy"],
                    "source": "tag",
                }
            )
        print(f"notes n={len(items)} labels=assigned tags")

    topics = sorted({r["topic"] for r in items})
    if len(topics) < 3 or len(items) < 8:
        print("ERROR: not enough rooms or rows", file=sys.stderr)
        return 1
    t_ix = {t: i for i, t in enumerate(topics)}
    print("rooms=" + ",".join(topics) + f" source={items[0]['source']}")

    tok, model = load_model(args.model)
    device = model.device
    with torch.no_grad():
        for r in items:
            path = hidden_path(model, tok, r["text"], args.max_length, device, args.layer)
            r["h"] = pooled_from_path(path, "last").float().cpu()
    dim = items[0]["h"].numel()
    print(f"dim={dim}")

    ens_pairs = []
    ens_rooms = defaultdict(list)
    head_rooms = [defaultdict(list) for _ in range(args.heads)]
    corrs = []

    for hold in topics:
        train = [r for r in items if r["topic"] != hold]
        test = [r for r in items if r["topic"] == hold]
        if not train or not test:
            continue
        H = torch.stack([r["h"] for r in train])
        H = F.normalize(H, dim=1)
        y = torch.tensor([1.0 if r["y"] == "deceptive" else 0.0 for r in train])
        tlab = torch.tensor([t_ix[r["topic"]] for r in train], dtype=torch.long)
        W = torch.nn.Parameter(torch.randn(args.heads, dim) * 0.01)
        topic_head = torch.nn.Linear(args.heads, len(topics))
        opt_r = torch.optim.Adam([W], lr=args.lr)
        opt_t = torch.optim.Adam(topic_head.parameters(), lr=args.lr)
        for _ in range(args.steps):
            scores = H @ W.t()  # [n, M]
            opt_t.zero_grad()
            lt = F.cross_entropy(topic_head(scores.detach()), tlab)
            lt.backward()
            opt_t.step()
            opt_r.zero_grad()
            lb = 0.0
            for i in range(args.heads):
                lb = lb + F.binary_cross_entropy_with_logits(scores[:, i], y)
            lb = lb / args.heads
            ld = scores.new_zeros(())
            n_pairs = 0
            for i in range(args.heads):
                for j in range(i + 1, args.heads):
                    ld = ld + corr2(scores[:, i], scores[:, j])
                    n_pairs += 1
            if n_pairs:
                ld = ld / n_pairs
            l_adv = F.cross_entropy(topic_head(scores), tlab)
            loss = lb - args.beta * l_adv + args.lam * ld
            loss.backward()
            opt_r.step()
        with torch.no_grad():
            Wn = F.normalize(W.detach(), dim=1)
            Ht = F.normalize(torch.stack([r["h"] for r in test]), dim=1)
            st = Ht @ Wn.t()
            ens = st.mean(1)
            if args.heads > 1:
                c = 0.0
                np_ = 0
                for i in range(args.heads):
                    for j in range(i + 1, args.heads):
                        c += float(corr2(st[:, i], st[:, j]))
                        np_ += 1
                corrs.append(c / max(np_, 1))
            for r, e, row in zip(test, ens.tolist(), st.tolist()):
                ens_pairs.append((r["y"], e))
                ens_rooms[hold].append((r["y"], e))
                for i, s in enumerate(row):
                    head_rooms[i][hold].append((r["y"], s))
        print(f"  hold={hold} n_train={len(train)} n_test={len(test)}")

    if not ens_pairs:
        print("ERROR: no scores", file=sys.stderr)
        return 1
    report_gap(ens_pairs, "multi_r_ensemble_loto")
    per_topic_gaps(ens_rooms, "per-topic multi_r_ensemble_loto")
    for i in range(args.heads):
        flat = [(lab, s) for t in head_rooms[i] for lab, s in head_rooms[i][t]]
        if flat:
            report_gap(flat, f"multi_r_head{i}_loto")
            per_topic_gaps(head_rooms[i], f"per-topic multi_r_head{i}_loto")
    if corrs:
        print(f"mean_held_score_corr2={sum(corrs)/len(corrs):.4f} n_holds={len(corrs)}")
    hik = gap_pairs(ens_rooms.get("hiking", []))
    trav = gap_pairs(ens_rooms.get("travel", []))
    print(
        f"ensemble hiking={hik if hik is None else f'{hik:.4f}'} "
        f"travel={trav if trav is None else f'{trav:.4f}'}"
    )
    print("Diversity is corr^2 of LOTO scores. Hiking thin means one arrow still.")
    print("Not a camera. Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
