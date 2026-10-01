import copy
import unittest
from byblos.core import load_bundle
from byblos.provenance import provenance_report


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle()

    def test_all_references_resolve_and_paths_are_exact(self):
        report = provenance_report(self.bundle)
        self.assertEqual([], report['unresolved_references'])
        for row in report['sources']:
            for use in row['uses']:
                value = self.bundle
                for part in use['path'].split('/')[1:]:
                    part = part.replace('~1', '/').replace('~0', '~')
                    value = value[int(part)] if isinstance(value, list) else value[part]
                self.assertEqual(row['source_id'], value)

    def test_leads_are_separate_from_claims(self):
        report = provenance_report(self.bundle, 'dunand-1945')
        self.assertEqual(1, len(report['sources']))
        roles = report['sources'][0]['role_counts']
        self.assertGreater(roles['primary_edition_lead'], 0)
        self.assertEqual('not_consulted', report['sources'][0]['consultation'])
        claims = provenance_report(self.bundle, 'mnamon-merlo')['sources'][0]
        self.assertGreater(claims['role_counts']['field_evidence'], 0)
        self.assertTrue(any(u['fields'] and u['locator'] for u in claims['uses']))

    def test_owner_namespace_and_nested_evidence(self):
        report = provenance_report(self.bundle)
        owners = [u['owner'] for row in report['sources'] for u in row['uses']]
        self.assertIn('/bibliography/entries:dunand-1945', owners)
        self.assertIn('/catalogue/records:BYB-A', owners)
        uses = [u for row in report['sources'] for u in row['uses']]
        self.assertTrue(any('/direction_claims/' in u['path'] for u in uses))

    def test_unknown_source_and_invalid_bundle_rejected(self):
        with self.assertRaises(ValueError):
            provenance_report(self.bundle, 'invented')
        bad = copy.deepcopy(self.bundle)
        bad['catalogue']['records'][0]['membership'] = 'invented'
        with self.assertRaises(ValueError):
            provenance_report(bad)

    def test_deterministic_and_read_only(self):
        before = copy.deepcopy(self.bundle)
        self.assertEqual(provenance_report(self.bundle), provenance_report(self.bundle))
        self.assertEqual(before, self.bundle)
