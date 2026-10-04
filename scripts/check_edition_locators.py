"""Cross-check source-located core metadata against the native catalogue."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def check(root=ROOT):
 root=Path(root)
 def read(p):return json.loads((root/p).read_text(encoding="utf-8"))
 register=read('research/core-edition-locators.json');catalogue=read('data/catalogue.json');surfaces=read('data/surfaces.json')
 core={r['id'] for r in catalogue['records'] if r['membership']=='reported_core'}
 entries=register['entries'];ids=[e['record_id'] for e in entries]
 if len(ids)!=len(set(ids)) or set(ids)!=core:raise ValueError('core locator identity coverage mismatch')
 index={e['record_id']:e for e in entries};groups={}
 for s in surfaces['surfaces']:groups.setdefault(s['inscription_id'],[]).append(s)
 for e in entries:
  if e['source_id']!=register['source_id'] or not e['survey_locator'] or not e['primary_edition_locator_reported']:raise ValueError('missing source locator')
  if e['verified_sign_sequence'] or e['independent_epigraphic_review'] or e['primary_edition_directly_collated']:raise ValueError('survey metadata cannot certify collation')
  found=groups.get(e['record_id'],[])
  if found:
   if sum(s['line_count'] for s in found)!=e['layout']['reported_lines']:raise ValueError('native surface counts disagree with source-located layout')
   faces=e['direction_claim'].get('faces',{})
   for s in found:
    direction=faces.get(s['label'],e['direction_claim']['value'])
    if direction in {'right_to_left','left_to_right'} and s['direction']!={'right_to_left':'rtl','left_to_right':'ltr'}[direction]:raise ValueError('source/native direction mismatch')
 if index['BYB-G']['layout']['reported_lines'] is not None:raise ValueError('columns must not be silently converted to lines')
 return {'format':'byblos-edition-locator-audit-v1','input_hashes':{p:hashlib.sha256((root/p).read_text(encoding="utf-8").encode("utf-8")).hexdigest() for p in ['research/core-edition-locators.json','data/catalogue.json','data/surfaces.json']},
  'core_labels_with_edition_locators':len(entries),'core_labels_with_native_line_surfaces':len(core & set(groups)),
  'native_surfaces':len(surfaces['surfaces']),'reported_line_targets':sum(s['line_count'] for s in surfaces['surfaces']),
  'column_layouts_kept_separate':['BYB-G'],'unresolved_printed_source_anomalies':[{'record_id':e['record_id'],'anomalies':e['source_anomalies']} for e in entries if e.get('source_anomalies')],
  'verified_sequences_added':0,'independent_reviews_added':0,'scientific_completeness_established':False}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();output=json.dumps(check(),ensure_ascii=False,indent=2)+'\n'
 if a.check:
  if (ROOT/'research/edition-locator-audit.json').read_text(encoding="utf-8")!=output:raise SystemExit('Edition locator audit stale')
  print('Fourteen core edition locators and native surface metadata reconciled.')
 else:print(output,end='')
