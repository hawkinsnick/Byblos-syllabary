"""Run with python -m byblos; requires no installed package."""
import argparse
import json
from pathlib import Path
from .references import reference_workflow, pilot_packet
from .evidence import evidence_ledger, acquisition_queue
from .release import release_check
from .jsonio import read_json
from .provenance import provenance_report
from .core import audit, load_bundle, ROOT
from .export import sequence_statistics, write_export, verify_export
from .workflow import review_packet, compare_snapshots
from .contributions import proposal_template, assess_proposal, stage_proposal, verify_staged_proposal, read_proposal

def main():
    parser = argparse.ArgumentParser(description="Byblos corpus evidence and export tools")
    parser.add_argument("--root", default=str(ROOT), help="Corpus repository root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("reference-workflow", help="Print source-by-source reference-only work plan")
    pilot = sub.add_parser("pilot-packet", help="Print one pending metadata review packet")
    pilot.add_argument("--record", default="BYB-A")
    sub.add_parser("evidence-ledger", help="Print field-level catalogue attribution")
    sub.add_parser("acquisition-queue", help="Print source inspection backlog")
    sub.add_parser("release-check", help="Check versions and committed export consistency")
    prov = sub.add_parser("provenance", help="Print citation usage and source dependencies")
    prov.add_argument("--source", help="Limit usage inventory to a registered source")
    sub.add_parser("review-packet", help="Print pending review tasks as JSON")
    template = sub.add_parser("proposal-template", help="Print an empty contribution form")
    template.add_argument("--record", action="append", help="Limit form targets to a known record; repeat as needed")
    check = sub.add_parser("check-proposal", help="Assess a submission without changing corpus data")
    check.add_argument("file")
    stage = sub.add_parser("stage-proposal", help="Write a pending proposal packet; never apply it")
    stage.add_argument("file")
    stage.add_argument("--output", required=True)
    staged = sub.add_parser("verify-proposal", help="Verify a staged proposal against current evidence")
    staged.add_argument("directory")
    compare = sub.add_parser("compare", help="Compare two lossless JSON bundles or export directories")
    compare.add_argument("before")
    compare.add_argument("after")
    compare.add_argument("--fail-on-change", action="store_true", help="Exit 3 if recorded data differs")
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
        if args.command == "release-check":
            report = release_check(args.root)
            print(json.dumps(report, indent=2, ensure_ascii=True))
            return 0 if report["repository_consistent"] else 1
        if args.command == "verify-export":
            verify_export(args.directory)
            print("PASS: snapshot hashes and derived views agree")
            return 0
        if args.command == "compare":
            def read(path):
                path = Path(path)
                if path.is_dir():
                    path = path / "bundle.json"
                return read_json(path)
            diff = compare_snapshots(read(args.before), read(args.after))
            print(json.dumps(diff, indent=2, ensure_ascii=True))
            return 3 if args.fail_on_change and diff["changes"] else 0
        bundle = load_bundle(args.root)
        result = audit(bundle)
        if not result["structure_valid"]:
            print(json.dumps(result, indent=2, ensure_ascii=True))
            return 1
        if args.command == "validate":
            print("PASS: structurally valid; scientific 1.0 ready:",
                  result["scientific_1_0_ready"])
        elif args.command == "reference-workflow":
            print(json.dumps(reference_workflow(bundle), indent=2, ensure_ascii=True))
        elif args.command == "pilot-packet":
            print(json.dumps(pilot_packet(bundle, args.record), indent=2, ensure_ascii=True))
        elif args.command == "evidence-ledger":
            print(json.dumps(evidence_ledger(bundle), indent=2, ensure_ascii=True))
        elif args.command == "acquisition-queue":
            print(json.dumps(acquisition_queue(bundle), indent=2, ensure_ascii=True))
        elif args.command == "provenance":
            print(json.dumps(provenance_report(bundle, args.source), indent=2, ensure_ascii=True))
        elif args.command == "audit":
            print(json.dumps(result, indent=2, ensure_ascii=True))
            if args.require_1_0 and not result["scientific_1_0_ready"]:
                return 2
        elif args.command == "export":
            print("Exported", write_export(bundle, args.output), "files")
        elif args.command == "stats":
            print(json.dumps(sequence_statistics(bundle, args.n, args.include_drafts),
                             indent=2, ensure_ascii=True))
        elif args.command == "review-packet":
            print(json.dumps(review_packet(bundle), indent=2, ensure_ascii=True))
        elif args.command == "proposal-template":
            print(json.dumps(proposal_template(bundle, args.record), indent=2, ensure_ascii=True))
        elif args.command == "check-proposal":
            proposal = read_proposal(args.file)
            report = assess_proposal(bundle, proposal)
            print(json.dumps(report, indent=2, ensure_ascii=True))
            return 0 if report["valid_proposal"] else 1
        elif args.command == "stage-proposal":
            proposal = read_proposal(args.file)
            report = stage_proposal(bundle, proposal, args.output)
            print(json.dumps(report, indent=2, ensure_ascii=True))
        elif args.command == "verify-proposal":
            verify_staged_proposal(bundle, args.directory)
            print("PASS: staged proposal matches current evidence; no changes admitted")
        return 0
    except (KeyError, TypeError, ValueError, OSError) as exc:
        print("FAIL:", str(exc))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
