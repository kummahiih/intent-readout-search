def load_rows(root: Path, limit: int) -> list[dict]:
    files = sorted(root.rglob("*.parquet")) + sorted(root.rglob("*.jsonl"))
    if not files:
        raise SystemExit(f"SKIP: no parquet or jsonl under {root}")
    rows = []
    for f in files:
        split = f.parent.name if f.stem.startswith("test") else f.stem
        if f.suffix == ".parquet":
            import pandas as pd
            frame = pd.read_parquet(f)
            recs = frame.to_dict(orient="records")
        else:
            recs = [json.loads(line) for line in f.read_text().splitlines() if line.strip()]
        for rec in recs:
            rec["_split"] = split
            if truth_yes(rec) is None or not rec.get("user_prompt"):
                continue
            rows.append(rec)
            if len(rows) >= limit:
                return rows
    return rows
