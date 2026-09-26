"""Paraphrase hold: fit v_T on wide rows whose fact != the transfer fact."""

from collections import defaultdict

import torch
import torch.nn.functional as F

from pair_contrast import cosine, per_topic_gaps, permute_p, report_gap


def paraphrase_hold_block(fit_paired, transfer_paired, hid, v_full, permute):
    print("para-hold: fit v_T on wide rows with a different fact. Score the reword.")
    inroom_ts = defaultdict(list)
    loto_ts = defaultdict(list)
    inroom_scores, loto_scores = [], []
    for t, tg in sorted(transfer_paired.items()):
        if t not in fit_paired:
            print(f"  topic={t} skip para-hold: no fit room")
            continue
        wide_d = list(fit_paired[t]["deceptive"])
        wide_h = list(fit_paired[t]["honest"])
        others = [v_full[u] for u in fit_paired if u != t and float(v_full[u].norm()) > 0]
        v_loto = F.normalize(torch.stack(others).mean(0), dim=0) if others else None
        facts = sorted(
            {
                r.get("fact", "")
                for r in tg["deceptive"] + tg["honest"]
                if r.get("fact")
            }
        )
        if not facts:
            print(f"  topic={t} skip para-hold: no fact field")
            continue
        for fact in facts:
            fit_d = [r for r in wide_d if r.get("fact") != fact]
            fit_h = [r for r in wide_h if r.get("fact") != fact]
            if not fit_d or not fit_h:
                print(f"  topic={t} skip fact: need leftover wide pair")
                continue
            v = torch.stack([hid[id(r)] for r in fit_d]).mean(0) - torch.stack(
                [hid[id(r)] for r in fit_h]
            ).mean(0)
            if float(v.norm()) <= 0:
                print(f"  topic={t} skip fact: zero v")
                continue
            v = F.normalize(v, dim=0)
            for strat in ("deceptive", "honest"):
                rows = [r for r in tg[strat] if r.get("fact") == fact]
                for r in rows:
                    s = cosine(hid[id(r)], v)
                    print(
                        f"  para_held_inroom topic={t} strategy={strat} s_v={s:.4f}"
                    )
                    inroom_ts[t].append((strat, s))
                    inroom_scores.append((strat, s))
                    if v_loto is None:
                        continue
                    sl = cosine(hid[id(r)], v_loto)
                    print(
                        f"  para_held_loto topic={t} strategy={strat} s_v={sl:.4f}"
                    )
                    loto_ts[t].append((strat, sl))
                    loto_scores.append((strat, sl))
    if not inroom_scores:
        print("ERROR: no para-hold scores")
        return
    gap_ir = report_gap(inroom_scores, "para_held_inroom")
    per_topic_gaps(inroom_ts, "per-topic para_held_inroom gaps")
    if gap_ir is not None and permute > 0:
        permute_p(inroom_ts, gap_ir, permute)
    if loto_scores:
        gap_lo = report_gap(loto_scores, "para_held_loto")
        per_topic_gaps(loto_ts, "per-topic para_held_loto gaps")
        if gap_lo is not None and permute > 0:
            permute_p(loto_ts, gap_lo, permute)
    print("para-hold is a diagnostic. Not a freeze voter. Do not fill D.")
