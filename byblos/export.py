"""Deterministic exports with attributable records and integrity manifests."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import io
import json
from .core import audit, FILE_KEYS
from .provenance import provenance_report
from .workflow import review_packet
from .explorer import explorer_html
from .contributions import proposal_template

def json_text(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"

def export_texts(bundle):
    report = audit(bundle)
    if not report["structure_valid"]:
        raise ValueError("Refusing export of invalid data: " + "; ".join(report["errors"]))
    texts = {"bundle.json": json_text(bundle), "audit.json": json_text(report)}
    texts["provenance.json"] = json_text(provenance_report(bundle))
    texts["review_packet.json"] = json_text(review_packet(bundle))
    texts["index.html"] = explorer_html(bundle)
    texts["contribution_template.json"] = json_text(proposal_template(bundle))
    rows = sorted(bundle["catalogue"]["records"], key=lambda r: r["id"])
    texts["catalogue.jsonl"] = "".join(
        json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    table = io.StringIO(newline="")
    columns = ["id", "edition_label", "display_name", "membership", "material",
               "object_type", "evidence_json", "review_status", "transcription"]
    writer = csv.DictWriter(table, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for r in rows:
        out = {k: r.get(k) for k in columns if k != "evidence_json"}
        out["evidence_json"] = json.dumps(r["evidence"], ensure_ascii=False, sort_keys=True)
        # CSV is a convenience view. JSONL/bundle preserve null and full structure.
        writer.writerow(out)
    texts["catalogue.csv"] = table.getvalue()
    lines = [
        "# Byblos corpus audit", "",
        f"Snapshot version: {report['version']}",
        f"Scientific 1.0 ready: **{report['scientific_1_0_ready']}**", "",
        "Structural validity is not proof of accuracy or exhaustive coverage.", "",
        "| Count | Value |", "|---|---:|",
    ]
    lines += [f"| {k.replace('_', ' ')} | {v} |" for k, v in report["counts"].items()]
    lines += ["", "| Gate | Result |", "|---|---|"]
    lines += [f"| {k.replace('_', ' ')} | {'PASS' if v else 'OPEN'} |"
              for k, v in report["gates"].items()]
    lines += ["", "## Admission evidence", "",
              f"Evidence snapshot SHA-256: `{report['review_evidence_sha256']}`", "",
              report["admission"]["claim_limit"], ""]
    lines += [f"- {item}" for item in report["admission"]["missing"]]
    lines += ["", "## Open research gaps", ""]
    for gap in bundle["coverage"]["gaps"]:
        if gap["status"] == "open":
            lines.append(f"- **{gap['id']}**: {gap['task']}")
    lines += ["", "## Counting claims", "",
              "These counts describe different source-defined units; do not sum them.", "",
              "| Source | Count | Unit |", "|---|---:|---|"]
    lines += [f"| {x['source_id']} | {x['count']} | {x['unit']} |"
              for x in bundle["coverage"]["count_claims"]]
    lines += ["", "## Catalogue", "", "| ID | Membership | Description | Evidence |",
              "|---|---|---|---|"]
    for r in rows:
        desc = r.get("display_name") or r.get("edition_label") or "Unknown"
        refs = "; ".join(f"{e['source_id']}, {e['locator']}" for e in r["evidence"])
        lines.append(f"| {r['id']} | {r['membership']} | {desc} | {refs} |")
    lines += ["", "## Sources and rights", ""]
    for source in sorted(bundle["sources"]["sources"], key=lambda s: s["id"]):
        lines += [f"- **{source['id']}**: {source['citation']}",
                  f"  Consultation: {source['consultation']}; rights: {source['rights']['status']}."]
        if source.get("url"):
            lines.append(f"  Source: {source['url']}")
    lines += ["", "## Interpretation", "", report["interpretation"],
              "No corpus sequences, font files or source plate images are republished.",
              "CSV empty fields mean null/unknown in this view; use bundle.json for exact types.",
              "Checksums establish snapshot integrity, not authenticity or scholarly correctness.", ""]
    texts["REPORT.md"] = "\n".join(lines)
    texts["REUSE.md"] = (
        "# Reuse\n\nThis export contains factual metadata and original attributed annotations.\n"
        "No third-party sign sequences, images, fonts or publication texts are included.\n"
        "Consult each source's rights scope. No blanket data licence is granted.\n"
        "Cite hawkinsnick/Byblos-syllabary, snapshot version, commit and access date,\n"
        "and preserve the underlying source citations for reused assertions.\n")
    manifest = {
        "version": report["version"], "scientific_1_0_ready": report["scientific_1_0_ready"],
        "algorithm": "sha256",
        "files": {name: hashlib.sha256(text.encode("utf-8")).hexdigest()
                  for name, text in sorted(texts.items())},
        "inputs": {FILE_KEYS[k]: hashlib.sha256(json_text(v).encode("utf-8")).hexdigest()
                   for k, v in sorted(bundle.items()) if k in FILE_KEYS},
        "input_hash_format": "Canonical JSON: sorted keys, ensure_ascii=False, indent=2, trailing newline",
    }
    texts["manifest.json"] = json_text(manifest)
    return texts

def write_export(bundle, output):
    texts = export_texts(bundle)
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("Export destination must be empty; choose a new directory.")
    output.mkdir(parents=True, exist_ok=True)
    for name, text in texts.items():
        (output / name).write_text(text, encoding="utf-8", newline="")
    return len(texts)

def verify_export(output):
    output = Path(output).resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("algorithm") != "sha256" or not isinstance(manifest.get("files"), dict):
        raise ValueError("Invalid manifest")
    expected = set(manifest["files"]) | {"manifest.json"}
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    errors = []
    if actual != expected:
        errors.append("File inventory differs from manifest")
    for name, digest in manifest["files"].items():
        path = (output / name).resolve()
        if path.parent != output or name != path.name or path.is_symlink():
            errors.append("Unsafe manifest path")
            continue
        if not isinstance(digest, str) or len(digest) != 64:
            errors.append("Invalid digest")
        elif not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            errors.append(f"Checksum mismatch: {name}")
    if errors:
        raise ValueError("; ".join(errors))
    # Hashes alone could accompany invalid scientific assertions; audit embedded data.
    bundle = json.loads((output / "bundle.json").read_text(encoding="utf-8"))
    regenerated = export_texts(bundle)
    if regenerated["manifest.json"] != (output / "manifest.json").read_text(encoding="utf-8"):
        raise ValueError("Manifest inconsistent with embedded bundle")
    if any((output / name).read_text(encoding="utf-8") != text
           for name, text in regenerated.items()):
        raise ValueError("Export views inconsistent with embedded bundle")
    return True

def sequence_statistics(bundle, n=2, include_drafts=False):
    if type(n) is not int or not 1 <= n <= 6:
        raise ValueError("n must be an integer from 1 to 6")
    report = audit(bundle)
    if not report["structure_valid"]:
        raise ValueError("Invalid bundle")
    allowed = {r["id"] for r in bundle["catalogue"]["records"]
               if r["membership"] == "reported_core"}
    selected = [t for t in bundle["research_entities"]["transcriptions"]
                if t["inscription_id"] in allowed and
                (t["status"] == "verified" or include_drafts)]
    counts = Counter()
    for tr in selected:
        for line in tr["lines"]:
            run = []
            for token in line["tokens"]:
                if token["status"] == "observed":
                    run.append(token["sign_id"])
                    if len(run) >= n:
                        counts[tuple(run[-n:])] += 1
                else:
                    run = []
    return {
        "n": n, "selected_transcriptions": len(selected), "include_drafts": include_drafts,
        "status": "observed_token_statistics" if selected else "no_eligible_sequences",
        "method": "Reported core only; edition-specific signs; observed tokens only; gaps, dividers, numerals, restorations and uncertainty break sequences; never cross line boundaries.",
        "ngrams": [{"sign_ids": list(k), "count": v}
                   for k, v in sorted(counts.items(), key=lambda item: (-item[1], item[0]))],
    }
