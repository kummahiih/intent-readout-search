# Scenario bank expansion prompt

Find more material for the intent readout scenario bank.

## What the bank needs

The bank tests whether a candidate readout sees a strategy (hide or name) independently of topic and question. Each scenario has:

- A private note that states a fact
- A public ask that asks about that fact
- A name_ask that asks the same fact under "refuse the cover"
- A realized YES/NO button

## What to look for

1. Public datasets with fact-plus-question pairs where the fact is known and the question asks about it
2. Paraphrase sets of the same proposition under different wordings
3. Role or persona prompts that are not topic labels
4. Scenarios where the same fact is asked under different incentives

## What to avoid

- Scenarios where the fact is not in the note
- Scenarios where the question does not ask the fact
- Scenarios where YES/NO is not a clean button
- Scenarios that are only topic labels

## Output

Write each candidate as a JSONL row with:

- scenario_id
- note
- ask
- name_ask
- source
- why it fits

Not a camera. Not handoverPass. Do not fill D.
