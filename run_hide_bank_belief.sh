#!/bin/sh
# Third arm asks the planted fact. No cover instruction.
# Join on fact. Three rates per room. Hiking stays. Not honesty.
set -eu
MODEL="${1:?model dir or id}"
DATA="${2:-data/pairs_wide.jsonl}"
DUMP="${3:-results/hide_bank_belief.jsonl}"
exec python3 hide_bank.py \
  --model "$MODEL" \
  --data "$DATA" \
  --arm three \
  --dump "$DUMP"
