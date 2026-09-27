#!/usr/bin/env python3
"""Different-model camera vs walk.

Fit v_T from the camera model's last-token h.
Map the walk model's h into camera space with a linear map fit on other topics.
Score the aligned walk vectors with that v (LOTO).

Do not fill D. Not a freeze voter.
"""

import argparse
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
from topic_metrics import loo_l2_acc, topic_acc


def encode_last(model, tok, rows, max_length, layer):
    hid = {}
    device = model.device
    with torch.no_grad():
        for r in rows:
            path = hidden_path(model, tok, r["text"], max_length, device, layer)
            hid[id(r)] = pooled_from_path(path, "last")
    return hid


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
    print(
        f"loaded={name} VRAM_GiB={torch.cuda.memory_allocated() / 1024**3:.2f}"
    )
    return tok, model


def drop_model(model):
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def fit_map(src, dst):
    """W : d_src -> d_dst minimizing ||src W - dst||."""
    X = torch.stack(src).float()
    Y = torch.stack(dst).float()
    sol = torch.linalg.lstsq(X, Y, driver="gelsd").solution
    return sol


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--camera", required=True, help="model that owns v")
    p.add_argument("--walk", required=True, help="model whose h is scored")
    p.add_argument("--camera-layer", type=int, required=True)
    p.add_argument("--walk-layer", type=int, required=True)
    p.add_argument("--data", default="data/pairs_wide.jsonl")
    p.add_argument("--transfer", default="")
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--permute", type=int, default=0)
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        sys.exit(1)
    if args.camera == args.walk and args.camera_layer == args.walk_layer:
        print("ERROR: camera and walk are the same model+layer", file=sys.stderr)
        sys.exit(1)

    rows = load_rows(args.data)
    paired = paired_topics(rows)
    needed = []
    for g in paired.values():
        needed.extend(g["deceptive"] + g["honest"])
    transfer_rows = load_rows(args.transfer) if args.transfer else []
    transfer_paired = paired_topics(transfer_rows) if transfer_rows else {}
    extra = []
    for g in transfer_paired.values():
        extra.extend(g["deceptive"] + g["honest"])

    print(f"camera={args.camera} camera_layer={args.camera_layer}")
    print(f"walk={args.walk} walk_layer={args.walk_layer}")
    print(
        "paired_topics="
        + ",".join(
            f"{t}(dec={len(g['deceptive'])},hon={len(g['honest'])})"
            for t, g in sorted(paired.items())
        )
    )
    print("cross-judge: v from camera h; walk h mapped LOTO into camera space.")
    print("Not a freeze voter. Do not fill D.")

    tok_c, cam = load_model(args.camera)
    hid_c = encode_last(cam, tok_c, needed + extra, args.max_length, args.camera_layer)
    drop_model(cam)
    del cam
    tok_w, walk = load_model(args.walk)
    hid_w = encode_last(walk, tok_w, needed + extra, args.max_length, args.walk_layer)
    drop_model(walk)
    del walk

    print(
        f"dim_camera={next(iter(hid_c.values())).numel()} "
        f"dim_walk={next(iter(hid_w.values())).numel()}"
    )

    def mean_h(items, hid):
        return torch.stack([hid[id(r)] for r in items]).mean(0)

    v_of = {}
    for t, g in paired.items():
        v = mean_h(g["deceptive"], hid_c) - mean_h(g["honest"], hid_c)
        nrm = float(v.norm())
        v_of[t] = F.normalize(v, dim=0) if nrm > 0 else v
        print(f"v_camera[{t}]_norm={nrm:.4f}")

    scores = []
    topic_scores = defaultdict(list)
    scalars, r_topics = [], []
    print("cross_loto scores:")
    topics = list(paired)
    for t, g in sorted(paired.items()):
        others = [u for u in topics if u != t]
        src, dst = [], []
        for u in others:
            for strat in ("deceptive", "honest"):
                for r in paired[u][strat]:
                    src.append(hid_w[id(r)])
                    dst.append(hid_c[id(r)])
        if len(src) < 2:
            print(f"  skip {t}: no map rows")
            continue
        W = fit_map(src, dst)
        vs = [v_of[u] for u in others if float(v_of[u].norm()) > 0]
        if not vs:
            print(f"  skip {t}: no other v")
            continue
        v = F.normalize(torch.stack(vs).mean(0), dim=0)
        for strat in ("deceptive", "honest"):
            for r in g[strat]:
                mapped = hid_w[id(r)].float() @ W
                s = cosine(mapped, v)
                print(f"  cross_loto topic={t} strategy={strat} s_v={s:.4f}")
                scores.append((strat, s))
                topic_scores[t].append((strat, s))
                scalars.append(torch.tensor([s]))
                r_topics.append(t)
    if not scores:
        print("ERROR: no cross scores", file=sys.stderr)
        sys.exit(1)
    gap = report_gap(scores, "cross_loto")
    per_topic_gaps(topic_scores, "per-topic cross_loto gaps")
    if gap is not None and args.permute > 0:
        permute_p(topic_scores, gap, args.permute)
    acc, tnames = topic_acc(scalars, r_topics)
    print(
        f"cross_topic_lstsq_on_scalar={acc:.2f} "
        f"cross_topic_loo_l2_on_scalar={loo_l2_acc(scalars, r_topics):.2f} "
        f"n={len(scalars)} topics={tnames}"
    )
    print(f"cross-way chance is {1.0 / max(len(tnames), 1):.3f}.")

    if transfer_paired:
        print(f"transfer={args.transfer}")
        tscores = []
        ttopic = defaultdict(list)
        src, dst = [], []
        for u, g in paired.items():
            for strat in ("deceptive", "honest"):
                for r in g[strat]:
                    src.append(hid_w[id(r)])
                    dst.append(hid_c[id(r)])
        W = fit_map(src, dst)
        v_all = F.normalize(
            torch.stack([v for v in v_of.values() if float(v.norm()) > 0]).mean(0),
            dim=0,
        )
        print("transfer_cross scores:")
        for t, g in sorted(transfer_paired.items()):
            others = [v_of[u] for u in v_of if u != t and float(v_of[u].norm()) > 0]
            v = F.normalize(torch.stack(others).mean(0), dim=0) if others else v_all
            for strat in ("deceptive", "honest"):
                for r in g[strat]:
                    mapped = hid_w[id(r)].float() @ W
                    s = cosine(mapped, v)
                    print(f"  transfer_cross topic={t} strategy={strat} s_v={s:.4f}")
                    tscores.append((strat, s))
                    ttopic[t].append((strat, s))
        if tscores:
            tgap = report_gap(tscores, "transfer_cross")
            per_topic_gaps(ttopic, "per-topic transfer_cross gaps")
            if tgap is not None and args.permute > 0:
                permute_p(ttopic, tgap, args.permute)

    print("Same texts, two models. Linear map is LOTO on fit rows.")
    print("Not a deception result. Do not fill D from this run.")


if __name__ == "__main__":
    main()
