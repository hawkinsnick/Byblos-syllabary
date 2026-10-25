#!/usr/bin/env python3
"""Executable scoped exclusions from existing source evidence; no adjudication."""
import argparse,csv,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT='research/closure-controls.json'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def build(root=ROOT):
    root=Path(root);inputs=[]
    def load(path,kind='json'):
        raw=(root/path).read_bytes();inputs.append({'path':path,'sha256':sha(raw)})
        return json.loads(raw) if kind=='json' else list(csv.DictReader(io.StringIO(raw.decode())))
    rows=[]
    if (root/'research/edition-concordance.csv').exists():
        kind='linear-a-reference-gaps';source=load('research/edition-concordance.csv','csv')
        for i,r in enumerate(source):
            if not r['reference_gap']:continue
            if r['reference_gap'] not in ('ABSENT','LITERAL_MISSING'):raise ValueError('Unknown reference-gap state')
            if r['gorila_source_url']:raise ValueError('Gap disposition conflicts with source route')
            rows.append({'id':r['source_record_id'],'source_record_id':r['source_record_id'],
                         'source_row_index':i,'reference_gap':r['reference_gap'],
                         'disposition':'EXCLUDED_FROM_EXACT_EDITION_TARGET_COHORT',
                         'admitted_exact_edition_target':False,'resolved_edition_url':None,
                         'underlying_locator_recovered':False,
                         'reason':'Pinned source supplies no usable exact edition route. Retain the source entry and unresolved gap; do not substitute a context citation or guessed page.'})
        counts={'gap_records':len(rows),'absent':sum(r['reference_gap']=='ABSENT' for r in rows),'literal_missing':sum(r['reference_gap']=='LITERAL_MISSING' for r in rows),'admitted_exact_targets':0}
    elif (root/'research/stele-a-type-table.json').exists():
        kind='byblos-printed-type-lookup';table=load('research/stele-a-type-table.json');index=load('research/stele-a-facsimile-number-index.json')
        labels={}
        for r in table['rows']:
            for n in r['source_numbered_positions']:
                labels.setdefault(n,[]).append(r['edition_sign_label'])
        ordinals=[]
        for line in index['lines']:ordinals.extend(range(line['first_source_ordinal'],line['last_source_ordinal']+1))
        if len(ordinals)!=len(set(ordinals)):raise ValueError('Overlapping printed ordinal ranges')
        if set(labels)-set(ordinals):raise ValueError('Type table ordinal outside source numbering')
        for n in ordinals:
            candidates=labels.get(n,[]);eligible=len(candidates)==1
            rows.append({'id':f'BYB-A-D1930-ordinal-{n:03}','record_id':'BYB-A','source_numbered_position':n,
                         'source_id':table['source_id'],'locator':table['locator'],
                         'printed_type_assertions':candidates,'unambiguous_printed_type':candidates[0] if eligible else None,
                         'source_table_lookup_admitted':eligible,
                         'exclusion_reason':None if eligible else 'NO_PRINTED_MEMBERSHIP' if not candidates else 'CONFLICTING_PRINTED_MEMBERSHIPS',
                         'erratum_adopted':False,'canonical_sign_identity_admitted':False,
                         'physical_occurrence_certified':False})
        counts={'source_numbered_positions':len(rows),'unambiguous_source_table_lookups':sum(r['source_table_lookup_admitted'] for r in rows),
                'excluded_conflicts':sum(r['exclusion_reason']=='CONFLICTING_PRINTED_MEMBERSHIPS' for r in rows),
                'excluded_unassigned':sum(r['exclusion_reason']=='NO_PRINTED_MEMBERSHIP' for r in rows)}
    elif (root/'research/source-reconciliation.json').exists():
        kind='cretan-hieroglyphic-material-conflicts';source=load('research/source-reconciliation.json')
        for c in source['comparisons']:
            if c['field']!='material':continue
            assertions=c['assertions']
            if len({a['value'] for a in assertions})<2 or any(not a['locator'] or not a['source_id'] for a in assertions):raise ValueError('Unbound conflict assertions')
            rows.append({'id':c['record_id'],'record_id':c['record_id'],'comparison_id':c['comparison_id'],
                         'material_assertions':assertions,'resolved_material':None,
                         'single_material_value_admitted':False,'status':'UNRESOLVED_SOURCE_DISAGREEMENT',
                         'physical_identity_adjudicated':False,'material_adjudicated':False})
        counts={'paired_conflict_records':len(rows),'single_material_values_admitted':0}
    else:raise ValueError('Unsupported native evidence layout')
    return {'format':'academic-closure-controls-v1','kind':kind,'inputs':inputs,'records':rows,'counts':counts,
            'scientific_approval_granted':False,'source_literals_changed':False,
            'boundary':'A completed exclusion/representation control is not recovered missing evidence or adjudicated scholarship. Preserve native source assertions and unresolved scientific requirements.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    result=build();text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.check:
        if (ROOT/OUT).read_text()!=text:raise ValueError('Closure-control replay drift')
    else:(ROOT/OUT).write_text(text)
    print(json.dumps({'status':'PASS_SCOPED_CONTROLS_ONLY','kind':result['kind'],'counts':result['counts']}))
