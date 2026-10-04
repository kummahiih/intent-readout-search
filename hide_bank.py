def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="", help="required unless --self-check")
    p.add_argument("--data", default="data/pairs_wide.jsonl")
    p.add_argument("--arm", choices=("hide", "name", "belief", "both", "three"), default="both")
    p.add_argument("--self-check", action="store_true")
    p.add_argument("--n-samples", type=int, default=2)
    p.add_argument("--new-tokens", type=int, default=4)
    p.add_argument("--temperature", type=float, default=0.9)
    p.add_argument("--dump", default="results/hide_bank.jsonl")
    args = p.parse_args()
    if args.self_check:
        return self_check()
    if not args.model:
        print("ERROR: --model required unless --self-check", file=sys.stderr)
        return 1
