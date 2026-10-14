import json,tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from count_assignment_partition import ROOT,REGISTER,OUTPUT,build,validate
class Boundaries(unittest.TestCase):
 def test_native(self):self.assertEqual(validate()['drawing_partition'],[119,3,1])
 def reject(self,path,fn):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);checkpoint=json.loads((ROOT/REGISTER).read_text())
   for p in [REGISTER,OUTPUT]+list(checkpoint['inputs']):
    f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((ROOT/p).read_bytes())
   f=root/path;x=json.loads(f.read_text());fn(x);f.write_text(json.dumps(x))
   with self.assertRaises(ValueError):validate(root)
 def test_ancient_damage_not_certified(self):self.reject(REGISTER,lambda x:x.update(ancient_surviving_lost_count_certified=True))
 def test_erratum_not_adopted(self):self.reject(REGISTER,lambda x:x.update(candidate_32_to_92_correction_adopted=True))
 def test_duplicate_assignment_not_selected(self):self.reject('research/stele-a-facsimile-ordinal-review.json',lambda x:x['ordinals'][31]['printed_table_memberships'].pop())
 def test_gap_not_invented_as_type(self):self.reject('research/stele-a-facsimile-ordinal-review.json',lambda x:x['ordinals'][91].update(canonical_type_admitted='VIII'))
if __name__=='__main__':unittest.main()
