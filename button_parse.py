"""YES/NO button parser. No torch. A missing button is not a label. Do not fill D."""

from __future__ import annotations


def button_of(reply: str) -> str:
    """S is YES or NO as a whole token. A prefix is not a press.

    **YES** and \"YES\" count. Nobody, Yesterday, and a preamble do not.
    """
    import re
    cleaned = (reply or "").strip()
    cleaned = re.sub(r"^[\*_\"'`]+|[\*_\"'`]+$", "", cleaned).strip()
    head = re.split(r"[\s,.!:;]+", cleaned.upper(), maxsplit=1)[0] if cleaned else ""
    head = head.strip("*_\"'`")
    if head == "YES":
        return "YES"
    if head == "NO":
        return "NO"
    return "other"


def strip_reasoning(reply: str) -> str:
    """Drop reasoning blocks. A closed <think>...</think> block is removed.
    An unclosed <think> (truncated reasoning) leaves nothing to read."""
    import re
    text = reply or ""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S | re.I)
    if re.search(r"<think>", text, flags=re.I):
        return ""
    # some templates open the block in the prompt, so the reply has only </think>
    if re.search(r"</think>", text, flags=re.I):
        text = re.split(r"</think>", text, flags=re.I)[-1]
    return text.strip()


def final_button(reply: str) -> str:
    """button_of after reasoning is removed; else an explicit final answer.

    Same as button_of when the reply starts with YES/NO and has no think block.
    Otherwise only an explicit final answer counts: a last non-empty line that is
    YES or NO, or a last 'Answer:'/'Final answer:' YES/NO. Truncated reasoning
    with no final answer stays 'other'. A missing button is not a label.
    """
    import re
    text = strip_reasoning(reply)
    b = button_of(text)
    if b != "other" or not text:
        return b
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if lines:
        last = button_of(lines[-1])
        if last != "other" and len(re.split(r"\s+", lines[-1])) <= 3:
            return last
    m = re.findall(r"(?:final\s+answer|answer)\s*(?::|is)\s*[\*_\"'`]*\s*(YES|NO)\b(?![\*_\"'`\s]*(?:or\b|/))", text, flags=re.I)
    if m:
        return m[-1].upper()
    return "other"
