"""Evidence requirements for a dated, bounded scientific release.

These checks verify declarations. A real specialist must assess their truth.
"""
import copy
from datetime import date
import hashlib
import json


def evidence_digest(bundle):
    """Bind reviews to data, excluding only review records and derived flags.

    Version, source inventory, evidence, tokens and admission decisions are bound.
    Adding approvals or promoting reviewed/draft flags does not change the hash.
    """
    data = copy.deepcopy(bundle)
    data.get("research_entities", {})["reviews"] = []
    data.get("coverage", {}).pop("release_gates", None)
    for row in data.get("catalogue", {}).get("records", []):
        if isinstance(row, dict):
            row.pop("review_status", None)
    for row in data.get("research_entities", {}).get("transcriptions", []):
        if isinstance(row, dict):
            row.pop("status", None)
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def approved(bundle, entity_type, ident):
    digest = evidence_digest(bundle)
    authors = bundle.get("coverage", {}).get("admission_audit", {}).get("contributor_ids", [])
    return any(r.get("scope") == {"entity_type": entity_type, "id": ident}
               and r.get("status") == "approved" and r.get("independent") is True
               and r.get("reviewed_bundle_sha256") == digest
               and isinstance(authors, list) and bool(authors)
               and r.get("reviewer_id") and r["reviewer_id"] not in authors
               for r in bundle.get("research_entities", {}).get("reviews", [])
               if isinstance(r, dict))


def admission_assessment(bundle):
    """A positive result needs complete inventory decisions and bound review."""
    missing = []
    def need(condition, code):
        if not condition:
            missing.append(code)
    coverage = bundle.get("coverage", {})
    policy = coverage.get("admission_audit", {})
    if not isinstance(policy, dict):
        policy = {}
    def declared_rows(key):
        value = policy.get(key, [])
        return value if isinstance(value, list) else []
    sources = {s["id"]: s for s in bundle.get("sources", {}).get("sources", [])
               if isinstance(s, dict) and isinstance(s.get("id"), str)}
    records = [r for r in bundle.get("catalogue", {}).get("records", []) if isinstance(r, dict)]
    entities = bundle.get("research_entities", {})
    core = [r for r in records if r.get("membership") == "reported_core"]
    def supported(row):
        ev = row.get("evidence", [])
        return isinstance(ev, list) and bool(ev) and all(
            isinstance(e, dict) and e.get("source_id") in sources
            and sources[e["source_id"]].get("consultation") != "not_consulted"
            and isinstance(e.get("locator"), str) and bool(e["locator"].strip())
            for e in ev)
    try:
        cutoff = date.fromisoformat(policy.get("cutoff_date", ""))
        dated = cutoff <= date.fromisoformat(coverage.get("as_of", ""))
    except (ValueError, TypeError):
        dated = False
    need(type(policy.get("policy_version")) is int and policy["policy_version"] == 1 and dated
         and all(isinstance(policy.get(k), str) and policy[k].strip()
                 for k in ("scope_statement", "inclusion_criteria", "exclusion_criteria")),
         "dated_scope_and_criteria")
    need(supported(policy), "scope_evidence")
    authors = policy.get("contributor_ids", [])
    need(isinstance(authors, list) and bool(authors)
         and all(isinstance(a, str) and a.strip() for a in authors), "contributor_identity_declaration")

    def dispositions(key, expected):
        rows = policy.get(key, [])
        if not isinstance(rows, list):
            return False
        ids = [r.get("id") for r in rows if isinstance(r, dict)]
        if len(ids) != len(rows) or len(ids) != len(set(ids)) or set(ids) != set(expected):
            return False
        return all(r.get("status") in {"collated", "excluded"}
                   and isinstance(r.get("rationale"), str) and r["rationale"].strip()
                   and supported(r) for r in rows)
    need(dispositions("source_dispositions", sources), "source_inventory_dispositions")
    need(all(r.get("status") != "collated" or sources.get(r.get("id"), {}).get("consultation")
             in {"consulted_online", "selected_sections", "selected_pages"}
             for r in declared_rows("source_dispositions") if isinstance(r, dict)),
         "collated_sources_directly_consulted")
    need(dispositions("bibliography_dispositions", [b.get("id") for b in bundle.get("bibliography", {}).get("entries", [])]),
         "bibliography_dispositions")
    need(dispositions("count_reconciliations", [c.get("id") for c in coverage.get("count_claims", [])]),
         "count_reconciliations")
    # A search log must describe reproducible coverage and its limits, not only hits.
    protocol = policy.get("search_protocol", {})
    need(isinstance(protocol, dict) and bool(protocol.get("databases"))
         and bool(protocol.get("queries")) and bool(protocol.get("languages"))
         and bool(protocol.get("date_range")) and bool(protocol.get("citation_chaining"))
         and bool(protocol.get("limitations")) and supported(protocol), "systematic_search_protocol")
    need(bool(records) and all(approved(bundle, "records", r.get("id")) for r in records),
         "all_membership_decisions_reviewed")
    need(bool(core) and all(r.get("object_id") and r.get("surfaces")
                           and r.get("evidence_level") in {"publication_checked", "artifact_checked"}
                           for r in core), "core_identity_and_direct_evidence")
    surfaces = {s.get("id"): s for s in bundle.get("surfaces", {}).get("surfaces", [])}
    editions = {e.get("id"): e for e in entities.get("editions", [])}
    transcriptions = {t.get("id"): t for t in entities.get("transcriptions", [])}
    for r in core:
        tr = transcriptions.get(r.get("transcription"), {})
        required = {(sid, n) for sid in (r.get("surfaces") or [])
                    for n in range(1, surfaces.get(sid, {}).get("line_count", 0) + 1)}
        actual = {(line.get("surface_id"), line.get("line")) for line in tr.get("lines", [])}
        need(bool(required) and actual == required and tr.get("status") == "verified"
             and approved(bundle, "transcriptions", tr.get("id")), "complete_sequence:" + str(r.get("id")))
        ed = editions.get(tr.get("edition_id"), {})
        source = sources.get(ed.get("source_id"), {})
        need(source.get("consultation") in {"consulted_online", "selected_sections", "selected_pages"}
             and ed.get("collation_complete") is True and supported(ed), "edition_collation:" + str(r.get("id")))
    need(all(e.get("mapping_status") in {"verified", "excluded"} and supported(e)
             for e in bundle.get("external_crosswalk", {}).get("entries", [])), "external_crosswalk_decisions")
    need(all(g.get("status") == "resolved" and supported(g) for g in coverage.get("gaps", [])),
         "research_gaps_resolved")
    need(approved(bundle, "admission", "scientific-1.0"), "independent_admission_review")
    return {"policy_version": 1, "ready": not missing, "missing": missing,
            "claim_limit": "Complete within the independently reviewed scope and cutoff; future finds and publications remain possible."}
