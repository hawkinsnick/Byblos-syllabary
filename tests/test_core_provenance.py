import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('provenance',R/'scripts/audit_core_provenance.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class CoreProvenanceTests(unittest.TestCase):
 def test_field_level_statuses_replay(self):
  x=m.build();self.assertEqual(x,json.loads((R/'research/core-field-provenance-audit.json').read_text(encoding='utf-8')))
  self.assertEqual(x['core_labels'],14);self.assertEqual(x['core_labels_with_survey_edition_locator'],14)
  self.assertEqual(x['core_labels_with_directly_inspected_primary_metadata'],1);self.assertEqual(x['core_labels_with_primary_corpus_edition_collation'],0)
  self.assertEqual(x['core_labels_with_verified_sign_sequence'],0);self.assertEqual(x['core_labels_with_museum_or_object_identity'],0)
  rows={r['record_id']:r for r in x['records']};self.assertEqual(rows['BYB-A']['directly_inspected_primary_metadata'][0]['source_id'],'dunand-1930')
 def test_primary_metadata_cannot_become_sequence_verification(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__'));p=root/'research/core-edition-locators.json';x=json.loads(p.read_text(encoding='utf-8'));x['entries'][0]['verified_sign_sequence']=True;p.write_text(json.dumps(x),encoding='utf-8')
   with self.assertRaises(ValueError):m.build(root)
