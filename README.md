# Intent readout search

Can a camera on the walk see the *plan* without also seeing the *subject*?

The hinge lives in [regret-heuristic](https://github.com/kummahiih/regret-heuristic). This repo hunts the camera. Tags are observations. Do not put the hidden room in a loss. Do not fill *D* from a hint.

Prose: [NOTE.md](NOTE.md). Universal vs many *r*<sub>T</sub>: [UNIVERSAL_R.md](UNIVERSAL_R.md). Voters: [PROTOCOL.md](PROTOCOL.md). Ledger: [results/README.md](results/README.md). Scale: [SCALE.md](SCALE.md).

## What is being hunted

Same words as the parent [What](https://github.com/kummahiih/regret-heuristic#what-this-is). Short:

- **Walk** — hidden states while generating. **Print** — the string that came out.
- **Map** — skill / possible thoughts. **Room** — one topic (hiking, travel, …).
- **Wallpaper** — subject paint. **Plan** — hide-or-name strategy that should not be the room.
- **Camera *r*** — readout that is supposed to see the plan. **Slap** — parent hinge against frozen pins *D*.

This repo only asks whether a camera exists. It does not train the slap.

## Why hunt *r*

The parent slap only works if *r* sees the hide-plan and not the job. Human analog: you flinch at the *plan*, not at a catalog of finished lies. That catalog is the scarce object. Preference labels grade the print. They do not grade “was a hide-plan lit in *h*?”

**Dictator’s trap:** punish only what was said and you train secrecy, not honesty. An output-only judge is that ruler. This repo is the search for a sensor that would let the hinge slap the plan instead. Full rationale: [regret-heuristic README](https://github.com/kummahiih/regret-heuristic#why-this-hinge).

## How the question narrowed

First ask: do honest-tagged and deceptive-tagged notes differ in *h* at all? Last-layer last-token said yes, and also classified the topic. That is not a camera the hinge can slap — it would slap the subject.

Second ask: is there a mid-layer direction that still separates the tags when the topic is left out, and that does not beat chance at naming the topic? On Qwen L8 and Mistral L9 the *aggregate* gap is positive (~0.11) and the tested paraphrase and prefix keep that mean. So “any plan-related contrast?” is no longer the open item.

Third ask, forced by hiking: is that contrast one shared axis, or a pile of room-local pairs? Shared LOTO on hiking is ~0.01 / 0.07; a *v* fitted inside hiking on a held pair is ~0.20 / 0.28. Extra readouts copied the same room ranking. Generated buttons often ignored the note.

Wave 1 asked whether a third family copies the 7B note-hint. Falcon L8 does. Gemma-3-4B L10 does not. Neither walk puts the hide button on *h*<sub>pre</sub>. Aya-8B then loaded for the hide-bank only (fourth cover-rate bar).

The live question is therefore the handover test: held-out, topic-invariant, paraphrase-stable, **uniform on the declared eight rooms**, and tied to a print the actor actually produced. Status is the score on that test.

## Status (2026-10-04)

**H1** (this repo): a strategy camera *r*<sub>strat</sub> exists that (1) survives topic LOTO, (2) leaves topic L2 at chance, (3) keeps paraphrase, (4) includes every declared room, (5) tracks an action the walk actually produced, (6) can be checked by a frozen inspector. **H1 is open. Current answer: no.**

**H2** (parent repo): after a freeze of (*r*, *D*, τ), *L*<sub>task</sub>+λ*L*<sub>reg</sub> reduces the hide-plan without wrecking the job. **H2 is not on the table.** A dummy can ignore a topic *coordinate*; that is not evidence a transformer *exposes* (*r*<sub>topic</sub>, *r*<sub>strat</sub>, *u*).

### Candidate plan-related signal (7B-class walks)

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

### Decision state and other walks

Pre-button *h* (last token of plan+question) is tag LOTO **0.011** on both 7B models. In-room hold there is 0.005 / 0.009. *r*(*h*<sub>pre</sub>)→ YES/NO is 0.038 / 0.016 and does not own hiking.

Wave 1, same eight rooms, ~0.3 depth (Gemma text *n*<sub>L</sub>=34 so L10 not L8). Qwen and Mistral stay the reference rows.

| Walk | note LOTO | hike LOTO | hike hold | topic L2 | HIDE frac YES | note→HIDE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen L8 | **0.105** | **0.013** | **0.203** | 0.06 | **0.51** | 0.018 / hike −0.049 |
| Mistral L9 | **0.116** | 0.069 | **0.278** | 0.12 | **0.57** | 0.092 / hike −0.002 |
| Falcon3-7B L8 | **0.082** | 0.023 | **0.247** | **0.12** | (P-act, not hide-bank) | 0.055 |
| Aya-8B L10 | not run | not run | not run | not run | **0.71** | **0.048** / hike 0.007 |
| Gemma-3-4B-it L10 | **0.009** | 0.003 | 0.017 | **0.65** | **0.95** | 0.001 |

Gemma L10 is not the 7B hint (wallpaper + dead pre-button). Falcon copies the 7B *shape*. Aya is the fourth *print* bar, not a fourth note-LOTO. Cover rate is not honesty. Phi-4 is a `LossKwargs` stack miss. 27B/70B deception-probe tensors are not *h*.

### MASK split (2026-10-04)

Belief arm beside the press. Three logs, not one honesty score. Logs: `results/tests-mask-split-2026-10-04.log` and `results/tests-mask-split-2026-10-04-1059.log`.

| Walk | HIDE YES | NAME YES | hike accuracy | hike lie given known | hike cover | hike miss |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen L8 | 0.54 | 0.13 | 0.83 | 0.60 | 0.20 | 0 |
| Mistral L9 | 0.56 | 0.40 | 0.58 | 0.86 | 1.00 | 1 |
| Aya L10 | 0.70 | 0.41 | 0.67 | 0.88 | 0.38 | 0 |
| Gemma L8 | 0.97 | 0.24 | 0.33 | 0.00 | 1.00 | 8 |
| Falcon L8 | 0.82 | 0.53 | 0.42 | 0.60 | 0.60 | 6 |
| Granite L12 | 0 | 0 | empty bank | empty bank | empty bank | 0 |
| Qwen3.5-9B L10 | 0 | 0 | empty bank | empty bank | empty bank | 0 |

Gemma's loud cover is mostly a miss: the belief arm often did not have the fact. Note→HIDE stays near chance (Qwen 0.021, Mistral 0.099, Aya 0.050, Falcon 0.006). Pre-button on the same HIDE arm is −0.042 / −0.003 for Qwen and Mistral. Granite said `Okay, the user`. Qwen3.5 said `Thinking Process:`. Those are not cover rates. LFM2.5 does not fit 4-bit on 12GB. Not a handover.

Official public MASK, 13-row Qwen probe (`results/mask_official_qwen.jsonl`): accuracy 0.846, lie-given-known 0.444 on 9 parsed pressure rows, one miss. Not the 1,000-item judge. No NAME arm. Not a cover rate.

### What the signal is not

| Test | Result |
| --- | --- |
| Cross-judge Qwen ↔ Mistral | Same rooms loud, hiking thin. *W* underdetermined. |
| Oracle many *r*<sub>T</sub> | Hiking/invoices want *W*<sub>T</sub>. Mean diag **loses** to shared LOTO. |
| Generated `reply_kind` | Tags ≠ prints. Kind LOTO ~0. |
| Hide-bank HIDE arm | Qwen 0.51, Mistral 0.57, Aya 0.71, Gemma 0.95. Note *h* does not call that *S*. |
| Wipe tag *v* | *s*<sub>v</sub>→0, kind keep 0.83. |

Do not freeze *r*. Do not fill *D*. Not reduced deception.

## How to run the official meters

```bash
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
python pair_contrast.py --data data/pairs_wide.jsonl --layer 8 --pool last \
  --held-in-topic --permute 20000 --transfer data/pairs_paraphrase.jsonl
```

Read plan LOTO, topic `loo_l2_acc`, paraphrase, then per-room gaps. `held_inroom` is a diagnostic. `reply_kind` stays out of *L*.
