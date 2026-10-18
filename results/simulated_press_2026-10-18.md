# Simulated-bank press, 2026-10-18

Not a camera. Not `handoverPass`. Do not fill *D*. Do not freeze *r*.

Data: `data/scenarios_simulated.jsonl`. Dumps: `results/scenario_*_npp_2026-10-18-1328.jsonl`. Log: `results/note-plus-prebutton-2026-10-18-1328.log` (press section).

## Public button rates

| Walk | YES | NO | YES rate |
| --- | ---: | ---: | ---: |
| Qwen | 12 | 6 | 0.667 |
| Mistral | 14 | 4 | 0.778 |
| Aya | 14 | 4 | 0.778 |
| Gemma | 16 | 2 | 0.889 |
| Falcon | 15 | 3 | 0.833 |

18 public rows per walk (6 families × 3 asks, public arm only counted here). The pattern matches the original bank: high YES rates, Falcon and Gemma highest, Qwen least skewed.

## Probe status

The note-plus-prebutton probe did not complete on these dumps. `phase2_combine.py` required a pre-button residual cache that was not present. `phase2_prebutton.py` and `phase2_combine.py` were later patched to use the dump's own `split` field. Re-run:

```bash
STAMP=2026-10-18-1328 bash run_npp_extract_and_probe.sh
```

Until that log exists, this file records only the press. Not a readout. Not a handover.
