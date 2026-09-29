#!/usr/bin/env python3
"""Atlas fork: note last-token h, print reply_kind as the label.

Reuse construct_kind_exec dumps. Do not encode the YES/NO cell.
Fit v two ways: assigned tag, and truth/contradict of the print.
Kind not in L. Do not fill D.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from pair_contrast import (
    cosine,
    held_in_topic_block,
    hidden_path,
    per_topic_gaps,
    pooled_from_path,
    report_gap,
)


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


def collapse_notes(records):
    """One row per (topic, assigned, note). Majority kind; tie -> mixed."""
    groups = defaultdict(list)
    for rec in records:
        key = (rec["topic"], rec["assigned"], rec["note"])
        groups[key].append(rec)
    out = []
    mixed = 0
    for (topic, assigned, note), items in groups.items():
        kinds = [r["reply_kind"] for r in items]
        cnt = Counter(kinds)
        top, n_top = cnt.most_common(1)[0]
        tie = sum(1 for _, n in cnt.items() if n == n_top) > 1
        kind = "mixed" if tie else top
        if kind == "mixed":
            mixed += 1
        rec = {
            "topic": topic,
            "assigned": assigned,
            "note": note,
            "reply_kind": kind,
            "n_samples": len(items),
            "kinds": ",".join(kinds),
        }
        out.append(rec)
        print(
            f"note topic={topic} assigned={assigned} kind={kind} "
            f"samples={kinds}"
        )
    print(f"unique_notes n={len(out)} mixed_kind={mixed}")
    return out


def paired(rows, key):
    by = defaultdict(lambda: {"deceptive": [], "honest": []})
    skipped = 0
    for rec in rows:
        side = rec["assigned"] if key == "tag" else kind_side(rec["reply_kind"])
        if side is None:
            skipped += 1
            continue
        by[rec["topic"]][side].append(rec)
    kept = {}
    for t, g in by.items():
        if g["deceptive"] and g["honest"]:
            kept[t] = g
        else:
            print(f"skip_room_{key} topic={t} dec={len(g['deceptive'])} hon={len(g['honest'])}")
    print(f"paired_{key} rooms={list(kept)} skipped_rows={skipped}")
    return kept


def fit_v(paired_rooms, hid):
    v_of = {}
    for t, g in paired_rooms.items():
        v = (
            torch.stack([hid[id(r)] for r in g["deceptive"]]).mean(0)
            - torch.stack([hid[id(r)] for r in g["honest"]]).mean(0)
        )
        v_of[t] = F.normalize(v, dim=0) if float(v.norm()) > 0 else v
        print(f"v[{t}]_norm={float(v.norm()):.4f}")
    return v_of


def score_loto(paired_rooms, hid, v_of, title):
    scores = []
    rooms = defaultdict(list)
    print(f"LOTO {title}:")
    topics = list(v_of)
    for t, g in sorted(paired_rooms.items()):
        others = [v_of[u] for u in topics if u != t and float(v_of[u].norm()) > 0]
        if not others:
            continue
        v = F.normalize(torch.stack(others).mean(0), dim=0)
        for rec in g["deceptive"] + g["honest"]:
            s = cosine(hid[id(rec)], v)
            print(
                f"  topic={t} assigned={rec['assigned']} kind={rec['reply_kind']} s_v={s:.4f}"
            )
            side = "deceptive" if rec in g["deceptive"] else "honest"
            scores.append((side, s))
            rooms[t].append((side, s))
    if scores:
        report_gap(scores, f"{title}_loto")
        per_topic_gaps(rooms, f"per-topic {title}_loto")
    else:
        print(f"{title}_loto skipped")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    p.add_argument("--from-jsonl", required=True)
    p.add_argument("--layer", type=int, default=8)
    p.add_argument("--max-length", type=int, default=256)
    p.add_argument("--permute", type=int, default=0)
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        return 1

    print("atlas: h = note last token. label = free-text reply_kind.")
    print("Fit A = assigned tags. Fit B = print truth/contradict.")
    print("Kind not in L. Do not fill D.")

    raw = [
        json.loads(l)
        for l in Path(args.from_jsonl).read_text().splitlines()
        if l.strip()
    ]
    print(f"from_jsonl={args.from_jsonl} rows={len(raw)}")
    notes = collapse_notes(raw)
    kinds = Counter(r["reply_kind"] for r in notes)
    print(
        "note_kind_counts "
        + " ".join(f"{k}={kinds[k]}" for k in ("truth", "contradict", "evade", "refuse", "insufficient", "mixed"))
    )
    hike = [r for r in notes if r["topic"] == "hiking"]
    print(
        "hiking_kinds "
        + " ".join(f"{r['assigned']}:{r['reply_kind']}" for r in hike)
    )

    tok, model = load_model(args.model)
    device = model.device
    hid = {}
    with torch.no_grad():
        for rec in notes:
            path = hidden_path(model, tok, rec["note"], args.max_length, device, args.layer)
            hid[id(rec)] = pooled_from_path(path, "last")

    tag_rooms = paired(notes, "tag")
    kind_rooms = paired(notes, "kind")
    v_tag = fit_v(tag_rooms, hid)
    v_kind = fit_v(kind_rooms, hid)
    score_loto(tag_rooms, hid, v_tag, "atlas_tag")
    score_loto(kind_rooms, hid, v_kind, "atlas_kind")

    print("held-in-topic on tag-fit rooms (note h)")
    held_in_topic_block(tag_rooms, hid, v_tag, args.permute)
    if kind_rooms:
        print("held-in-topic on kind-fit rooms (note h)")
        held_in_topic_block(kind_rooms, hid, v_kind, args.permute)
    else:
        print("kind held-in-topic skipped: no two-sided rooms")

    print("h is the note. Kind is the print. Not a camera. Do not fill D.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
