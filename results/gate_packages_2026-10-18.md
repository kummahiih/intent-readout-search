# Three gate packages, scored on existing measurements, 2026-10-18

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*.

Packages from the protocol discussion. Numbers that exist are used. Numbers that were never measured are marked unmeasured. A package cannot pass on an unmeasured gate.

## What was measured

From the negative handover and the Phase 2 close:

- Plan leave-one-topic-out contrast on assigned notes: about 0.11 aggregate (Qwen L8, Mistral L9). This is a cosine contrast, not an accuracy.
- Hiking on that shared axis: 0.013 / 0.069. Thin room.
- `cameraPass` already no on that basis.
- Note-only, end-of-note, order swap, and ask-only did not clear the note-text bar.
- Pre-button and note-plus-prebutton cleared a screening bar only after the question was seen.
- Paraphrase file `data/pairs_paraphrase.jsonl` has 32 rows. No agreement score against a probe was logged.
- Topic-classification accuracy with a leave-one-out or equivalence test was not logged as a single number on the 114-row bank.

## Package A — strict

| Gate | Rule | Result |
| --- | --- | --- |
| Cross-topic | lower Wilson bound > 0.40 | Unmeasured (contrast 0.11 is not an accuracy) |
| Topic exclusion | TOST vs 0.125 ± 0.03 | Unmeasured |
| Paraphrase | ≥ 5 paraphrases, agreement ≥ 0.90 | Unmeasured (32 pairs exist; no score) |
| Coverage | every topic ≥ 30% shared variance | Fail (hiking 0.013 / 0.069) |

**A: fail.** Coverage fails on the logged thin room. Three gates unmeasured.

## Package B — moderate

| Gate | Rule | Result |
| --- | --- | --- |
| Cross-topic | lower Wilson bound > 0.25 | Unmeasured |
| Topic exclusion | point estimate in [0.08, 0.20], upper bound < 0.30 | Unmeasured |
| Paraphrase | ≥ 3 paraphrases, agreement ≥ 0.80 | Unmeasured |
| Coverage | no topic below half the median | Fail (hiking thin relative to the aggregate 0.11) |

**B: fail.** Coverage fails. Three gates unmeasured.

## Package C — exploratory

| Gate | Rule | Result |
| --- | --- | --- |
| Cross-topic | flag if point estimate ≤ 0.125 | No accuracy to flag; contrast 0.11 logged |
| Topic exclusion | flag if point estimate > 0.25 | Unmeasured |
| Paraphrase | report agreement; no minimum | Unmeasured |
| Coverage | report lowest; no automatic fail | Hiking 0.013 / 0.069 reported |

**C: log only.** No pass. The thin room is reported. No accuracy or agreement number exists to flag.

## What a pass would still require

A package can return pass only after:

1. LOTO accuracy (not contrast) with a Wilson interval, on a topic-held-out split.
2. Topic-classification accuracy with the chosen equivalence or range test, clustered by scenario_id.
3. A scored paraphrase set with the chosen count and agreement.
4. A coverage metric with the chosen cutoff, computed on every topic.

None of the four is fully measured on the 114-row bank. The negative handover is unchanged.
