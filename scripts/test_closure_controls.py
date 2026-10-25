"""Regression checks for scoped exclusions, null conflicts and researcher queries."""
import csv,io,json,shutil,tempfile,unittest
from pathlib import Path
import closure_controls as m
from evidence_query import Evidence

class Controls(unittest.TestCase):
    def setUp(self):self.result=m.build();self.e=Evidence()
    def linked(self,identity,collection):
        return [x['native_record'] for x in self.e.dossier(identity,collection)['explicitly_linked_records'] if x['collection']=='closure-controls']
    def test_actual_researcher_queries_enforce_the_native_qualification(self):
        k=self.result['kind']
        if k=='linear-a-reference-gaps':
            self.assertEqual(self.result['counts'],{'gap_records':23,'absent':19,'literal_missing':4,'admitted_exact_targets':0})
            for row in self.result['records']:
                linked=self.linked(row['id'],'source-documents');self.assertEqual(len(linked),1)
                self.assertFalse(linked[0]['admitted_exact_edition_target']);self.assertIsNone(linked[0]['resolved_edition_url'])
        elif k=='cretan-hieroglyphic-material-conflicts':
            self.assertEqual(len(self.result['records']),2)
            for identity in ['CHIC-202','CHIC-252']:
                rows=self.linked(identity,'catalogue-dossiers');self.assertEqual(len(rows),1)
                self.assertEqual({a['value'] for a in rows[0]['material_assertions']},{'Ivoire','Animal bone'})
                self.assertIsNone(rows[0]['resolved_material']);self.assertFalse(rows[0]['material_adjudicated'])
        else:
            rows=self.linked('BYB-A','catalogue');self.assertEqual(len(rows),123)
            by={r['source_numbered_position']:r for r in rows}
            self.assertEqual(by[32]['printed_type_assertions'],['VIII','XIX'])
            for n in [14,27,32,34,40,41,42,92,95]:
                self.assertFalse(by[n]['source_table_lookup_admitted']);self.assertIsNone(by[n]['unambiguous_printed_type'])
                self.assertFalse(by[n]['erratum_adopted'])
            self.assertEqual(sum(r['source_table_lookup_admitted'] for r in rows),114)
            self.assertEqual(by[1]['unambiguous_printed_type'],'I')
            self.assertTrue(all(not r['canonical_sign_identity_admitted'] for r in rows))
    def test_controls_are_source_pinned_and_do_not_change_literals(self):
        self.assertFalse(self.result['source_literals_changed']);self.assertFalse(self.result['scientific_approval_granted'])
        for pin in self.result['inputs']:self.assertEqual(m.sha((m.ROOT/pin['path']).read_bytes()),pin['sha256'])
    def test_inconsistent_source_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for pin in self.result['inputs']:
                p=root/pin['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(m.ROOT/pin['path'],p)
            k=self.result['kind']
            if k=='linear-a-reference-gaps':
                p=root/'research/edition-concordance.csv';rows=list(csv.DictReader(io.StringIO(p.read_text())))
                next(r for r in rows if r['reference_gap'])['gorila_source_url']='https://example.invalid/guessed'
                out=io.StringIO();w=csv.DictWriter(out,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows);p.write_text(out.getvalue())
            elif k=='cretan-hieroglyphic-material-conflicts':
                p=root/'research/source-reconciliation.json';v=json.loads(p.read_text());v['comparisons'][0]['assertions'][0]['locator']='';p.write_text(json.dumps(v))
            else:
                p=root/'research/stele-a-type-table.json';v=json.loads(p.read_text());v['rows'][0]['source_numbered_positions'].append(999);p.write_text(json.dumps(v))
            with self.assertRaises(ValueError):m.build(root)
if __name__=='__main__':unittest.main()
