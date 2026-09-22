"""Topic metrics. In-sample lstsq can memorize. Official B0 on vectors is LOO centroid.

On 1-d scores, cosine keeps only the sign. Use loo_l2_acc there.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def cosine(a, b):
    return float(
        (F.normalize(a.unsqueeze(0), dim=-1) @ F.normalize(b.unsqueeze(0), dim=-1).T)
        .clamp(-1, 1)
        .item()
    )


def topic_acc_lstsq(vecs, topics):
    """Fit and score on the same rows. Can hit 1.00 on random labels."""
    names = sorted(set(topics))
    tid = {t: i for i, t in enumerate(names)}
    X = F.normalize(torch.stack(vecs), dim=-1)
    y = torch.tensor([tid[t] for t in topics])
    Y = F.one_hot(y, num_classes=len(names)).float()
    W = torch.linalg.lstsq(X, Y).solution
    pred = (X @ W).argmax(dim=-1)
    return float((pred == y).float().mean()), names


def topic_acc(vecs, topics):
    return topic_acc_lstsq(vecs, topics)


def loo_centroid_acc(vecs, labels):
    """Cosine to leave-one-out class means. On 1-d input this is sign-only."""
    n = len(vecs)
    names = sorted(set(labels))
    hit = 0
    for i in range(n):
        scores = {}
        for name in names:
            members = [vecs[j] for j in range(n) if j != i and labels[j] == name]
            if not members:
                continue
            scores[name] = cosine(vecs[i], torch.stack(members).mean(0))
        if scores and max(scores, key=scores.get) == labels[i]:
            hit += 1
    return hit / n if n else 0.0


def loo_l2_acc(vecs, labels):
    """Nearest leave-one-out class mean in Euclidean distance. Keeps magnitude."""
    n = len(vecs)
    names = sorted(set(labels))
    hit = 0
    for i in range(n):
        best_name, best_d = None, None
        x = vecs[i].reshape(-1).float()
        for name in names:
            members = [vecs[j] for j in range(n) if j != i and labels[j] == name]
            if not members:
                continue
            mu = torch.stack(members).mean(0).reshape(-1).float()
            d = float((x - mu).norm())
            if best_d is None or d < best_d:
                best_d, best_name = d, name
        if best_name == labels[i]:
            hit += 1
    return hit / n if n else 0.0
