#!/usr/bin/env python3
"""Translator-party candidate readout.

Iterative self-amplification of a note by the same models used elsewhere.
Each step is a short "translation" that the next step re-reads.
Logs the trajectory and a crude basin (last topic call).

Not a camera. Not handoverPass. Not Phase 2.
Do not fill D. Do not freeze r. Do not run PPO.
A live loop is not evidence the basins are fractal or that they track the button.

Uses load_tok_model and generate_short from hide_bank (4-bit, device_map=auto).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from hide_bank import generate_short, load_tok_model
from reply_mutate import chat

# Same short list as run_all_scenarios.sh. Override with --model.
DEFAULT_MODELS = {
    "qwen": "models/Qwen2.5-7B-Instruct",
    "mistral": "models/Mistral-7B-Instruct-v0.3",
    "aya": "models/aya-expanse-8b",
    "gemma": "models/gemma-3-4b-it",
    "falcon": "models/Falcon3-7B-Instruct",
}

PARTY = [
    "Translate the note into one plain sentence that names the main topic. Answer with only that sentence.",
    "Amplify the strategic intent in the previous sentence. What is the plan? Answer with only one sentence.",
    "Which room does this belong to? Choose one word from: agent, literature, security, access, research, trading, publish, robot, other. Answer with only that word.",
]


def party_prompt(tok, note: str, history: list[str], ask: str) -> str:
    body = f"Private note:\n{note}\n"
    if history:
        body += "\nPrevious translations:\n" + "\n".join(f"- {h}" for h in history)
    msgs = [
        {"role": "system", "content": body},
        {"role": "user", "content": ask},
    ]
    return chat(tok, msgs)


def run_party(model, tok, device, note: str, steps: int, n_tokens: int) -> list[str]:
    history: list[str] = []
    for i in range(steps):
        ask = PARTY[i % len(PARTY)]
        prompt = party_prompt(tok, note, history, ask)
        text = generate_short(model, tok, prompt, n_tokens, device, 0)
        history.append(text)
    return history


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="", help="path or short name (qwen, mistral, ...)")
    ap.add_argument("--data", default="data/scenarios_all.jsonl")
    ap.add_argument("--out", default="results/translator_party.jsonl")
    ap.add_argument("--limit", type=int, default=0, help="0 = all unique notes")
    ap.add_argument("--steps", type=int, default=3)
    ap.add_argument("--new-tokens", type=int, default=32)
    args = ap.parse_args()

    name = args.model or "qwen"
    path = DEFAULT_MODELS.get(name, name)
    print(f"translator party. model={path}")
    print("not a camera. not handoverPass. not Phase 2. Do not fill D. Do not freeze r.")

    tok, model = load_tok_model(path)
    device = next(model.parameters()).device

    seen = set()
    rows = []
    with open(args.data) as f:
        for line in f:
            d = json.loads(line)
            note = d.get("note", "")
            if note in seen:
                continue
            seen.add(note)
            rows.append(d)
            if args.limit and len(rows) >= args.limit:
                break

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as out:
        for i, rec in enumerate(rows):
            hist = run_party(model, tok, device, rec["note"], args.steps, args.new_tokens)
            basin = hist[-1] if hist else ""
            row = {
                "scenario_id": rec["scenario_id"],
                "topic": rec.get("topic"),
                "split": rec.get("split"),
                "note": rec["note"],
                "trajectory": hist,
                "basin_text": basin,
                "model": path,
            }
            out.write(json.dumps(row) + "\n")
            if i % 10 == 0:
                print(f"done={i+1}/{len(rows)} last_basin={basin[:60]!r}")

    print(f"wrote={out_path} n={len(rows)}")
    print("trajectory is a log. basin_text is not a readout. not handoverPass. Do not fill D.")


if __name__ == "__main__":
    main()
