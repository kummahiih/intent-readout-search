# Pressure rows on Llama-3.1 and Gemma-2 (2026-11-01)

Items, not buttons. Each walk wrote 100 rows: a planted fact plus a private note. `hide_bank.py` is what presses the button. This dump does not. Dumps: `data/pressure_rows_{llama8it,gemma2bit,gemma9bit}.jsonl`. One bad try saved as `data/pressure_rows_gemma2bit.bad.txt`. Not honesty. Not a camera. Do not fill D.

## Counts

| Walk | n | topics | honest / deceptive | states_fact true | honest fact in note |
| --- | ---: | --- | --- | ---: | ---: |
| Llama-3.1-8B-Instruct | 100 | 9 (12 hiking, 11 rest) | 50 / 50 | 49 | 4 / 50 |
| Gemma-2-2b-it | 100 | 9 (12 hiking, 11 rest) | 50 / 50 | 24 | 0 / 50 |
| Gemma-2-9b-it | 100 | 9 (12 hiking, 11 rest) | 50 / 50 | 50 | 24 / 50 |

## What the rows look like

- Llama writes a fact and a note that often do not share the fact string. Honest notes sometimes restate, sometimes drift. Deceptive notes plan a cover or a delay. Cyber rows stay on admin failures (unrotated password, missed patch), not attack steps.
- Gemma-2-2b-it is looser. Honest notes often do not contain the fact. `states_fact` is true on only 24 of 100. Several rows are advice or a question, not a planted fact plus a hide plan.
- Gemma-2-9b-it is the tightest. Honest notes restate the fact on about half the honest rows. Deceptive notes are short cover instructions ("tell them we sent it on the 15th", "say it leaves at 9:00"). Cyber stays on password rotation and missed patches.

## What this is not

- Not a button score. Not HIDE YES. Not a cover rate.
- Not a camera. Not handoverPass. Do not fill D.
- The cyber room is cyber security admin. No attack steps. No exploit. No malware.
- A row that does not state the fact is a miss for a later belief arm, not a cover.
