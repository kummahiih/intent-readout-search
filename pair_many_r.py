#!/usr/bin/env python3
"""Many room cameras r_T = v_T.

Fit each v_T on a 2+2 fold. Score the held 1+1 of every room with every v_T.
Oracle many-r is the diagonal. Shared LOTO is the off-room mean v.
This is not r_strat. Knowing T is a topic feature. Do not fill D.
"""

from __future__ import annotations

import argparse
import itertools
import sys
from collections import defaultdict

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from pair_contrast import (
    cosine,
    hidden_path,
    load_rows,
    paired_topics,
    per_topic_gaps,
    permute_p,
    pooled_from_path,
    report_gap,
)


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


def folds(dec, hon):
    out = []
    if len(dec) < 3 or len(hon) < 3:
        return out
    for i, j in itertools.product(range(len(dec)), range(len(hon))):
        fd = [x for k, x in enumerate(dec) if k != i]
        fh = [x for k, x in enumerate(hon) if k != j]
        if len(fd) < 2 or len(fh) < 2:
            continue
        out.append((fd[:2], fh[:2], [dec[i]], [hon[j]]))
        if len(out) >= 3:
            return out
    return out


def mean_h(items, hid):
    return torch.stack([hid[id(r)] for r in items]).mean(0)


def gap_of(pairs):
    dec = [s for lab, s in pairs if lab == "deceptive"]
    hon = [s for lab, s in pairs if lab == "honest"]
    if not dec or not hon:
        return None
    return sum(dec) / len(dec) - sum(hon) / len(hon)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs_wide.jsonl")
    p.add_argument("--transfer", default="")
    p.add_argument("--layer", type=int, default=8)
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--permute", type=int, default=0)
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        return 1

    rows = load_rows(args.data)
    paired = paired_topics(rows)
    needed = []
    for g in paired.values():
        needed.extend(g["deceptive"] + g["honest"])
    xfer_rows = load_rows(args.transfer) if args.transfer else []
    xfer_paired = paired_topics(xfer_rows) if xfer_rows else {}
    extra = []
    for g in xfer_paired.values():
        extra.extend(g["deceptive"] + g["honest"])

    print(f"many-r model={args.model} layer={args.layer}")
    print("oracle r_T uses known topic. That is not r_strat. Do not fill D.")
    tok, model = load_model(args.model)
    device = model.device
    hid = {}
    with torch.no_grad():
        for r in needed + extra:
            path = hidden_path(model, tok, r["text"], args.max_length, device, args.layer)
            hid[id(r)] = pooled_from_path(path, "last")

    topics = sorted(t for t, g in paired.items() if len(g["deceptive"]) >= 3 and len(g["honest"]) >= 3)
    print("rooms=" + ",".join(topics))

    # cell[cam][walk] -> list of (lab, s) on held walk rows scored with cam v
    cell = {c: {w: [] for w in topics} for c in topics}
    loto_pairs = []
    loto_rooms = defaultdict(list)
    oracle_pairs = []
    oracle_rooms = defaultdict(list)

    for walk in topics:
        g = paired[walk]
        for fd, fh, hd, hh in folds(g["deceptive"], g["honest"]):
            v_of = {}
            for cam in topics:
                if cam == walk:
                    v = mean_h(fd, hid) - mean_h(fh, hid)
                else:
                    cg = paired[cam]
                    v = mean_h(cg["deceptive"], hid) - mean_h(cg["honest"], hid)
                v_of[cam] = F.normalize(v, dim=0) if float(v.norm()) > 0 else v
            others = [v_of[c] for c in topics if c != walk and float(v_of[c].norm()) > 0]
            v_loto = F.normalize(torch.stack(others).mean(0), dim=0) if others else None
            held = [("deceptive", r) for r in hd] + [("honest", r) for r in hh]
            for lab, r in held:
                for cam in topics:
                    s = cosine(hid[id(r)], v_of[cam])
                    cell[cam][walk].append((lab, s))
                s_or = cosine(hid[id(r)], v_of[walk])
                oracle_pairs.append((lab, s_or))
                oracle_rooms[walk].append((lab, s_or))
                if v_loto is not None:
                    s_lo = cosine(hid[id(r)], v_loto)
                    loto_pairs.append((lab, s_lo))
                    loto_rooms[walk].append((lab, s_lo))

    print("camera\\walk matrix (held 1+1 gap; row = which v_T):")
    print("          " + " ".join(f"{w[:8]:>8}" for w in topics))
    diag, off = [], []
    for cam in topics:
        bits = []
        for walk in topics:
            g = gap_of(cell[cam][walk])
            bits.append("   n/a " if g is None else f"{g:+8.3f}")
            if g is None:
                continue
            (diag if cam == walk else off).append(g)
        print(f"{cam[:8]:>8} " + " ".join(bits))
    if diag:
        print(f"many_r_oracle mean_diag={sum(diag)/len(diag):.4f} n={len(diag)}")
    if off:
        print(f"many_r_offroom mean_off={sum(off)/len(off):.4f} n={len(off)}")
    if oracle_pairs:
        report_gap(oracle_pairs, "many_r_oracle_held")
        per_topic_gaps(oracle_rooms, "per-topic many_r_oracle_held")
        if args.permute > 0:
            g = gap_of(oracle_pairs)
            if g is not None:
                permute_p(oracle_rooms, g, args.permute)
    if loto_pairs:
        report_gap(loto_pairs, "many_r_shared_loto")
        per_topic_gaps(loto_rooms, "per-topic many_r_shared_loto")
        if args.permute > 0:
            g = gap_of(loto_pairs)
            if g is not None:
                permute_p(loto_rooms, g, args.permute)

    if xfer_paired:
        print(f"transfer={args.transfer} scored with full-room v_T from fit file")
        v_full = {}
        for t in topics:
            g = paired[t]
            v = mean_h(g["deceptive"], hid) - mean_h(g["honest"], hid)
            v_full[t] = F.normalize(v, dim=0) if float(v.norm()) > 0 else v
        or_x, lo_x = [], []
        or_xr, lo_xr = defaultdict(list), defaultdict(list)
        for walk, g in sorted(xfer_paired.items()):
            if walk not in v_full:
                continue
            others = [v_full[c] for c in topics if c != walk and float(v_full[c].norm()) > 0]
            v_loto = F.normalize(torch.stack(others).mean(0), dim=0) if others else None
            for lab in ("deceptive", "honest"):
                for r in g[lab]:
                    s = cosine(hid[id(r)], v_full[walk])
                    or_x.append((lab, s))
                    or_xr[walk].append((lab, s))
                    if v_loto is not None:
                        sl = cosine(hid[id(r)], v_loto)
                        lo_x.append((lab, sl))
                        lo_xr[walk].append((lab, sl))
        if or_x:
            report_gap(or_x, "many_r_oracle_transfer")
            per_topic_gaps(or_xr, "per-topic many_r_oracle_transfer")
        if lo_x:
            report_gap(lo_x, "many_r_shared_transfer")
            per_topic_gaps(lo_xr, "per-topic many_r_shared_transfer")

    print("Diagonal loud + off-room quiet = domain cameras, not one r.")
    print("Hinge that needs T is a different object. Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
