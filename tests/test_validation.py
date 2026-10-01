"""Reject mutations that would inflate evidence or corrupt provenance."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from byblos.core import audit, load_bundle, validate_bundle

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = load_bundle()
    def rejected(self):
        self.assertTrue(validate_bundle(self.data))
    def test_seed_consistent_but_not_release_ready(self):
        self.assertEqual(validate_bundle(self.data), [])
        self.assertFalse(audit(self.data)["scientific_1_0_ready"])
    def test_unknown_source_rejected(self):
        self.data["catalogue"]["records"][0]["evidence"][0]["source_id"] = "missing"
        self.rejected()
    def test_duplicate_record_rejected(self):
        self.data["catalogue"]["records"].append(copy.deepcopy(self.data["catalogue"]["records"][0]))
        self.rejected()
    def test_unsupported_transcription_rejected(self):
        self.data["catalogue"]["records"][0]["transcription"] = []
        self.rejected()
    def test_false_exhaustive_claim_rejected(self):
        self.data["coverage"]["release_gates"]["exhaustive_claim_allowed"] = True
        self.rejected()
    def test_unearned_review_count_rejected(self):
        self.data["coverage"]["release_gates"]["independent_reviews"] = 1
        self.rejected()
    def test_unconsulted_source_cannot_support_assertion(self):
        self.data["catalogue"]["records"][0]["evidence"][0]["source_id"] = "dunand-1945"
        self.rejected()
    def test_unattributed_new_metadata_rejected(self):
        self.data["catalogue"]["records"][1]["dimensions_mm"] = {"height": 200}
        self.rejected()
    def test_surface_wrong_parent_rejected(self):
        self.data["surfaces"]["surfaces"][0]["inscription_id"] = "BYB-A"
        self.rejected()
    def test_duplicate_surface_rejected(self):
        self.data["surfaces"]["surfaces"].append(copy.deepcopy(self.data["surfaces"]["surfaces"][0]))
        self.rejected()
    def test_bool_not_valid_count(self):
        self.data["coverage"]["count_claims"][0]["count"] = True
        self.rejected()
    def test_false_reviewed_flag_rejected(self):
        self.data["catalogue"]["records"][0]["review_status"] = "reviewed"
        self.rejected()
    def test_resolved_gap_needs_evidence(self):
        self.data["coverage"]["gaps"][0]["status"] = "resolved"
        self.rejected()
    def test_fake_crosswalk_target_rejected(self):
        self.data["external_crosswalk"]["entries"][0]["proposed_project_record"] = "unknown"
        self.rejected()
    def test_font_license_is_not_transcription_permission(self):
        self.data["research_entities"]["assets"].append({
            "id":"ASSET-TEST", "kind":"transcription", "source_id":"ocbi-current",
            "rights":{"status":"not_assessed", "license":"OFL-1.1"}})
        self.rejected()
    def test_sound_values_not_canonical_sign_facts(self):
        self.data["research_entities"]["signs"].append({
            "id":"SIGN-TEST","edition_id":"unknown","edition_sign_label":"1",
            "sound_value":"ka","evidence":[]})
        self.rejected()
    def test_missing_required_unknown_field_rejected(self):
        del self.data["catalogue"]["records"][0]["museum_id"]
        self.rejected()
    def test_nonobject_row_rejected(self):
        self.data["catalogue"]["records"].append("bad")
        self.rejected()
