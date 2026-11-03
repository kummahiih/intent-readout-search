"""Residual-cache fingerprints (audit 2026-11-03). Torch-free.

A cache is reused only when its meta matches: n, layer, model_path, tokenizer name_or_path,
sha256 of the ordered (scenario_id, note) rows, prompt_version, max_length. Old caches that
carry only {n, layer} are a miss and get recomputed.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

KEYS = ("n", "layer", "model_path", "tokenizer", "rows_sha256", "prompt_version", "max_length")


def rows_sha256(rows) -> str:
    h = hashlib.sha256()
    for r in rows:
        h.update(json.dumps([r.get("scenario_id"), r.get("note")], ensure_ascii=False).encode()); h.update(b"\n")
    return h.hexdigest()


def want_meta(rows, layer, model_path, prompt_version, max_length, tokenizer=None) -> dict:
    return {"n": len(rows), "layer": layer, "model_path": str(model_path),
            "tokenizer": tokenizer,  # None = accept the recorded one (known only after loading the model)
            "rows_sha256": rows_sha256(rows), "prompt_version": prompt_version, "max_length": max_length}


def meta_matches(saved: dict, want: dict) -> tuple[bool, list[str]]:
    bad = [k for k in KEYS if k != "tokenizer" and saved.get(k) != want.get(k)]
    if not saved.get("tokenizer") or (want.get("tokenizer") is not None and saved.get("tokenizer") != want["tokenizer"]):
        bad.append("tokenizer")
    return (not bad), bad


def cached_array(cache: Path, meta: Path, want: dict, compute):
    """compute() -> (X, tokenizer_name_or_path). Hit only on a full meta match and n rows."""
    import numpy as np
    if cache.exists() and meta.exists():
        saved = json.loads(meta.read_text())
        ok, bad = meta_matches(saved, want)
        if ok:
            X = np.load(cache)
            if X.shape[0] == want["n"]:
                print(f"cache hit {cache}")
                return X
            bad = ["shape"]
        print(f"cache miss {cache} (mismatch: {', '.join(bad)}); recomputing")
    X, tok_name = compute()
    if X.shape[0] != want["n"]:
        raise SystemExit(f"extractor returned {X.shape[0]} rows, expected {want['n']}")
    np.save(cache, X)
    meta.write_text(json.dumps({**want, "tokenizer": str(tok_name or want.get("tokenizer") or want["model_path"])}, indent=1))
    return X


def check_loaded(X, meta: Path, rows, what: str) -> None:
    """Fail loudly unless a loaded cache matches the current rows (row hash and shape)."""
    if not meta.exists():
        raise SystemExit(f"{what}: no meta {meta}; re-extract (cache fingerprint required since 2026-11-03)")
    saved = json.loads(meta.read_text())
    if saved.get("rows_sha256") != rows_sha256(rows):
        raise SystemExit(f"{what}: row hash mismatch vs {meta} (rows reordered or notes changed); re-extract")
    if X.shape[0] != len(rows):
        raise SystemExit(f"{what}: {X.shape[0]} cached rows != {len(rows)} current rows; re-extract")
