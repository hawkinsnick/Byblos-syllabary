"""Audit field-level provenance for core Byblos objects without promoting readings."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATHS=['data/catalogue.json','data/sources.json','research/core-edition-locators.json']

def build(root=ROOT):
 root=Path(root)
 def read(path):return json.loads((root/path).read_text(encoding='utf-8'))
 catalogue=read(PATHS[0]);sources=read(PATHS[1]);locators=read(PATHS[2]);source_index={s['id']:s for s in sources['sources']}
 cores=[r for r in catalogue['records'] if r['membership']=='reported_core'];located={e['record_id']:e for e in locators['entries']}
 if {r['id'] for r in cores}!=set(located):raise ValueError('core/locator identity mismatch')
 rows=[]
 for record in cores:
  direct=[];reported=[]
  for claim in record['evidence']:
   source=source_index[claim['source_id']]
   item={'source_id':claim['source_id'],'locator':claim['locator'],'fields':claim['fields']}
   if source['type']=='primary_edition' and source['consultation'] not in {'not_consulted','metadata_only'}:direct.append(item)
   else:reported.append(item)
  locator=located[record['id']]
  rows.append({'record_id':record['id'],'directly_inspected_primary_metadata':direct,'other_attributed_metadata':reported,
   'survey_edition_locator':locator['primary_edition_locator_reported'],'primary_corpus_edition_directly_collated':locator['primary_edition_directly_collated'],
   'verified_sign_sequence':locator['verified_sign_sequence'],'museum_or_object_identity_established':bool(record.get('museum_id') or record.get('object_id'))})
 if any(r['verified_sign_sequence'] or r['primary_corpus_edition_directly_collated'] for r in rows):raise ValueError('unreviewed source layer promoted')
 return {'format':'byblos-core-field-provenance-audit-v1','input_hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in PATHS},
  'core_labels':len(rows),'core_labels_with_survey_edition_locator':sum(bool(r['survey_edition_locator']) for r in rows),
  'core_labels_with_directly_inspected_primary_metadata':sum(bool(r['directly_inspected_primary_metadata']) for r in rows),
  'core_labels_with_primary_corpus_edition_collation':sum(r['primary_corpus_edition_directly_collated'] for r in rows),
  'core_labels_with_verified_sign_sequence':sum(r['verified_sign_sequence'] for r in rows),
  'core_labels_with_museum_or_object_identity':sum(r['museum_or_object_identity_established'] for r in rows),'records':rows,
  'boundary':'Direct inspection of selected factual fields in Dunand 1930 for BYB-A does not equal collation of the later corpus edition, its plates, or a verified sign sequence. Survey-reported edition locators and direct primary inspection are separate evidentiary statuses.'}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();output=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';target=ROOT/'research/core-field-provenance-audit.json'
 if a.check:
  if target.read_text(encoding='utf-8')!=output:raise SystemExit('Core field-provenance audit stale')
  print('Fourteen core records replay with field-level provenance boundaries.')
 else:print(output,end='')
