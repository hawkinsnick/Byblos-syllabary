"""Synthetic admission cases only; no fabricated entities enter real data."""
import copy
import unittest
from byblos.admission import admission_assessment, evidence_digest
from byblos.core import audit, validate_bundle


def synthetic_complete():
    ev = [{"source_id": "TEST-SOURCE", "locator": "SYNTHETIC TEST ONLY",
           "fields": ["edition_label", "material", "object_type", "membership", "label", "line_count", "direction"]}]
    def disposition(ident):
        return {"id": ident, "status": "collated", "rationale": "Synthetic fixture only", "evidence": ev}
    b = {
        "sources": {"sources": [{"id": "TEST-SOURCE", "citation": "Synthetic source, not historical data",
                                  "consultation": "selected_pages", "rights": {"scope": "Test fixture only"}}]},
        "catalogue": {"records": [{"id": "TEST-RECORD", "edition_label": "TEST", "material": "test",
                                   "object_type": "test", "membership": "reported_core", "evidence_level": "publication_checked",
                                   "primary_edition_lead": "TEST-SOURCE", "museum_id": None, "object_id": "TEST-OBJECT",
                                   "date_claims": [], "surfaces": ["TEST-SURFACE"], "transcription": "TEST-TR",
                                   "review_status": "reviewed", "evidence": ev}]},
        "surfaces": {"surfaces": [{"id": "TEST-SURFACE", "inscription_id": "TEST-RECORD", "label": "test",
                                    "line_count": 1, "direction": "rtl", "evidence": ev}]},
        "relations": {"relations": []},
        "bibliography": {"entries": [{"id": "TEST-BIB", "discovery_source": "TEST-SOURCE", "discovery_locator": "test"}]},
        "external_crosswalk": {"source_id": "TEST-SOURCE", "entries": []},
        "search_log": {"searches": []},
        "coverage": {"version": "TEST", "as_of": "2026-10-01", "gaps": [],
                     "count_claims": [{"id": "TEST-COUNT", "source_id": "TEST-SOURCE", "locator": "test", "unit": "test", "count": 1}],
                     "release_gates": {"exhaustive_claim_allowed": True, "verified_transcriptions": 1,
                                       "independent_reviews": 3, "rights_cleared_assets": 1},
                     "admission_audit": {"policy_version": 1, "cutoff_date": "2026-10-01",
                                         "scope_statement": "Synthetic test", "inclusion_criteria": "Test", "exclusion_criteria": "Test",
                                         "contributor_ids": ["test-author"], "evidence": ev,
                                         "source_dispositions": [disposition("TEST-SOURCE")],
                                         "bibliography_dispositions": [disposition("TEST-BIB")],
                                         "count_reconciliations": [disposition("TEST-COUNT")],
                                         "search_protocol": {"databases": ["test"], "queries": ["test"], "languages": ["test"],
                                                             "date_range": "test", "citation_chaining": "test",
                                                             "limitations": "test", "evidence": ev}}},
        "research_entities": {"objects": [{"id": "TEST-OBJECT", "evidence": ev}],
                              "editions": [{"id": "TEST-EDITION", "source_id": "TEST-SOURCE", "inscription_id": "TEST-RECORD",
                                            "collation_complete": True, "evidence": ev}],
                              "signs": [{"id": "TEST-SIGN", "edition_id": "TEST-EDITION", "edition_sign_label": "1", "evidence": ev}],
                              "assets": [{"id": "TEST-ASSET", "kind": "transcription", "source_id": "TEST-SOURCE",
                                          "rights": {"status": "original", "reference": "synthetic", "creator": "test-author",
                                                     "attribution": "Test only", "scope": "Test only"}}],
                              "transcriptions": [{"id": "TEST-TR", "inscription_id": "TEST-RECORD", "edition_id": "TEST-EDITION",
                                                  "asset_id": "TEST-ASSET", "status": "verified", "evidence": ev,
                                                  "method": {"origin": "independent_collation", "creator_ids": ["test-author"],
                                                             "source_version": "synthetic", "normalization_log": []},
                                                  "lines": [{"surface_id": "TEST-SURFACE", "line": 1, "direction": "rtl",
                                                             "tokens": [{"position": 1, "status": "observed", "sign_id": "TEST-SIGN", "evidence": ev}]}]}],
                              "reviews": []}}
    digest = evidence_digest(b)
    for i, (kind, ident) in enumerate([("records", "TEST-RECORD"), ("transcriptions", "TEST-TR"), ("admission", "scientific-1.0")]):
        b["research_entities"]["reviews"].append({"id": f"TEST-REVIEW-{i}", "scope": {"entity_type": kind, "id": ident},
                                                "reviewer": "Synthetic reviewer", "reviewer_id": "test-reviewer", "independent": True,
                                                "status": "approved", "reviewed_bundle_sha256": digest, "review_record": "TEST ONLY",
                                                "expertise": "Synthetic expertise", "reviewed_on": "2026-10-01", "evidence": ev})
    return b


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.b = synthetic_complete()
    def test_complete_synthetic_admission_can_pass(self):
        self.assertEqual(validate_bundle(self.b), [])
        self.assertTrue(audit(self.b)["scientific_1_0_ready"])
    def test_changed_evidence_invalidates_old_reviews(self):
        self.b["catalogue"]["records"][0]["material"] = "edited"
        self.assertTrue(validate_bundle(self.b))
        self.assertFalse(admission_assessment(self.b)["ready"])
    def test_approval_flags_do_not_change_evidence_hash(self):
        before = evidence_digest(self.b)
        self.b["coverage"]["release_gates"]["exhaustive_claim_allowed"] = False
        self.b["catalogue"]["records"][0]["review_status"] = "unreviewed"
        self.b["research_entities"]["transcriptions"][0]["status"] = "draft"
        self.assertEqual(before, evidence_digest(self.b))
        self.assertFalse(audit(self.b)["scientific_1_0_ready"])
    def test_review_cannot_substitute_for_missing_line(self):
        self.b["surfaces"]["surfaces"][0]["line_count"] = 2
        digest = evidence_digest(self.b)
        for r in self.b["research_entities"]["reviews"]:
            r["reviewed_bundle_sha256"] = digest
        self.assertIn("complete_sequence:TEST-RECORD", admission_assessment(self.b)["missing"])
        self.assertTrue(validate_bundle(self.b))
    def test_self_review_is_not_independent(self):
        self.b["research_entities"]["reviews"][0]["reviewer_id"] = "test-author"
        self.assertTrue(validate_bundle(self.b))
        self.assertFalse(audit(self.b)["scientific_1_0_ready"])
    def test_unreconciled_counts_block_admission(self):
        self.b["coverage"]["admission_audit"]["count_reconciliations"] = []
        self.assertIn("count_reconciliations", admission_assessment(self.b)["missing"])
    def test_abstract_is_not_edition_collation(self):
        self.b["sources"]["sources"][0]["consultation"] = "abstract_only"
        self.assertIn("edition_collation:TEST-RECORD", admission_assessment(self.b)["missing"])
    def test_duplicate_disposition_does_not_prove_coverage(self):
        rows = self.b["coverage"]["admission_audit"]["source_dispositions"]
        rows.append(copy.deepcopy(rows[0]))
        self.assertIn("source_inventory_dispositions", admission_assessment(self.b)["missing"])
    def test_missing_documented_review_blocks_valid_flags(self):
        del self.b["research_entities"]["reviews"][0]["review_record"]
        self.assertTrue(validate_bundle(self.b))
    def test_imported_sequence_needs_encoding_map_rights(self):
        self.b["research_entities"]["transcriptions"][0]["method"]["origin"] = "imported"
        digest = evidence_digest(self.b)
        for r in self.b["research_entities"]["reviews"]:
            r["reviewed_bundle_sha256"] = digest
        self.assertTrue(any("encoding map" in e for e in validate_bundle(self.b)))
