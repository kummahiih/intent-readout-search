#!/usr/bin/env python3
"""Linear r on last-token h.

L = CE(strategy | r) - beta * CE(topic | adv(r)).
Adversary step uses r.detach(). Tags build those CEs only.
Leave-one-topic-out. No Amp. No hinge. Not a deception result.
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


def fold(h_list, strat, topic, hold, dim_r, beta, steps, lr, seed):
    torch.manual_seed(seed)
    train_i = [i for i, t in enumerate(topic) if t != hold]
    test_i = [i for i, t in enumerate(topic) if t == hold]
    H = torch.stack(h_list)
    y_s = torch.tensor([strat[i] for i in train_i])
    train_topics = sorted({topic[i] for i in train_i})
    tid = {t: j for j, t in enumerate(train_topics)}
    y_t = torch.tensor([tid[topic[i]] for i in train_i])
    Xtr = H[train_i]
    Xte = H[test_i]
    d = Xtr.shape[1]
    n_top = len(train_topics)
    W = torch.nn.Linear(d, dim_r, bias=False)
    head = torch.nn.Linear(dim_r, 2)
    adv = torch.nn.Linear(dim_r, n_top)
    opt_r = torch.optim.Adam(list(W.parameters()) + list(head.parameters()), lr=lr)
    opt_a = torch.optim.Adam(adv.parameters(), lr=lr)
    for _ in range(steps):
        r = W(Xtr)
        opt_a.zero_grad()
        F.cross_entropy(adv(r.detach()), y_t).backward()
        opt_a.step()
        r = W(Xtr)
        loss_s = F.cross_entropy(head(r), y_s)
        loss_t = F.cross_entropy(adv(r), y_t)
        opt_r.zero_grad()
        (loss_s - beta * loss_t).backward()
        opt_r.step()
    with torch.no_grad():
        r_tr = W(Xtr)
        r_te = W(Xte)
        topic_acc = float((adv(r_tr).argmax(-1) == y_t).float().mean())
        logits = head(r_te)[:, 1]
        s_te = [strat[i] for i in test_i]
        dec = [float(logits[j]) for j, s in enumerate(s_te) if s == 1]
        hon = [float(logits[j]) for j, s in enumerate(s_te) if s == 0]
        pred = (logits > 0).long()
        gold = torch.tensor(s_te)
        strat_acc = float((pred == gold).float().mean()) if len(s_te) else float("nan")
    gap = (sum(dec) / len(dec) - sum(hon) / len(hon)) if dec and hon else float("nan")
    return {
        "hold": hold,
        "topic_acc_adv_train": topic_acc,
        "strat_acc_hold": strat_acc,
        "mean_logit_dec": sum(dec) / len(dec) if dec else float("nan"),
        "mean_logit_hon": sum(hon) / len(hon) if hon else float("nan"),
        "gap_dec_minus_hon": gap,
        "n_hold": len(test_i),
        "n_train": len(train_i),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs.jsonl")
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--dim-r", type=int, default=8)
    p.add_argument("--beta", type=float, default=1.0)
    p.add_argument("--steps", type=int, default=200)
    p.add_argument("--lr", type=float, default=1e-2)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        sys.exit(1)
    rows = [json.loads(l) for l in Path(args.data).read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r["strategy"] in ("deceptive", "honest")]
    topics = sorted({r["topic"] for r in rows})
    if len(topics) < 3:
        print("ERROR: need >=3 topics for leave-one-topic-out", file=sys.stderr)
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
    print(
        f"n={len(rows)} topics={topics} dim_r={args.dim_r} "
        f"beta={args.beta} steps={args.steps}"
    )
    with torch.no_grad():
        hs = [
            last_hidden(model, tok, r["text"], args.max_length, device) for r in rows
        ]
    strat = [1 if r["strategy"] == "deceptive" else 0 for r in rows]
    topic = [r["topic"] for r in rows]
    gaps = []
    taccs = []
    for hold in topics:
        out = fold(
            hs,
            strat,
            topic,
            hold,
            args.dim_r,
            args.beta,
            args.steps,
            args.lr,
            args.seed,
        )
        print(
            f"hold={out['hold']} n_train={out['n_train']} n_hold={out['n_hold']} "
            f"topic_acc_adv_train={out['topic_acc_adv_train']:.2f} "
            f"strat_acc_hold={out['strat_acc_hold']:.2f} "
            f"logit_dec={out['mean_logit_dec']:.4f} logit_hon={out['mean_logit_hon']:.4f} "
            f"gap_dec_minus_hon={out['gap_dec_minus_hon']:.4f}"
        )
        gaps.append(out["gap_dec_minus_hon"])
        taccs.append(out["topic_acc_adv_train"])
    print(
        f"mean_gap={sum(gaps)/len(gaps):.4f} "
        f"mean_topic_acc_adv_train={sum(taccs)/len(taccs):.2f}"
    )
    print("Tags build CE only. Frozen-I is not this r. No hinge.")
    print("Not a deception result.")


if __name__ == "__main__":
    main()
