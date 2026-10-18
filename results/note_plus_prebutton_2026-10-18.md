# Note-plus-prebutton runs, 2026-10-18

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*.

Script: `run_note_plus_prebutton.sh`. Logs: `results/note-plus-prebutton-2026-10-18-1328.log`, `results/note-plus-prebutton-2026-10-18-1330.log`.

## Existing dumps (night press, stamp 2026-10-12-0031)

Reproduced the earlier combination result.

| Walk | Joint | Note-text | Intervals |
| --- | --- | --- | --- |
| Qwen L8 | 52/55 = 0.945 [0.851, 0.981] | 39/55 = 0.709 | no overlap |
| Mistral L9 | 53/55 = 0.964 [0.877, 0.990] | 47/55 = 0.855 | no overlap |
| Aya L10 | 54/55 = 0.982 [0.904, 0.997] | 46/55 = 0.836 | no overlap |
| Gemma L10 | 52/53 = 0.981 [0.901, 0.997] | 42/53 = 0.792 | no overlap |
| Falcon L8 | 49/55 = 0.891 [0.782, 0.949] | 45/55 = 0.818 | overlap |

Same pattern as the negative handover: the joint score clears the note-text bar. The earlier analysis still holds: the score is carried by the pre-button residual that has seen the ask. Not a handover.

## Simulated and reworded presses

`DATA=data/scenarios_simulated.jsonl` (1328) and `DATA=data/scenarios_reworded_control.jsonl` (1330) both pressed and wrote dumps (`results/scenario_*_npp_2026-10-18-*.jsonl`). The probe step then stopped:

```
missing results/prebutton_<model>_npp_<stamp>_L-1.npy; extract prebutton on this dump first
```

`phase2_combine.py` expects a pre-button residual cache for the dump. The new dumps do not have one. The presses themselves completed; the probe did not run on them.

To finish: extract pre-button residuals on the npp dumps (same procedure as `phase2_prebutton.py`), then re-run the probe with those caches present.

## What this is not

- Not a new camera pass.
- Not a change to the negative handover.
- The simulated and reworded banks have no probe score yet.
