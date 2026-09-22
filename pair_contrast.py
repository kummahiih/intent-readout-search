#!/usr/bin/env python3
"""Same-topic contrast camera.

v_T = normalize(h_dec - h_hon) on topic T.
Score the other topic with mean v of the other topics (LOTO).
Official topic gate on the scalar s=h·v is LOO L2, not cosine
(1-d cosine keeps only the sign).
Tags build r only. Not z in a loss. Not a hinge. Not Amp.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from topic_metrics import loo_centroid_acc, loo_l2_acc, topic_acc


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
    by_topic = defaultdict(lambda: {"deceptive": [], "honest": []})
    for r in rows:
        if r["strategy"] in ("deceptive", "honest"):
            by_topic[r["topic"]][r["strategy"]].append(r)
    paired = {
        t: g
        for t, g in by_topic.items()
        if g["deceptive"] and g["honest"]
    }
    if len(paired) < 2:
        print("ERROR: need >=2 topics with both strategies", file=sys.stderr)
        sys.exit(1)
    print(
        "paired_topics="
        + ",".join(
            f"{t}(dec={len(g['deceptive'])},hon={len(g['honest'])})"
            for t, g in sorted(paired.items())
        )
    )
    bank_only_dec = [
        r for r in rows if r["split"] == "bank" and r["strategy"] == "deceptive"
    ]
    print(
        f"bank_deceptive_only={len(bank_only_dec)} "
        "(no honest bank; v from matched pairs, leave-one-topic-out)"
    )
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
    needed = []
    for g in paired.values():
        needed.extend(g["deceptive"] + g["honest"])
    with torch.no_grad():
        hid = {
            id(r): last_hidden(model, tok, r["text"], args.max_length, device)
            for r in needed
        }

    def mean_h(items):
        return torch.stack([hid[id(r)] for r in items]).mean(0)

    v_of = {}
    for t, g in paired.items():
        v = mean_h(g["deceptive"]) - mean_h(g["honest"])
        nrm = float(v.norm())
        v_of[t] = F.normalize(v, dim=0) if nrm > 0 else v
        print(f"v[{t}]_norm={nrm:.4f}")

    scalars, r_topics, scores = [], [], []
    print("leave-one-topic-out scores (v from other topics):")
    for t, g in sorted(paired.items()):
        others = [v_of[u] for u in paired if u != t and float(v_of[u].norm()) > 0]
        if not others:
            print(f"  skip {t}: no other v")
            continue
        v = F.normalize(torch.stack(others).mean(0), dim=0)
        for strat in ("deceptive", "honest"):
            for r in g[strat]:
                h = hid[id(r)]
                s = cosine(h, v)
                print(f"  topic={t} strategy={strat} s_v={s:.4f}")
                scalars.append(torch.tensor([s]))
                r_topics.append(t)
                scores.append((strat, s))
    dec = [s for strat, s in scores if strat == "deceptive"]
    hon = [s for strat, s in scores if strat == "honest"]
    if not dec or not hon:
        print("ERROR: empty score bins", file=sys.stderr)
        sys.exit(1)
    gap = (sum(dec) / len(dec)) - (sum(hon) / len(hon))
    acc_lstsq, tnames = topic_acc(scalars, r_topics)
    acc_loo_cos = loo_centroid_acc(scalars, r_topics)
    acc_loo_l2 = loo_l2_acc(scalars, r_topics)
    print(
        f"mean s_v deceptive={sum(dec)/len(dec):.4f} honest={sum(hon)/len(hon):.4f} "
        f"gap_dec_minus_hon={gap:.4f}"
    )
    print(
        f"topic_lstsq_on_scalar={acc_lstsq:.2f} "
        f"topic_loo_cos_on_scalar={acc_loo_cos:.2f} "
        f"topic_loo_l2_on_scalar={acc_loo_l2:.2f} "
        f"n={len(scalars)} topics={tnames}"
    )
    print("Official topic gate on scalars is topic_loo_l2_on_scalar.")
    print("topic_loo_cos_on_scalar is sign-only in 1-d. Do not read 0.17 as topic-blind.")
    print("v built from pair tags. Tags are not a loss input.")
    print("Not a deception result. Do not train the hinge on this r yet.")


if __name__ == "__main__":
    main()
