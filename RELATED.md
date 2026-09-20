# Related work

This repo asks whether an $r$ tracks **strategy given topic**. It is not a detector paper.
Same citations as [regret-heuristic/neighbors.md](https://github.com/kummahiih/regret-heuristic/blob/main/neighbors.md), aimed at the sensor.

- Goldowsky-Dill et al. 2025 (arXiv:2502.03407): linear probes can look strong and still not be a defence. Our identity control is that failure on n=4: topic acc 1.0, strategy gap 0.01.
- Wang et al. 2025 (arXiv:2506.04909): steering at inference. Different lever than training $r$.
- Long et al. EMNLP 2025: SAE features of *deceptive instructions*. Treat as wallpaper until they survive a topic probe.
- Kumar 2026 (arXiv:2605.27958): clean AUROC dies under style shift; $k=1$ rejected. $\max\cos$ to a two-sentence bank is that geometry. Paraphrase shift is the cheap version of their style test.
- LEACE / INLP: erase a labeled concept. Useful slogan; not implemented here.
- Elhage et al. 2022 (Transformer Circuits, superposition): residual streams pack more features than dimensions. That is why last-token identity smears topic and plan (0.77 / 0.80 in the hinge repo).
- Liu et al. 2025: interference among packed directions scales like $1/m$. A wider model is not automatically a factored $r_{\mathrm{strat}}$.

The hinge in [regret-heuristic](https://github.com/kummahiih/regret-heuristic) consumes a vector that has already failed the topic probe. Do not train that hinge here.

Do not cite these as evidence that the hinge works.
