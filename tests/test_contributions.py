"""Synthetic submissions only; none are admitted to the historical corpus."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from datetime import date
from byblos.core import ROOT, load_bundle
from byblos.contributions import proposal_template, assess_proposal, stage_proposal, verify_staged_proposal, read_proposal


class ContributionTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle()
        self.proposal = proposal_template(self.bundle, ["BYB-A"])
        self.proposal.update(proposal_id="TEST-ONLY", submitted_on="2026-10-01",
                             contributor={"id": "synthetic-contributor", "name": "Synthetic test only"})
        self.proposal["changes"] = [{"record_id": "BYB-A", "field": "museum_id",
                                     "expected": {"present": True, "value": None}, "value": "SYNTHETIC-NOT-REAL",
                                     "evidence": [{"source_id": "dunand-1930", "locator": "SYNTHETIC TEST ONLY", "fields": ["museum_id"]}]}]
    def assert_invalid(self):
        self.assertFalse(assess_proposal(self.bundle, self.proposal)["valid_proposal"])
    def test_structured_submission_never_mutates_corpus(self):
        before = copy.deepcopy(self.bundle)
        result = assess_proposal(self.bundle, self.proposal)
        self.assertTrue(result["valid_proposal"])
        self.assertFalse(result["automatically_applied"])
        self.assertEqual(result["acceptance_status"], "awaiting_maintainer_and_scientific_review")
        self.assertEqual(self.bundle, before)
    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"submission.json";p.write_text('{"format":"one","format":"two"}')
            with self.assertRaises(ValueError):
                read_proposal(p)
    def test_empty_template_is_not_a_submission(self):
        self.assertFalse(assess_proposal(self.bundle, proposal_template(self.bundle))["valid_proposal"])
    def test_unknown_template_record_rejected(self):
        with self.assertRaises(ValueError):
            proposal_template(self.bundle, ["MISSING"])
    def test_stale_submission_is_rejected(self):
        self.bundle["search_log"]["annotation"] = "new evidence"
        self.assert_invalid()
    def test_expected_null_is_not_missing(self):
        self.proposal["changes"][0]["expected"] = {"present": False}
        self.assert_invalid()
    def test_duplicate_conflicting_changes_rejected(self):
        self.proposal["changes"].append(copy.deepcopy(self.proposal["changes"][0]))
        self.proposal["changes"][1]["value"] = "different"
        self.assert_invalid()
    def test_approval_and_permission_cannot_be_submitted_as_changes(self):
        for field in ["review_status", "transcription", "evidence_level", "rights", "exhaustive_claim_allowed"]:
            self.proposal["changes"][0]["field"] = field
            self.assert_invalid()
    def test_unconsulted_source_cannot_support_fact(self):
        self.proposal["changes"][0]["evidence"][0]["source_id"] = "dunand-1945"
        self.assert_invalid()
    def test_evidence_must_scope_the_changed_field(self):
        self.proposal["changes"][0]["evidence"][0]["fields"] = ["material"]
        self.assert_invalid()
    def test_future_or_invalid_submission_date(self):
        for value in ["2099-01-01", "not-a-date", None]:
            self.proposal["submitted_on"] = value
            self.assert_invalid()
    def test_submission_can_follow_the_frozen_snapshot_date(self):
        class LaterDate(date):
            @classmethod
            def today(cls):
                return cls(2026, 10, 3)
        self.proposal["submitted_on"] = "2026-10-02"
        with patch("byblos.contributions.date", LaterDate):
            self.assertTrue(assess_proposal(self.bundle, self.proposal)["valid_proposal"])
    def test_measurements_reject_boolean_and_nonfinite_values(self):
        change = self.proposal["changes"][0]
        change.update(field="dimensions_mm", expected={"present": True, "value": self.bundle["catalogue"]["records"][0]["dimensions_mm"]})
        change["evidence"][0]["fields"] = ["dimensions_mm"]
        for value in [True, float("nan"), float("inf"), -2, 0, 10**400]:
            change["value"] = {"height": value}
            self.assert_invalid()
    def test_source_lead_can_be_submitted_without_fact_changes(self):
        self.proposal["changes"] = []
        self.proposal["new_sources"] = [{"id": "TEST-SOURCE", "citation": "Synthetic source, not a real publication",
                                         "url": None, "doi": None, "consultation": "not_consulted",
                                         "rights": {"status": "not_assessed", "scope": "Source lead only"}}]
        self.assertTrue(assess_proposal(self.bundle, self.proposal)["valid_proposal"])
        self.proposal["new_sources"][0]["rights"]["status"] = "licensed"
        self.assert_invalid()
    def test_invalid_source_types_fail_without_crashing(self):
        self.proposal["new_sources"] = [{"id": "TEST-SOURCE", "citation": "test", "consultation": [],
                                         "url": "javascript:alert(1)", "rights": {"status": "not_assessed", "scope": "test"}}]
        self.assert_invalid()
    def test_scope_mismatch_rejected(self):
        self.proposal["changes"][0]["record_id"] = "BYB-B"
        self.assert_invalid()
    def test_staging_roundtrip_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as d:
            stage_proposal(self.bundle, self.proposal, d)
            self.assertTrue(verify_staged_proposal(self.bundle, d))
            p = Path(d)/"assessment.json"
            p.write_text(p.read_text().replace('"automatically_applied": false', '"automatically_applied": true'))
            with self.assertRaises(ValueError):
                verify_staged_proposal(self.bundle, d)
    def test_staging_rejects_extra_files_and_preserves_nonempty_directory(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"existing";p.write_text("preserve")
            with self.assertRaises(ValueError):
                stage_proposal(self.bundle, self.proposal, d)
            self.assertEqual(p.read_text(), "preserve")
            p.unlink()
            stage_proposal(self.bundle, self.proposal, d)
            p.write_text("extra")
            with self.assertRaises(ValueError):
                verify_staged_proposal(self.bundle, d)
    def test_staged_submission_becomes_stale_when_evidence_changes(self):
        with tempfile.TemporaryDirectory() as d:
            stage_proposal(self.bundle, self.proposal, d)
            self.bundle["search_log"]["annotation"] = "edited"
            with self.assertRaises(ValueError):
                verify_staged_proposal(self.bundle, d)
    def test_cli_stage_check_verify_do_not_apply(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/"submission.json";source.write_text(json.dumps(self.proposal))
            output=Path(d)/"pending"
            for args in [["check-proposal",str(source)], ["stage-proposal",str(source),"--output",str(output)], ["verify-proposal",str(output)]]:
                p=subprocess.run([sys.executable,"-m","byblos",*args],cwd=ROOT,capture_output=True,text=True)
                self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            self.assertIsNone(load_bundle()["catalogue"]["records"][0]["museum_id"])
