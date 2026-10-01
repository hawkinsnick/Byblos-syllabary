"""Run with python -m byblos; requires no installed package."""
import argparse
import json
from .core import audit, load_bundle, ROOT
from .export import sequence_statistics, write_export, verify_export

def main():
    parser = argparse.ArgumentParser(description="Byblos corpus evidence and export tools")
    parser.add_argument("--root", default=str(ROOT), help="Corpus repository root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    aud = sub.add_parser("audit")
    aud.add_argument("--require-1-0", action="store_true",
                     help="Exit 2 unless scientific release gates pass")
    exp = sub.add_parser("export")
    exp.add_argument("--output", required=True, help="New empty export directory")
    ver = sub.add_parser("verify-export")
    ver.add_argument("directory")
    stats = sub.add_parser("stats")
    stats.add_argument("--n", type=int, default=2)
    stats.add_argument("--include-drafts", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "verify-export":
            verify_export(args.directory)
            print("PASS: snapshot hashes and derived views agree")
            return 0
        bundle = load_bundle(args.root)
        result = audit(bundle)
        if not result["structure_valid"]:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 1
        if args.command == "validate":
            print("PASS: structurally valid; scientific 1.0 ready:",
                  result["scientific_1_0_ready"])
        elif args.command == "audit":
            print(json.dumps(result, indent=2, ensure_ascii=False))
            if args.require_1_0 and not result["scientific_1_0_ready"]:
                return 2
        elif args.command == "export":
            print("Exported", write_export(bundle, args.output), "files")
        elif args.command == "stats":
            print(json.dumps(sequence_statistics(bundle, args.n, args.include_drafts),
                             indent=2, ensure_ascii=False))
        return 0
    except (KeyError, TypeError, ValueError, OSError) as exc:
        print("FAIL:", str(exc))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
