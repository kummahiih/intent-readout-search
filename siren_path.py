#!/usr/bin/env python3
"""SIREN path object. Query f(t). Do not put theta in L.

Matches regret-heuristic/simulation_siren_path.py:
three-layer sine MLP, first-layer omega 30, Adam on MSE(h_t).
r is f(query_t), default t=1 (path end). theta L2 is a log.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class TinySiren(nn.Module):
    def __init__(self, d: int, hidden: int = 16, omega: float = 30.0):
        super().__init__()
        self.fc1 = nn.Linear(1, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        self.fc3 = nn.Linear(hidden, d)
        with torch.no_grad():
            self.fc1.weight.mul_(omega)

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        x = torch.sin(self.fc1(t))
        x = torch.sin(self.fc2(x))
        return self.fc3(x)


def fit_path(
    path: torch.Tensor,
    steps: int = 80,
    hidden: int = 16,
    lr: float = 1e-2,
    omega: float = 30.0,
    seed: int = 0,
) -> TinySiren:
    if path.ndim != 2:
        raise ValueError(f"path must be T x d, got {tuple(path.shape)}")
    T, d = path.shape
    g = torch.Generator()
    g.manual_seed(int(seed) & 0x7FFFFFFF)
    torch.manual_seed(int(seed) & 0x7FFFFFFF)
    net = TinySiren(d, hidden=hidden, omega=omega)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    t = torch.linspace(0, 1, T).unsqueeze(-1)
    path = path.float().detach()
    for _ in range(steps):
        pred = net(t)
        loss = F.mse_loss(pred, path)
        opt.zero_grad()
        loss.backward()
        opt.step()
    return net


def theta_vec(net: TinySiren) -> torch.Tensor:
    return torch.cat([p.detach().flatten() for p in net.parameters()])


def query_end(net: TinySiren, t: float = 1.0) -> torch.Tensor:
    with torch.no_grad():
        return net(torch.tensor([[float(t)]]))[0].detach()


def fit_and_query(
    path: torch.Tensor,
    query_t: float = 1.0,
    steps: int = 80,
    hidden: int = 16,
    lr: float = 1e-2,
    seed: int = 0,
) -> tuple[torch.Tensor, torch.Tensor, float, float]:
    net = fit_path(path, steps=steps, hidden=hidden, lr=lr, seed=seed)
    r = query_end(net, query_t)
    th = theta_vec(net)
    T = path.shape[0]
    tgrid = torch.linspace(0, 1, T).unsqueeze(-1)
    with torch.no_grad():
        pred = net(tgrid)
        mse = float(F.mse_loss(pred, path.float()))
        last = path[-1].float()
        cos = float(
            (
                F.normalize(r.unsqueeze(0), dim=-1)
                @ F.normalize(last.unsqueeze(0), dim=-1).T
            ).clamp(-1, 1)
        )
    return r.cpu(), th.cpu(), mse, cos
