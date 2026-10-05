# Local pressure-row generation, 2026-10-04

Items, not buttons. Not honesty. Do not fill D. A file of 100 lines is not a cover rate.

The runner was `run_make_pressure_rows.sh`. Logs: `results/tests-pressure-rows-2026-10-04-2001.log`, `2104`, `2150`, `2158`.

| Source | File | n | honest / deceptive | cyber | Note |
| --- | --- | ---: | --- | ---: | --- |
| Qwen2.5-7B | `data/pressure_rows_qwen.jsonl` | 100 | 50 / 50 | 11 | clean parse |
| Mistral-7B | `data/pressure_rows_mistral.jsonl` | 100 | 50 / 50 | 11 | clean parse |
| Aya Expanse 8B | `data/pressure_rows_aya.jsonl` | 100 | 50 / 50 | 11 | clean parse |
| Gemma 3 4B | `data/pressure_rows_gemma.jsonl` | 100 | 50 / 50 | 11 | one short fact |
| Falcon3-7B | `data/pressure_rows_falcon.jsonl` | 100 | 50 / 50 | 11 | clean parse |
| Granite 4.2-8B | `data/pressure_rows_granite.jsonl` | 100 | 50 / 50 | 11 | first run 400 bad, n=0; second run 100/100 |
| Qwen3.5-9B | `data/pressure_rows_qwen35.jsonl` | 100 | 50 / 50 | 11 | 141 tries; one raw miss saved |
| Nimble 9B | none | 0 |  |  | skipped, incomplete weights at `models/Bespoke-Nimble-9B` |
| Phi-4-mini | none | 0 |  |  | not in these logs; earlier `LossKwargs` failure stands |
| ChatGPT free | `data/pressure_rows_chatgpt.jsonl` | 90 | 45 / 45 | 10 | paste, not this runner |
| Gemini | `data/pressure_rows_gemini.jsonl` | 100 | 50 / 50 | 12 | paste, not this runner |

Rooms are the nine asked for, including cyber. The local files are about 11 per room because 100 is not divisible by 9. Hiking has 12.

Granite's first run wrote no `{...}` in 400 tries. That was before thinking was turned off. The later run filled 100 rows on the first try each. Qwen3.5's saved miss is unquoted JSON, keys without quotes, so `json.loads` correctly rejected it. The kept file does not contain that line.

These rows are not yet a button bank. Several notes do not match the tag: an honest note that does not state the fact, a deceptive note that does not hide it, a cyber fact that is only the phrase "unrotated login password". The score runner now drops those before the call. Nimble still needs its shard files. LFM and Bonsai were not in this loop.
The score runner `run_pressure_score.sh` now writes `data/valid/pressure_rows_<src>.jsonl` and scores that. Dropped: strategy/states_fact clash, fact copied into the note, a hiding instruction, a cover claim stored as the fact, a deceptive note that still states the fact, duplicates. An old `results/pressure_score_*` dump without a matching `.rows` stamp is rewritten. The drop count is not a lie rate. Do not fill D.
