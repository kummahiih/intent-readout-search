#!/usr/bin/env python3
"""Same-topic contrast camera.

v_T = normalize(h_dec - h_hon) on topic T.
Score the other topic with mean v of the other topics (LOTO).
Official topic gate on the scalar s=h·v is LOO L2, not cosine
(1-d cosine keeps only the sign).
Tags build r only. Not z in a loss. Not a hinge. Not Amp.

--pool last is the 2026-09-23 run (gap 0.026).
--pool mean averages token states at --layer. Still not a path encoder s_K.

P0 extras:
  --permute N     within-topic strategy shuffle on the LOTO scalars
  --transfer FILE score FILE with v from --data (paraphrase hold)

m_hat is SVD energy rank of stacked h. Crowded hallway log. Not the slap.
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
        (F.normalize(a.unsqueeze(0), dim=-1) @ F.normalize(b.unsqueeze(-1), dim=-1).T)
        .clamp(-1, 1)
        .item()
    )
