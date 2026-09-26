# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The live question: a held-out, topic-invariant, paraphrase-stable strategy readout that survives within-topic cross-validation **and** is uniform on the declared eight rooms.

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill $D$ from a hint.

Prose writeup: [NOTE.md](NOTE.md). Voters: [PROTOCOL.md](PROTOCOL.md). Ledger: [results/README.md](results/README.md).

## Status (2026-09-27)

Mid-layer last-token contrast on Qwen2.5-7B layer 8 and Mistral-7B layer 9 is a **hint**, not $r_{\mathrm{strat}}$.

| | plan fit | topic L2 | paraphrase | 8-topic frame |
| --- | ---: | ---: | ---: | ---: |
| Qwen L8 last | 0.105 | 0.06 | 0.108 | 0.102 |
| Mistral L9 last | 0.116 | 0.12 | 0.123 | 0.125 |

Eight-way chance is 0.125. Last layer fails the topic gate (0.17–0.29). K-step / SIREN $f(1)$ / mid3 are one arrow.

| | LOTO hiking | held_inroom hiking | para_held_inroom hiking | LOTO travel |
| --- | ---: | ---: | ---: | ---: |
| Qwen L8 | **0.013** | **0.203** | **0.160** | ~0.17 |
| Mistral L9 | 0.069 | **0.278** | **0.179** | ~0.17 |

Hiking has a pair on a held fact and a reword. That pair is not the eight-room axis. Office-log / radio genre kills LOTO (Qwen held 0.004). Genre is out of the voter set. Hold is a log, not a fifth freeze gate.

Do not freeze $r$. Do not fill $D$. Do not drop hiking. Not reduced deception.

## How to run the official meters

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --held-in-topic --permute 20000 --transfer data/pairs_paraphrase.jsonl
```

Read plan LOTO, topic `loo_l2_acc`, paraphrase, per-room gaps. `held_inroom` / `para_held_inroom` are diagnostics.
