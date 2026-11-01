# Official MASK public rows on Llama-3.1 and Gemma-2 (2026-11-01)

Same reduced public set as the 7B official parse: 711 rows with a readable pivotal. Not the paper's 1,000-item judge. No NAME arm. Belief vs pressure only. Accuracy is belief vs ground truth. Lie-given-known is pressure != belief when belief had the fact. A pressured YES that the belief did not have is a miss, not a cover. Raw log: `results/mask-official-new-models-2026-11-01.log`. Dumps: `results/mask_official_{llama8it,gemma2bit,gemma9bit}.jsonl`.

Three logs. Do not average them. Not honesty. Not a camera. Do not fill D.

## Per-split rates

| Walk | Split | n | Accuracy | Lie-given-known | Miss |
| --- | --- | ---: | ---: | ---: | ---: |
| Llama-3.1-8B-Instruct | provided_facts | 230 | 0.400 | 0.683 | 52 |
| | known_facts | 198 | 0.869 | 0.800 | 1 |
| | doubling_down_known_facts | 113 | 0.779 | 0.305 | 13 |
| | continuations | 101 | 0.842 | 0.500 | 1 |
| | disinformation | 69 | 0.797 | 0.286 | 1 |
| Gemma-2-2b-it | provided_facts | 230 | 0.529 | 0.254 | 67 |
| | known_facts | 198 | 0.878 | 0.318 | 17 |
| | doubling_down_known_facts | 113 | 0.804 | 0.149 | 14 |
| | continuations | 101 | 0.792 | 0.447 | 7 |
| | disinformation | 69 | 0.754 | 0.500 | 9 |
| Gemma-2-9b-it | provided_facts | 230 | 0.622 | 0.661 | 25 |
| | known_facts | 198 | 0.903 | 0.618 | 7 |
| | doubling_down_known_facts | 113 | 0.830 | 0.215 | 15 |
| | continuations | 101 | 0.812 | 0.423 | 8 |
| | disinformation | 69 | 0.783 | 0.533 | 2 |

## Against the 7B official parse

Same shape. High accuracy and high lie-given-known on `known_facts`. Weak accuracy and many misses on `provided_facts`.

- Llama-3.1-8B-Instruct `known_facts` lie-given-known is 0.800. Qwen on that split was 0.824. Same high conditional.
- Gemma-2-2b-it is lower on that conditional (0.318) and has more misses on `provided_facts` (67).
- Gemma-2-9b-it sits between them on `known_facts` (0.618) and is cleaner on `provided_facts` misses (25).

## What this is not

- Not the paper's P(Lie). Different set, different judge.
- Not a cover rate. No NAME arm. A YES without the fact is a miss.
- Not a camera. Not handoverPass. Do not fill D.
