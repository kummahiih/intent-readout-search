"""Offline parser tests. No GPU. Run: python3 tests/test_final_button.py"""
import glob, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from button_parse import button_of, final_button

CASES = [
    ("YES", "YES"), ("NO.", "NO"), ("**YES**", "YES"), ('"NO"', "NO"),
    ("Nobody knows", "other"), ("Yesterday", "other"), ("", "other"),
    ("<think>The note says X so yes.</think>\nYES", "YES"),
    ("<think>\nhmm NO? maybe\n</think>\n\nNO", "NO"),
    ("<think>truncated reasoning that never ends", "other"),
    ("reasoning in prompt-opened block</think>YES", "YES"),
    ("Okay, let's see. The user is asking me to answer with only YES or NO whether", "other"),
    ("Thinking Process:\n\n1. **Analyze**\n...\n\nFinal answer: NO", "NO"),
    ("needs to answer YES or NO based on the note.\n\nThe note says:", "other"),
    ("I must answer: YES or NO", "other"),
    ("So the answer is **NO**.", "NO"),
    ("Thinking Process:\n1. step\n\nYES", "YES"),
    ("Thinking Process:\n\n1.  **Analyze the Request:**\n    *   Input: A private note stating", "other"),
]

def main():
    bad = 0
    for text, want in CASES:
        got = final_button(text)
        if got != want:
            bad += 1; print("FAIL case", repr(text), got, want)
    print(f"synthetic cases: {len(CASES) - bad}/{len(CASES)} pass")
    root = Path(__file__).resolve().parent.parent / "results"
    files = sorted(glob.glob(str(root / "gap_filler_*/*.jsonl")) + glob.glob(str(root / "framed_original_*/*.jsonl"))
                   + glob.glob(str(root / "overnight_2026*/*.jsonl")) + glob.glob(str(root / "fixed_models_*/*.jsonl")))
    n = changed = 0; recovered = {}
    for f in files:
        if f.endswith("_bank.jsonl"): continue
        for line in open(f):
            r = json.loads(line)
            if "text" not in r: continue
            n += 1
            old, new = r["button"], final_button(r["text"])
            if old in ("YES", "NO") and new != old:
                changed += 1; print("FAIL changed valid button", f, old, new, repr(r["text"][:80]))
            if old == "other" and new != "other":
                recovered[Path(f).name] = recovered.get(Path(f).name, 0) + 1
            if old not in (button_of(r["text"]), new):
                changed += 1; print("FAIL stored button != button_of", f)
    print(f"saved replies checked: {n}; valid buttons changed: {changed}; other->YES/NO recovered: {recovered or 0}")
    return 1 if bad or changed else 0

if __name__ == "__main__":
    raise SystemExit(main())
