"""Talker-count m-hat. Uncertainty log. Not in L. Not r.

Same meter as regret-heuristic/simulation_source_count.py.
Crowded hallway is not the slap.
"""

from __future__ import annotations

import torch


def source_count(H: torch.Tensor, rel: float = 0.05) -> int:
    """H: (n, d). Count singular values >= rel * s_max."""
    if H.ndim != 2 or H.shape[0] == 0:
        return 0
    s = torch.linalg.svdvals(H.float())
    if s.numel() == 0 or float(s[0]) <= 0:
        return 0
    return int((s >= rel * s[0]).sum().item())


def report_mhat(name: str, vecs, rel: float) -> int:
    if not vecs:
        print(f"m_hat_{name}=0 n=0 rel={rel}")
        return 0
    H = torch.stack([v.reshape(-1).float() for v in vecs])
    m = source_count(H, rel=rel)
    print(f"m_hat_{name}={m} n={H.shape[0]} d={H.shape[1]} rel={rel}")
    return m
