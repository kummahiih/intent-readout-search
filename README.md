# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The live question: a held-out, topic-invariant, paraphrase-stable strategy readout that survives within-topic cross-validation **and** is uniform on the declared eight rooms **and** tracks a print the actor actually produced.

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

Prose: [NOTE.md](NOTE.md). Universal vs many $r_{T}$: [UNIVERSAL_R.md](UNIVERSAL_R.md). Voters: [PROTOCOL.md](PROTOCOL.md). Ledger: [results/README.md](results/README.md).

## Status (2026-09-28)

Mid-layer last-token contrast on Qwen2.5-7B layer 8 and Mistral-7B layer 9 is a **note-space hint**, not $r_{\mathrm{strat}}$.

| Official gate (notes) | Qwen L8 | Mistral L9 |
| --- | ---: | ---: |
| plan LOTO | 0.105 | 0.116 |
| topic L2 | 0.06 | 0.12 |
| paraphrase | 0.108 | 0.123 |
| frame | 0.102 | 0.125 |
| LOTO hiking / travel | **0.013** / ~0.17 | 0.069 / ~0.17 |
| held_inroom hiking | 0.203 | 0.278 |
| para_held_inroom hiking | 0.160 | 0.179 |

Eight-way chance is 0.125. Last layer fails the topic gate. K-step / SIREN / mid3 are one arrow. Genre is out. Hold is a log, not a fifth gate.

### What else we ran

| Test | Result |
| --- | --- |
| Cross-judge Qwen $\leftrightarrow$ Mistral | Same rooms loud, hiking thin. $W$ underdetermined. |
| Oracle many $r_{T}$ | Hiking/invoices want $W_{T}$. Mean diag **loses** to shared LOTO. |
| 3-probe multi-$r$ (tag + adversary + corr²) | Weaker than plain LOTO. Same room ranking. |
| Generate + `fact_margin` kind | Tags $\neq$ prints. Qwen mostly `truth`. Kind LOTO $\approx 0$. |
| Execute-plan + sample | Qwen contradict 0.08 $\to$ 0.14. Hiking still all `truth`. |
| Forced YES/NO (rule grader) | Honest = all NO. Hiking/travel = all NO. ~10 YES on other deceptive rooms. |

After a crude alignment, the same rooms stay loud and the same room stays thin. That is evidence the mid-layer hint is **domain-shaped**, not a portable judge. Many local $r_{T}$ are not the hinge camera. A print-level `reply_kind` still does not give a shared axis.

Do not freeze $r$. Do not fill $D$. Do not drop hiking. Not reduced deception.

## How to run the official meters

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --held-in-topic --permute 20000 --transfer data/pairs_paraphrase.jsonl
```

Read plan LOTO, topic `loo_l2_acc`, paraphrase, per-room gaps. `held_inroom` is a diagnostic. `reply_kind` stays out of $L$.
