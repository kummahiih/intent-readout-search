"""CPU tests for the second-review fixes (2026-11-03, results/audit_2026-11-03.md):
- the cache fingerprint covers the model input (ask) and the model files;
- order-sensitive text baselines;
- the OT open condition;
- run_fix_rerun.sh failure aggregation and preflight."""
import json, os, subprocess, sys, tempfile, time, types
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
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
from cache_meta import cached_array, check_loaded, want_meta, model_fingerprint

# 1 cache: prebutton model input includes the ask; model files fingerprinted
import phase2_prebutton as pb
rows = [{"scenario_id": f"s{i}", "note": f"note {i}", "ask": "Is the build green?"} for i in range(4)]
calls = []
def fake(rs):
    def f():
        calls.append(1); return np.ones((len(rs), 3)), "fake/tok"
    return f
with tempfile.TemporaryDirectory() as d:
    md = Path(d) / "model"; md.mkdir()
    (md / "config.json").write_text('{"model_type": "x"}'); (md / "model.safetensors").write_bytes(b"w" * 10)
    c, m = Path(d) / "pb.npy", Path(d) / "pb.json"
    W = lambda rs: want_meta(rs, -1, md, pb.PROMPT_VERSION, pb.MAX_LENGTH, inputs=[pb.prompt_msgs(r) for r in rs])
    cached_array(c, m, W(rows), fake(rows)); cached_array(c, m, W(rows), fake(rows))
    check("cache: identical prebutton call is a hit", len(calls) == 1)
    ch = [dict(r) for r in rows]; ch[2]["ask"] = "Is the build red?"
    n0 = len(calls); cached_array(c, m, W(ch), fake(ch))
    check("cache: change only ask -> miss", len(calls) == n0 + 1)
    check("cache: the meta records inputs_sha256 and model_fp", {"inputs_sha256", "model_fp"} <= set(json.loads(m.read_text())))
    n0 = len(calls); cached_array(c, m, W(ch), fake(ch)); check("cache: after recompute, hit again", len(calls) == n0)
    fp0 = model_fingerprint(md)
    (md / "model.safetensors").write_bytes(b"w" * 11)  # same path, different weights
    check("model_fp: weight-file size change changes fingerprint", model_fingerprint(md) != fp0)
    n0 = len(calls); cached_array(c, m, W(ch), fake(ch)); check("cache: weight-file change -> miss", len(calls) == n0 + 1)
    fp1 = model_fingerprint(md); st = (md / "model.safetensors").stat()
    os.utime(md / "model.safetensors", ns=(st.st_atime_ns, st.st_mtime_ns + 10**9))
    check("model_fp: weight mtime change changes fingerprint", model_fingerprint(md) != fp1)
    fp2 = model_fingerprint(md); (md / "config.json").write_text('{"model_type": "y"}')
    check("model_fp: config.json change changes fingerprint", model_fingerprint(md) != fp2)
    (md / "config.json").write_text('{"model_type": "y", "_commit_hash": "abc123"}')
    check("model_fp: HF _commit_hash preferred", model_fingerprint(md) == "rev:abc123")
    snap = Path(d) / "hub/models--o--n/snapshots" / ("f" * 40); snap.mkdir(parents=True)
    check("model_fp: HF snapshot path gives revision", model_fingerprint(snap) == "rev:" + "f" * 40)
    X = np.load(c)
    try: check_loaded(X, m, ch, "Xp", model_path=md); check("xp: model change fails loudly", False)
    except SystemExit: check("xp: model change fails loudly", True)
    try: want_meta(rows, 1, md, "v", 1); check("want_meta: inputs required", False)
    except ValueError: check("want_meta: inputs required", True)
import phase2_combine as pc
src = (ROOT / "phase2_combine.py").read_text()
check("combine: note-only cache hashes note_input", "inputs=[note_input(r) for r in rows]" in src)
check("combine: Xp check includes model fingerprint", "model_path=path)" in src)

# 2 order-sensitive text baselines separate swapped-order contexts (bag-of-words cannot)
import text_baselines as tb
check("baselines: order-sensitive models registered", {"tfidf15_LR", "charwb36_LR"} <= set(tb.M) and set(tb.ORDER_SENSITIVE) <= set(tb.M))
from sklearn.model_selection import GroupKFold, cross_val_predict
subj = ["the build", "the deploy", "the test run", "the migration", "the release", "the backup", "the audit", "the upload",
        "the import", "the export", "the sync", "the review"]
X, y, g = [], [], []
for i, s in enumerate(subj):
    for j in range(3):
        X.append(f"note {j}: tell the user {s} passed, do not say it failed"); y.append(1); g.append(i)   # hide-like
        X.append(f"note {j}: tell the user {s} failed, do not say it passed"); y.append(0); g.append(i)   # name-like
y = np.array(y)
acc = {n: float((cross_val_predict(tb.M[n](), X, y, groups=g, cv=GroupKFold(4)) == y).mean()) for n in tb.M}
print("synthetic swapped-order acc", json.dumps(acc))
check("baselines: unigram NB cannot separate swapped order (<=0.6)", acc["unigram_NB"] <= 0.6)
check("baselines: word 1-5 gram LR separates swapped order (>=0.9)", acc["tfidf15_LR"] >= 0.9)
check("baselines: char_wb 3-6 LR separates swapped order (>=0.9)", acc["charwb36_LR"] >= 0.9)
check("baselines: result rows report order-sensitive eval", "order_sensitive_eval_acc" in (ROOT / "scripts/text_baselines.py").read_text())

# 3 OT open condition and recorded ask
from prompt_text import visible_messages, OPEN_ASK
r = {"note": "n", "incentive_context": "c"}
for rf in ("", "user-says", "agent-stakes"):
    o = visible_messages(r, "", False, rf, "open"); yn = visible_messages(r, "", False, rf)
    check(f"ot open ({rf or 'system'}): no YES/NO instruction", all("YES or NO" not in x["content"] for x in o) and OPEN_ASK in o[1]["content"])
    check(f"ot open ({rf or 'system'}): same note/context", ("c" in o[0]["content"] + o[1]["content"]) and o[0]["content"].startswith("Private note:\nn"))
    check(f"ot yesno ({rf or 'system'}): default unchanged", "Answer with only YES or NO." in yn[1]["content"])
som = (ROOT / "scripts/som_ot_bank.py").read_text()
check("ot: rows record ot_ask and ot_format", '"ot_ask": a.ot_ask, "ot_format": a.ot_format' in som)

# 4 run_fix_rerun.sh
sh = ROOT / "run_fix_rerun.sh"
check("run: bash -n", subprocess.run(["bash", "-n", str(sh)]).returncode == 0)
t = sh.read_text()
check("run: FAIL aggregate and final status", "FAIL=0" in t and 'echo "RUN FAILED: inspect $LOG"; exit 1' in t and 'echo "RUN COMPLETED"; exit 0' in t)
check("run: no WARN-only baseline failure", "WARN baselines" not in t)
check("run: --ot-ask and --ot-format passed", '--ot-ask "$OT_ASK"' in t and '--ot-format "$cond"' in t)
check("run: BOS auto rerun", "AUTO_RERUN_BOS=${AUTO_RERUN_BOS:-1}" in t and "DOUBLE_BOS_BEFORE_FIX" in t)
with tempfile.TemporaryDirectory() as d:
    env = dict(os.environ)
    def run(**kw):
        e = {**env, **kw}; return subprocess.run(["bash", str(sh)], cwd=ROOT, env=e, capture_output=True, text=True)
    p = run(HF_HOME=str(Path(d) / "nohf"), OUT=str(Path(d) / "o1"))
    check("run: missing HF_HOME -> exit 2", p.returncode == 2 and "HF_HOME" in p.stdout and not (Path(d) / "o1").exists())
    (Path(d) / "hf").mkdir()
    p = run(HF_HOME=str(Path(d) / "hf"), MODELS_DIR=str(Path(d) / "none"), OUT=str(Path(d) / "o2"))
    check("run: missing gemma -> exit 2", p.returncode == 2 and "gemma-2-9b-it missing" in p.stdout)
    p = run(HF_HOME=str(Path(d) / "hf"), MODELS_DIR=str(Path(d) / "none"), SKIP_GEMMA="1", OUT=str(Path(d) / "o3"))
    check("run: zero models found -> exit 2", p.returncode == 2 and "no requested model" in p.stdout)
    p = run(HF_HOME=str(Path(d) / "hf"), MODELS_DIR=str(Path(d) / "none"), OT_ASKS="bogus", OUT=str(Path(d) / "o4"))
    check("run: bad OT_ASKS -> exit 2", p.returncode == 2)
    try: import torch; has_torch = hasattr(torch, "cuda")
    except Exception: has_torch = False
    if not has_torch:
        g = Path(d) / "models/gemma-2-9b-it"; g.mkdir(parents=True); (g / "config.json").write_text("{}")
        p = run(HF_HOME=str(Path(d) / "hf"), MODELS_DIR=str(Path(d) / "models"), OUT=str(Path(d) / "o5"))
        check("run: dry run without torch -> nonzero, no OUT written", p.returncode != 0 and "torch" in p.stdout and not (Path(d) / "o5").exists())
print("ALL PASS" if ok else "SOME FAILED"); sys.exit(0 if ok else 1)
