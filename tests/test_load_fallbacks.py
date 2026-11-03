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
            if mode == "perm":
                raise PermissionError("[Errno 13] Permission denied: '/media/pauli/datapata'")
            if mode == "meta":
                raise RuntimeError("Tensor.item() cannot be called on meta tensors")
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
check(r == "MODEL" and len(c) == 2 and c[1]["quantization_config"] is None and c[1]["dtype"] == "bf16"
      and c[1]["max_memory"] == {0: "7GiB", "cpu": "48GiB"},
      "LFM dispatch -> straight to unquantized bf16 offload, GPU 7GiB + CPU 48GiB (no 4-bit offload)")
A, c = make_auto(["losskwargs", "dispatch"])
check(hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()) == "MODEL" and len(c) == 3
      and c[2]["trust_remote_code"] is False and c[2]["quantization_config"] is None, "native then bf16 offload chain")
A, c = make_auto(["other"])
try:
    hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()); check(False, "unknown error raises")
except RuntimeError:
    check(len(c) == 1, "unknown error raises after 1 attempt (runner logs FAIL, continues)")
A, c = make_auto(["dispatch", "dispatch"])
try:
    hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()); check(False, "offload fail raises")
except ValueError:
    check(len(c) == 2, "bf16 offload failure raises after 2 attempts, no loop")
A, c = make_auto(["perm"])
check(hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()) == "MODEL" and len(c) == 2
      and c[1]["trust_remote_code"] is False, "Phi PermissionError (unwritable modules cache) -> native")
A, c = make_auto(["meta"])
check(hide_bank._load_model_with_fallbacks("m", torch, A, FakeBnb, FakeBnb()) == "MODEL" and len(c) == 2
      and c[1]["quantization_config"] is None, "meta-tensor error on a 4-bit stage -> bf16 offload")

# 2026-11-03 LFM: from_pretrained returns an offloaded 4-bit model whose first forward hits
# QuantState.code.to(device) on meta. Fakes reproduce that; the loader must smoke-test and fall back.
class FT:  # minimal fake torch for the smoke forward
    bfloat16 = "bf16"; long = "long"
    class device:
        def __init__(self, s): self.type = str(s).split(":")[0]; self.s = str(s)
        def __eq__(self, o): return str(o) == self.s
        def __repr__(self): return self.s
    @staticmethod
    def zeros(shape, dtype=None, device=None): FT.last_dev = device; return ("ids", shape)
    class no_grad:
        def __enter__(self): pass
        def __exit__(self, *a): return False
class Emb:
    class weight: device = FT.device("meta")
class OffModel:
    calls = 0
    def __init__(self, broken, dm): self.broken = broken; self.hf_device_map = dm; self.emb = Emb()
    def get_input_embeddings(self): return self.emb
    def named_modules(self): return [("", self), ("model.embed_tokens", self.emb)]
    def parameters(self): return iter([])
    def __call__(self, **kw):
        OffModel.calls += 1
        if self.broken: raise NotImplementedError("Cannot copy out of meta tensor; no data!")
        return "out"
def make_off(seq):
    calls = []
    class Auto:
        @staticmethod
        def from_pretrained(name, **kw):
            calls.append(kw); mode = seq.pop(0)
            if mode == "dispatch": raise ValueError("Some modules are dispatched on the CPU or the disk.")
            return mode
    return Auto, calls
DM = {"model.embed_tokens": 0, "model.layers.0": 0, "model.layers.20": "cpu", "lm_head": "cpu"}
broken, good = OffModel(True, DM), OffModel(False, DM)
A, c = make_off([broken, good])
OffModel.calls = 0
m = hide_bank._load_model_with_fallbacks("m", FT, A, FakeBnb, FakeBnb())
check(m is good and len(c) == 2 and c[1]["quantization_config"] is None and OffModel.calls == 1,
      "offloaded 4-bit model failing first forward ('Cannot copy out of meta tensor') -> bf16 offload; bf16 not re-smoked")
A, c = make_off([good])
OffModel.calls = 0
check(hide_bank._load_model_with_fallbacks("m", FT, A, FakeBnb, FakeBnb()) is good and OffModel.calls == 1
      and FT.last_dev == "cuda:0", "working offloaded 4-bit model passes smoke; ids on embedding exec device cuda:0")
A, c = make_off([OffModel(True, {"": 0})])
OffModel.calls = 0
check(hide_bank._load_model_with_fallbacks("m", FT, A, FakeBnb, FakeBnb()).broken and OffModel.calls == 0,
      "fully-on-GPU model: no smoke forward (unchanged behaviour)")
A, c = make_off(["dispatch", broken])
try:
    hide_bank._load_model_with_fallbacks("m", FT, A, FakeBnb, FakeBnb()); r = "returned"
except Exception as e:  # noqa: BLE001
    r = type(e).__name__
check(r == "returned" and len(c) == 2, "bf16 stage is not smoke-tested (offload of plain bf16 is accelerate's normal path)")

# input_device: never meta; embedding offloaded -> main GPU; no device map -> first real param
check(str(hide_bank.input_device(OffModel(False, {"model.embed_tokens": "cpu", "model.layers.0": 0}), FT)) == "cuda:0",
      "input_device: offloaded embedding -> execution GPU cuda:0")
class P:
    def __init__(self, d): self.device = FT.device(d)
class Plain(OffModel):
    def parameters(self): return iter([P("meta"), P("cuda:0")])
check(str(hide_bank.input_device(Plain(False, {}), FT)) == "cuda:0", "input_device: no map -> first non-meta param")

# leak: a failed attempt's half-loaded model must be freed before the retry
import gc, weakref
class Big: pass
refs = []
def leaky(name, **kw):
    obj = Big(); refs.append(weakref.ref(obj))
    if len(refs) == 1:  # obj is only alive via the traceback frames
        raise ValueError("Some modules are dispatched on the CPU or the disk.")
    return "MODEL"
class A2:
    from_pretrained = staticmethod(leaky)
check(hide_bank._load_model_with_fallbacks("m", torch, A2, FakeBnb, FakeBnb()) == "MODEL" and refs[0]() is None,
      "half-loaded model from a failed attempt is freed before the retry")

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
# LFM2.5 empty think prefill
class TokLFM:
    name_or_path = "models/LFM2.5-8B-A1B"
    def apply_chat_template(self, m, **kw): return "<|im_start|>assistant\n"
o = reply_mutate.chat_nothink(TokLFM(), [{"role": "user", "content": "x"}])
check(o.endswith("<think>\n</think>\n\n"), "LFM2.5 gets empty think prefill")
class TokOther(TokLFM): name_or_path = "models/granite"
check(not reply_mutate.chat_nothink(TokOther(), [{"role": "user", "content": "x"}]).endswith("</think>\n\n"), "non-LFM unchanged")
raise SystemExit(0 if ok else 1)
