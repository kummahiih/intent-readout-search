# Sensor ledger

Do not collapse attempts. A drop in cosine is not reduced deception.

## Baseline A — last-token identity (old jsonl)

Source: kummahiih/regret-heuristic §2. 0.7742 / 0.8003. Failed.

## Baseline B — mean-pool identity (old jsonl)

Source: same repo §6. 0.8575 / 0.8524. Failed.

## Identity control on pairs.jsonl — 2026-09-16 00:00

`pair_metrics.py --model Qwen/Qwen2.5-7B-Instruct --data data/pairs.jsonl`
VRAM 5.18 / 5.33 GiB. Last-token identity. Frozen D = two bank deceptive sentences (one per topic).

| topic | deceptive s* | honest s* |
| --- | --- | --- |
| invoices | 0.9447 | 0.9298 |
| hiking | 0.8919 | 0.9264 |
| mean | 0.9183 | **0.9281** |

`gap_hon_minus_dec=0.0098`  
`topic_probe_acc=1.00` n=4 topics={hiking, invoices}

Topic linear probe on the same four vectors is perfect. Strategy gap is noise. Within hiking, honest is closer to D than deceptive. Identity last-token failed the topic test on this pair set too.

Not a deception result. Next sensor is not more pooling and not more SGD on I.
