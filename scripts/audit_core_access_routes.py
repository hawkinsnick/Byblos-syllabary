"""Reconcile exact primary-edition access routes with the 10+4 core genealogy."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ROUTES='research/core-primary-access-routes.json';GENEALOGY='research/core-publication-genealogy-audit.json'
def build(root=ROOT):
 root=Path(root);raw=(root/ROUTES).read_bytes();routes=json.loads(raw);genealogy=json.loads((root/GENEALOGY).read_text());expected={'Dunand 1945':[], 'Dunand 1978':[]}
 for row in genealogy['records']:expected[row['edition_cohort']].append(row['dunand_label'])
 got={r['edition']:r['core_labels'] for r in routes['routes']}
 if got!=expected:raise ValueError('access-route labels diverge from genealogy')
 if any(r['primary_pages_collated'] or r['verified_sequences'] or any(c['content_inspected'] for c in r['catalogues']) for r in routes['routes']):raise ValueError('catalogue route promoted to primary inspection')
 return {'format':'byblos-core-access-route-audit-v1','routes_sha256':hashlib.sha256(raw).hexdigest(),'genealogy_sha256':hashlib.sha256((root/GENEALOGY).read_bytes()).hexdigest(),'edition_count':2,'core_label_count':sum(map(len,got.values())),'catalogue_record_count':sum(len(r['catalogues']) for r in routes['routes']),'primary_pages_collated':0,'verified_sequences':0,'certified_physical_monuments':None,'routes':[{'edition':r['edition'],'labels':r['core_labels'],'access_states':[c['access_state'] for c in r['catalogues']]} for r in routes['routes']],'boundary':routes['boundary']}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();output=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';target=ROOT/'research/core-primary-access-route-audit.json'
 if a.check:
  if target.read_text()!=output:raise SystemExit('Core primary-access route audit stale')
  print('Byblos 10+4 primary-edition access routes replay without inspection promotion.')
 else:print(output,end='')
