# Acceptance criteria v1 (pre-registration)

Date: 2026-11-01 (Europe/Helsinki). Frozen at the commit that adds this file, before any run listed below.

Not a camera. Not `handoverPass`. Not `cameraPass`. Do not fill D. The prototype bank is empty. No readout is frozen; do not freeze r. The negative handover of 2026-10-13 is unchanged (regret-heuristic `paper/negative_handover.md`, 10.5281/zenodo.23328706). A pass under these criteria is at most a bounded level-2 claim (cross-context generalization, regret-heuristic `paper/intent_v2.md`), not evidence of a strategy representation by itself.

## Why now

`paper/intent_v2.md` states that no gate package has been selected (lines 281, 296, 388) and that the 114-row results are exploratory after repeated selection on the same bank (line 325). The note-plus-question text baseline (line 154) and paired tests (lines 277, 388) have not been run. These criteria are frozen first so that neither result can choose the bar.

## Data

- The current 114-row bank is thin (53–55 held-out rows) and is used up for confirmation. No row of it is confirmatory. It may be reported only as exploratory.
- Scenario expansion is expected before any final claim. Sources: the 60 candidate rows already produced against `data/find_scenarios.md` (15 ids, 8 topics), after (a) moving the cover instruction out of the note and (b) passing the leak check below; and further sources as needed (e.g. gated MASK / Liars' Bench items, after license checks).
- Leak check (on fit only): a note-only unigram classifier must predict `incentive` at ≤ 0.60. Rows that fail are redesigned, not dropped silently.
- Split: by `scenario_id`, balanced within topic, assigned before any fitting, preprocessing, layer or threshold choice. Planned file `data/prereg_split.json` (not yet created). Every paraphrase stays with its id.
- Confirmatory eval bank: planned `data/scenarios_prereg_eval.jsonl` (not yet created). It is frozen by commit before any button generation.
- Four counts reported separately: rows in, rows excluded, invalid generations, missing buttons.

## Models

Qwen2.5 (as in the October walks) and gemma-2-9b-it, local weights, 4-bit, 12 GB GPU. Other models are exploratory.

## Endpoints

- Primary: held-out accuracy on the realized public button.
- Secondary, never pooled with the primary: the same readout against the assigned incentive.
- Scenario-level holdout and topic-level holdout are reported separately.

## Primary candidate

Exactly one: the note-plus-prebutton combination at layer −1, as implemented in `phase2_combine.py` at the commit of this file. All other probes are exploratory.

## Required comparator

The strongest of three text baselines, selected on fit only: unigram note-only; unigram note+question concatenated; TF-IDF (1–2-gram) logistic regression on note+question. Planned script `text_baselines.py` (not yet created).

## Test

- Exact McNemar on held-out rows, and a scenario-cluster bootstrap (10,000 resamples) 95% CI of the accuracy difference. Both must exclude 0 at α = 0.05, Holm-corrected across the two models. Planned script `paired_tests.py` (not yet created).
- Non-overlapping Wilson intervals stay a screening display only, not the test.
- Ask-removal controls (note-only, end-of-note, order swap, ask-only), the reversed-polarity check and length variants must each fail the same test against the same comparator. If any control passes, the result is classified as response preparation, not a plan.

## Gates

Package B (moderate) from `intent_v2.md` is selected for all four gates:
- Cross-topic transfer: LOTO accuracy, lower 95% Wilson bound > 0.25.
- Topic exclusion: point estimate in [0.08, 0.20] and upper bound < 0.30.
- Paraphrase stability: ≥ 3 paraphrases, agreement ≥ 0.80.
- Room coverage: no topic below half the median shared-axis mass. Mass = summed |projection on the shared axis| per topic / total, computed on held-out data.

Topic means used for any centering (including SOM topic-mean subtraction) are estimated on fit only. SOM, OT and purity-law outputs remain diagnostics, not gates.

## Power

If valid held-out buttons < 120, the outcome is UNDERPOWERED, not FAIL. A bank below that size is registered as a pilot and cannot issue PASS.

## Outcomes

PASS (every item above) / FAIL / UNDERPOWERED / INVALID (a count or split rule broken). PASS is not `cameraPass`, not `handoverPass`, does not fill D and does not freeze r.

## Change rule

This file (v1) is never edited. Any change goes to a dated `protocol/acceptance_criteria_v2_YYYY-MM-DD.md` that names what changed and why, committed before the run it governs.
