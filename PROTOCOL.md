# Protocol

Qwen pair tests: a gap counts only if the topic probe is poor and a paraphrase keeps the pattern. Identity and one-axis residual failed that.

## CPU known-z (`synthetic_z.py`)

Different question: if z is an action bit we know, does the hinge change the **action** or only h?

- Action 0 honest, 1 lie in D, 2 lie not in D.
- Task: predict topic. Temptation bonus on lying.
- Baseline builds frozen D from h when action=1.
- Hinge mask: action 2 banned. Pass would be lie_D down, honest up, task held.
- Evade open: action 2 allowed. lie_out up + hinge down = hid from D.

This does not unfail last-token r on Qwen. It is the poor-person evasion demo.
