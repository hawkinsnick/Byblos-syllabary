"""End-to-end export preservation and boundary-sensitive sequence analysis."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from byblos.core import ROOT, load_bundle, validate_bundle
from byblos.export import export_texts, sequence_statistics, verify_export, write_export

class ExportTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle()
    def test_reproducible_export_and_null_preservation(self):
        a, b = export_texts(self.bundle), export_texts(copy.deepcopy(self.bundle))
        self.assertEqual(a, b)
        records = [json.loads(line) for line in a["catalogue.jsonl"].splitlines()]
        self.assertTrue(all(r["transcription"] is None for r in records))
        self.assertEqual(len(records), 38)
    def test_export_roundtrip_and_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "snapshot"
            write_export(self.bundle, out)
            self.assertTrue(verify_export(out))
            (out / "catalogue.csv").write_text("changed", encoding="utf-8")
            with self.assertRaises(ValueError):
                verify_export(out)
    def test_extra_file_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            write_export(self.bundle, d)
            (Path(d) / "untracked.txt").write_text("not in manifest")
            with self.assertRaises(ValueError):
                verify_export(d)
    def test_nonempty_destination_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "existing"; p.write_text("preserve")
            with self.assertRaises(ValueError):
                write_export(self.bundle, d)
            self.assertEqual(p.read_text(), "preserve")
    def test_invalid_corpus_cannot_be_exported(self):
        self.bundle["catalogue"]["records"][0]["evidence"] = []
        with self.assertRaises(ValueError):
            export_texts(self.bundle)
    def test_no_statistics_invented_for_empty_sequences(self):
        result = sequence_statistics(self.bundle)
        self.assertEqual(result["status"], "no_eligible_sequences")
        self.assertEqual(result["ngrams"], [])
    def test_cli_scientific_release_gate_fails(self):
        p = subprocess.run([sys.executable, "-m", "byblos", "audit", "--require-1-0"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertFalse(json.loads(p.stdout)["scientific_1_0_ready"])
    def test_cli_malformed_input_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, "-m", "byblos", "--root", d, "validate"],
                               cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(p.returncode, 1)
    def test_ngram_boundaries_with_explicit_synthetic_fixture(self):
        # Purely synthetic test data; never exported into the actual corpus.
        b = self.bundle
        evidence = [{"source_id":"vita-zamora-2018","locator":"SYNTHETIC TEST ONLY","fields":["test"]}]
        b["research_entities"]["editions"] = [{
            "id":"TEST-EDITION", "source_id":"vita-zamora-2018",
            "inscription_id":"BYB-C","evidence":evidence}]
        b["research_entities"]["signs"] = [
            {"id":"TEST-A","edition_id":"TEST-EDITION","edition_sign_label":"A","evidence":evidence},
            {"id":"TEST-B","edition_id":"TEST-EDITION","edition_sign_label":"B","evidence":evidence}]
        b["research_entities"]["assets"] = [{
            "id":"TEST-ASSET","kind":"transcription","source_id":"vita-zamora-2018",
            "rights":{"status":"original","reference":"synthetic fixture","creator":"test",
                      "attribution":"synthetic test","scope":"test data only"}}]
        b["coverage"]["release_gates"]["rights_cleared_assets"] = 1
        def tokens(items):
            return [{"position":i,"sign_id":sign,"status":"observed" if sign else "gap",
                     "evidence":evidence} for i,sign in enumerate(items,1)]
        b["research_entities"]["transcriptions"] = [{
            "id":"TEST-TR","inscription_id":"BYB-C","edition_id":"TEST-EDITION",
            "asset_id":"TEST-ASSET","status":"draft","evidence":evidence,
            "lines":[{"surface_id":"BYB-C-A","line":1,"direction":"rtl",
                      "tokens":tokens(["TEST-A","TEST-B",None,"TEST-B"])},
                     {"surface_id":"BYB-C-A","line":2,"direction":"rtl",
                      "tokens":tokens(["TEST-A"])}]}]
        self.assertEqual(validate_bundle(b), [])
        self.assertEqual(sequence_statistics(b)["ngrams"], [])
        self.assertEqual(sequence_statistics(b,include_drafts=True)["ngrams"],
                         [{"sign_ids":["TEST-A","TEST-B"],"count":1}])
