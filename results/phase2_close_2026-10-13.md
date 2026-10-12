# Phase 2 close, 2026-10-13

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*. Do not run PPO.

The note-text confound is addressed. The strategy-camera hypothesis is not.

## Ledger

| Observation | Supported | Not established |
| --- | --- | --- |
| Pre-button residual clears the note-text bar | The signal is not the note text alone | That it identifies a hiding strategy |
| Combination probe clears the note-text bar | The pair captures more than the note text | That the pair is a strategy camera |
| Note-only and end-of-note fail | The signal needs more than the note | That the signal encodes a plan |
| Order swap, ask-only, and mid-layer note fail | Those controls do not reproduce the result | Generalization to unseen strategies |
| Unicode and four bytes of noise do not move the lie count | Those perturbations do not move the metric | General robustness |
| Note-then-ask predicts the button; note-only and ask-only do not | The prediction needs both, in that order | A prediction on held-out ids without the ask tokens |
| Aggregate plan contrast ~0.11; hiking 0.013 / 0.069 | A candidate contrast under the reported conditions | A validated strategy representation |

## Status

- H1 open. The note-text confound is addressed. The strategy camera is not proven.
- H2 blocked. Do not train on the assumption that the current readout is valid.
- `cameraPass`: no.
- `handoverPass`: no.
- Phase 2: open.
- Do not fill *D*. Do not freeze *r*.

Causal intervention, capability curves, and baseline bake-offs are H2. They do not substitute for a readout that predicts the realized button on held-out ids without the ask tokens.

This is a negative handover. The controls narrow what the signal can be. They do not relabel it as a plan.
