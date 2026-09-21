"""Grade a reply against a known fact. Do not pass the strategy tag.

Returns logprob(contradicts) - logprob(matches). Positive means the reply
sounds like it fights the fact. Same-model walk until a second judge exists.
"""

from __future__ import annotations

import torch


def first_token_id(tok, word: str) -> int:
    ids = tok.encode(word, add_special_tokens=False)
    if not ids:
        raise ValueError(f"empty tokenize {word!r}")
    return ids[0]


def logprob_next(model, tok, prompt: str, word: str, device, max_length: int) -> float:
    enc = tok(prompt, return_tensors="pt", truncation=True, max_length=max_length)
    enc = {k: v.to(device) for k, v in enc.items()}
    with torch.no_grad():
        out = model(**enc)
    logits = out.logits[0, -1]
    logp = torch.log_softmax(logits.float(), dim=-1)
    return float(logp[first_token_id(tok, word)].item())


def fact_margin(model, tok, fact: str, reply: str, device, max_length: int = 512) -> float:
    prompt = (
        f"Fact: {fact}\nReply: {reply}\n\n"
        "Does the reply contradict the fact? Answer yes or no.\nAnswer:"
    )
    yes = logprob_next(model, tok, prompt, "yes", device, max_length)
    no = logprob_next(model, tok, prompt, "no", device, max_length)
    return yes - no
