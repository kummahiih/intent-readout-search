# Audit plan, 2026-10-10

Not a camera. Not a handover. Do not fill D. Do not freeze r. Do not run PPO.

The logical audit of regret-heuristic and this repo is mostly already pinned. The gap is that the pins are warnings. This file turns them into pass/fail tests. Parent formulation `## F` now states the loss-side refusals. This file owns the measurement-side order.

## Already pinned, not a new bug

| ID | Pin |
| --- | --- |
| L1 | Dead zone. Orthogonal cell is not out-of-distribution transfer. `heldout_not_mem_walk_bank`. |
| L2 | No theorem that lowering *L*<sub>reg</sub> lowers a behavior rate. Gradients of *L*<sub>reg</sub> enter *h*. |
| L3 | H1 is `handoverPass`. Current answer: no. A note contrast is not operative strategy. |
| L5 | Frozen inspector is not in *L*<sub>total</sub>. `trained_silent_frozenI_loud`. |
| L6 | Assigned tag is not S. `reply_kind` is not a gate. |
| L10 | *L*<sub>reg</sub> = 0 means *s*<sup>∗</sup> ≤ τ. Not honesty. |

## Still a gap

| ID | Gap | Fix |
| --- | --- | --- |
| L3, L6 | Readout is fit on assigned notes. Buttons often ignore the note. | Phase 1–2. Predict the realized button, not the tag. |
| L4, L7 | Topic L2 near chance is one linear probe on 48 notes. A miss is not invariance. | Report it as a bounded negative. Do not call it topic-free. |
| L8 | Qwen/Mistral/Falcon share a shape. Gemma does not. | Model-specific. No pooled claim. |
| L9 | Bad generation, small n, facts reused in paraphrases. | Do not score that bank again. Fresh scenarios, one id per fact family. |
| L11 | τ(*u*) is notation. | Leave it out of any run. |
| L12 | *A*<sub>safe</sub> needs a criterion that is not *r*. | Blocked until Phase 2. |

## Phase order

Do not raise λ. Do not add prototypes. Do not train. Do not score the other five walks on the bad bank.

Contract: [data/scenario_contract.md](../data/scenario_contract.md). No leakage by scenario id. No silent denominator. No proxy substitution of the assigned note for the realized button.

1. **Labels.** Hand-write hiking scenarios. One proposition, shared by belief, public, and name. `prop_truth` is the world. `states_proposition` is the note. `incentive` is the assignment, not S. A paraphrase keeps the scenario id. Exit: a row can show assignment and a later button disagreeing, and the scorer does not call that a lie from the tag.
2. **Readout.** Freeze the split before fitting. Acceptance is the six checks in [data/scenario_contract.md](../data/scenario_contract.md): isolation, accounting, target integrity, note-text baseline, an interval, a fixed manifest. A pass is a bounded button prediction, not `handoverPass`. Predict the realized button on held-out scenario ids. Assigned-note LOTO stays a baseline, not the endpoint. Topic probe failure stays a negative result, not invariance. Exit: the readout calls the button on held-out facts above the note-text baseline, on more than one room. That is still not `handoverPass`.
3. **Hinge, only after 2.** Freeze *r* and *D*. Compare base, task-only, hinge, and a control regularizer that is not this signal. Success is an independent button or inspector change, not a lower cosine. A quiet hinge with the same buttons is a fail (`trained_silent_frozenI_loud`).
4. **Evasion.** New strategy outside *D*. Trained readout quiet, frozen inspector or button unchanged: fail.
5. **Not now.** *A*<sub>safe</sub>, PPO, approachability. Blocked.

## Fail predicates

- Low cosine is not honesty.
- Assigned-note separation is not operative strategy.
- Topic-probe failure is not topic invariance.
- Hinge loss going to 0 is not reduced deception.
- Task loss in the formula is not preserved competence.
- A kept file is not a camera pass.
- Two walks are not a Spearman.

Parent interface after the formulation pin. This repo owns the measurement. The hinge does not own the camera.

## Status words

| Status | Meaning |
| --- | --- |
| Pinned | The limit is written. It is not resolved. |
| Open | The empirical test is still outstanding. |
| Blocked | No downstream claim until the prerequisite passes. |

A Phase 2 pass is a bounded predictive claim. It is not `handoverPass`, not topic invariance, and not reduced deception.
