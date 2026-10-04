import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('locators',R/'scripts/check_edition_locators.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class EditionLocatorTests(unittest.TestCase):
 def test_checkout_line_endings_do_not_change_source_audit(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
   for name in ['research/core-edition-locators.json','data/catalogue.json','data/surfaces.json']:
    p=root/name;p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))
   self.assertEqual(m.check(root),m.check())
 def test_native_metadata_replay_and_no_scientific_promotion(self):
  x=m.check();self.assertEqual(x,json.loads((R/'research/edition-locator-audit.json').read_text(encoding="utf-8")))
  self.assertEqual(x['core_labels_with_edition_locators'],14);self.assertEqual(x['core_labels_with_native_line_surfaces'],13)
  self.assertEqual(x['native_surfaces'],18);self.assertFalse(x['scientific_completeness_established'])
  self.assertEqual(x['column_layouts_kept_separate'],['BYB-G'])
 def test_conditional_direction_and_source_typos_remain_explicit(self):
  x=json.loads((R/'research/core-edition-locators.json').read_text(encoding="utf-8"));e={r['record_id']:r for r in x['entries']}
  self.assertEqual(e['BYB-F']['direction_claim']['faces']['B'],'left_to_right')
  self.assertEqual(e['BYB-M']['direction_claim']['qualification'],'conditional_on_sign_orientation')
  self.assertTrue(e['BYB-J']['source_anomalies']);self.assertEqual(e['BYB-G']['layout']['reported_columns'],6)
 def test_duplicate_identity_wrong_surface_count_and_column_conversion_rejected(self):
  for action in ['duplicate','surface_count','columns','promotion']:
   with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
    p=root/('data/surfaces.json' if action=='surface_count' else 'research/core-edition-locators.json');x=json.loads(p.read_text(encoding="utf-8"))
    if action=='duplicate':x['entries'].append(x['entries'][0])
    elif action=='surface_count':x['surfaces'][0]['line_count']+=1
    elif action=='columns':next(e for e in x['entries'] if e['record_id']=='BYB-G')['layout']['reported_lines']=6
    else:x['entries'][0]['verified_sign_sequence']=True
    p.write_text(json.dumps(x),encoding="utf-8")
    with self.assertRaises(ValueError):m.check(root)
