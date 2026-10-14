"""Partition source-drawing ordinals; never equate drawing categories with ancient damage."""
import argparse,collections,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTER='research/count-assignment-checkpoint-2026-10-14.json'
OUTPUT='research/count-assignment-partition.json'
PIN='bc23036f92de0a0e413701f1eea9c2b56716ac5a57864f18fe23046e2ec1ccd3'
def load(root,p):return json.loads((root/p).read_text())
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build(root=ROOT):
 checkpoint=load(root,REGISTER)
 if digest(checkpoint)!=PIN:raise ValueError('source checkpoint or scientific boundary changed')
 for p,h in checkpoint['inputs'].items():
  if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h:raise ValueError('frozen source review changed: '+p)
 review=load(root,'research/stele-a-facsimile-ordinal-review.json');rows=review['ordinals']
 if [r['source_ordinal'] for r in rows]!=list(range(1,124)):raise ValueError('source ordinal population drift')
 form={'OUTLINED_DRAWN_FORM_PRESENT','DRAWN_FORM_PRESENT','DOTTED_OR_FRAGMENTARY_DRAWN_FORM','HATCHED_DRAWN_FORM'}
 buckets={'form_bearing_drawing':[],'minimal_marks':[],'edge_only':[]};assignment={'single_literal':[],'conflicting_literal':[],'unassigned_literal':[]}
 for row in rows:
  category=row['drawing_observation']['category']
  key='form_bearing_drawing' if category in form else 'minimal_marks' if category=='MINIMAL_MARKS_NO_ASSIGNABLE_CONTOUR' else 'edge_only' if category=='EDGE_HATCHING_WITHOUT_ASSIGNABLE_FORM' else None
  if key is None:raise ValueError('unreviewed drawing category')
  buckets[key].append(row['source_ordinal'])
  types=row['printed_table_memberships'];assignment['single_literal' if len(types)==1 else 'unassigned_literal' if not types else 'conflicting_literal'].append(row['source_ordinal'])
  if row['canonical_type_admitted'] is not None or row['verified_glyph'] or row['analysis_eligible']:raise ValueError('unreviewed source type promoted')
 e=checkpoint['expectation']
 if len(buckets['form_bearing_drawing'])!=e['form_bearing_source_drawings'] or buckets['minimal_marks']!=e['minimal_marks_positions'] or buckets['edge_only']!=e['edge_only_positions']:raise ValueError('drawing partition drift')
 if len(assignment['single_literal'])!=e['single_literal_type_assignment'] or assignment['conflicting_literal']!=e['conflicting_literal_type_assignment'] or assignment['unassigned_literal']!=e['unassigned_literal_type_positions']:raise ValueError('literal assignments silently reconciled')
 reported=load(root,'research/stele-a-count-comparison.json')['assertions']
 return {'format':'byblos-count-assignment-partition-v1','scope':checkpoint['scope'],'input_hashes':checkpoint['inputs'],'drawing_partition':{k:{'count':len(v),'source_ordinals':v} for k,v in buckets.items()},'literal_assignment_partition':{k:{'count':len(v),'source_ordinals':v} for k,v in assignment.items()},'source_claims_retained':reported,'partition_sum':sum(map(len,buckets.values())),'reported_119_equals_form_bearing_drawing_count':True,'physical_surviving_lost_categories_certified':False,'candidate_errata_adopted':False,'canonical_types_added':0,'verified_sequences_added':0,'independent_reviews_added':0,'remaining_source_count_questions':load(root,'research/final-source-pass-audit.json')['count_policy_review_targets'],'boundary':checkpoint['boundary']}
def validate(root=ROOT):
 data=build(root)
 if load(root,OUTPUT)!=data:raise ValueError('derived count partition stale')
 return {'status':'PASS_SOURCE_DRAWING_PARTITION_ONLY','source_ordinals':123,'drawing_partition':[119,3,1],'literal_assignments':[114,1,8],'ancient_counts_certified':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
 if a.write:(ROOT/OUTPUT).write_text(json.dumps(build(),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(validate()))
