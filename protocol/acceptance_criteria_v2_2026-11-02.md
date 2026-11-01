# Acceptance criteria v2 (draft, 2026-11-02, Europe/Helsinki)

Supplements v1 (`protocol/acceptance_criteria.md`, commit 57ff994). This file does not edit v1. Everything in v1 stands except the additions below. It must be committed before any run it governs.

Not a camera. Not `handoverPass`. Not `cameraPass`. D is not filled. r is not frozen. The negative handover of 2026-10-13 is unchanged.

## What changed and why
v1 does not say whether the text-baseline comparator may see `incentive_context`, the persona/pressure text moved out of the note in `data/prereg/` (commit 0f9b5a9). If the readout's model input contains that text and the comparator does not, the comparator is weaker than the input it is compared with.

## Rule: same visible text, expanded comparator set
Every text-baseline comparator receives the full visible text that the readout model sees up to the readout position: note + question, plus `incentive_context` whenever it is in the model prompt, in prompt order. This replaces v1's narrower inputs; v1's "note-only" and "note+question" baselines are run on the full visible text. The required comparator set is:
1. Unigram classifier (v1 "unigram note-only").
2. Unigram classifier (v1 "unigram note+question").
3. TF-IDF (1–2-gram) logistic regression (v1).
4. **New:** TF-IDF (1–3-gram) logistic regression.

The strongest of the four is selected on fit only (GroupKFold by `scenario_id`). The residual readout must beat it on held-out rows by v1's test: exact McNemar and a scenario-cluster bootstrap (10,000 resamples) 95% CI of the accuracy difference. Both must exclude 0 at α = 0.05, Holm-corrected across the two models. A sentence-embedding baseline is allowed only if pre-declared in a later dated file. It is not part of v2.

## Leak rule (scoped)
The incentive has to be visible to the model somewhere, or there is nothing for a readout to read. Leakage through `incentive_context`, and therefore through the full visible prompt, is inherent and is not a defect. The honest guard against it is the rule above: the comparator sees that same text and may exploit it, so a recoverable context raises the bar the readout must clear rather than invalidating the bank. What must not carry the incentive is the fact-bearing text. If the note, or note + question, predicts incentive, then the readout cannot be separated from the fact wording that the contract keeps shared across incentives. Therefore: **INVALID-by-leak only if note or note+question is predicted at > 0.60 on fit CV by any comparator family**, including the 1–3-gram LR. Context and full-prompt leak numbers are reported for every family but do not gate. When the context is recoverable at a high rate (e.g. ≥ 0.90), a PASS becomes correspondingly hard, and that is reported, not hidden.

## Leak-check reporting (fit only, GroupKFold by scenario_id; Wilson 95%; eval reported, not used for selection)
All three comparator families (unigram NB, TF-IDF 1–2 LR, TF-IDF 1–3 LR; comparators 1 and 2 coincide once both see the full visible text) are run on each of four inputs:
1. note
2. note + question (public_ask primary; name_ask also reported)
3. incentive_context
4. full visible prompt up to the readout position

Inputs 1–2 gate (≤ 0.60). Inputs 3–4 are reported. Failing rows or pools are redesigned, not silently dropped.

## Power-floor plan
- Floor (v1): 120 valid held-out buttons per model. At 15–25% invalid+missing, that is ~160 eval rows ≈ 27 eval ids at 6 rows/id, ≈ 54 ids total.
- Target: ~300 valid buttons per model, i.e. ~400 eval rows, ~67 eval ids, ~134 ids total. Both models (Qwen2.5, gemma-2-9b-it) run the same bank.
- At least 2 ids per topic, so the within-topic split balances. At least 3 note paraphrases per id, shared across incentives.
- Exact McNemar power (α 0.025, Holm worst case, 2000 simulations), accuracy difference 0.08:

| valid buttons | 10% discordant | 15% discordant |
|---|---|---|
| 120 | 0.69 | 0.44 |
| 200 | 0.94 | 0.72 |
| 300 | 0.99 | 0.92 |

  A difference of 0.05 has power ≤ 0.65 even at 300 buttons.
- Below 120 valid buttons: UNDERPOWERED (v1), registered as a pilot.
