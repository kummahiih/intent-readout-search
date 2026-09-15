# Protocol

Truth is a random variable. Pair tags and toy actions are **observations**, not nature.

\(u\) is uncertainty of that observation (label-flip rate, or walk entropy / NLL). It is not \(p(\mathrm{lie})\).

Rules that apply from the first file, not after a clean toy:

1. Do not put a point in \(D\) if \(u > u_0\).
2. Report strategy gaps in sure / unsure bins. A gap only on \(u=0\) author tags is a toy gap.
3. Wider hinge threshold on high \(u\) (glossary §F). Quiet on mush is not honesty.
4. Topic probe still has to fail on the same vectors.
5. Paraphrase still required for a language gap.

Qwen identity / residual already failed under author-sure tags (\(u=0\) in the jsonl). That does not licence treating those tags as nature.

## CPU (`synthetic_z.py`)

`--noise p` flips the *labeler* that builds \(D\). True action is still logged.
Contamination of \(D\) is printed. Hinge on a dirty bank is the default story, not a variant.
