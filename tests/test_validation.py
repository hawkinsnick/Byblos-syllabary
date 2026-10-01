import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = [json.loads((ROOT / "data" / p).read_text(encoding="utf-8"))
                     for p in ("catalogue.json", "sources.json", "coverage.json")]

    def test_seed_is_consistent(self):
        self.assertEqual(validator.validate(*self.data), [])

    def test_unknown_source_rejected(self):
        self.data[0]["records"][0]["evidence"][0]["source_id"] = "missing"
        self.assertTrue(validator.validate(*self.data))

    def test_duplicate_record_rejected(self):
        self.data[0]["records"].append(copy.deepcopy(self.data[0]["records"][0]))
        self.assertTrue(validator.validate(*self.data))

    def test_unsupported_transcription_rejected(self):
        self.data[0]["records"][0]["transcription"] = []
        self.assertTrue(validator.validate(*self.data))

    def test_false_exhaustive_claim_rejected(self):
        self.data[2]["release_gates"]["exhaustive_claim_allowed"] = True
        self.assertTrue(validator.validate(*self.data))

    def test_unearned_review_count_rejected(self):
        self.data[2]["release_gates"]["independent_reviews"] = 1
        self.assertTrue(validator.validate(*self.data))
