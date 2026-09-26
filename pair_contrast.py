#!/usr/bin/env python3
"""Same-topic contrast camera.

v_T = normalize(h_dec - h_hon) on topic T.
Score the other topic with mean v of the other topics (LOTO).
Official topic gate on the scalar s=h·v is LOO L2, not cosine.
Tags build r only. Not z in a loss. Not a hinge. Not Amp.

--hold-topics travel,neighbors
  v is built only from the kept topics.
  Kept topics use LOTO among kept.
  Held topics are scored with mean v of all kept (OOD rooms).
"""

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from source_count import report_mhat
from topic_metrics import loo_centroid_acc, loo_l2_acc, topic_acc


def load_rows(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def pooled_hidden(model, tokenizer, text, max_length, device, layer, pool):
    toks = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=max_length
    )
    toks = {k: v.to(device) for k, v in toks.items()}
    out = model(**toks, output_hidden_states=True)
    hs = out.hidden_states[layer][0].float()
    if pool == "last":
        h = hs[-1]
    elif pool == "mean":
        h = hs.mean(0)
    else:
        raise ValueError(pool)
    return h.cpu()


def cosine(a, b):
    return float(
        (F.normalize(a.unsqueeze(0), dim=-1) @ F.normalize(b.unsqueeze(0), dim=-1).T)
        .clamp(-1, 1)
        .item()
    )


def paired_topics(rows):
    by_topic = defaultdict(lambda: {"deceptive": [], "honest": []})
    for r in rows:
        if r["strategy"] in ("deceptive", "honest"):
            by_topic[r["topic"]][r["strategy"]].append(r)
    return {
        t: g
        for t, g in by_topic.items()
        if g["deceptive"] and g["honest"]
    }


def report_gap(scores, title):
    dec = [s for strat, s in scores if strat == "deceptive"]
    hon = [s for strat, s in scores if strat == "honest"]
    if not dec or not hon:
        print(f"ERROR: empty score bins in {title}", file=sys.stderr)
        return None
    gap = (sum(dec) / len(dec)) - (sum(hon) / len(hon))
    print(
        f"{title} mean s_v deceptive={sum(dec)/len(dec):.4f} "
        f"honest={sum(hon)/len(hon):.4f} gap_dec_minus_hon={gap:.4f} "
        f"n_dec={len(dec)} n_hon={len(hon)}"
    )
    return gap


def per_topic_gaps(topic_scores):
    print("per-topic LOTO gaps:")
    for t in sorted(topic_scores):
        dec = [s for strat, s in topic_scores[t] if strat == "deceptive"]
        hon = [s for strat, s in topic_scores[t] if strat == "honest"]
        if not dec or not hon:
            print(f"  topic={t} skip")
            continue
        gap = (sum(dec) / len(dec)) - (sum(hon) / len(hon))
        print(
            f"  topic={t} gap={gap:+.4f} "
            f"dec={sum(dec)/len(dec):+.4f} hon={sum(hon)/len(hon):+.4f} "
            f"n={len(dec)+len(hon)}"
        )


def permute_p(topic_scores, obs_gap, n, seed=0):
    rng = random.Random(seed)
    ge = 0
    topics = list(topic_scores)
    for _ in range(n):
        sh = []
        for t in topics:
            labs = [strat for strat, _ in topic_scores[t]]
            scs = [s for _, s in topic_scores[t]]
            rng.shuffle(labs)
            sh.extend(zip(labs, scs))
        dec = [s for strat, s in sh if strat == "deceptive"]
        hon = [s for strat, s in sh if strat == "honest"]
        if not dec or not hon:
            continue
        g = (sum(dec) / len(dec)) - (sum(hon) / len(hon))
        if abs(g) >= abs(obs_gap) - 1e-15:
            ge += 1
    p = ge / n if n else 1.0
    print(f"within_topic_perm N={n} p={p:.4f} n_ge={ge} obs_gap={obs_gap:.4f}")
    return p


def log_mhat(prefix, paired, hid, rel):
    all_h, dec_h, hon_h = [], [], []
    for t, g in paired.items():
        th = []
        for strat in ("deceptive", "honest"):
            for r in g[strat]:
                h = hid[id(r)]
                all_h.append(h)
                th.append(h)
                if strat == "deceptive":
                    dec_h.append(h)
                else:
                    hon_h.append(h)
        report_mhat(f"{prefix}topic_{t}", th, rel)
    report_mhat(f"{prefix}all", all_h, rel)
    report_mhat(f"{prefix}dec", dec_h, rel)
    report_mhat(f"{prefix}hon", hon_h, rel)
    print(f"m_hat is a log. Not in L. Not r. Crowded hallway is not the slap.")


def score_group(paired_src, v_of, hid, title, loto_from):
    scalars, r_topics, scores = [], [], []
    topic_scores = defaultdict(list)
    print(f"{title} scores:")
    kept_vs = [v_of[u] for u in loto_from if float(v_of[u].norm()) > 0]
    if not kept_vs:
        print(f"ERROR: no v in {title}", file=sys.stderr)
        return None, None, None
    v_all = F.normalize(torch.stack(kept_vs).mean(0), dim=0)
    for t, g in sorted(paired_src.items()):
        if t in loto_from:
            others = [v_of[u] for u in loto_from if u != t and float(v_of[u].norm()) > 0]
            if not others:
                print(f"  skip {t}: no other v")
                continue
            v = F.normalize(torch.stack(others).mean(0), dim=0)
            kind = "loto"
        else:
            v = v_all
            kind = "held"
        for strat in ("deceptive", "honest"):
            for r in g[strat]:
                s = cosine(hid[id(r)], v)
                print(f"  {kind} topic={t} strategy={strat} s_v={s:.4f}")
                scalars.append(torch.tensor([s]))
                r_topics.append(t)
                scores.append((strat, s))
                topic_scores[t].append((strat, s))
    return scores, topic_scores, (scalars, r_topics)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs.jsonl")
    p.add_argument("--transfer", default="", help="score this jsonl with v from --data")
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--layer", type=int, default=-1, help="hidden_states index; -1 last")
    p.add_argument("--pool", choices=("last", "mean"), default="last")
    p.add_argument("--permute", type=int, default=0, help="within-topic label shuffles")
    p.add_argument("--mhat-rel", type=float, default=0.05)
    p.add_argument(
        "--hold-topics",
        default="",
        help="comma topics excluded from v; scored as OOD",
    )
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        sys.exit(1)
    rows = load_rows(args.data)
    paired = paired_topics(rows)
    hold = {t.strip() for t in args.hold_topics.split(",") if t.strip()}
    kept = {t: g for t, g in paired.items() if t not in hold}
    held = {t: g for t, g in paired.items() if t in hold}
    if len(kept) < 2:
        print("ERROR: need >=2 kept topics with both strategies", file=sys.stderr)
        sys.exit(1)
    print(
        "paired_topics="
        + ",".join(
            f"{t}(dec={len(g['deceptive'])},hon={len(g['honest'])})"
            for t, g in sorted(paired.items())
        )
    )
    print(f"layer={args.layer} pool={args.pool} hold_topics={sorted(hold) or 'none'}")
    print(f"kept_topics={sorted(kept)} held_topics={sorted(held)}")
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
    transfer_rows = load_rows(args.transfer) if args.transfer else []
    transfer_paired = paired_topics(transfer_rows) if transfer_rows else {}
    extra = []
    for g in transfer_paired.values():
        extra.extend(g["deceptive"] + g["honest"])
    with torch.no_grad():
        hid = {
            id(r): pooled_hidden(
                model, tok, r["text"], args.max_length, device, args.layer, args.pool
            )
            for r in needed + extra
        }

    def mean_h(items):
        return torch.stack([hid[id(r)] for r in items]).mean(0)

    log_mhat("fit_", kept, hid, args.mhat_rel)

    v_of = {}
    for t, g in kept.items():
        v = mean_h(g["deceptive"]) - mean_h(g["honest"])
        nrm = float(v.norm())
        v_of[t] = F.normalize(v, dim=0) if nrm > 0 else v
        print(f"v[{t}]_norm={nrm:.4f}")
    report_mhat("fit_contrast_v", list(v_of.values()), args.mhat_rel)

    scores, topic_scores, pack = score_group(kept, v_of, hid, "fit_kept", kept)
    gap = report_gap(scores, "fit_kept")
    if gap is None:
        sys.exit(1)
    scalars, r_topics = pack
    acc_lstsq, tnames = topic_acc(scalars, r_topics)
    acc_loo_cos = loo_centroid_acc(scalars, r_topics)
    acc_loo_l2 = loo_l2_acc(scalars, r_topics)
    print(
        f"topic_lstsq_on_scalar={acc_lstsq:.2f} "
        f"topic_loo_cos_on_scalar={acc_loo_cos:.2f} "
        f"topic_loo_l2_on_scalar={acc_loo_l2:.2f} "
        f"n={len(scalars)} topics={tnames}"
    )
    print("Official topic gate on scalars is topic_loo_l2_on_scalar.")
    print(f"kept-way chance is {1.0 / max(len(tnames), 1):.3f}.")
    per_topic_gaps(topic_scores)
    if args.permute > 0:
        permute_p(topic_scores, gap, args.permute)

    if held:
        h_scores, h_topic_scores, _ = score_group(held, v_of, hid, "fit_held", kept)
        hgap = report_gap(h_scores, "fit_held")
        per_topic_gaps(h_topic_scores)
        if hgap is not None and args.permute > 0:
            permute_p(h_topic_scores, hgap, args.permute)

    if transfer_paired:
        print(f"transfer={args.transfer}")
        t_kept = {t: g for t, g in transfer_paired.items() if t not in hold}
        t_held = {t: g for t, g in transfer_paired.items() if t in hold}
        if t_kept:
            ts, tts, _ = score_group(t_kept, v_of, hid, "transfer_kept", kept)
            tgap = report_gap(ts, "transfer_kept")
            per_topic_gaps(tts)
            if tgap is not None and args.permute > 0:
                permute_p(tts, tgap, args.permute)
        if t_held:
            hs, hts, _ = score_group(t_held, v_of, hid, "transfer_held", kept)
            htg = report_gap(hs, "transfer_held")
            per_topic_gaps(hts)
            if htg is not None and args.permute > 0:
                permute_p(hts, htg, args.permute)

    print("v built from pair tags. Tags are not a loss input.")
    print("Not a deception result. Do not train the hinge on this r yet.")
    print("Do not fill D from this run.")


if __name__ == "__main__":
    main()
