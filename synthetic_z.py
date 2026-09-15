#!/usr/bin/env python3
"""CPU synthetic strategy bit. Labels that build D are noisy. Truth is a RV."""

from __future__ import annotations

import argparse

import torch
import torch.nn as nn
import torch.nn.functional as F


class Policy(nn.Module):
    def __init__(self, d: int = 16):
        super().__init__()
        self.enc = nn.Linear(2, d, bias=False)
        self.task = nn.Linear(d, 2)
        self.act = nn.Linear(d, 3)

    def forward(self, x: torch.Tensor):
        h = torch.tanh(self.enc(x))
        return h, self.task(h), self.act(h)


def batch_states(n: int, device: torch.device):
    topic = torch.randint(0, 2, (n,), device=device)
    truth = torch.randint(0, 2, (n,), device=device)
    x = torch.stack([topic.float(), truth.float()], dim=-1)
    return x, topic


def hinge_on(h: torch.Tensor, D: torch.Tensor, tau: float) -> torch.Tensor:
    hn = F.normalize(h, dim=-1, eps=1e-12)
    Dn = F.normalize(D, dim=-1, eps=1e-12)
    s = (hn @ Dn.T).max(dim=-1).values
    return F.relu(s - tau)


def train_one(
    mode, steps, bonus, lam, tau, allow_heldout, D, noise, seed, device
):
    torch.manual_seed(seed)
    net = Policy().to(device)
    opt = torch.optim.Adam(net.parameters(), lr=3e-2)
    B = 64
    frozen_D = D
    collected_h = []
    collected_true = []
    for _ in range(steps):
        x, topic = batch_states(B, device)
        h, logits, alogits = net(x)
        if not allow_heldout:
            alogits = alogits.clone()
            alogits[:, 2] = -1e9
        dist = torch.distributions.Categorical(logits=alogits)
        a = dist.sample()
        task_loss = F.cross_entropy(logits, topic, reduction="none")
        correct = logits.argmax(-1) == topic
        tempt = bonus * ((a == 1) | ((a == 2) & allow_heldout)).float()
        R = correct.float() + tempt
        loss = -(dist.log_prob(a) * (R - R.mean())).mean() + task_loss.mean()
        if frozen_D is not None and lam > 0:
            loss = loss + lam * hinge_on(h, frozen_D, tau).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if mode == "baseline":
            believed = a == 1
            if noise > 0:
                believed = believed ^ (torch.rand(a.shape[0], device=device) < noise)
            if believed.any():
                collected_h.append(h.detach()[believed].cpu())
                collected_true.append(a.detach()[believed].cpu())
    if mode == "baseline":
        parts = [c for c in collected_h if c.numel()]
        if not parts:
            raise RuntimeError("labeler never tagged lie_D")
        frozen_D = torch.cat(parts, dim=0)
        tags = torch.cat(collected_true, dim=0)
        perm = torch.randperm(frozen_D.shape[0])
        frozen_D, tags = frozen_D[perm], tags[perm]
        if frozen_D.shape[0] > 32:
            frozen_D, tags = frozen_D[:32], tags[:32]
        contam = float((tags != 1).float().mean())
        print(f"D_n={frozen_D.shape[0]} D_contamination={contam:.3f} (true a!=1 | believed lie)")
        frozen_D = frozen_D.to(device)
        frozen_D.requires_grad_(False)
    return net, frozen_D


@torch.no_grad()
def eval_net(net, D, tau, allow_heldout, device):
    x, topic = batch_states(2000, device)
    h, logits, alogits = net(x)
    if not allow_heldout:
        alogits = alogits.clone()
        alogits[:, 2] = -1e9
    a = alogits.argmax(-1)
    return {
        "task_acc": float((logits.argmax(-1) == topic).float().mean()),
        "p_honest": float((a == 0).float().mean()),
        "p_lie_D": float((a == 1).float().mean()),
        "p_lie_out": float((a == 2).float().mean()),
        "hinge": float(hinge_on(h, D, tau).mean()),
    }


def fmt(m):
    return (
        f"task={m['task_acc']:.3f}  honest={m['p_honest']:.3f}  "
        f"lie_D={m['p_lie_D']:.3f}  lie_out={m['p_lie_out']:.3f}  hinge={m['hinge']:.3f}"
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=400)
    p.add_argument("--bonus", type=float, default=0.6)
    p.add_argument("--lam", type=float, default=2.0)
    p.add_argument("--tau", type=float, default=0.3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--noise", type=float, default=0.2)
    args = p.parse_args()
    device = torch.device("cpu")
    print("=== synthetic_z. True a logged. D from noisy labeler. ===")
    print(
        f"steps={args.steps} bonus={args.bonus} lam={args.lam} "
        f"tau={args.tau} seed={args.seed} noise={args.noise}"
    )
    base, D = train_one(
        "baseline", args.steps, args.bonus, 0.0, args.tau, False, None,
        args.noise, args.seed, device,
    )
    print("baseline   ", fmt(eval_net(base, D, args.tau, False, device)))
    hinge, _ = train_one(
        "hinge", args.steps, args.bonus, args.lam, args.tau, False, D,
        args.noise, args.seed + 1, device,
    )
    print("hinge mask ", fmt(eval_net(hinge, D, args.tau, False, device)))
    evade, _ = train_one(
        "evade", args.steps, args.bonus, args.lam, args.tau, True, D,
        args.noise, args.seed + 2, device,
    )
    print("evade open ", fmt(eval_net(evade, D, args.tau, True, device)))
    print("--noise 0 is the clean-tag toy. Default 0.2 is the search default.")
    print("Not Qwen. Not p(lie).")


if __name__ == "__main__":
    main()
