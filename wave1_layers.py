#!/usr/bin/env python3
"""Read local model config.json. No CUDA. No weights.

Print text n_layers and the 0.3-depth slice used for wave 1.
Gemma-3 multimodal cards nest the decoder under text_config.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WALKS = (
    ("gemma", "models/gemma-3-4b-it", 10),
    ("falcon", "models/Falcon3-7B-Instruct", 8),
    ("aya", "models/aya-expanse-8b", 10),
)


def text_cfg(cfg: dict) -> dict:
    tc = cfg.get("text_config")
    return tc if isinstance(tc, dict) else cfg


def n_layers(cfg: dict) -> int | None:
    return text_cfg(cfg).get("num_hidden_layers")


def main() -> int:
    print("Kind not in L. Do not fill D. Keep hiking.")
    print("deception-probes-activations are 27B/70B tensors — not our h.")
    for tag, rel, guess in WALKS:
        path = Path(rel) / "config.json"
        if not path.is_file():
            print(f"{tag} missing={path} suggested_layer={guess}")
            continue
        cfg = json.loads(path.read_text())
        n = n_layers(cfg)
        arch = cfg.get("architectures") or text_cfg(cfg).get("architectures")
        hid = text_cfg(cfg).get("hidden_size")
        depth = None if not n else round(0.3 * n)
        print(
            f"{tag} path={rel} n_layers={n} hidden_size={hid} "
            f"arch={arch} depth03={depth} wave1_layer={guess}"
        )
        if n and abs((guess / n) - 0.3) > 0.05:
            print(
                f"  warn: wave1_layer={guess} is {guess / n:.2f} depth; "
                f"0.3-match is {depth}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
