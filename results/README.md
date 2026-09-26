# Sensor ledger

Do not collapse attempts.

## P0l — travel/neighbors voice — 2026-09-27 00:44 EEST

Same register as hiking/invoices. In-room transfer vs LOTO transfer_held:

| | Qwen | Mistral |
| --- | --- | --- |
| in-room travel voice | 0.109 $p=0.30$ | 0.160 $p=0.20$ |
| in-room neighbors voice | 0.096 $p=0.50$ | 0.148 $p=0.29$ |
| LOTO voice held | **0.004** $p=0.87$ | **0.036** $p=0.13$ |
| in-room travel paraphrase (earlier) | 0.276 | 0.352 |
| in-room neighbors paraphrase | 0.388 | 0.512 |

Voice style cuts own-$v$ by ~3x and kills the shared LOTO axis even in loud rooms. Hiking was not a special hole. This register is the hole.

## P0k hiking voice rewrite

Qwen 0.045 / Mistral 0.121. Still weak.
