"""Reconcile the 10+4 publication genealogy with native core labels."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATHS=['research/mnamon-corpus-genealogy.json','research/core-object-reconciliation.json','data/catalogue.json']
def build(root=ROOT):
 root=Path(root)
 def read(p):return json.loads((root/p).read_text(encoding='utf-8'))
 genealogy=read(PATHS[0])['corpus_genealogy'];reconciliation=read(PATHS[1]);catalogue=read(PATHS[2]);cohorts={'Dunand 1945':genealogy['dunand_1945']['labels'],'Dunand 1978':genealogy['dunand_1978']['labels']}
 if genealogy['dunand_1945']['count']!=10 or genealogy['dunand_1978']['count']!=4:raise ValueError('publication cohort count changed')
 if set(cohorts['Dunand 1945']) & set(cohorts['Dunand 1978']) or set(cohorts['Dunand 1945']+cohorts['Dunand 1978'])!=set('abcdefghijklmn'):raise ValueError('publication cohorts overlap or omit core labels')
 objects={o['dunand_label']:o for o in reconciliation['objects']};native={r['edition_label']:r for r in catalogue['records'] if r['membership']=='reported_core'}
 if set(objects)!=set(native) or reconciliation['identity_count']!=14:raise ValueError('native/reconciliation core identity mismatch')
 rows=[]
 for edition,labels in cohorts.items():
  for label in labels:
   if objects[label]['edition']!=edition or native[label]['id']!=objects[label]['project_id']:raise ValueError('edition cohort/object join mismatch')
   rows.append({'edition_cohort':edition,'dunand_label':label,'project_id':objects[label]['project_id'],'object_class':objects[label]['object_class'],'verified_sequence':objects[label]['verified_sequence']})
 if any(r['verified_sequence'] for r in rows):raise ValueError('genealogy cannot verify sequence')
 return {'format':'byblos-core-publication-genealogy-audit-v1','input_hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in PATHS},'publication_label_counts':{'Dunand 1945':10,'Dunand 1978':4},'conventional_core_label_count':14,'minimum_distinct_physical_monument_count':None,'maximum_distinct_physical_monument_count':None,'potential_coreference_groups':[['BYB-H','BYB-J']],'verified_sequence_count':0,'records':rows,'boundary':'Ten 1945 labels plus four 1978 labels yield fourteen publication labels, not fourteen certified physical monuments. The reported h/j possible join is retained without adjudication; publication cohorts do not verify sequences or the source-attributed sign inventory.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();output=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';target=ROOT/'research/core-publication-genealogy-audit.json'
 if a.check:
  if target.read_text(encoding='utf-8')!=output:raise SystemExit('Core publication genealogy audit stale')
  print('Byblos 10+4 publication cohorts replay without physical-object inflation.')
 else:print(output,end='')
