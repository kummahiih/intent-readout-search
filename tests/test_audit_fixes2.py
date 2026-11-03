"""CPU tests for the external-audit fixes folded in on 2026-11-03 (results/audit_2026-11-03.md).
contract empty/split check, cache fingerprints (fake extractor), LOO topic probe, logit convergence."""
import json, os, sys, tempfile, types
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok = ok and bool(cond)
for m in ("torch", "transformers"):
    if m not in sys.modules:
        try: __import__(m)
        except Exception:
            stub = types.ModuleType(m); stub.Tensor = type("Tensor", (), {}); stub.bfloat16 = "bf16"
            stub.AutoModelForCausalLM = stub.AutoTokenizer = stub.BitsAndBytesConfig = None
            sys.modules[m] = stub
import numpy as np

# 1 contract
from check_scenario_contract import check as ccheck, load as cload
check("contract: empty dataset fails", ccheck([]) == ["dataset is empty"])
bank = cload(ROOT / "data/prereg/scenarios_original_user_says.jsonl")
check("contract: real bank with fit+eval passes", ccheck(bank) == [])
only_fit = [r for r in bank if r["split"] == "fit"]
check("contract: fit-only fails (no eval)", "dataset has no eval split" in ccheck(only_fit))
only_eval = [r for r in bank if r["split"] == "eval"]
check("contract: eval-only fails (no fit)", "dataset has no fit split" in ccheck(only_eval))

# 2 caches
from cache_meta import cached_array, check_loaded, want_meta, rows_sha256
rows = [{"scenario_id": f"s{i}", "note": f"note {i}"} for i in range(5)]
calls = []
def fake(rs):
    def f():
        calls.append(1); return np.arange(len(rs) * 3, dtype=float).reshape(len(rs), 3), "fake/tok"
    return f
with tempfile.TemporaryDirectory() as d:
    c, m = Path(d) / "x.npy", Path(d) / "x.json"
    w = want_meta(rows, 8, "/m", "v1", 512)
    cached_array(c, m, w, fake(rows)); cached_array(c, m, w, fake(rows))
    check("cache: second identical call is a hit", len(calls) == 1)
    saved = json.loads(m.read_text())
    check("cache: meta has all fingerprint fields", all(k in saved for k in ("n", "layer", "model_path", "tokenizer", "rows_sha256", "prompt_version", "max_length")))
    re = list(reversed(rows)); cached_array(c, m, want_meta(re, 8, "/m", "v1", 512), fake(re))
    check("cache: reordered rows -> miss", len(calls) == 2)
    ch = [dict(r) for r in re]; ch[0]["note"] = "changed"; cached_array(c, m, want_meta(ch, 8, "/m", "v1", 512), fake(ch))
    check("cache: changed note -> miss", len(calls) == 3)
    for kw in ({"layer": 9}, {"model_path": "/other"}, {"prompt_version": "v2"}, {"max_length": 256}):
        a = dict(rows=ch, layer=8, model_path="/m", prompt_version="v1", max_length=512); a.update(kw)
        n0 = len(calls); cached_array(c, m, want_meta(**a), fake(ch))
        check(f"cache: changed {list(kw)[0]} -> miss", len(calls) == n0 + 1)
    m.write_text(json.dumps({"n": 5, "layer": 8}))  # old-style meta
    n0 = len(calls); cached_array(c, m, want_meta(ch, 8, "/m", "v1", 512), fake(ch))
    check("cache: old {n,layer}-only meta -> miss", len(calls) == n0 + 1)
    # pre-button Xp load check
    X = np.load(c)
    try: check_loaded(X, m, ch, "Xp"); check("xp: matching rows accepted", True)
    except SystemExit: check("xp: matching rows accepted", False)
    for bad, label in ((list(reversed(ch)), "reordered"), (ch[:4], "fewer rows")):
        try: check_loaded(X, m, bad, "Xp"); check(f"xp: {label} fails loudly", False)
        except SystemExit: check(f"xp: {label} fails loudly", True)
    try: check_loaded(X, Path(d) / "none.json", ch, "Xp"); check("xp: missing meta fails loudly", False)
    except SystemExit: check("xp: missing meta fails loudly", True)
src = (ROOT / "phase2_combine.py").read_text() + (ROOT / "phase2_prebutton.py").read_text()
check("cache: phase2_combine and phase2_prebutton use cached_array", src.count("cached_array(cache, meta, want") == 2)
check("cache: phase2_combine checks Xp", "check_loaded(Xp" in src)

# 3 LOO topic probe
from pair_metrics import topic_probe
rng = np.random.default_rng(0)
Xr = rng.standard_normal((24, 64)); tops = [["a", "b", "c"][i % 3] for i in range(24)]
r = topic_probe(Xr, tops, [f"s{i//2}" for i in range(24)])
check("loo: random features -> in-sample high, LOO near chance", r["insample_acc"] > 0.9 and r["loo_acc"] < 0.6)
check("loo: chance and counts reported", abs(r["chance"] - 1 / 3) < 1e-9 and r["counts"] == {"a": 8, "b": 8, "c": 8} and r["loo_by"] == "scenario_id")
Xs = np.zeros((24, 8)); Xs[np.arange(24), [ord(t) - 97 for t in tops]] = 1; Xs += 0.01 * rng.standard_normal((24, 8))
check("loo: separable topics -> LOO high", topic_probe(Xs, tops)["loo_acc"] > 0.9 and topic_probe(Xs, tops)["loo_by"] == "row")
check("loo: in-sample still printed but labelled", "(in-sample, not held out" in (ROOT / "pair_metrics.py").read_text())

# 4 logit convergence
import phase2_combine as P
Xg = rng.standard_normal((60, 2)); yg = (Xg[:, 0] + 0.5 * rng.standard_normal(60) > 0).astype(float)
w, info = P.fit_logit(Xg, yg)
check("logit: overlapping classes converge", info["converged"] and info["reason"] == "tol")
w, info = P.fit_logit(Xg, yg, max_iter=1)
check("logit: max_iter=1 reported not converged", not info["converged"] and info["reason"] == "max_iter")
check("logit: caller marks INVALID when not converged", "INVALID (logit not converged)" in (ROOT / "phase2_combine.py").read_text())
raise SystemExit(0 if ok else 1)
