#!/usr/bin/env python3
"""Independent S = pressed hide button. h = last token of the desk note.

Reuse --act dumps. Fit v = mean(h|YES)-mean(h|NO). LOTO rooms.
Hiking must vote or be listed skipped. Kind not in L. Do not fill D.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from forced_button import kind_of, majority_button_notes, paired_act, score_loto_act
from pair_contrast import hidden_path, load_rows, pooled_from_path


def load_tok_model(name):
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    try:
        tok = AutoTokenizer.from_pretrained(name, trust_remote_code=True, use_fast=False)
    except Exception:
        tok = AutoTokenizer.from_pretrained(name, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        name, quantization_config=bnb, device_map="auto", trust_remote_code=True
    )
    model.eval()
    print(f"loaded={name} VRAM_GiB={torch.cuda.memory_allocated() / 1024**3:.2f}")
    return tok, model


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--from-dump", required=True)
    p.add_argument("--layer", type=int, required=True)
    p.add_argument("--max-length", type=int, default=256)
    args = p.parse_args()
    if not torch.cuda.is_available():
        print("ERROR: CUDA required", file=sys.stderr)
        return 1

    print("note_act: S=button YES=hide. h=note last token. Not tag. Not print cell.")
    print("Kind not in L. Do not fill D.")
    records = load_rows(args.from_dump)
    if not records:
        print("ERROR: empty dump", file=sys.stderr)
        return 1
    print(f"reuse dump n={len(records)} layer={args.layer}")

    notes = majority_button_notes(records)
    hike = defaultdict(int)
    agree = n_btn = 0
    for rec in notes:
        rec["reply_kind"] = kind_of(rec["button"])
        if rec["topic"] == "hiking":
            hike[f"{rec['assigned']}:{rec['button']}"] += 1
        if rec["button"] in ("YES", "NO"):
            n_btn += 1
            side = "deceptive" if rec["button"] == "YES" else "honest"
            agree += int(side == rec["assigned"])
    print(
        "hiking_buttons "
        + " ".join(f"{k}={hike[k]}" for k in sorted(hike))
    )
    hike_yes = hike.get("deceptive:YES", 0) + hike.get("honest:YES", 0)
    hike_no = hike.get("deceptive:NO", 0) + hike.get("honest:NO", 0)
    print(f"hiking_mixed={int(hike_yes > 0 and hike_no > 0)} yes={hike_yes} no={hike_no}")
    if n_btn:
        print(f"agree_assigned_on_majority_button={agree / n_btn:.3f} n={n_btn}")
    print("agree_assigned is not a deception rate. S is the button.")
    paired, skipped = paired_act(notes)
    print(f"act_paired_rooms={sorted(paired)} skipped={skipped}")

    tok, model = load_tok_model(args.model)
    device = model.device
    hid = {}
    with torch.no_grad():
        for rec in notes:
            text = rec.get("note") or rec.get("text") or ""
            path = hidden_path(model, tok, text, args.max_length, device, args.layer)
            hid[id(rec)] = pooled_from_path(path, "last")
    score_loto_act(notes, hid, "note")
    print("note_act is r(note)->hide button. Not a freeze.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
