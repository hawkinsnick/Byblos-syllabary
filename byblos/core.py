"""Original dependency-free validation and release audit.

Validation checks recorded assertions, not their historical truth.
No remote requests and no automatic decipherment or rights assumptions.
"""
from collections import Counter
from pathlib import Path
import json
import re
from datetime import date
from .jsonio import read_json
from .admission import admission_assessment, evidence_digest, approved

ROOT = Path(__file__).resolve().parents[1]
CONSULTED = {"consulted_online", "abstract_only", "selected_sections", "selected_pages",
             "metadata_only", "not_consulted"}
MEMBERSHIP = {"reported_core", "disputed", "excluded"}
KINDS = {"objects", "signs", "editions", "transcriptions", "reviews", "assets"}
FILE_KEYS = {
    "catalogue": "catalogue.json", "sources": "sources.json",
    "coverage": "coverage.json", "surfaces": "surfaces.json",
    "relations": "relations.json", "external_crosswalk": "external_crosswalk.json",
    "research_entities": "research_entities.json", "bibliography": "bibliography.json",
    "search_log": "search_log.json",
}

def load_bundle(root=ROOT):
    root = Path(root)
    return {key: read_json(root / "data" / name)
            for key, name in FILE_KEYS.items()}

def validate_bundle(bundle):
    errors = []
    def fail(where, message):
        errors.append(f"{where}: {message}")

    def rows(container, key, where):
        if not isinstance(container, dict) or not isinstance(container.get(key), list):
            fail(where, f"expected list {key}")
            return []
        result = []
        seen = set()
        for i, row in enumerate(container[key]):
            pos = f"{where}.{key}[{i}]"
            if not isinstance(row, dict):
                fail(pos, "expected object")
                continue
            ident = row.get("id")
            if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", ident):
                fail(pos, "invalid or missing ID")
            elif ident in seen:
                fail(pos, f"duplicate ID {ident}")
            else:
                seen.add(ident)
            result.append(row)
        return result

    sources = rows(bundle.get("sources"), "sources", "sources")
    records = rows(bundle.get("catalogue"), "records", "catalogue")
    surfaces = rows(bundle.get("surfaces"), "surfaces", "surfaces")
    relations = rows(bundle.get("relations"), "relations", "relations")
    claims = rows(bundle.get("coverage"), "count_claims", "coverage")
    gaps = rows(bundle.get("coverage"), "gaps", "coverage")
    bibliography = rows(bundle.get("bibliography"), "entries", "bibliography")
    crosswalk = rows(bundle.get("external_crosswalk"), "entries", "external_crosswalk")
    entities = {k: rows(bundle.get("research_entities"), k, "research_entities") for k in sorted(KINDS)}
    index = {k: {row.get("id"): row for row in vals if isinstance(row.get("id"), str)}
             for k, vals in entities.items()}
    src = {s.get("id"): s for s in sources if isinstance(s.get("id"), str)}
    rec = {r.get("id"): r for r in records if isinstance(r.get("id"), str)}
    surf = {s.get("id"): s for s in surfaces if isinstance(s.get("id"), str)}

    def evidence(row, where, required=True):
        es = row.get("evidence")
        if not isinstance(es, list) or (required and not es):
            fail(where, "missing evidence list")
            return
        fields = set()
        for e in es:
            if not isinstance(e, dict):
                fail(where, "evidence must be an object")
                continue
            if e.get("source_id") not in src:
                fail(where, "unknown evidence source")
            elif src[e["source_id"]].get("consultation") == "not_consulted":
                fail(where, "unconsulted source cannot support an assertion directly")
            if not isinstance(e.get("locator"), str) or not e["locator"].strip():
                fail(where, "evidence lacks precise locator")
            if not isinstance(e.get("fields"), list) or not all(isinstance(f, str) for f in e["fields"]):
                fail(where, "evidence fields must be a string list")
            else:
                fields.update(e["fields"])
        return fields

    for s in sources:
        where = str(s.get("id"))
        if not isinstance(s.get("citation"), str) or not s["citation"].strip():
            fail(where, "missing source citation")
        if s.get("consultation") not in CONSULTED:
            fail(where, "invalid consultation depth")
        if not isinstance(s.get("rights"), dict) or not s["rights"].get("scope"):
            fail(where, "missing scope-specific rights observation")
        for bc in s.get("bibliographic_claims", []):
            if bc.get("source_id") not in src or not bc.get("locator"):
                fail(where, "bibliographic claim lacks source/locator")

    labels = []
    for r in records:
        where = str(r.get("id"))
        for field in ("edition_label", "material", "object_type", "membership", "evidence_level",
                      "primary_edition_lead", "museum_id", "object_id", "date_claims", "surfaces",
                      "transcription", "review_status"):
            if field not in r:
                fail(where, f"missing field {field}; use null for unknowns")
        fields = evidence(r, where) or set()
        if r.get("membership") not in MEMBERSHIP:
            fail(where, "invalid membership")
        if r.get("review_status") not in {"unreviewed", "reviewed"}:
            fail(where, "invalid review status")
        if r.get("evidence_level") not in {"secondary_report", "publication_checked", "artifact_checked"}:
            fail(where, "invalid evidence level")
        for f in ("edition_label", "display_name", "material", "object_type", "membership",
                  "membership_note", "dimensions_mm", "discovery_context", "museum_id",
                  "reported_excavation_identifier"):
            if r.get(f) is not None and f not in fields:
                fail(where, f"asserted field {f} lacks evidence")
        label = r.get("edition_label")
        if label is not None:
            if not isinstance(label, str) or not label:
                fail(where, "invalid edition label")
            else:
                labels.append(label)
        if r.get("primary_edition_lead") is not None and r["primary_edition_lead"] not in src:
            fail(where, "unknown primary edition lead")
        if r.get("object_id") is not None and r["object_id"] not in index["objects"]:
            fail(where, "unknown object ID")
        if r.get("surfaces") is not None:
            if not isinstance(r["surfaces"], list) or len(r["surfaces"]) != len(set(r["surfaces"])):
                fail(where, "surface IDs must be a unique list or null")
            else:
                for sid in r["surfaces"]:
                    if sid not in surf or surf[sid].get("inscription_id") != r.get("id"):
                        fail(where, "invalid surface link")
        if r.get("transcription") is not None:
            tid = r["transcription"]
            if not isinstance(tid, str) or tid not in index["transcriptions"] or index["transcriptions"][tid].get("inscription_id") != r.get("id"):
                fail(where, "invalid transcription link")
        if not isinstance(r.get("date_claims"), list):
            fail(where, "date claims must be an array")
        else:
            for dc in r["date_claims"]:
                evidence(dc, where + ".date")
                if not isinstance(dc.get("proposer"), str) or not dc["proposer"]:
                    fail(where, "date hypothesis lacks proposer")
        for hypothesis in r.get("direction_claims", []):
            evidence(hypothesis, where + ".direction")
            if hypothesis.get("value") not in {"ltr", "rtl", "vertical", "unknown"} or not hypothesis.get("proposer"):
                fail(where, "direction hypothesis lacks value/proposer")
        if r.get("reported_museum_identifier") is not None:
            museum = r["reported_museum_identifier"]
            evidence(museum, where + ".museum")
            if museum.get("verification") != "reported_only" or not museum.get("value") or not museum.get("institution"):
                fail(where, "invalid reported museum identity")
        if r.get("review_status") == "reviewed" and not approved(bundle, "records", r.get("id")):
            fail(where, "reviewed flag without independent approval")
    if len(labels) != len(set(labels)):
        fail("catalogue", "duplicate edition labels")

    for s in surfaces:
        where = str(s.get("id"))
        fs = evidence(s, where) or set()
        if s.get("inscription_id") not in rec:
            fail(where, "unknown inscription")
        if s.get("direction") not in {"rtl", "ltr", "vertical", "mixed", "unknown"}:
            fail(where, "invalid direction")
        if type(s.get("line_count")) is not int or s["line_count"] < 1:
            fail(where, "invalid line count")
        for f in ("label", "line_count", "direction"):
            if f not in fs:
                fail(where, f"surface field {f} lacks evidence")
        if s.get("inscription_id") in rec and s.get("id") not in (rec[s["inscription_id"]].get("surfaces") or []):
            fail(where, "surface not linked back from inscription")

    for rel in relations:
        evidence(rel, str(rel.get("id")))
        if not isinstance(rel.get("subjects"), list) or any(x not in rec for x in rel["subjects"]):
            fail(str(rel.get("id")), "unknown relation subject")
        if rel.get("assessment") not in {"hypothesis", "verified", "rejected"}:
            fail(str(rel.get("id")), "invalid relation assessment")

    for claim in claims:
        if claim.get("source_id") not in src or not claim.get("locator") or not claim.get("unit"):
            fail(str(claim.get("id")), "count claim lacks valid source, locator or unit")
        if type(claim.get("count")) is not int or claim["count"] < 0:
            fail(str(claim.get("id")), "invalid count claim")
    for gap in gaps:
        if gap.get("status") not in {"open", "resolved"}:
            fail(str(gap.get("id")), "invalid gap status")
        if not isinstance(gap.get("source_ids"), list) or any(x not in src for x in gap["source_ids"]):
            fail(str(gap.get("id")), "unknown gap source")
        if gap.get("status") == "resolved":
            evidence(gap, str(gap.get("id")))
    for b in bibliography:
        if b.get("discovery_source") not in src or not b.get("discovery_locator"):
            fail(str(b.get("id")), "bibliography entry lacks discovery source")
    cwsrc = bundle.get("external_crosswalk", {}).get("source_id")
    if cwsrc not in src:
        fail("external_crosswalk", "unknown source")
    for entry in crosswalk:
        if not entry.get("provider_label") or not entry.get("locator"):
            fail(str(entry.get("id")), "missing external label or locator")
        target = entry.get("proposed_project_record")
        if target is not None and target not in rec:
            fail(str(entry.get("id")), "unknown crosswalk target")
        if entry.get("mapping_status") not in {"unresolved", "label_match_only", "caption_match_only", "verified", "excluded"}:
            fail(str(entry.get("id")), "invalid mapping status")
        if entry.get("mapping_status") in {"caption_match_only", "verified", "excluded"}:
            evidence(entry, str(entry.get("id")))
        if entry.get("mapping_status") == "excluded" and not entry.get("exclusion_reason"):
            fail(str(entry.get("id")), "excluded crosswalk entry lacks reason")
        if entry.get("project_evidence_source_id") is not None and entry["project_evidence_source_id"] not in src:
            fail(str(entry.get("id")), "unknown project crosswalk evidence source")

    for obj in entities["objects"]:
        evidence(obj, str(obj.get("id")))
    for sign in entities["signs"]:
        evidence(sign, str(sign.get("id")))
        if not sign.get("edition_sign_label") or sign.get("edition_id") not in index["editions"]:
            fail(str(sign.get("id")), "sign lacks edition identity")
        # Sound values cannot be promoted to canonical sign facts.
        if sign.get("sound_value") is not None:
            fail(str(sign.get("id")), "sound values belong in attributed hypotheses")
    for ed in entities["editions"]:
        evidence(ed, str(ed.get("id")))
        if ed.get("source_id") not in src or ed.get("inscription_id") not in rec:
            fail(str(ed.get("id")), "edition lacks source or inscription")
    for asset in entities["assets"]:
        if not rights_supported(asset):
            fail(str(asset.get("id")), "asset rights or attribution unresolved")
        if asset.get("source_id") not in src:
            fail(str(asset.get("id")), "asset source missing")
    for review in entities["reviews"]:
        evidence(review, str(review.get("id")))
        scope = review.get("scope", {})
        table = ({"scientific-1.0": True} if scope.get("entity_type") == "admission" else
                 rec if scope.get("entity_type") == "records" else index.get(scope.get("entity_type"), {}))
        if scope.get("id") not in table or not review.get("reviewer") or not review.get("reviewer_id"):
            fail(str(review.get("id")), "review scope or reviewer missing")
        if type(review.get("independent")) is not bool or review.get("status") not in {"approved", "changes_requested"}:
            fail(str(review.get("id")), "invalid review declaration")
        if review.get("reviewed_bundle_sha256") != evidence_digest(bundle):
            fail(str(review.get("id")), "review does not bind current evidence snapshot")
        if not review.get("review_record") or not review.get("expertise") or not review.get("reviewed_on"):
            fail(str(review.get("id")), "review lacks record, expertise or date")
        try:
            if date.fromisoformat(review.get("reviewed_on", "")) > date.fromisoformat(bundle["coverage"]["as_of"]):
                fail(str(review.get("id")), "review date exceeds snapshot date")
        except (ValueError, TypeError):
            fail(str(review.get("id")), "invalid review date")
        contributors = bundle.get("coverage", {}).get("admission_audit", {}).get("contributor_ids", [])
        if review.get("independent") and (not contributors or review.get("reviewer_id") in contributors):
            fail(str(review.get("id")), "independence lacks separate contributor/reviewer identities")

    for tr in entities["transcriptions"]:
        where = str(tr.get("id"))
        evidence(tr, where)
        rid = tr.get("inscription_id")
        ed = index["editions"].get(tr.get("edition_id"), {})
        if rid not in rec or not ed or ed.get("inscription_id") != rid:
            fail(where, "transcription edition/inscription mismatch")
        asset = index["assets"].get(tr.get("asset_id"), {})
        if not rights_supported(asset) or asset.get("kind") != "transcription":
            fail(where, "transcription lacks rights-supported transcription asset")
        if tr.get("status") not in {"draft", "verified"}:
            fail(where, "invalid transcription status")
        if tr.get("status") == "verified" and not approved(bundle, "transcriptions", tr.get("id")):
            fail(where, "verified sequence lacks independent approval")
        if tr.get("status") == "verified":
            method = tr.get("method", {})
            if (not isinstance(method, dict) or method.get("origin") not in {"independent_collation", "imported"}
                    or not method.get("creator_ids") or not method.get("source_version")
                    or not isinstance(method.get("normalization_log"), list)):
                fail(where, "verified sequence lacks origin, creators, source version or normalization log")
            elif method["origin"] == "imported":
                encoding = index["assets"].get(method.get("encoding_map_asset_id"), {})
                if encoding.get("kind") != "encoding_map" or not rights_supported(encoding):
                    fail(where, "imported sequence lacks rights-supported encoding map")
        lines = tr.get("lines")
        if not isinstance(lines, list) or not lines:
            fail(where, "missing transcription lines")
            continue
        line_ids = set()
        for line in lines:
            if not isinstance(line, dict):
                fail(where, "line must be an object")
                continue
            sid = line.get("surface_id")
            num = line.get("line")
            surface = surf.get(sid, {})
            if surface.get("inscription_id") != rid or type(num) is not int or num < 1 or num > surface.get("line_count", 0):
                fail(where, "invalid surface or line position")
            line_key = (sid, num) if isinstance(sid, str) and type(num) is int else None
            if line_key in line_ids:
                fail(where, "duplicate line position")
            line_ids.add(line_key)
            if line.get("direction") not in {"rtl", "ltr", "vertical", "unknown"}:
                fail(where, "line direction not explicit")
            tokens = line.get("tokens")
            if not isinstance(tokens, list) or not tokens:
                fail(where, "empty or missing token list")
                continue
            for pos, token in enumerate(tokens, 1):
                if not isinstance(token, dict):
                    fail(where, "token must be an object")
                    continue
                if token.get("position") != pos:
                    fail(where, "non-contiguous token positions")
                status = token.get("status")
                if status not in {"observed", "uncertain", "restored", "unreadable", "gap", "divider", "numeral"}:
                    fail(where, "invalid token status")
                sign_id = token.get("sign_id")
                if status == "observed" and sign_id not in index["signs"]:
                    fail(where, "observed token lacks registered sign")
                if sign_id is not None and sign_id not in index["signs"]:
                    fail(where, "unknown sign token")
                if status in {"gap", "unreadable"} and sign_id is not None:
                    fail(where, "gap/unreadable token cannot assert a sign")
                if sign_id in index["signs"] and index["signs"][sign_id].get("edition_id") != tr.get("edition_id"):
                    fail(where, "sign belongs to another edition")
                alternatives = token.get("alternatives", [])
                if not isinstance(alternatives, list) or any(x not in index["signs"] for x in alternatives):
                    fail(where, "invalid token alternatives")
                if status == "uncertain" and not sign_id and not alternatives:
                    fail(where, "uncertainty lacks alternatives; use unreadable")
                if status == "restored" and not token.get("rationale"):
                    fail(where, "restoration lacks rationale")
                evidence(token, where + f".token{pos}")

    # Old hand-maintained counters must agree with recorded evidence.
    gates = bundle.get("coverage", {}).get("release_gates", {})
    actual = {
        "verified_transcriptions": sum(t.get("status") == "verified" for t in entities["transcriptions"]),
        "independent_reviews": sum(r.get("independent") is True and r.get("status") == "approved" for r in entities["reviews"]),
        "rights_cleared_assets": sum(rights_supported(a) for a in entities["assets"]),
    }
    for k, value in actual.items():
        if gates.get(k) != value:
            fail("coverage.release_gates", f"{k} disagrees with recorded entities")
    if type(gates.get("exhaustive_claim_allowed")) is not bool:
        fail("coverage.release_gates", "exhaustiveness flag must be boolean")
    elif gates["exhaustive_claim_allowed"] and not admission_assessment(bundle)["ready"]:
        fail("coverage.release_gates", "exhaustiveness claim lacks complete audited admission evidence")
    return errors

def rights_supported(asset):
    rights = asset.get("rights", {}) if isinstance(asset, dict) else {}
    if not isinstance(rights, dict):
        return False
    if rights.get("status") not in {"licensed", "permission_granted", "original"}:
        return False
    if not all(isinstance(rights.get(f), str) and rights[f].strip()
               for f in ("reference", "creator", "attribution", "scope")):
        return False
    if rights.get("status") == "licensed" and not rights.get("license"):
        return False
    if rights.get("status") == "permission_granted" and not rights.get("permission_record"):
        return False
    return True

def audit(bundle):
    errors = validate_bundle(bundle)
    records = bundle["catalogue"]["records"]
    entities = bundle["research_entities"]
    trs = entities["transcriptions"]
    core = [r for r in records if r["membership"] == "reported_core"]
    verified = {t["inscription_id"] for t in trs if t.get("status") == "verified"}
    missing_sequences = [r["id"] for r in core if r["id"] not in verified]
    missing_reviews = [r["id"] for r in core if not approved(bundle, "records", r["id"])]
    missing_objects = [r["id"] for r in core if not r.get("object_id")]
    missing_surfaces = [r["id"] for r in core if not r.get("surfaces")]
    unresolved = [e["id"] for e in bundle["external_crosswalk"]["entries"] if e["mapping_status"] not in {"verified", "excluded"}]
    open_gaps = [g["id"] for g in bundle["coverage"]["gaps"] if g["status"] == "open"]
    admission = admission_assessment(bundle)
    gates = {
        "structure": not errors,
        "nonempty_core": bool(core),
        "core_sequences": bool(core) and not missing_sequences,
        "independent_core_review": bool(core) and not missing_reviews,
        "object_identity": bool(core) and not missing_objects,
        "surface_inventory": bool(core) and not missing_surfaces,
        "external_crosswalk": not unresolved,
        "research_gaps_resolved": not open_gaps,
        "admission_evidence": admission["ready"],
        "exhaustiveness_audit": admission["ready"] and bundle["coverage"]["release_gates"].get("exhaustive_claim_allowed") is True,
    }
    return {
        "version": bundle["coverage"]["version"], "structure_valid": not errors,
        "scientific_1_0_ready": all(gates.values()), "gates": gates, "errors": errors,
        "counts": {
            "catalogue_records": len(records), "reported_core": len(core),
            "disputed_candidates": sum(r["membership"] == "disputed" for r in records),
            "sources_and_leads": len(bundle["sources"]["sources"]),
            "surfaces_described": len(bundle["surfaces"]["surfaces"]),
            "signs_registered": len(entities["signs"]),
            "transcriptions": len(trs), "verified_core_sequences": len(verified.intersection({r["id"] for r in core})),
            "independent_approvals": sum(r.get("independent") is True and r.get("status") == "approved" for r in entities["reviews"]),
            "external_entries": len(bundle["external_crosswalk"]["entries"]),
        },
        "review_evidence_sha256": evidence_digest(bundle),
        "admission": admission,
        "blockers": {"core_without_verified_sequence": missing_sequences,
                     "core_without_independent_review": missing_reviews,
                     "core_without_object_identity": missing_objects,
                     "core_without_surface_inventory": missing_surfaces,
                     "unverified_external_entries": unresolved, "open_gaps": open_gaps},
        "interpretation": "Passing software checks validates recorded structure, not archaeological truth, licence validity or completeness.",
    }
