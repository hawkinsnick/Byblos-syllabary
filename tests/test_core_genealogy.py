import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('genealogy',R/'scripts/audit_core_genealogy.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class CoreGenealogyTests(unittest.TestCase):
 def test_ten_plus_four_labels_are_not_physical_count(self):
  x=m.build();self.assertEqual(x,json.loads((R/'research/core-publication-genealogy-audit.json').read_text(encoding='utf-8')));self.assertEqual(x['publication_label_counts'],{'Dunand 1945':10,'Dunand 1978':4});self.assertEqual(x['conventional_core_label_count'],14);self.assertIsNone(x['minimum_distinct_physical_monument_count']);self.assertIn(['BYB-H','BYB-J'],x['potential_coreference_groups']);self.assertEqual(x['verified_sequence_count'],0)
 def test_cohort_overlap_or_sequence_promotion_rejected(self):
  for target in ['overlap','promotion']:
   with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__'));p=root/('research/mnamon-corpus-genealogy.json' if target=='overlap' else 'research/core-object-reconciliation.json');x=json.loads(p.read_text(encoding='utf-8'))
    if target=='overlap':x['corpus_genealogy']['dunand_1978']['labels'][0]='a'
    else:x['objects'][0]['verified_sequence']=True
    p.write_text(json.dumps(x),encoding='utf-8')
    with self.assertRaises(ValueError):m.build(root)
