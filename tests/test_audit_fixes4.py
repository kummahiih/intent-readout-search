"""CPU tests for the third-review fixes (2026-11-04):
- phase2_combine checks the prebutton cache against the exact model input (ask included);
- tokenizer / chat-template files are part of the model fingerprint;
- a corrupt cache meta is a miss, not a crash;
- som_ot_bank reports grid_fit_purity_insample (not grid_fit_cv);
- run_fix_rerun.sh: all-zero identical OT files are 'uninformative', non-zero identical files fail."""
import json, os, re, subprocess, sys, tempfile, types
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
import phase2_prebutton as pb
import phase2_combine as pc

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    # 1 combine: public_rows keeps ask; check_loaded with inputs catches an ask change
    dump = td / "dump.jsonl"
    dump.write_text("".join(json.dumps({"arm": "public", "button": b, "scenario_id": f"s{i}", "split": "fit",
                                        "note": f"n{i}", "ask": "Ship it?"}) + "\n" for i, b in enumerate("YNYN".replace("Y", "YES ").replace("N", "NO ").split())))
    rows = pc.public_rows(str(dump), {})
    check("combine public_rows keeps ask", all(r.get("ask") == "Ship it?" for r in rows))
    src = (ROOT / "phase2_combine.py").read_text()
    check("combine check_loaded passes inputs=prompt_msgs", "inputs=[prompt_msgs(r) for r in rows])" in src and "from phase2_prebutton import prompt_msgs" in src)
    mdir = td / "model"; mdir.mkdir(); (mdir / "config.json").write_text("{}")
    meta = td / "pre.json"
    meta.write_text(json.dumps(want_meta(rows, -1, str(mdir), "v", 512, inputs=[pb.prompt_msgs(r) for r in rows])))
    X = np.zeros((len(rows), 2))
    try: check_loaded(X, meta, rows, "t", model_path=str(mdir), inputs=[pb.prompt_msgs(r) for r in rows]); same = True
    except SystemExit: same = False
    check("combine check passes on the same ask", same)
    rows2 = [{**r, "ask": "Delete it?"} for r in rows]
    try: check_loaded(X, meta, rows2, "t", model_path=str(mdir), inputs=[pb.prompt_msgs(r) for r in rows2]); caught = False
    except SystemExit as e: caught = "ask" in str(e)
    check("combine check fails on a changed ask (same notes)", caught)

    # 2 tokenizer files in the fingerprint
    fp0 = model_fingerprint(str(mdir))
    (mdir / "tokenizer_config.json").write_text('{"chat_template": "a"}')
    fp1 = model_fingerprint(str(mdir))
    check("adding tokenizer_config.json changes fingerprint", fp0 != fp1)
    (mdir / "tokenizer_config.json").write_text('{"chat_template": "b"}')
    fp2 = model_fingerprint(str(mdir))
    check("editing chat template changes fingerprint", fp2 != fp1)
    (mdir / "chat_template.jinja").write_text("{{x}}")
    check("chat_template.jinja is hashed", model_fingerprint(str(mdir)) != fp2)
    (mdir / "notes.txt").write_text("irrelevant")
    fp3 = model_fingerprint(str(mdir)); (mdir / "notes.txt").write_text("changed")
    check("unrelated file does not change fingerprint", model_fingerprint(str(mdir)) == fp3)
    (mdir / "config.json").write_text('{"_commit_hash": "' + "a" * 40 + '"}')
    fr = model_fingerprint(str(mdir)); (mdir / "tokenizer.json").write_text("{}")
    check("rev fingerprint still includes local tokenizer files", fr.startswith("rev:") and model_fingerprint(str(mdir)) != fr)

    # tokenizer change invalidates a cache
    calls = []
    def comp():
        calls.append(1); return np.ones((len(rows), 3)), "tok"
    cache, cmeta = td / "c.npy", td / "c.json"
    want = lambda: want_meta(rows, 3, str(mdir), "v", 512, inputs=[pb.prompt_msgs(r) for r in rows])
    cached_array(cache, cmeta, want(), comp); cached_array(cache, cmeta, want(), comp)
    check("cache hit when nothing changed", len(calls) == 1)
    (mdir / "tokenizer.json").write_text('{"v": 2}')
    cached_array(cache, cmeta, want(), comp)
    check("tokenizer change invalidates cache", len(calls) == 2)

    # 3 corrupt meta => miss
    for bad_meta in ("{not json", "", "[1, 2]", "\xff\xfe"):
        cmeta.write_text(bad_meta, errors="surrogateescape") if False else cmeta.write_bytes(bad_meta.encode("latin-1"))
        n = len(calls)
        try: cached_array(cache, cmeta, want(), comp); fine = len(calls) == n + 1
        except Exception as e: fine = False
        check(f"corrupt meta {bad_meta!r} recomputes", fine)
    check("meta rewritten valid after recompute", json.loads(cmeta.read_text())["n"] == len(rows))
    cmeta.write_text("{bad")
    try: check_loaded(np.ones((len(rows), 3)), cmeta, rows, "t"); msg = ""
    except SystemExit as e: msg = str(e)
    check("check_loaded corrupt meta: clean SystemExit", "corrupt meta" in msg)

# 4 renamed SOM field
sob = (ROOT / "scripts" / "som_ot_bank.py").read_text()
check("som_ot_bank writes grid_fit_purity_insample", '"grid_fit_purity_insample": sel' in sob)
check("som_ot_bank no longer writes grid_fit_cv key", '{"grid_fit_cv"' not in sob)

# 5 OT identity check in run_fix_rerun.sh (functions extracted from the script)
sh = (ROOT / "run_fix_rerun.sh").read_text()
m = re.search(r"^ot_allzero\(\).*?^  \[\[ -f \$g \]\] && ot_identity \"\$f\" \"\$g\"; done$", sh, re.S | re.M)
check("run_fix_rerun.sh has ot_allzero / ot_identity", m is not None)
if m:
    body = 'FAIL=0; ST=(); bad () { ST+=("$1"); FAIL=1; echo "FAIL $1"; }\n' + m.group(0) + '\necho "FAIL=$FAIL"\n'
    def run(us, ag):
        with tempfile.TemporaryDirectory() as o:
            for k, rs in (("user_says", us), ("agent_stakes", ag)):
                Path(o, f"M__{k}_ot.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rs))
            return subprocess.run(["bash", "-c", f'OUT="{o}"\n' + body], capture_output=True, text=True).stdout
    z = [{"mass_note": 0.0, "in_room": False, "ot": 1}] * 3
    nz = [{"mass_note": 0.0, "in_room": False}, {"mass_note": 0.3, "in_room": True}]
    out = run(z, z)
    check("all-zero identical OT: uninformative, not failed", "OT uninformative (all-zero)" in out and "FAIL=0" in out)
    out = run(nz, nz)
    check("non-zero identical OT: fails", "OT IDENTICAL" in out and "FAIL=1" in out)
    out = run(nz, z)
    check("differing OT: differ, no fail", "differ" in out and "FAIL=0" in out)
    out = run([], [])
    check("empty identical OT files still fail", "OT IDENTICAL" in out and "FAIL=1" in out)
check("bash -n run_fix_rerun.sh", subprocess.run(["bash", "-n", str(ROOT / "run_fix_rerun.sh")]).returncode == 0)

print("ALL PASS" if ok else "SOME FAILED"); sys.exit(0 if ok else 1)
