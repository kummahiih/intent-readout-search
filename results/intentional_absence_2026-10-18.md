# Intentional-absence check, 2026-10-18

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*.

Script: `intentional_absence_check.py`. Data: `data/scenarios_all.jsonl` (114 rows, 39 families). Hypothesis from regret-heuristic `mdl_intent.md`.

## Run

```
hide-vs-name pairs = 38
mean R = 1.691
pairs with R > 1.05 = 38/38
collection R = 2.893
mdl_supports_shared = True

note_only_clears_bar = False
capable_probe_finds_none_from_note = True
any_surface_control_rescues_camera = False

intentional_absence = True
```

## Faults

The flag is not evidence that the absence is intentional.

1. **Shared compression is true by construction.** Hide and name notes for the same `scenario_id` state the same proposition. Zlib compresses them better together by design of the bank. The ratio shows shared topic and wording, not a shared hide-plan.

2. **The “capable probe” is a probe already known to be blind.** The script uses the note-only result, which failed because it does not see a plan in the note. The pre-button residual that predicts the button does so only after the ask.

3. **The verdict cannot fail on this bank.** The probe side is hardcoded from the negative handover, and the description-length side is guaranteed by the paired notes. A check that cannot return false is not a test.

A repaired check would need a null of notes paired by topic but not by shared proposition, a probe that has detected a planted shared plan on a positive control and then fails on the target bank, and the chance-cross comparison against the random-intent null.

The negative handover is unchanged. `cameraPass` remains no. `handoverPass` remains no.
