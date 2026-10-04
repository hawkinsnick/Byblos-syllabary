import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location("units",R/"scripts/audit_core_counting_units.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class CoreCountingUnitTests(unittest.TestCase):
 def test_denominators_remain_distinct(self):
  x=m.build();self.assertEqual(x,json.loads((R/"research/core-counting-unit-ledger.json").read_text()));self.assertEqual(x["denominators"],{"publication_labels":14,"publication_cohorts":2,"core_labels_with_line_surfaces":13,"reported_surfaces":18,"reported_line_targets":126,"column_only_core_labels":1,"BYB_G_reported_columns":6,"BYB_G_certainly_textual_columns":5,"verified_sign_sequences":0,"certified_distinct_physical_monuments":None})
 def test_surface_line_inflation_is_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/"repo";shutil.copytree(R,root,ignore=shutil.ignore_patterns(".git","__pycache__"));p=root/"data/surfaces.json";x=json.loads(p.read_text());x["surfaces"][0]["line_count"]+=1;p.write_text(json.dumps(x));
   with self.assertRaises(ValueError):m.build(root)
