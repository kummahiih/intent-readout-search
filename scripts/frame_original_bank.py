#!/usr/bin/env python3
"""Produce user-says and agent-stakes framed versions of data/scenarios_all.jsonl.

The original notes already embed the incentive. This script adds an incentive_context
field and a framing prefix so run_scenario.py --role-frame can be used, and also
writes two ready-to-run banks where the note itself is wrapped.

Not a camera. Not handoverPass. Do not fill D.
"""

import json
from pathlib import Path

SRC = Path("data/scenarios_all.jsonl")
OUT_USER = Path("data/prereg/scenarios_original_user_says.jsonl")
OUT_AGENT = Path("data/prereg/scenarios_original_agent_stakes.jsonl")

def main():
    rows = [json.loads(l) for l in SRC.read_text().splitlines() if l.strip()]
    user_rows, agent_rows = [], []
    for r in rows:
        note = r.get("note", "")
        # user-says: the user is stating the pressure
        u = dict(r)
        u["incentive_context"] = note
        u["note"] = "Private note."
        u["framing"] = "user-says"
        user_rows.append(u)
        # agent-stakes: the agent is describing its own stakes
        a = dict(r)
        a["incentive_context"] = note
        a["note"] = "Private note."
        a["framing"] = "agent-stakes"
        agent_rows.append(a)
    OUT_USER.parent.mkdir(parents=True, exist_ok=True)
    OUT_USER.write_text("".join(json.dumps(r) + "\n" for r in user_rows))
    OUT_AGENT.write_text("".join(json.dumps(r) + "\n" for r in agent_rows))
    print(f"wrote {len(user_rows)} user-says rows to {OUT_USER}")
    print(f"wrote {len(agent_rows)} agent-stakes rows to {OUT_AGENT}")

if __name__ == "__main__":
    main()
