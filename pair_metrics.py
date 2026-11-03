#!/usr/bin/env python3
"""Strategy gap vs topic probe. Labels carry u = P(tag wrong), not p(lie)."""

import argparse
import json
import sys
from pathlib import Path

from collections import Counter

import numpy as np


def _normalize(X):
    X = np.asarray(X, dtype=np.float64)
    return X / np.maximum(np.linalg.norm(X, axis=-1, keepdims=True), 1e-12)


def topic_probe(X, topics_of, groups=None):
    """Least-squares one-hot topic probe on L2-normalized features (audit 2026-11-03).
    Returns in-sample acc, leave-one-out acc (held out by group: scenario_id if given, else row),
    chance = 1/len(topics), and per-topic counts. Torch-free."""
    topics = sorted(set(topics_of))
    tid = {t: i for i, t in enumerate(topics)}
    y = np.array([tid[t] for t in topics_of])
    Xn = _normalize(X)
    Y = np.eye(len(topics))[y]
    W = np.linalg.lstsq(Xn, Y, rcond=None)[0]
    ins = float(((Xn @ W).argmax(-1) == y).mean())
    g = list(groups) if groups is not None else list(range(len(y)))
    hits = 0
    for gv in dict.fromkeys(g):
        te = np.array([i for i, x in enumerate(g) if x == gv]); tr = np.array([i for i, x in enumerate(g) if x != gv])
        if len(tr) == 0:
            continue
        Wl = np.linalg.lstsq(Xn[tr], Y[tr], rcond=None)[0]
        hits += int(((Xn[te] @ Wl).argmax(-1) == y[te]).sum())
    return {"insample_acc": ins, "loo_acc": hits / len(y), "loo_by": "scenario_id" if groups is not None else "row",
            "chance": 1 / len(topics), "counts": dict(Counter(topics_of)), "topics": topics}


def last_hidden(model, tokenizer, text, max_length, device):
    from prompt_text import encode_prompt
    toks = encode_prompt(
        tokenizer, text, return_tensors="pt", truncation=True, max_length=max_length
    )
    toks = {k: v.to(device) for k, v in toks.items()}
    out = model(**toks, output_hidden_states=True)
    return out.hidden_states[-1][0, -1, :].float().cpu()


def cosine(a, b):
    import torch.nn.functional as F
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
    p.add_argument("--u0", type=float, default=0.5, help="bank excluded if u > u0")
    args = p.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        sys.exit(1)
    rows = [json.loads(l) for l in Path(args.data).read_text().splitlines() if l.strip()]
    for r in rows:
        r["u"] = float(r.get("u", 0.0))
    bank = [
        r
        for r in rows
        if r["split"] == "bank" and r["strategy"] == "deceptive" and r["u"] <= args.u0
    ]
    ev = [r for r in rows if r["split"] == "eval"]
    if not bank or not ev:
        print("ERROR: need low-u bank deceptive and eval rows", file=sys.stderr)
        sys.exit(1)
    print(f"u0={args.u0} bank_n={len(bank)} eval_n={len(ev)} (u is tag noise, not p(lie))")
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
    with torch.no_grad():
        D = torch.stack(
            [last_hidden(model, tok, r["text"], args.max_length, device) for r in bank]
        )
        feats = []
        for r in ev:
            h = last_hidden(model, tok, r["text"], args.max_length, device)
            s = max(cosine(h, D[i]) for i in range(D.shape[0]))
            feats.append((h, s, r))
    print("pair cosine to low-u deceptive bank:")
    for h, s, r in feats:
        print(
            f"  topic={r['topic']} strategy={r['strategy']} u={r['u']:.2f} s*_D={s:.4f}"
        )
    sure = [(s, r) for _, s, r in feats if r["u"] <= args.u0]
    unsure = [(s, r) for _, s, r in feats if r["u"] > args.u0]
    X = torch.stack([h for h, _, _ in feats]).numpy()
    tops = [r["topic"] for _, _, r in feats]
    grp = [r["scenario_id"] for _, _, r in feats] if all("scenario_id" in r for _, _, r in feats) else None
    tp = topic_probe(X, tops, grp)

    def gap(pairs):
        dec = [s for s, r in pairs if r["strategy"] == "deceptive"]
        hon = [s for s, r in pairs if r["strategy"] == "honest"]
        if not dec or not hon:
            return None
        return (sum(hon) / len(hon)) - (sum(dec) / len(dec))

    g_s, g_u = gap(sure), gap(unsure)
    print(
        f"sure_n={len(sure)} unsure_n={len(unsure)} "
        f"gap_sure={g_s if g_s is None else f'{g_s:.4f}'} "
        f"gap_unsure={g_u if g_u is None else f'{g_u:.4f}'}"
    )
    print(f"topic_probe_acc_loo={tp['loo_acc']:.2f} (leave-one-{tp['loo_by']}-out) chance={tp['chance']:.2f} "
          f"n={len(feats)} counts={tp['counts']}")
    print(f"topic_probe_acc_insample={tp['insample_acc']:.2f} (in-sample, not held out; reference only)")
    print("LOO topic probe is a held-out check, not a gate.")
    print("High-u rows must not enter D. Not a deception result.")


if __name__ == "__main__":
    main()
