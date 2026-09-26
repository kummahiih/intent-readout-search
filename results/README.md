# Sensor ledger

Do not collapse attempts.

## P0h — Qwen layer-8 K-step — 2026-09-27 00:00 EEST

Source: `results/tests-qwen-kstep-2026-09-26.log`. `model=Qwen/Qwen2.5-7B-Instruct`.

```
L8 kstep gap=0.1948  topic L2=0.15  transfer=0.183 p=0  cos_to_last=0.70
hold T/N kept=0.144 L2=0.19  held=0.245 p=0.005
voice hiking/invoices -0.004 p=0.65
last-layer kstep gap=0.098 L2=0.23 transfer p=0.013
```

Plan+paraphrase hold. Topic L2 a bit above eight-way chance (0.125). Same dead rooms as last-token.

## P0g — Mistral layer 9

last 0.116 / L2 0.12 / para $p=0$. kstep 0.192 / L2 0.10. siren 0.058 / L2 0.04. Voice dead. Last layer fails topic.
Misnamed log is now `tests-mistral-layer8-kstep-2026-09-26.log`.

## P0f / P0c — Qwen last-token / SIREN layer 8

last 0.105 / L2 0.06. SIREN 0.140 / L2 0.08. Voice dead.
