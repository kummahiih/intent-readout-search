#!/usr/bin/env python3
"""K-step dynamical readout. Settle, then look. Not a SIREN. Not in L.

r = mean(h_{T-K+1:T}). Default K=8.
If cos(r, h_T) ~ 1, this is last-token in a wig.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def kstep_query(path: torch.Tensor, k: int = 8) -> tuple[torch.Tensor, float, int]:
    if path.ndim != 2:
        raise ValueError(f"path must be T x d, got {tuple(path.shape)}")
    T = path.shape[0]
    kk = max(1, min(int(k), T))
    vec = path[-kk:].float().mean(0)
    last = path[-1].float()
    cos = float(
        (
            F.normalize(vec.unsqueeze(0), dim=-1)
            @ F.normalize(last.unsqueeze(0), dim=-1).T
        ).clamp(-1, 1)
    )
    return vec.detach().cpu(), cos, kk
