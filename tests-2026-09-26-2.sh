python pair_contrast.py --data data/pairs_wide.jsonl --layer -1 --pool last \
  --permute 20000 --transfer data/pairs_paraphrase.jsonl
python leace_residual.py --data data/pairs_wide.jsonl
python head_write_probe.py --data data/pairs_wide.jsonl --layer 8 --k 4
python head_write_probe.py --data data/pairs_wide.jsonl --layer 8 --k 4 --quiet