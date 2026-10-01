"""Validate catalogue structure; does not certify evidence or completeness."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate(catalogue, sources, coverage):
    errors = []
    source_rows = sources["sources"]
    source_ids = [s["id"] for s in source_rows]
    if len(source_ids) != len(set(source_ids)):
        errors.append("Duplicate source IDs")
    ids = set(source_ids)
    records = catalogue["records"]
    record_ids = [r["id"] for r in records]
    if len(record_ids) != len(set(record_ids)):
        errors.append("Duplicate inscription IDs")
    labels = [r["edition_label"] for r in records if r["edition_label"] is not None]
    if len(labels) != len(set(labels)):
        errors.append("Duplicate edition labels")
    for r in records:
        if not r["evidence"]:
            errors.append(f'{r["id"]}: missing evidence')
        for e in r["evidence"]:
            if e["source_id"] not in ids or not e["locator"].strip():
                errors.append(f'{r["id"]}: invalid evidence reference')
        if r["primary_edition_lead"] is not None and r["primary_edition_lead"] not in ids:
            errors.append(f'{r["id"]}: unknown edition lead')
        if r["membership"] not in {"reported_core", "disputed", "excluded"}:
            errors.append(f'{r["id"]}: invalid membership')
        if r["transcription"] is not None:
            errors.append(f'{r["id"]}: transcription model not supported by schema 0.1.0')
        if r["evidence_level"] != "secondary_report" or r["review_status"] != "unreviewed":
            errors.append(f'{r["id"]}: evidence upgrade requires a schema update')
    for claim in coverage["count_claims"]:
        if claim["source_id"] not in ids or not claim["locator"]:
            errors.append("Count claim lacks valid source")
        if not isinstance(claim["count"], int) or claim["count"] < 0:
            errors.append("Invalid count claim")
    for gap in coverage["gaps"]:
        if not set(gap["source_ids"]).issubset(ids):
            errors.append("Gap references unknown source")
    gates = coverage["release_gates"]
    if gates["exhaustive_claim_allowed"]:
        errors.append("Schema 0.1.0 cannot establish exhaustive coverage")
    if any(gates[k] != 0 for k in ("verified_transcriptions", "independent_reviews", "rights_cleared_assets")):
        errors.append("Foundation gates must remain zero")
    return errors

def main():
    data = [json.loads((ROOT / "data" / p).read_text(encoding="utf-8"))
            for p in ("catalogue.json", "sources.json", "coverage.json")]
    errors = validate(*data)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(data[0]['records'])} provisional records; "
          f"{len(data[1]['sources'])} sources/leads; "
          f"{len(data[2]['gaps'])} open gaps; 0 verified transcriptions.")

if __name__ == "__main__":
    main()
