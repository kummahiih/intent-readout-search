#!/usr/bin/env python3
"""Combined mid-layer view. Not in L.

r = normalize( normalize(h_T) + normalize(kstep) + normalize(f(1)) )
Logs pairwise cosines so we can see if the three views are the same arrow.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F

from kstep_path import kstep_query
from siren_path import fit_and_query


def _unit(v: torch.Tensor) -> torch.Tensor:
    n = float(v.norm())
    if n <= 0:
        return v
    return v / n


def _cos(a: torch.Tensor, b: torch.Tensor) -> float:
    return float(
        (
            F.normalize(a.unsqueeze(0), dim=-1)
            @ F.normalize(b.unsqueeze(0), dim=-1).T
        ).clamp(-1, 1)
    )


def mid3_query(
    path: torch.Tensor,
    k: int = 8,
    siren_t: float = 1.0,
    siren_steps: int = 80,
    siren_hidden: int = 16,
    siren_lr: float = 1e-2,
) -> tuple[torch.Tensor, dict]:
    last = path[-1].float().cpu()
    kvec, kcos, kk = kstep_query(path, k=k)
    svec, theta, mse, scos = fit_and_query(
        path, query_t=siren_t, steps=siren_steps, hidden=siren_hidden, lr=siren_lr
    )
    combo = _unit(_unit(last) + _unit(kvec) + _unit(svec))
    meta = {
        "kstep_k": kk,
        "kstep_cos_to_last": kcos,
        "siren_mse": mse,
        "siren_cos_to_last": scos,
        "cos_last_kstep": _cos(last, kvec),
        "cos_last_siren": _cos(last, svec),
        "cos_kstep_siren": _cos(kvec, svec),
        "cos_mid3_last": _cos(combo, last),
        "theta": theta,
    }
    return combo, meta
