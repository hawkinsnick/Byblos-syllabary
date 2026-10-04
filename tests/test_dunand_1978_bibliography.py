import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location('bib',R/'scripts/audit_dunand_1978_bibliography.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class DunandBibliographyTests(unittest.TestCase):
 def test_conflict_remains_explicit(self):
  x=m.build();self.assertEqual(x,json.loads((R/'research/dunand-1978-bibliographic-conflict-audit.json').read_text(encoding='utf-8')));self.assertEqual(x['shared_page_span'],'52–58');self.assertEqual(x['union_page_span'],'51–59');self.assertEqual(x['disputed_boundary_pages'],[51,59]);self.assertFalse(x['pagination_resolved']);self.assertFalse(x['primary_article_inspected'])
 def test_inspection_promotion_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__'));p=root/'research/core-primary-access-routes.json';x=json.loads(p.read_text(encoding='utf-8'));x['routes'][1]['primary_pages_collated']=1;p.write_text(json.dumps(x),encoding='utf-8');
   with self.assertRaises(ValueError):m.build(root)
if __name__=='__main__':unittest.main()
