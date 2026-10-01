"""Review preparation and lossless snapshot comparison, without changing evidence."""
import copy
from .admission import evidence_digest
from .core import audit


def review_packet(bundle):
    report = audit(bundle)
    if not report["structure_valid"]:
        raise ValueError("Cannot prepare review packet from invalid corpus")
    surfaces = {s["id"]: s for s in bundle["surfaces"]["surfaces"]}
    sources = {s["id"]: s for s in bundle["sources"]["sources"]}
    tasks = []
    for row in sorted(bundle["catalogue"]["records"], key=lambda r: r["id"]):
        sid_list = row.get("surfaces")
        targets = []
        for sid in sid_list or []:
            surface = surfaces[sid]
            targets += [{"surface_id": sid, "line": n, "reported_direction": surface["direction"],
                         "inventory_evidence": copy.deepcopy(surface["evidence"])}
                        for n in range(1, surface["line_count"] + 1)]
        tasks.append({
            "record_id": row["id"], "membership": row["membership"],
            "record": copy.deepcopy(row),
            "primary_edition_lead": copy.deepcopy(sources.get(row.get("primary_edition_lead"))),
            "surface_inventory_status": "reported_inventory_requires_completeness_check" if sid_list else "not_established",
            "line_targets": targets,
            "requested_checks": ["object_identity", "membership_and_alternatives", "source_and_locator",
                                 "surface_inventory", "directions_and_damage", "edition_sign_labels",
                                 "transcription_and_encoding", "attribution_and_reuse_terms"],
            "response": {"status": "pending", "reviewer_id": None, "expertise": None,
                         "independence_statement": None, "reviewed_on": None,
                         "findings": [], "decision": None, "review_record": None},
        })
    return {
        "format": "byblos-review-packet-v1", "version": report["version"],
        "as_of": bundle["coverage"]["as_of"], "reviewed_bundle_sha256": evidence_digest(bundle),
        "scientific_1_0_ready": report["scientific_1_0_ready"],
        "purpose": "Review task inventory; pending responses are not approvals or corpus transcriptions.",
        "limitations": ["Reported line targets are not independent surface verification.",
                        "An empty line-target list means unknown inventory, not zero lines.",
                        "This packet is never automatically imported as evidence or approval."],
        "tasks": tasks, "gaps": copy.deepcopy(bundle["coverage"]["gaps"]),
        "crosswalk": copy.deepcopy(bundle["external_crosswalk"]),
        "sources": copy.deepcopy(bundle["sources"]["sources"]),
        "assets": copy.deepcopy(bundle["research_entities"]["assets"]),
        "admission_requirements": report["admission"],
    }


def compare_snapshots(before, after):
    """JSON-pointer changes; preserve missing versus null and list ordering.

    ID-bearing lists match by ID rather than positional coincidence. An @order
    entry separately records ordering changes; no sign equivalences are inferred.
    """
    for bundle in (before, after):
        if not audit(bundle)["structure_valid"]:
            raise ValueError("Cannot compare invalid corpus snapshots")
    changes = []
    missing = object()
    def pointer(part):
        return str(part).replace("~", "~0").replace("/", "~1")
    def state(value):
        return {"present": False} if value is missing else {"present": True, "value": copy.deepcopy(value)}
    def emit(path, a, b):
        changes.append({"path": path or "/", "before": state(a), "after": state(b)})
    def id_list(value):
        return isinstance(value, list) and all(isinstance(r, dict) and isinstance(r.get("id"), str) for r in value) and len({r["id"] for r in value}) == len(value)
    def walk(a, b, path):
        if a is missing or b is missing:
            emit(path, a, b)
        elif type(a) is not type(b):
            emit(path, a, b)
        elif isinstance(a, dict):
            for key in sorted(set(a) | set(b)):
                walk(a.get(key, missing), b.get(key, missing), path + "/" + pointer(key))
        elif isinstance(a, list):
            if id_list(a) and id_list(b):
                ai, bi = {r["id"]: r for r in a}, {r["id"]: r for r in b}
                for key in sorted(set(ai) | set(bi)):
                    walk(ai.get(key, missing), bi.get(key, missing), path + "/" + pointer(key))
                if [r["id"] for r in a] != [r["id"] for r in b]:
                    emit(path + "/@order", [r["id"] for r in a], [r["id"] for r in b])
            else:
                for n in range(max(len(a), len(b))):
                    walk(a[n] if n < len(a) else missing, b[n] if n < len(b) else missing, path + "/" + str(n))
        elif a != b:
            emit(path, a, b)
    walk(before, after, "")
    old_digest, new_digest = evidence_digest(before), evidence_digest(after)
    return {"format": "byblos-snapshot-diff-v1", "before_version": before["coverage"]["version"],
            "after_version": after["coverage"]["version"], "before_evidence_sha256": old_digest,
            "after_evidence_sha256": new_digest, "evidence_changed": old_digest != new_digest,
            "change_count": len(changes), "changes": changes,
            "interpretation": "Recorded data changes, not automatic corrections, sign alignments or scientific judgments."}
