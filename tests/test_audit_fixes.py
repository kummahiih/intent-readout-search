"""CPU tests for the 2026-11-03 audit fixes (results/audit_2026-11-03.md). No GPU, no real model.
1 BOS dedup  2 OT chat prompt carries the frame  3 topic SOM N/A on one topic
4 new text-baseline inputs  5 prompt refactor keeps the old text."""
import json, os, subprocess, sys, tempfile, types
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name); ok = ok and bool(cond)

# stub heavy imports so run_scenario / som_ot_bank import on CPU without torch/transformers
for m in ("torch", "transformers"):
    if m not in sys.modules:
        try: __import__(m)
        except Exception:
            stub = types.ModuleType(m)  # real module type with a Tensor class so scipy/sklearn probes work
            stub.Tensor = type("Tensor", (), {}); stub.bfloat16 = "bf16"
            stub.AutoModelForCausalLM = stub.AutoTokenizer = stub.BitsAndBytesConfig = None
            sys.modules[m] = stub
from prompt_text import encode_prompt, has_leading_bos, visible_messages, visible_text

class FakeTok:
    bos_token = "<bos>"; name_or_path = "fake/gemma-2-9b-it"
    def __call__(self, text, add_special_tokens=True, **kw):
        ids = [2] if add_special_tokens else []
        rest = text
        if rest.startswith("<bos>"): ids.append(2); rest = rest[5:]
        return {"input_ids": ids + [ord(c) for c in rest[:5]]}
    def apply_chat_template(self, msgs, tokenize=False, add_generation_prompt=True, **kw):
        if any(m["role"] == "system" for m in msgs): raise ValueError("System role not supported")
        return "<bos>" + "".join(f"<start_of_turn>{m['role']}\n{m['content']}<end_of_turn>\n" for m in msgs) + "<start_of_turn>model\n"

t = FakeTok()
# 1 BOS
check("bos: chat-rendered text gets one BOS", encode_prompt(t, "<bos>hi")["input_ids"][:2] != [2, 2])
check("bos: plain text still gets BOS", encode_prompt(t, "hi")["input_ids"][0] == 2)
os.environ["RH_KEEP_DOUBLE_BOS"] = "1"
check("bos: RH_KEEP_DOUBLE_BOS=1 restores old double BOS", encode_prompt(t, "<bos>hi")["input_ids"][:2] == [2, 2])
del os.environ["RH_KEEP_DOUBLE_BOS"]
check("bos: tokenizer without bos_token untouched", not has_leading_bos(types.SimpleNamespace(bos_token=None), "<bos>x"))
src = (ROOT / "hide_bank.py").read_text() + (ROOT / "scripts/som_ot_bank.py").read_text() + (ROOT / "reply_mutate.py").read_text()
check("bos: generate_short/last_h/OT sample/reply_mutate use encode_prompt", src.count("encode_prompt(tok,") >= 5)

# 2 OT prompt
import som_ot_bank as S
load = lambda p: [json.loads(l) for l in open(ROOT / p) if l.strip()]
us = load("data/prereg/scenarios_original_user_says.jsonl")[:3]
ag = load("data/prereg/scenarios_original_agent_stakes.jsonl")[:3]
tu = S.ot_texts(t, us, "chat", "", False, "user-says"); ta = S.ot_texts(t, ag, "chat", "", False, "agent-stakes")
check("ot chat: user_says prompt has 'The user says:'", all("The user says:" in x for x in tu["rows"]))
check("ot chat: agent_stakes prompt has 'As the agent,'", all("As the agent," in x for x in ta["rows"]))
check("ot chat: the two banks' OT prompts differ", tu["rows"] != ta["rows"])
check("ot chat: note is in the prompt", us[0]["note"] in tu["rows"][0])
check("ot chat: empty baseline has no note", us[0]["note"] not in tu["empty"])
d = load("data/prereg/scenarios_defect_bank_provisional.jsonl")[:2]
td = S.ot_texts(t, d, "chat", "", True, "")
check("ot chat: defect hide/name prompts differ by incentive context", td["rows"][0] != td["rows"][1] and d[0]["incentive_context"] in td["rows"][0])
tn = S.ot_texts(t, us, "note", "", False, "user-says")
check("ot note mode: old raw text kept for comparison", tn["rows"][0] == f"Note: {us[0]['note']}" and tn["empty"] == "")

# 3 topic N/A
import numpy as np
dd = load("data/prereg/scenarios_defect_bank_provisional.jsonl")
meta = S.join_meta(dd, "")
X = np.random.default_rng(0).standard_normal((len(dd), 16)).astype(np.float32)
r = S.analyze_matrix(X, meta, seeds=2, steps=1, nulls=4, pca=8)
check("topic: single-topic bank -> topic N/A", isinstance(r["som"]["raw"]["topic"], str) and "N/A" in r["som"]["raw"]["topic"])
check("topic: topic_mean_subtracted N/A on single topic", isinstance(r["som"]["topic_mean_subtracted"], str))
check("topic: incentive still scored", isinstance(r["som"]["raw"]["incentive"], dict))
mu = S.join_meta(load("data/prereg/scenarios_original_user_says.jsonl"), "")
r2 = S.analyze_matrix(np.random.default_rng(0).standard_normal((len(mu), 16)).astype(np.float32), mu, seeds=2, steps=1, nulls=4, pca=8)
check("topic: multi-topic bank keeps topic purity", isinstance(r2["som"]["raw"]["topic"], dict) and isinstance(r2["som"]["topic_mean_subtracted"], dict))

# 4 text baselines
try:
    import sklearn  # noqa
    with tempfile.TemporaryDirectory() as td_:
        dump = Path(td_) / "d.jsonl"; out = Path(td_) / "o.json"
        rows = []
        for i, b in enumerate(dd):
            for arm in ("belief", "public", "name"):
                rows.append({**{k: b[k] for k in ("scenario_id", "topic", "proposition", "prop_truth", "states_proposition", "incentive", "split", "note")},
                             "arm": arm, "button": "YES" if (i % 3) else "NO", "text": ""})
        dump.write_text("".join(json.dumps(x) + "\n" for x in rows))
        subprocess.run([sys.executable, str(ROOT / "scripts/text_baselines.py"), "--dump", str(dump),
                        "--bank", str(ROOT / "data/prereg/scenarios_defect_bank_provisional.jsonl"), "--out", str(out)],
                       check=True, capture_output=True)
        res = json.load(open(out))["results"]
        inputs = {x["input"] for x in res}
        check("baselines: new inputs present", {"incentive_context", "note+incentive_context", "full_prompt"} <= inputs)
        inc = {x["input"]: x for x in res if x["target"] == "incentive"}
        # defect hide/name contexts are word-order swaps of the same words ("deny ... make the sale" vs
        # "confirm ... make the sale"), so n<=3 bag-of-ngrams stay near chance even on the context: scored, not asserted high
        check("baselines: incentive_context / full_prompt inputs scored", all(isinstance(inc[k].get("eval_acc"), float) for k in ("incentive_context", "full_prompt")))
        check("baselines: defect incentive at chance from note only (<0.6)", inc["note"]["eval_acc"] < 0.6)
        check("baselines: selection still fit-only (fit_cv present)", all("fit_cv" in x for x in res if "status" not in x))
except ImportError:
    print("SKIP baselines (no sklearn)")

# 5 refactor
m = visible_messages(us[0], us[0]["public_ask"], False, "user-says")
check("prompt: system holds note, user holds frame+ask",
      us[0]["note"] in m[0]["content"] and m[1]["content"].startswith("The user says: ") and m[1]["content"].endswith("Answer with only YES or NO."))
check("prompt: visible_text joins both", us[0]["note"] in visible_text(us[0], "", False, "user-says"))
raise SystemExit(0 if ok else 1)
