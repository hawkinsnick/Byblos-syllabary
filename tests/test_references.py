import copy
import unittest
from byblos.core import load_bundle
from byblos.references import reference_workflow, pilot_packet


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle()

    def test_unknown_rights_remain_unknown_and_scopes_stay_separate(self):
        report = reference_workflow(self.bundle)
        self.assertEqual(len(self.bundle['sources']['sources']), len(report['sources']))
        rows = {r['source_id']: r for r in report['sources']}
        self.assertEqual('not_assessed', rows['dunand-1945']['recorded_rights']['status'])
        self.assertEqual('not_determined_by_this_report', rows['dunand-1945']['copyright_determination'])
        photo = rows['commons-beirut-photo']['assets'][0]
        self.assertTrue(photo['declared_rights_supported'])
        self.assertEqual('external_reference_only', photo['delivery'])
        self.assertEqual('references_and_original_metadata_only', rows['commons-beirut-photo']['publication_plan'])
        self.assertEqual([], rows['dunand-1945']['assets'])

    def test_pilot_inventory_is_reported_without_sequence_admission(self):
        packet = pilot_packet(self.bundle)
        self.assertEqual('BYB-A', packet['record_id'])
        self.assertEqual('pending', packet['task']['response']['status'])
        self.assertEqual('reported_inventory_requires_completeness_check', packet['task']['surface_inventory_status'])
        self.assertEqual(10, len(packet['task']['line_targets']))
        self.assertTrue(all(t['inventory_evidence'][0]['source_id']=='dunand-1930' for t in packet['task']['line_targets']))
        self.assertEqual({'dunand-1945','dunand-1930','mnamon-merlo'}, {s['id'] for s in packet['sources']})
        self.assertIsNone(packet['task']['record']['transcription'])

    def test_surface_citations_and_targets_retained_for_other_pilot(self):
        packet = pilot_packet(self.bundle, 'BYB-C')
        self.assertEqual(15, len(packet['task']['line_targets']))
        self.assertIn('vita-zamora-2018', {s['id'] for s in packet['sources']})

    def test_deterministic_and_detached(self):
        before = copy.deepcopy(self.bundle)
        for function in (reference_workflow, pilot_packet):
            a = function(self.bundle)
            self.assertEqual(a, function(self.bundle))
            self.assertEqual(before, self.bundle)
        report = reference_workflow(self.bundle)
        report['sources'][0]['recorded_rights']['status'] = 'SYNTHETIC-MUTATION'
        self.assertEqual(before, self.bundle)

    def test_invalid_bundle_and_unknown_record_fail(self):
        with self.assertRaises(ValueError):
            pilot_packet(self.bundle, 'unknown')
        self.bundle['catalogue']['records'][0]['evidence'] = []
        for function in (reference_workflow, pilot_packet):
            with self.assertRaises(ValueError):
                function(self.bundle)
