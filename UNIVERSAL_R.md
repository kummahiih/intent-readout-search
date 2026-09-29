# Universal $r$ vs many room cameras

2026-09-29. Search repo. Not a freeze. Do not fill $D$.

## Evidence against one $r_{\mathrm{strat}}$

A single linear camera is $r(h)=v^\top h$ with one $v$ (or a small frozen bank $D$) meant to slap the *plan* in every declared room.

What the ledger actually shows:

| Test | What it does to one $v$ |
| --- | --- |
| Hiking LOTO Qwen $0.013$ / Mistral $0.069$ vs travel $\sim 0.16$ | The shared axis misses a declared room. |
| Hiking `held_inroom` $0.20$ / $0.28$ | That room still has a pair. |
| Fact-held paraphrase hiking $0.16$ / $0.18$ | The pair is not one wording. |
| Genre-out LOTO $\approx 0$ | Even loud rooms die when the speech act changes. |
| Cross-judge, crude $W$ | Same rooms stay loud, hiking stays thin. |
| Cross-judge vs LOTO $r\sim 0.9$; vs `held_inroom` $r\sim -0.6$ | The map copies the shared ranking. It does not import the private pair. |
| Pre-button $h$ (plan+question, before YES/NO) tag LOTO $0.011$ / $0.011$ | The note is in context at the decision token and still does not make a shared axis. Mistral print $0.68$ was the button cell. |

After a crude alignment, the same rooms stay loud and the same room stays thin. That is evidence the mid-layer hint is **domain-shaped**, not evidence you have a portable judge.

Lean already names the cheat: `seven_is_not_eight`. Dropping hiking manufactures a pass. It does not create a universal $r$.

## Could many domain-specific $r_T$ work better?

Yes, **as local sensors**. No, **as the hinge camera** without changing the object.

`held_inroom` is exactly $r_T(h)=v_T^\top h$. On hiking that number is loud and held-out. A bank $D_T=\{v_T\}$ per room would slap hiking plans that the shared $v$ never sees.

Cost:

- The trainer must know $T$ or take $\max_T v_T^\top h$. Knowing $T$ is a topic feature in the slap. Max-over-rooms bills whatever room vector is closest, including wallpaper.
- $D$ is no longer a short list of *plans*. It is a list of *plan-in-room* pins. Coverage becomes eight cameras, then a new room is another miss.
- $L_{\mathrm{total}}$ in [regret-heuristic](https://github.com/kummahiih/regret-heuristic) assumes one $r_{\mathrm{strat}}$ against a frozen plan bank. A family $\{r_T\}$ is a different interface (`inroom_hold_not_a_gate`).

So: many $r_T$ would likely **work better on the rooms you already named**. That is not a reason to freeze them as $r_{\mathrm{strat}}$. It is a reason to treat the mid-layer hint as a map of local pairs until a shared $v$ owns hiking *and* a behavioral label agrees.

## What is still missing

Tags built every $v_T$. A deceptive tag can print a true sentence. Construct test: fit $v$ on tags, score generated prints against `reply_kind`. That script does not write `reply_kind` into $L$. Pre-button $h$ was the next place a shared $v$ could have shown up. It did not.
