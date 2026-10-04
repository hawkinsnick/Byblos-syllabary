"""Preserve conflicting Dunand 1978 pagination and appearance metadata."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PATHS=['data/sources.json','research/core-primary-access-routes.json']
def span(s):a,b=s.replace('–','-').split('-');return set(range(int(a),int(b)+1))
def build(root=ROOT):
 root=Path(root);sources=json.loads((root/PATHS[0]).read_text(encoding='utf-8'))['sources'];routes=json.loads((root/PATHS[1]).read_text(encoding='utf-8'));src=next(x for x in sources if x['id']=='dunand-1978');claims=src['bibliographic_claims'];by={x['source_id']:x for x in claims}
 if set(by)!= {'mnamon-bibliography','keibi-dunand-1978'}:raise ValueError('Dunand bibliographic claims changed')
 m,k=by['mnamon-bibliography'],by['keibi-dunand-1978'];ms,ks=span(m['pages']),span(k['pages']);route=next(x for x in routes['routes'] if x['edition']=='Dunand 1978')
 if route['primary_pages_collated'] or route['verified_sequences']:raise ValueError('unearned inspection promotion')
 return {'format':'byblos-dunand-1978-bibliographic-conflict-audit-v1','input_hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in PATHS},'edition':'Dunand 1978','core_labels':route['core_labels'],'claims':[{'source_id':m['source_id'],'pages':m['pages'],'nominal_year':m['nominal_year'],'appeared_year':m['appeared_year']},{'source_id':k['source_id'],'pages':k['pages'],'nominal_year':k['nominal_year'],'appeared_year':k['appeared_year']}],'shared_page_span':f'{min(ms&ks)}–{max(ms&ks)}','union_page_span':f'{min(ms|ks)}–{max(ms|ks)}','disputed_boundary_pages':sorted((ms|ks)-(ms&ks)),'pagination_resolved':False,'appearance_year_independently_confirmed':False,'primary_article_inspected':False,'verified_sequences':0,'boundary':'Mnamon reports pp. 52–58; KeiBi reports pp. 51–59 and says the nominal 1978 article appeared in 1981. The physical article has not been inspected, so the project preserves both claims, uses their union only as an acquisition target, and does not choose pagination, certify the appearance year, or infer inscription content.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args();out=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';target=ROOT/'research/dunand-1978-bibliographic-conflict-audit.json'
 if a.check:
  if json.loads(target.read_text(encoding='utf-8'))!=build():raise SystemExit('Dunand 1978 bibliography audit stale')
  print('Dunand 1978 pagination conflict replays without false resolution.')
 else:print(out,end='')
