"""Read-only contribution intake. Proposals never become corpus evidence here."""
import copy
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import re
from urllib.parse import urlsplit
from .admission import evidence_digest
from .core import audit, CONSULTED, MEMBERSHIP

FORMAT = "byblos-contribution-proposal-v1"
TEXT_FIELDS = {"display_name", "material", "object_type", "membership_note", "museum_id",
               "reported_excavation_identifier", "discovery_context"}
ALLOWED_FIELDS = TEXT_FIELDS | {"membership", "dimensions_mm"}


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def _positive_number(value):
    if type(value) not in {int, float}:
        return False
    try:
        return math.isfinite(value) and value > 0
    except OverflowError:
        return False


def read_proposal(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON field: " + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def proposal_template(bundle, record_ids=None):
    if not audit(bundle)["structure_valid"]:
        raise ValueError("Cannot prepare a template from invalid corpus")
    records = {r["id"]: r for r in bundle["catalogue"]["records"]}
    selected = sorted(records if record_ids is None else record_ids)
    if not selected or len(selected) != len(set(selected)) or any(r not in records for r in selected):
        raise ValueError("Template targets must be unique known record IDs")
    return {
        "format": FORMAT, "base_evidence_sha256": evidence_digest(bundle),
        "proposal_id": None, "submitted_on": None, "contributor": {"id": None, "name": None},
        "changes": [], "new_sources": [], "note": "",
        "target_records": selected,
        "instructions": "Fill identity and date, then add evidenced changes or new source leads. This empty template is not a valid submission.",
        "allowed_fields": sorted(ALLOWED_FIELDS),
    }


def assess_proposal(bundle, proposal):
    """Check submission structure and base conditions, never historical truth."""
    if not audit(bundle)["structure_valid"]:
        raise ValueError("Cannot assess proposals against invalid corpus")
    errors = []
    def fail(message):
        errors.append(message)
    def text(value):
        return isinstance(value, str) and bool(value.strip())
    def identifier(value):
        return isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value) is not None
    digest = evidence_digest(bundle)
    if not isinstance(proposal, dict):
        return {"valid_proposal": False, "errors": ["Proposal must be an object"], "automatically_applied": False}
    try:
        _json(proposal)
    except (ValueError, TypeError):
        return {"valid_proposal": False, "errors": ["Proposal must contain finite JSON values"], "automatically_applied": False}
    expected_keys = {"format", "base_evidence_sha256", "proposal_id", "submitted_on", "contributor",
                     "changes", "new_sources", "note", "target_records", "instructions", "allowed_fields"}
    if set(proposal) - expected_keys:
        fail("Unsupported proposal fields: " + ", ".join(sorted(set(proposal) - expected_keys)))
    if proposal.get("format") != FORMAT:
        fail("Unsupported proposal format")
    if proposal.get("base_evidence_sha256") != digest:
        fail("Stale or unknown evidence snapshot; regenerate the template")
    if not identifier(proposal.get("proposal_id")):
        fail("Missing or invalid proposal ID")
    contributor = proposal.get("contributor", {})
    if not isinstance(contributor, dict) or set(contributor) != {"id", "name"} or not all(text(contributor.get(k)) for k in ("id", "name")):
        fail("Contributor requires a stable ID and name")
    try:
        if date.fromisoformat(proposal.get("submitted_on", "")) > date.today():
            fail("Submission date is in the future")
    except (ValueError, TypeError):
        fail("Submission date must be YYYY-MM-DD")
    if not isinstance(proposal.get("note", ""), str):
        fail("Proposal note must be text")
    sources = {s["id"]: s for s in bundle["sources"]["sources"]}
    records = {r["id"]: r for r in bundle["catalogue"]["records"]}
    targets = proposal.get("target_records", list(records))
    if not isinstance(targets, list) or not all(isinstance(r, str) and r in records for r in targets) or len(targets) != len(set(targets)):
        fail("Target record list is invalid")
        targets = []
    new_sources = proposal.get("new_sources")
    if not isinstance(new_sources, list):
        fail("new_sources must be a list")
        new_sources = []
    proposed_source_ids = []
    for n, source in enumerate(new_sources):
        label = f"new_sources[{n}]"
        if not isinstance(source, dict):
            fail(label + " must be an object")
            continue
        ident = source.get("id")
        if not identifier(ident) or ident in sources:
            fail(label + " has duplicate, existing or invalid source ID")
        else:
            sources[ident] = source
            proposed_source_ids.append(ident)
        if set(source) - {"id", "citation", "url", "doi", "consultation", "accessed", "notes", "rights"}:
            fail(label + " has unsupported fields")
        if not text(source.get("citation")) or not isinstance(source.get("consultation"), str) or source["consultation"] not in CONSULTED:
            fail(label + " requires a citation and consultation depth")
        for field in ("doi", "notes"):
            if source.get(field) is not None and not isinstance(source[field], str):
                fail(label + " " + field + " must be text or null")
        if source.get("accessed") is not None:
            try:
                if date.fromisoformat(source["accessed"]) > date.today():
                    fail(label + " access date is in the future")
            except (ValueError, TypeError):
                fail(label + " access date must be YYYY-MM-DD or null")
        url = source.get("url")
        try:
            if url is not None and (not isinstance(url, str) or urlsplit(url).scheme not in {"http", "https"} or not urlsplit(url).netloc):
                fail(label + " URL must be HTTP(S) or null")
        except ValueError:
            fail(label + " URL is malformed")
        rights = source.get("rights", {})
        if not isinstance(rights, dict) or rights.get("status") != "not_assessed" or not text(rights.get("scope")):
            fail(label + " must leave reuse rights not_assessed with an explicit scope")
    changes = proposal.get("changes")
    if not isinstance(changes, list):
        fail("changes must be a list")
        changes = []
    if not changes and not new_sources:
        fail("Submission has no proposed changes or source leads")
    seen = set()
    proposed_changes = []
    for n, change in enumerate(changes):
        label = f"changes[{n}]"
        if not isinstance(change, dict) or set(change) != {"record_id", "field", "expected", "value", "evidence"}:
            fail(label + " requires exactly record_id, field, expected, value and evidence")
            continue
        rid, field = change["record_id"], change["field"]
        if not isinstance(rid, str) or rid not in records or rid not in targets:
            fail(label + " has an unknown or out-of-scope record")
            continue
        if not isinstance(field, str) or field not in ALLOWED_FIELDS:
            fail(label + " cannot change identity links, signs, approvals, rights or release gates")
            continue
        if (rid, field) in seen:
            fail(label + " duplicates a record/field change")
        seen.add((rid, field))
        row = records[rid]
        before = {"present": field in row}
        if field in row:
            before["value"] = row[field]
        try:
            if _json(change["expected"]) != _json(before):
                fail(label + " expected value does not match the snapshot")
        except (ValueError, TypeError):
            fail(label + " expected value is invalid")
        value = change["value"]
        if field in TEXT_FIELDS and value is not None and not text(value):
            fail(label + " value must be nonempty text or null")
        if field == "membership" and (not isinstance(value, str) or value not in MEMBERSHIP):
            fail(label + " membership is invalid")
        if field == "dimensions_mm" and value is not None:
            if not isinstance(value, dict) or not value or not all(
                    isinstance(k, str) and bool(k.strip()) and _positive_number(v)
                    for k, v in value.items()):
                fail(label + " dimensions require positive finite numbers, not booleans")
        evidence = change["evidence"]
        if not isinstance(evidence, list) or not evidence:
            fail(label + " requires attributable evidence")
            evidence = []
        for ev in evidence:
            if not isinstance(ev, dict) or set(ev) != {"source_id", "locator", "fields"}:
                fail(label + " evidence requires source_id, locator and fields")
                continue
            sid = ev.get("source_id")
            source = sources.get(sid) if isinstance(sid, str) else None
            if source is None or source.get("consultation") == "not_consulted":
                fail(label + " evidence source is unknown or unconsulted")
            if not text(ev.get("locator")) or ev.get("fields") != [field]:
                fail(label + " evidence must identify a precise locator and exactly the proposed field")
        proposed_changes.append({"record_id": rid, "field": field, "before": copy.deepcopy(before),
                                 "proposed": {"present": True, "value": copy.deepcopy(value)},
                                 "evidence": copy.deepcopy(evidence)})
    return {"format": "byblos-proposal-assessment-v1", "valid_proposal": not errors,
            "errors": errors, "base_evidence_sha256": digest, "automatically_applied": False,
            "acceptance_status": "awaiting_maintainer_and_scientific_review" if not errors else "invalid_submission",
            "proposed_changes": proposed_changes, "proposed_source_ids": proposed_source_ids,
            "review_refresh_required_if_admitted": bool(proposed_changes or proposed_source_ids),
            "interpretation": "A valid submission is structurally reviewable. Evidence claims, identity, scientific merit and permission remain unverified."}


def stage_proposal(bundle, proposal, output):
    report = assess_proposal(bundle, proposal)
    if not report["valid_proposal"]:
        raise ValueError("Invalid proposal: " + "; ".join(report["errors"]))
    output = Path(output)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Staging destination must be a new or empty directory")
    texts = _staging_texts(proposal, report)
    output.mkdir(parents=True, exist_ok=True)
    for name, text in texts.items():
        (output / name).write_text(text, encoding="utf-8", newline="")
    return report


def _staging_texts(proposal, report):
    texts = {"proposal.json": _json(proposal), "assessment.json": _json(report),
             "README.md": "# Pending contribution\n\nThis is a proposed change, not an accepted corpus snapshot.\nNo corpus files have been changed. Review sources and scientific claims manually.\nNo permission or approval is granted. Evidence edits require renewed review.\n"}
    manifest = {"format": "byblos-proposal-staging-v1", "algorithm": "sha256",
                "files": {name: hashlib.sha256(text.encode("utf-8")).hexdigest() for name, text in sorted(texts.items())}}
    texts["manifest.json"] = _json(manifest)
    return texts


def verify_staged_proposal(bundle, output):
    """Verify hashes and regenerate the assessment against the current evidence."""
    output = Path(output)
    names = {"proposal.json", "assessment.json", "README.md", "manifest.json"}
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    if actual != names or any((output / name).is_symlink() for name in names):
        raise ValueError("Staging file inventory is incomplete, extra or unsafe")
    proposal = read_proposal(output / "proposal.json")
    report = assess_proposal(bundle, proposal)
    if not report["valid_proposal"]:
        raise ValueError("Staged proposal is invalid or stale")
    expected = _staging_texts(proposal, report)
    if any((output / name).read_text(encoding="utf-8") != text for name, text in expected.items()):
        raise ValueError("Staging content or manifest differs from regenerated assessment")
    return True
