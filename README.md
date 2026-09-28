# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill *D* from a hint.

Prose: [NOTE.md](NOTE.md). Universal vs many *r*<sub>T</sub>: [UNIVERSAL_R.md](UNIVERSAL_R.md). Voters: [PROTOCOL.md](PROTOCOL.md). Ledger: [results/README.md](results/README.md).

## How the question narrowed

First ask: do honest-tagged and deceptive-tagged notes differ in *h* at all? Last-layer last-token said yes, and also classified the topic. That is not a camera the hinge can slap — it would slap the subject.

Second ask: is there a mid-layer direction that still separates the tags when the topic is left out, and that does not beat chance at naming the topic? On Qwen L8 and Mistral L9 the *aggregate* gap is positive (~0.11) and the tested paraphrase and prefix keep that mean. So “any plan-related contrast?” is no longer the open item.

Third ask, forced by hiking: is that contrast one shared axis, or a pile of room-local pairs? Shared LOTO on hiking is ~0.01 / 0.07; a *v* fitted inside hiking on a held pair is ~0.20 / 0.28. Extra readouts copied the same room ranking. Generated buttons often ignored the note.

The live question is therefore the handover test: held-out, topic-invariant, paraphrase-stable, **uniform on the declared eight rooms**, and tied to a print the actor actually produced. Status is the score on that test.

## Status (2026-09-28)

### Candidate plan-related signal

Mid-layer last-token contrast on assigned notes (Qwen2.5-7B layer 8, Mistral-7B layer 9) separates the two plan tags on held-out topics and keeps that *aggregate* under the tested rewords and prefix.

| Official meter on notes | Qwen L8 | Mistral L9 |
| --- | ---: | ---: |
| Plan LOTO (other topics fit *v*) | **0.105** | **0.116** |
| Paraphrase transfer | 0.108 | 0.123 |
| Prefix / frame | 0.102 | 0.125 |
| Topic L2 (chance 0.125) | 0.06 | 0.12 |

A gap of 0.105 is a cosine-score difference, not 10.5% accuracy. Last layer fails the topic gate. K-step / SIREN / mid3 track the same rooms (one arrow). Phrase: **candidate plan-related signal**. Not *r*<sub>strat</sub>. Not operative intent.

### Shared versus local

Hiking is the informative room. The shared eight-topic direction is thin there. A direction fitted *inside* hiking still separates a held pair and a fact-held reword.

| Hiking | Qwen L8 | Mistral L9 |
| --- | ---: | ---: |
| Shared LOTO | **0.013** | 0.069 |
| Within-topic hold (2+2 / 1+1) | **0.203** | **0.278** |
| Fact-held paraphrase (own *v*<sub>T</sub>) | 0.160 | 0.179 |
| LOTO on that paraphrase | 0.009 | 0.052 |
| Travel LOTO (same shared *v*) | ~0.17 | ~0.17 |

Weak shared transfer is not “no information in hiking.” It is not eight-room uniformity either. Genre (office-log / radio) is out of the voter set. Hold is a log, not a fifth freeze gate. Do not drop hiking.

### What the signal is not

| Test | Result |
| --- | --- |
| Cross-judge Qwen ↔ Mistral | Same rooms loud, hiking thin. *W* underdetermined. |
| Oracle many *r*<sub>T</sub> | Hiking/invoices want *W*<sub>T</sub>. Mean diag **loses** to shared LOTO. |
| 3-probe multi-*r* | Weaker than plain LOTO. Same room ranking. |
| Generated `reply_kind` | Tags ≠ prints. Kind LOTO ~0. |
| Forced YES/NO (fact ask) | Honest all NO. Hiking/travel all NO. |
| Plan-action YES/NO | Mistral hiking mixed (9/9). Qwen hiking still 0 YES. Kind 0.99 is token geometry. |

Do not freeze *r*. Do not fill *D*. Not reduced deception.

## How to run the official meters

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --held-in-topic --permute 20000 --transfer data/pairs_paraphrase.jsonl
```

Read plan LOTO, topic `loo_l2_acc`, paraphrase, then per-room gaps. `held_inroom` is a diagnostic. `reply_kind` stays out of *L*.
