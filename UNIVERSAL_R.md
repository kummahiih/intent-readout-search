# Universal $r$ vs many room cameras

2026-09-29. Search repo. Not a freeze. Do not fill $D$.

## Evidence against one $r_{\mathrm{strat}}$

A single linear camera is $r(h)=v^\top h$ with one $v$ (or a small frozen bank $D$) meant to slap the *plan* in every declared room.

What the ledger actually shows:

| Test | What it does to one $v$ |
| --- | --- |
| Hiking LOTO Qwen $0.013$ / Mistral $0.069$ vs travel $\sim 0.16$ | The shared axis misses a declared room. |
| Hiking `held_inroom` $0.20$ / $0.28$ | That room still has a pair *on the note token*. |
| Fact-held paraphrase hiking $0.16$ / $0.18$ | The pair is not one wording. |
| Genre-out LOTO $\approx 0$ | Even loud rooms die when the speech act changes. |
| Cross-judge, crude $W$ | Same rooms stay loud, hiking stays thin. |
| Cross-judge vs LOTO $r\sim 0.9$; vs `held_inroom` $r\sim -0.6$ | The map copies the shared ranking. It does not import the private pair. |
| Pre-button $h$ tag LOTO $0.011$ / $0.011$ | Shared axis missing at the decision token. |
| Pre-button `held_inroom` $0.005$ / $0.009$ | Local $r_T$ missing there too. |
| Atlas kind-fit Qwen $0.057$ ($n_{\mathrm{dec}}=5$); Mistral skipped | Free-text print is not an eight-room label. Hiking Qwen 6/6 truth. |

After a crude alignment, the same rooms stay loud and the same room stays thin. That is evidence the mid-layer hint is **domain-shaped**, not evidence you have a portable judge.

Lean already names the cheat: `seven_is_not_eight`. Dropping hiking manufactures a pass. It does not create a universal $r$.

## Could many domain-specific $r_T$ work better?

Yes, **as local sensors on the note token**. No, **as the hinge camera** without changing the object. No, **on pre-button $h$**: that hold is $0.005$ / $0.009$.

`held_inroom` on the *note* is $r_T(h)=v_T^\top h$. On hiking that number is loud and held-out. A bank $D_T=\{v_T\}$ per room would slap hiking *notes* that the shared $v$ never sees. It would not slap the pre-button state we just measured.

Cost:

- The trainer must know $T$ or take $\max_T v_T^\top h$. Knowing $T$ is a topic feature in the slap. Max-over-rooms bills whatever room vector is closest, including wallpaper.
- $D$ is no longer a short list of *plans*. It is a list of *plan-in-room* pins. Coverage becomes eight cameras, then a new room is another miss.
- $L_{\mathrm{total}}$ in [regret-heuristic](https://github.com/kummahiih/regret-heuristic) assumes one $r_{\mathrm{strat}}$ against a frozen plan bank. A family $\{r_T\}$ is a different interface (`inroom_hold_not_a_gate`).

So: many $r_T$ would likely **work better on the rooms you already named, at the note last token**. That is not a reason to freeze them as $r_{\mathrm{strat}}$. It is a reason to treat the mid-layer hint as a map of local pairs until a shared $v$ owns hiking *and* a behavioral label agrees.

## What is still missing

Tags built every $v_T$. Atlas used the print as the label instead. Kind-fit is not eight-room: Qwen hiking never contradicts; Mistral only taxes is two-sided. The candidate signal is still a *tag* contrast on the note token, not a behavior camera. Bailey tax (quiet that tag $v$, keep the print) is the remaining open fork. Kind does not enter $L$. Do not fill $D$.
