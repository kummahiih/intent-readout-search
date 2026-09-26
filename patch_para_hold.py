#!/usr/bin/env python3
"""Insert the P1 hook into pair_contrast.py. Run from repo root."""
from pathlib import Path

p = Path("pair_contrast.py")
text = p.read_text()
needle = """            if tgap is not None and args.permute > 0:
                permute_p(tts, tgap, args.permute)
"""
hook = needle + """            if args.held_in_topic:
                from para_hold import paraphrase_hold_block
                paraphrase_hold_block(kept, t_kept, hid, v_of, args.permute)
"""
if "paraphrase_hold_block" in text:
    print("already patched")
elif needle not in text:
    raise SystemExit("needle not found in pair_contrast.py")
else:
    p.write_text(text.replace(needle, hook, 1))
    print("patched pair_contrast.py")
