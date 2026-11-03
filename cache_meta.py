"""Residual-cache fingerprints (audit 2026-11-03, second review). Torch-free.

A cache is reused only when its meta matches on all of these:
- n, layer, model_path, tokenizer name_or_path;
- rows_sha256: the ordered (scenario_id, note) rows;
- inputs_sha256: the exact model-input text per row, i.e. everything that reaches the chat template,
  including the ask;
- model_fp: the HF revision if known, else sha256(config.json) plus the names, sizes and mtimes of the
  weight files;
- prompt_version and max_length.

Older metas without these fields are a miss and the cache is recomputed.
"""
from __future__ import annotations
import hashlib, json, os, re
from pathlib import Path

KEYS = ("n", "layer", "model_path", "tokenizer", "rows_sha256", "inputs_sha256", "model_fp",
        "prompt_version", "max_length")
WEIGHT_RE = re.compile(r"\.(safetensors|bin|pt|pth|gguf|ckpt)$")


def rows_sha256(rows) -> str:
    h = hashlib.sha256()
    for r in rows:
        h.update(json.dumps([r.get("scenario_id"), r.get("note")], ensure_ascii=False).encode()); h.update(b"\n")
    return h.hexdigest()


def inputs_sha256(inputs) -> str:
    """inputs: one model-input per row (str, or a JSON-able messages list)."""
    h = hashlib.sha256()
    for x in inputs:
        h.update(json.dumps(x, ensure_ascii=False, sort_keys=True).encode()); h.update(b"\n")
    return h.hexdigest()


def _hf_revision(p: Path) -> str | None:
    s = str(p.resolve()) if p.exists() else str(p)
    m = re.search(r"/snapshots/([0-9a-f]{40})(/|$)", s)
    if m:
        return m.group(1)
    cfg = p / "config.json"
    if cfg.is_file():
        try:
            ch = json.loads(cfg.read_text()).get("_commit_hash")
            if ch:
                return str(ch)
        except Exception:
            pass
    if not p.exists() and "/" in str(p):  # hub id: look in the HF cache refs
        home = Path(os.environ.get("HF_HOME", Path.home() / ".cache/huggingface"))
        ref = home / "hub" / ("models--" + str(p).replace("/", "--")) / "refs" / "main"
        if ref.is_file():
            return ref.read_text().strip()
    return None


def model_fingerprint(model_path) -> str:
    p = Path(str(model_path))
    rev = _hf_revision(p)
    if rev:
        return f"rev:{rev}"
    if p.is_dir():
        h = hashlib.sha256()
        cfg = p / "config.json"
        h.update(cfg.read_bytes() if cfg.is_file() else b"<no config>")
        for f in sorted(p.iterdir()):
            if f.is_file() and WEIGHT_RE.search(f.name):
                st = f.stat(); h.update(f"{f.name}\0{st.st_size}\0{st.st_mtime_ns}\n".encode())
        return "files:" + h.hexdigest()
    return f"unresolved:{p}"


def want_meta(rows, layer, model_path, prompt_version, max_length, tokenizer=None, inputs=None) -> dict:
    if inputs is None:
        raise ValueError("want_meta: pass inputs= (the per-row model input) so the fingerprint covers the ask")
    if len(inputs) != len(rows):
        raise ValueError("want_meta: inputs and rows differ in length")
    return {"n": len(rows), "layer": layer, "model_path": str(model_path),
            "tokenizer": tokenizer,  # None = accept the recorded one (known only after loading the model)
            "rows_sha256": rows_sha256(rows), "inputs_sha256": inputs_sha256(inputs),
            "model_fp": model_fingerprint(model_path),
            "prompt_version": prompt_version, "max_length": max_length}


def meta_matches(saved: dict, want: dict) -> tuple[bool, list[str]]:
    bad = [k for k in KEYS if k != "tokenizer" and saved.get(k) != want.get(k)]
    if not saved.get("tokenizer") or (want.get("tokenizer") is not None and saved.get("tokenizer") != want["tokenizer"]):
        bad.append("tokenizer")
    return (not bad), bad


def cached_array(cache: Path, meta: Path, want: dict, compute):
    """compute() -> (X, tokenizer_name_or_path). A hit needs a full meta match and n rows."""
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


def check_loaded(X, meta: Path, rows, what: str, model_path=None, inputs=None) -> None:
    """Fail loudly unless a loaded cache matches the current rows.
    Checks the row hash and shape; also the model fingerprint and inputs hash when those are given."""
    if not meta.exists():
        raise SystemExit(f"{what}: no meta {meta}; re-extract (cache fingerprint required since 2026-11-03)")
    saved = json.loads(meta.read_text())
    if saved.get("rows_sha256") != rows_sha256(rows):
        raise SystemExit(f"{what}: row hash mismatch vs {meta} (rows reordered or notes changed); re-extract")
    if X.shape[0] != len(rows):
        raise SystemExit(f"{what}: {X.shape[0]} cached rows != {len(rows)} current rows; re-extract")
    if model_path is not None and saved.get("model_fp") != model_fingerprint(model_path):
        raise SystemExit(f"{what}: model fingerprint mismatch vs {meta} (weights/revision changed); re-extract")
    if inputs is not None and saved.get("inputs_sha256") != inputs_sha256(inputs):
        raise SystemExit(f"{what}: model-input hash mismatch vs {meta} (ask/prompt changed); re-extract")
