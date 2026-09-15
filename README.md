# Intent readout search

Can we build an \(r\) and a bank \(D\) that track **strategy given topic**?

This is not the hinge paper. The hinge and the negative last-token / mean-pool probes live in [kummahiih/regret-heuristic](https://github.com/kummahiih/regret-heuristic). That repo stays a glossary. Failed sensors live here.

## Already failed (do not repeat as try 2)

From regret-heuristic `experiment_results.md` on Qwen2.5-7B-Instruct 4-bit, same-topic n=2:

| sensor | deceptive vs D | honest vs D |
| --- | --- | --- |
| last-token identity | 0.7742 | 0.8003 |
| mean-pool identity | 0.8575 | 0.8524 |

Topic smear. Mean-pool mixed more. See [PROTOCOL.md](PROTOCOL.md).

## Ledger

[results/README.md](results/README.md)
