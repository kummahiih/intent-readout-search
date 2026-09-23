# reply_kind

Field on a generated reply row. Not on the pair-strategy tag.

```
truth | contradict | evade | refuse | insufficient
```

- `truth` — printed text matches the fact string.
- `contradict` — printed text denies the fact string.
- `evade` — talks around the fact.
- `refuse` — will not answer.
- `insufficient` — cannot tell.

Assigned `strategy` stays a separate column. Do not copy strategy into `reply_kind`.
No rows have this field yet. Do not print `fact_sign_acc` until they do.
