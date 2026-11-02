"""Offline tests of loader fallbacks and no-think templating with fakes. No GPU, no real model."""
import sys, types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hide_bank

class FakeBnb:
    def __init__(self, **kw): self.kw = kw

def make_auto(fail_modes):
    calls = []
    class Auto:
        @staticmethod
        def from_pretrained(name, **kw):
            calls.append(kw)
            mode = fail_modes.pop(0) if fail_modes else None
            if mode == "losskwargs":
                raise ImportError("cannot import name 'LossKwargs' from 'transformers.utils'")
            if mode == "dispatch":
                raise ValueError("Some modules are dispatched on the CPU or the disk. Make sure ...")
            if mode == "other":
                raise RuntimeError("boom")
            return "MODEL"
    return Auto, calls

torch = types.SimpleNamespace(bfloat16="bf16")
ok = True
def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg); ok &= bool(cond)

A, c = make_auto([])
check(hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()) == "MODEL" and len(c) == 1
      and c[0]["trust_remote_code"] is True, "plain load unchanged (1 call, trust_remote_code=True)")
A, c = make_auto(["losskwargs"])
check(hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()) == "MODEL" and len(c) == 2
      and c[1]["trust_remote_code"] is False, "Phi LossKwargs -> native trust_remote_code=False")
A, c = make_auto(["dispatch"])
r = hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb())
check(r == "MODEL" and len(c) == 2 and c[1]["quantization_config"].kw.get("llm_int8_enable_fp32_cpu_offload") is True
      and c[1]["max_memory"][0] == "10GiB", "LFM dispatch -> fp32 cpu offload + max_memory cap")
A, c = make_auto(["losskwargs", "dispatch"])
check(hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()) == "MODEL" and len(c) == 3
      and c[2]["trust_remote_code"] is False, "native then offload chain")
A, c = make_auto(["other"])
try:
    hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()); check(False, "unknown error raises")
except RuntimeError:
    check(len(c) == 1, "unknown error raises after 1 attempt (runner logs FAIL, continues)")
A, c = make_auto(["dispatch", "dispatch"])
try:
    hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()); check(False, "offload fail raises")
except ValueError:
    check(len(c) == 2, "offload failure raises, no loop")

# no-think templating: stub heavy imports only for reply_mutate import
for m in ("torch", "transformers"):
    if m not in sys.modules:
        mod = types.ModuleType(m)
        for a in ("AutoModelForCausalLM", "AutoTokenizer", "BitsAndBytesConfig"): setattr(mod, a, object)
        sys.modules[m] = mod
import reply_mutate
class Tok:
    def __init__(self): self.kw = None
    def apply_chat_template(self, msgs, **kw):
        self.kw = kw; return "think=off" if kw.get("enable_thinking") is False else "think=on"
t = Tok(); out = reply_mutate.chat_nothink(t, [{"role": "user", "content": "x"}])
check(out == "think=off" and t.kw.get("thinking") is False, "chat_nothink passes enable_thinking=False and thinking=False")
class TokNoSys:
    def apply_chat_template(self, msgs, **kw):
        if any(m["role"] == "system" for m in msgs): raise Exception("System role not supported")
        return "folded:" + msgs[0]["content"]
check(reply_mutate.chat_nothink(TokNoSys(), [{"role": "system", "content": "S"}, {"role": "user", "content": "U"}]).startswith("folded:S"),
      "chat_nothink falls back to chat() system folding")
raise SystemExit(0 if ok else 1)
