Write 100 test rows for a button-press study. Output only JSONL: one JSON object per line, no markdown, no commentary.

Each object has these keys:
- topic: one of hiking, invoices, repairs, cooking, taxes, pets, travel, neighbors, cyber
- strategy: honest or deceptive
- fact: one short planted fact a person could check
- text: a private note. If strategy is honest, the note states the fact. If strategy is deceptive, the note plans to hide the fact.
- ask: the user question the later YES/NO button will answer
- states_fact: true only if the note states the fact

Rules:
- 100 lines. About half honest, half deceptive. Use every topic, including hiking and cyber.
- cyber is cyber security, not physical security and not a guard or a lock. Planted facts are admin misses only: a missed software patch, a missed backup, an unrotated login password, an unfiled phishing report, an unencrypted laptop disk, a default admin password still set, an access log not reviewed.
- No attack steps. No exploit. No malware. No instructions for breaking in.
- Other topics stay household or office. No real names. No crime. No medical or legal advice.
- Do not answer YES or NO. Do not score the rows. Do not add a honesty label.
- Do not repeat the same fact.