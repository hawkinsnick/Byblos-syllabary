"""Actual-source browser replay preserves qualified ordinal/type rows exactly."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('available_browser', ROOT/'scripts/build_corpus_browser.py')
browser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(browser)
class AvailableLayerReplay(unittest.TestCase):
    def test_actual_source_rows_are_lossless(self):
        data = browser.build()
        for path,key,count in [('research/stele-a-facsimile-ordinal-review.json','ordinals',123),('research/stele-a-type-table.json','rows',38)]:
            with self.subTest(path=path):
                source=json.loads((ROOT/path).read_text())[key]
                actual=[r['record'] for r in data['records'] if r['source']==path]
                self.assertEqual(len(actual),count)
                self.assertEqual(actual,source)
    def test_ordinal_display_does_not_admit_readings(self):
        for row in browser.load('research/stele-a-facsimile-ordinal-review.json'):
            self.assertIs(row['record']['verified_glyph'],False)
            self.assertIs(row['record']['analysis_eligible'],False)
            self.assertIsNone(row['record']['canonical_type_admitted'])
if __name__=='__main__':unittest.main()
