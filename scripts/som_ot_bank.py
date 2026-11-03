#!/usr/bin/env python3
"""SOM purity and OT room-entry diagnostics on the PROVISIONAL bank files (logs only).

Port of regret-heuristic night_sims/som_layout_run.py (SOM on last-token residuals, purity vs
shuffle null, topic-mean-subtracted control) and night_sims/ot_rooms.py (room = high-mass set of
sampled continuations, tau=0.5; OT = 0 if the empty prompt is already in the room, else the
length of the shortest prompt tried that enters it, inf if none) to bank rows.

Subcommands:
  extract  (GPU)  last-token residual at --layer for each bank row, on the PUBLIC-arm prompt built
                  exactly as run_scenario.py builds it (same --incentive-in-user / --role-frame, no-think
                  template), plus an ask-removed control (note + framing only). Optional --ot: sample
                  continuations of "Note: {note}" and of the empty prompt and score the fact room.
  analyze  (CPU)  SOM trained on FIT rows only; centering means estimated on FIT only; grid chosen
                  on FIT only (incentive purity, grids 3/4/5); scored on EVAL rows. Labels: incentive,
                  realized public button (joined from an existing run_scenario dump), topic.
                  Null: EVAL labels shuffled (--nulls). Split is the bank's scenario_id split.
  smoke           analyze on synthetic residuals with the real bank and dump labels. No model.

OT room for a bank row (adaptation, stated, not from the source script): R = continuations that
mention the row's proposition, keyword match = at least 2 (or all, if fewer) content words of the
proposition. Keyword matching is the known bottleneck of the OT log.

DOES NOT: change the banks or contract semantics, gate anything, fill D, freeze r, claim a camera
or handoverPass, or change the negative handover. SOM/OT/purity outputs are diagnostics, not gates.
"""
from __future__ import annotations

import argparse, json, re, sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
STOP = set("the a an and or of to in on for is are was were be been that this with by as at it its can "
           "not no every one all from about which who what will would has have had they them their".split())


def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def keywords(prop):
    w = [x for x in re.findall(r"[a-z0-9]+", prop.lower()) if len(x) > 3 and x not in STOP]
    return list(dict.fromkeys(w))


def in_fact_room(text, kws):
    if not kws:
        return False
    need = min(2, len(kws))
    t = text.lower()
    return sum(k in t for k in kws) >= need


# ---------------- SOM (numpy port of MiniSOM in som_layout_run.py) ----------------
class MiniSOM:
    def __init__(self, m, n, dim, sigma=1.5, lr=0.3, steps=30, seed=0):
        rng = np.random.default_rng(seed)
        self.m, self.n = m, n
        self.w = rng.standard_normal((m, n, dim)).astype(np.float32)
        self.sigma, self.lr, self.steps = sigma, lr, steps
        self.coords = np.stack(np.meshgrid(np.arange(m), np.arange(n), indexing="ij"), -1).astype(np.float32)

    def winners(self, X):
        W = self.w.reshape(-1, self.w.shape[-1])
        d = (X ** 2).sum(1)[:, None] - 2 * X @ W.T + (W ** 2).sum(1)[None]
        return d.argmin(1)

    def train(self, X):
        for _ in range(self.steps):
            for x in X:
                i, j = divmod(int(((self.w - x) ** 2).sum(-1).argmin()), self.n)
                dist = np.linalg.norm(self.coords - np.array([i, j], np.float32), axis=-1)
                k = (dist < self.sigma) * np.clip(1 - dist / self.sigma, 0, None)
                self.w += self.lr * k[..., None] * (x - self.w)


def purity(assign, labels):
    tot = 0
    for k in set(assign.tolist()):
        labs = [labels[i] for i in range(len(labels)) if assign[i] == k]
        tot += Counter(labs).most_common(1)[0][1]
    return tot / max(len(labels), 1)


def standardize_fit(Xf, Xe):
    mu = Xf.mean(0); sd = Xf.std(0) + 1e-6
    return (Xf - mu) / sd, (Xe - mu) / sd


def subtract_topic_mean_fit(Xf, Xe, tf, te):
    means = {t: Xf[[i for i, x in enumerate(tf) if x == t]].mean(0) for t in set(tf)}
    g = Xf.mean(0)
    return (Xf - np.stack([means[t] for t in tf]),
            Xe - np.stack([means.get(t, g) for t in te]))


def analyze_matrix(X, meta, grids=(3, 4, 5), seeds=3, steps=30, nulls=20, pca=32):
    fit = [i for i, m in enumerate(meta) if m["split"] == "fit"]
    ev = [i for i, m in enumerate(meta) if m["split"] == "eval"]
    out = {"n_fit": len(fit), "n_eval": len(ev)}
    if not fit or not ev:
        out["status"] = "missing split"; return out
    lab = {k: [m.get(k) for m in meta] for k in ("incentive", "public_button", "topic")}
    res = {}
    n_topics = len({lab["topic"][i] for i in fit + ev})
    conds = ("raw", "topic_mean_subtracted") if n_topics >= 2 else ("raw",)
    if n_topics < 2:  # one topic: topic purity is trivially 1.0 and topic-mean subtraction == raw
        res["topic_mean_subtracted"] = "N/A (single topic; identical to raw)"
    for cond in conds:
        Xf, Xe = X[fit].astype(np.float32), X[ev].astype(np.float32)
        if cond == "topic_mean_subtracted":
            Xf, Xe = subtract_topic_mean_fit(Xf, Xe, [lab["topic"][i] for i in fit], [lab["topic"][i] for i in ev])
        Xf, Xe = standardize_fit(Xf, Xe)
        if pca and Xf.shape[1] > pca:  # PCA fit on FIT only
            _, _, Vt = np.linalg.svd(Xf - Xf.mean(0), full_matrices=False)
            P = Vt[:pca].T; Xf, Xe = Xf @ P, Xe @ P
        sel = {}
        for g in grids:  # grid selected on FIT purity of incentive only
            sel[g] = float(np.mean([purity(
                                           _fit(MiniSOM(g, g, Xf.shape[1], steps=steps, seed=s), Xf).winners(Xf),
                                           [lab["incentive"][i] for i in fit]) for s in range(seeds)]))
        g = max(sel, key=sel.get)
        soms = [_fit(MiniSOM(g, g, Xf.shape[1], steps=steps, seed=s), Xf) for s in range(seeds)]
        r = {"grid_fit_cv": sel, "grid_selected": g}
        rng = np.random.default_rng(0)
        for name, L in lab.items():
            if name == "topic" and n_topics < 2:
                r[name] = "N/A (single topic)"; continue
            le_all = [L[i] for i in ev]
            keep = [j for j, x in enumerate(le_all) if x is not None]  # drop rows with no valid label
            if not keep:  # (e.g. one 'other' public button used to blank the whole label)
                r[name] = "missing"; continue
            le = [le_all[j] for j in keep]
            win = [s.winners(Xe)[keep] for s in soms]
            ps = [purity(w, le) for w in win]
            # null over all seeds (was seed 0 only before the 2026-11-03 audit)
            null = [purity(win[j % len(win)], list(rng.permutation(le))) for j in range(nulls)]
            r[name] = {"n_eval_labelled": len(keep),"eval_purity_mean": float(np.mean(ps)), "per_seed": [float(p) for p in ps],
                       "shuffle_null_mean": float(np.mean(null)), "shuffle_null_p95": float(np.percentile(null, 95)),
                       "majority": Counter(le).most_common(1)[0][1] / len(le)}
        res[cond] = r
    out["som"] = res
    return out


def _fit(som, X):
    som.train(X); return som


def join_meta(bank, dump):
    btn = {}
    if dump and Path(dump).is_file():
        for r in load(dump):
            if r["arm"] == "public":
                btn[(r["scenario_id"], r["incentive"], r["note"])] = r["button"] if r["button"] in ("YES", "NO") else None
    meta = []
    for r in bank:
        k = (r["scenario_id"], r["incentive"], r["note"])
        meta.append({"scenario_id": r["scenario_id"], "split": r.get("split", ""), "incentive": r["incentive"],
                     "topic": r.get("topic", ""), "public_button": btn.get(k) if btn else None})
    return meta


def ot_texts(tok, bank, mode, ask, incentive_in_user, role_frame, answer_format="yesno"):
    """OT prompts. mode 'chat' (default since the 2026-11-03 audit): the same chat prompt the
    extraction uses (note + incentive context + role frame), with ask --ot-ask (default ''), and an
    empty-note/empty-context chat prompt as the empty baseline. mode 'note': the old raw
    'Note: {note}' text and the empty string; it ignores the frame and the incentive context, so
    user_says and agent_stakes gave byte-identical OT files in every run before the fix."""
    if mode == "note":
        return {"empty": "", "rows": [f"Note: {r['note']}" for r in bank]}
    from run_scenario import prompt
    blank = {"note": "", "incentive_context": ""}
    return {"empty": prompt(tok, blank, ask, incentive_in_user, role_frame, True, answer_format),
            "rows": [prompt(tok, r, ask, incentive_in_user, role_frame, True, answer_format) for r in bank]}


# ---------------- GPU extraction ----------------
def extract(a):
    import torch
    from hide_bank import load_tok_model
    from run_scenario import prompt
    bank = load(a.data)
    tok, model = load_tok_model(a.model)
    from hide_bank import input_device
    dev = input_device(model)  # not next(parameters()): may be meta/cpu when offloaded
    nl = model.config.get_text_config().num_hidden_layers if hasattr(model.config, "get_text_config") else model.config.num_hidden_layers
    layer = min(a.layer, nl)
    print(f"layer={layer} of {nl}")

    from prompt_text import encode_prompt  # no double BOS (audit 2026-11-03)

    def last_h(text):
        enc = encode_prompt(tok, text, return_tensors="pt", truncation=True, max_length=512)
        enc = {k: v.to(dev) for k, v in enc.items()}
        with torch.no_grad():
            o = model(**enc, output_hidden_states=True)
        return o.hidden_states[layer][0, -1].float().cpu().numpy()

    H, Hn, ot = [], [], []
    for i, r in enumerate(bank):
        H.append(last_h(prompt(tok, r, r["public_ask"], a.incentive_in_user, a.role_frame, True)))
        noask = dict(r); noask_ask = ""  # ask-removal control: note + framing, no question
        Hn.append(last_h(prompt(tok, noask, noask_ask, a.incentive_in_user, a.role_frame, True)))
        if i % 50 == 0:
            print(f"extract {i}/{len(bank)}")
    np.savez_compressed(a.out, H=np.stack(H), H_noask=np.stack(Hn))
    print(f"saved {a.out} n={len(bank)}")
    if a.ot:
        def sample(text):
            enc = encode_prompt(tok, text or " ", return_tensors="pt", truncation=True, max_length=256)
            enc = {k: v.to(dev) for k, v in enc.items()}
            with torch.no_grad():
                g = model.generate(**enc, max_new_tokens=a.max_new, do_sample=True, temperature=0.7,
                                   num_return_sequences=a.n_samples, pad_token_id=tok.eos_token_id)
            return [tok.decode(x[enc["input_ids"].shape[1]:], skip_special_tokens=True) for x in g]
        torch.manual_seed(0)
        texts = ot_texts(tok, bank, a.ot_mode, a.ot_ask, a.incentive_in_user, a.role_frame, a.ot_format)
        empty = sample(texts["empty"])
        for r, text in zip(bank, texts["rows"]):
            kws = keywords(r["proposition"])
            m0 = float(np.mean([in_fact_room(c, kws) for c in empty]))
            m = float(np.mean([in_fact_room(c, kws) for c in sample(text)]))
            inr = m >= a.tau
            cost = 0 if m0 >= a.tau else (len(text) if inr else None)
            ot.append({"scenario_id": r["scenario_id"], "incentive": r["incentive"], "split": r.get("split", ""),
                       "ot_mode": a.ot_mode, "ot_ask": a.ot_ask, "ot_format": a.ot_format, "keywords": kws, "mass_empty": m0, "mass_note": m, "in_room": inr, "ot": cost})
        Path(a.ot).write_text("".join(json.dumps(x) + "\n" for x in ot))
        print(f"saved {a.ot}")
    return 0


def ot_summary(rows):
    out = {}
    for inc in sorted({r["incentive"] for r in rows}):
        for sp in ("fit", "eval"):
            s = [r for r in rows if r["incentive"] == inc and r["split"] == sp]
            if s:
                out[f"{inc}/{sp}"] = {"n": len(s), "entered": sum(r["in_room"] for r in s),
                                      "entered_from_empty": sum(r["ot"] == 0 for r in s),
                                      "mean_mass_note": float(np.mean([r["mass_note"] for r in s]))}
    return out


def analyze(a):
    bank = load(a.data)
    meta = join_meta(bank, a.button_dump)
    if a.button_dump and not Path(a.button_dump).is_file():
        print(f"WARN button dump missing: {a.button_dump} (public_button purity = missing)")
    Z = np.load(a.npz)
    res = {"bank": a.data, "button_dump": a.button_dump or "missing", "provisional": True}
    for key in ("H", "H_noask"):
        res[key] = analyze_matrix(Z[key], meta, seeds=a.seeds, steps=a.steps, nulls=a.nulls)
    if a.ot and Path(a.ot).is_file():
        res["ot"] = ot_summary(load(a.ot))
    res["note"] = "Diagnostics only. Not a gate. Not a camera. Not handoverPass. D not filled. r not frozen."
    Path(a.out).write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1)[:4000])
    return 0


def smoke(a):
    bank = load(a.data)
    meta = join_meta(bank, a.button_dump)
    rng = np.random.default_rng(1)
    X = rng.standard_normal((len(bank), 64)).astype(np.float32)
    inc = np.array([m["incentive"] == "hide" for m in meta], np.float32)
    X[:, :8] += 6 * inc[:, None]  # plant an incentive signal so purity must exceed the null
    r = analyze_matrix(X, meta, seeds=2, steps=3, nulls=10, pca=16)
    print(json.dumps(r, indent=1)[:2500])
    ok = r["som"]["raw"]["incentive"]["eval_purity_mean"] > r["som"]["raw"]["incentive"]["shuffle_null_p95"]
    rows = [{"scenario_id": m["scenario_id"], "incentive": m["incentive"], "split": m["split"],
             "mass_note": 1.0, "in_room": True, "ot": 0} for m in meta]
    print("ot summary", json.dumps(ot_summary(rows))[:300])
    kw = keywords(bank[0]["proposition"]); print("keywords", kw, in_fact_room(bank[0]["proposition"], kw))
    print("smoke", "OK" if ok else "FAIL")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract"); e.add_argument("--model", required=True); e.add_argument("--data", required=True)
    e.add_argument("--layer", type=int, default=8); e.add_argument("--out", required=True)
    e.add_argument("--incentive-in-user", action="store_true"); e.add_argument("--role-frame", default="")
    e.add_argument("--ot", default=""); e.add_argument("--n-samples", type=int, default=4)
    e.add_argument("--max-new", type=int, default=24)
    e.add_argument("--ot-mode", choices=["chat", "note"], default="chat"); e.add_argument("--ot-ask", default=""); e.add_argument("--ot-format", choices=["yesno", "open"], default="yesno"); e.add_argument("--tau", type=float, default=0.5)
    an = sub.add_parser("analyze"); an.add_argument("--data", required=True); an.add_argument("--npz", required=True)
    an.add_argument("--button-dump", default=""); an.add_argument("--ot", default=""); an.add_argument("--out", required=True)
    an.add_argument("--seeds", type=int, default=3); an.add_argument("--steps", type=int, default=30); an.add_argument("--nulls", type=int, default=20)
    s = sub.add_parser("smoke"); s.add_argument("--data", required=True); s.add_argument("--button-dump", default="")
    a = p.parse_args()
    return {"extract": extract, "analyze": analyze, "smoke": smoke}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
