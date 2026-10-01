import json
from pathlib import Path
import shutil
import tempfile
import unittest
from byblos.core import ROOT, load_bundle
from byblos.export import write_export, verify_export
from byblos.jsonio import loads
from byblos.release import release_check


class StrictJSONTests(unittest.TestCase):
    def test_ambiguous_and_nonfinite_values_fail(self):
        for text in ('{"a":1,"a":2}', '{"nested":{"x":1,"x":2}}',
                     '[NaN]', '[Infinity]', '[-Infinity]', '[1e999]'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                loads(text)
        self.assertEqual({'x': [None, 2, 1.5]}, loads('{"x":[null,2,1.5]}'))

    def test_corpus_ingestion_uses_strict_reader(self):
        with tempfile.TemporaryDirectory() as d:
            shutil.copytree(ROOT / 'data', Path(d) / 'data')
            (Path(d) / 'data/catalogue.json').write_text('{"records":[],"records":[]}')
            with self.assertRaises(ValueError):
                load_bundle(d)

    def test_export_symlink_rejected_even_with_matching_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'snapshot'
            write_export(load_bundle(), out)
            target = Path(d) / 'external.csv'
            shutil.move(str(out / 'catalogue.csv'), target)
            try:
                (out / 'catalogue.csv').symlink_to(target)
            except OSError:
                self.skipTest('Host does not permit symlink creation')
            with self.assertRaises(ValueError):
                verify_export(out)


class ReleaseTests(unittest.TestCase):
    def test_current_repository_consistent_without_scientific_approval(self):
        report = release_check()
        self.assertTrue(report['repository_consistent'], report)
        self.assertFalse(report['scientific_1_0_ready'])

    def test_metadata_drift_and_other_valid_snapshot_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ('data', 'byblos', 'docs', 'exports'):
                shutil.copytree(ROOT / name, root / name)
            for name in ('README.md', 'CITATION.cff'):
                shutil.copyfile(ROOT / name, root / name)
            (root / 'CITATION.cff').write_text('version: "0.0.0"\n')
            report = release_check(root)
            self.assertFalse(report['checks']['citation_version'])
            self.assertFalse(report['repository_consistent'])
            bundle = load_bundle(root)
            bundle['catalogue']['records'][0]['open_tasks'].append('SYNTHETIC TEST ONLY')
            shutil.rmtree(root / 'exports')
            write_export(bundle, root / 'exports')
            report = release_check(root)
            self.assertTrue(report['checks']['snapshot_integrity'])
            self.assertFalse(report['checks']['snapshot_matches_repository'])
