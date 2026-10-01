import copy
import unittest
from byblos.core import load_bundle
from byblos.evidence import evidence_ledger, acquisition_queue


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle()

    def test_unknown_and_absent_are_distinct_and_no_reviews_invented(self):
        ledger = evidence_ledger(self.bundle)
        self.assertEqual(39, len(ledger['records']))
        record = next(r for r in ledger['records'] if r['record_id'] == 'BYB-A')
        fields = {c['field']: c for c in record['claims']}
        self.assertEqual('unknown', fields['museum_id']['status'])
        self.assertEqual('not_recorded', fields['display_name']['status'])
        self.assertFalse(any(r['current_independent_record_approval'] for r in ledger['records']))
        self.assertEqual(390, sum(ledger['field_status_counts'].values()))

    def test_citations_preserve_exact_binding_and_pointer(self):
        for record in evidence_ledger(self.bundle)['records']:
            for claim in record['claims']:
                if claim['status'] == 'asserted':
                    self.assertTrue(claim['citations'])
                for citation in claim['citations']:
                    value = self.bundle
                    for part in citation['evidence_path'].split('/')[1:]:
                        value = value[int(part)] if isinstance(value, list) else value[part]
                    self.assertIn(claim['field'], value['fields'])
                    self.assertEqual(citation['locator'], value['locator'])
                    self.assertEqual(citation['source_id'], value['source_id'])

    def test_source_repeats_do_not_inflate_distinct_count(self):
        record = self.bundle['catalogue']['records'][0]
        record['evidence'].append(copy.deepcopy(record['evidence'][0]))
        row = next(r for r in evidence_ledger(self.bundle)['records'] if r['record_id'] == record['id'])
        claim = next(c for c in row['claims'] if c['field'] == 'membership')
        self.assertEqual(2, len(claim['citations']))
        self.assertEqual(1, claim['distinct_cited_sources'])

    def test_acquisition_queue_order_and_read_only(self):
        before = copy.deepcopy(self.bundle)
        queue = acquisition_queue(self.bundle)
        self.assertEqual(queue['source_tasks'], sorted(queue['source_tasks'], key=lambda r: (-r['linked_record_count'], r['source_id'])))
        original = next(r for r in queue['source_tasks'] if r['source_id'] == 'dunand-1945')
        expected = {r['id'] for r in self.bundle['catalogue']['records']
                    if r['primary_edition_lead'] == 'dunand-1945'}
        self.assertEqual(expected, set(original['linked_record_ids']))
        self.assertEqual(len(set(original['linked_record_ids'])), original['linked_record_count'])
        self.assertTrue(queue['unexamined_bibliography_leads'])
        self.assertEqual(before, self.bundle)
        ledger = evidence_ledger(self.bundle)
        ledger['records'][0]['claims'][0]['value'] = 'SYNTHETIC MUTATION'
        self.assertEqual(before, self.bundle)

    def test_invalid_data_rejected(self):
        self.bundle['catalogue']['records'][0]['evidence'] = []
        for function in (evidence_ledger, acquisition_queue):
            with self.assertRaises(ValueError):
                function(self.bundle)
