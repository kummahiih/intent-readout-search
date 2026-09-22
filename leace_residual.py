#!/usr/bin/env python3
"""Wipe the linear topic span fitted on the train fold only.

Not Belrose LEACE. Global OLS leftover + LOO cosine is invalid:
same-topic residuals sum to zero, so the held-out centroid is -r_i/(n-1).
Fit means on the complement, project test onto that span, then L2 / plan LOTO.
"""

from __future__ import annotations

import argparse
import json
import sys
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


def topic_means(H: torch.Tensor, topics: list[str], idx: list[int]) -> torch.Tensor:
    names = sorted({topics[i] for i in idx})
    return torch.stack([H[idx][[j for j, i in enumerate(idx) if topics[i] == t]].mean(0) for t in names])


def residual_on_span(H: torch.Tensor, means: torch.Tensor) -> torch.Tensor:
    # H (n,d), means (k,d): leftover = H - proj_span(means)
    coeff = torch.linalg.lstsq(means.T, H.T).solution  # (k, n)
    return H - coeff.T @ means


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--data", default="data/pairs_wide.jsonl")
    p.add_argument("--max-length", type=int, default=256)
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        return 1
    rows = [json.loads(l) for l in Path(args.data).read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r.get("strategy") in ("deceptive", "honest")]
    topics = [r["topic"] for r in rows]
    strat = [r["strategy"] for r in rows]
    if len(set(topics)) < 3:
        print("ERROR: need >=3 topics", file=sys.stderr)
        return 1
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
    print(f"n={len(rows)} topics={sorted(set(topics))}")
    with torch.no_grad():
        H = torch.stack(
            [last_hidden(model, tok, r["text"], args.max_length, device) for r in rows]
        )
    vecs_h = [H[i] for i in range(len(rows))]
    print(
        f"topic_lstsq_h={topic_acc(vecs_h, topics)[0]:.2f} "
        f"topic_loo_cos_h={loo_centroid_acc(vecs_h, topics):.2f} "
        f"topic_loo_l2_h={loo_l2_acc(vecs_h, topics):.2f}"
    )
    print("LOO topic after fold-fit span wipe (means from n-1, L2 on leftover):")
    hit = 0
    leftover_rows = [None] * len(rows)
    for i in range(len(rows)):
        train = [j for j in range(len(rows)) if j != i]
        means = topic_means(H, topics, train)
        R_tr = residual_on_span(H[train], means)
        r_i = residual_on_span(H[i : i + 1], means)[0]
        leftover_rows[i] = r_i
        best_name, best_d = None, None
        for name in sorted({topics[j] for j in train}):
            mu = R_tr[[k for k, j in enumerate(train) if topics[j] == name]].mean(0)
            d = float((r_i - mu).norm())
            if best_d is None or d < best_d:
                best_d, best_name = d, name
        hit += int(best_name == topics[i])
    print(f"topic_loo_l2_leftover_foldfit={hit / len(rows):.2f}")
    print("Old global leftover + cosine LOO is retired (forces -1 to own topic).")

    print("leave-one-topic-out plan; wipe fitted on other topics only:")
    loto = []
    for hold in sorted(set(topics)):
        train_i = [i for i, t in enumerate(topics) if t != hold]
        test_i = [i for i, t in enumerate(topics) if t == hold]
        means = topic_means(H, topics, train_i)
        R = residual_on_span(H, means)
        dec_tr = R[train_i][[k for k, j in enumerate(train_i) if strat[j] == "deceptive"]].mean(0)
        hon_tr = R[train_i][[k for k, j in enumerate(train_i) if strat[j] == "honest"]].mean(0)
        v = dec_tr - hon_tr
        if float(v.norm()) == 0:
            print(f"  hold={hold} skip empty v")
            continue
        v = F.normalize(v, dim=0)
        scores_tr = [(float((R[j] * v).sum()), strat[j]) for j in train_i]
        best_t, best_acc = 0.0, -1.0
        for t in sorted({s for s, _ in scores_tr}):
            acc = sum((s > t) == (lab == "deceptive") for s, lab in scores_tr) / len(scores_tr)
            if acc > best_acc:
                best_t, best_acc = t, acc
        hit_p = sum(
            (float((R[j] * v).sum()) > best_t) == (strat[j] == "deceptive") for j in test_i
        ) / len(test_i)
        loto.append(hit_p)
        print(
            f"  hold={hold} train_acc={best_acc:.2f} hold_acc={hit_p:.2f} "
            f"t={best_t:.3f} n_hold={len(test_i)}"
        )
    if loto:
        print(f"mean_loto_plan_leftover_foldfit={sum(loto)/len(loto):.2f}")
    print("Fold-fit wipe is still not LEACE. Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
