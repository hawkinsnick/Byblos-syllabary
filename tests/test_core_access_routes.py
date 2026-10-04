import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location('routes',R/'scripts/audit_core_access_routes.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class CoreAccessRouteTests(unittest.TestCase):
 def test_exact_routes_cover_ten_plus_four(self):
  x=m.build();self.assertEqual(x,json.loads((R/'research/core-primary-access-route-audit.json').read_text()));self.assertEqual(x['edition_count'],2);self.assertEqual(x['core_label_count'],14);self.assertEqual(x['catalogue_record_count'],3);self.assertEqual(x['primary_pages_collated'],0);self.assertEqual(x['verified_sequences'],0);self.assertIsNone(x['certified_physical_monuments'])
 def test_false_content_inspection_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__'));p=root/'research/core-primary-access-routes.json';x=json.loads(p.read_text());x['routes'][0]['catalogues'][0]['content_inspected']=True;p.write_text(json.dumps(x));
   with self.assertRaises(ValueError):m.build(root)
