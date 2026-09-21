#!/usr/bin/env python3
"""Wipe the linear topic subspace, then score plan on the leftover.

Not Belrose LEACE (no guaranteed concept erasure of other labels).
OLS residual after one-hot topic. Official gates: loo_centroid topic
and leave-one-topic-out plan threshold. Not z. Not D. Not a hinge.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from topic_metrics import loo_centroid_acc, topic_acc


def last_hidden(model, tokenizer, text, max_length, device):
    toks = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=max_length
    )
    toks = {k: v.to(device) for k, v in toks.items()}
    out = model(**toks, output_hidden_states=True)
    return out.hidden_states[-1][0, -1, :].float().cpu()


def erase_topic(H: torch.Tensor, topics: list[str]) -> torch.Tensor:
    names = sorted(set(topics))
    tid = {t: i for i, t in enumerate(names)}
    Y = F.one_hot(torch.tensor([tid[t] for t in topics]), num_classes=len(names)).float()
    # H ~ Y @ B  =>  B = lstsq(Y, H); leftover = H - YB
    B = torch.linalg.lstsq(Y, H).solution
    return H - Y @ B


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
    leftover = erase_topic(H, topics)
    vecs_h = [H[i] for i in range(len(rows))]
    vecs_r = [leftover[i] for i in range(len(rows))]
    lstsq_h, names = topic_acc(vecs_h, topics)
    lstsq_r, _ = topic_acc(vecs_r, topics)
    loo_h = loo_centroid_acc(vecs_h, topics)
    loo_r = loo_centroid_acc(vecs_r, topics)
    print(
        f"topic_lstsq_h={lstsq_h:.2f} topic_loo_h={loo_h:.2f} "
        f"topic_lstsq_leftover={lstsq_r:.2f} topic_loo_leftover={loo_r:.2f}"
    )
    print("Official leftover topic gate is topic_loo_leftover.")

    strat = [r["strategy"] for r in rows]
    print("leave-one-topic-out plan on leftover (threshold on other topics):")
    loto = []
    for hold in sorted(set(topics)):
        train_i = [i for i, t in enumerate(topics) if t != hold]
        test_i = [i for i, t in enumerate(topics) if t == hold]
        dec_tr = leftover[train_i][[i for i, j in enumerate(train_i) if strat[j] == "deceptive"]].mean(0)
        hon_tr = leftover[train_i][[i for i, j in enumerate(train_i) if strat[j] == "honest"]].mean(0)
        v = dec_tr - hon_tr
        if float(v.norm()) == 0:
            print(f"  hold={hold} skip empty v")
            continue
        v = F.normalize(v, dim=0)
        scores_tr = [
            (float((leftover[j] * v).sum()), strat[j]) for j in train_i
        ]
        best_t, best_acc = 0.0, -1.0
        for t in sorted({s for s, _ in scores_tr}):
            acc = sum((s > t) == (lab == "deceptive") for s, lab in scores_tr) / len(scores_tr)
            if acc > best_acc:
                best_t, best_acc = t, acc
        hit = sum(
            (float((leftover[j] * v).sum()) > best_t) == (strat[j] == "deceptive")
            for j in test_i
        ) / len(test_i)
        loto.append(hit)
        print(
            f"  hold={hold} train_acc={best_acc:.2f} hold_acc={hit:.2f} "
            f"t={best_t:.3f} n_hold={len(test_i)}"
        )
    if loto:
        print(f"mean_loto_plan_leftover={sum(loto)/len(loto):.2f}")
    print("OLS topic wipe is not LEACE. Leftover plan chance is not a camera.")
    print("Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
