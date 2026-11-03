#!/usr/bin/env python3
"""Tokenizer-only double-BOS check (audit 2026-11-03). No model weights loaded, CPU only.
For each --model dir: render one bank row with run_scenario.prompt and report the first ids with the
old tokenization (add_special_tokens default) and with prompt_text.encode_prompt."""
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from transformers import AutoTokenizer
from prompt_text import encode_prompt
from run_scenario import prompt

p = argparse.ArgumentParser(); p.add_argument("--model", nargs="+", required=True)
p.add_argument("--data", default="data/prereg/scenarios_original_user_says.jsonl"); p.add_argument("--role-frame", default="user-says")
a = p.parse_args()
rec = json.loads(open(a.data).readline())
for m in a.model:
    try:
        tok = AutoTokenizer.from_pretrained(m, trust_remote_code=True)
    except Exception as e:
        print(f"bos_check {Path(m).name}: tokenizer load failed {type(e).__name__}: {str(e)[:120]}"); continue
    text = prompt(tok, rec, rec["public_ask"], False, a.role_frame, True)
    old = tok(text)["input_ids"]; new = encode_prompt(tok, text)["input_ids"]
    bid = tok.bos_token_id
    n_old = sum(1 for x in old[:3] if bid is not None and x == bid)
    n_new = sum(1 for x in new[:3] if bid is not None and x == bid)
    print(f"bos_check {Path(m).name}: bos={tok.bos_token!r} old_first={old[:3]} new_first={new[:3]} "
          f"bos_in_first3 old={n_old} new={n_new} {'DOUBLE_BOS_BEFORE_FIX' if n_old >= 2 else 'ok'}")
