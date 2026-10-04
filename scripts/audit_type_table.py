"""Audit source numeric group memberships, retaining printed collisions."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATHS=['research/stele-a-type-table.json','research/stele-a-numbered-assertions.json',
       'research/dunand-1930-acquisition.json','research/stele-a-facsimile-number-index.json']
LABELS='I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII XXIII XXIV XXV XXVI XXVII XXVIII XXIX XXX XXXI XXXII XXXIII XXXIV XXXV XXXVI XXXVII XXXVIII'.split()

def build(root=ROOT):
    root=Path(root)
    table,pilot,acquisition,facsimile=[json.loads((root/p).read_text(encoding='utf-8')) for p in PATHS]
    if any(table[k] for k in ['figure_redistributed','verified_full_sequence','glyph_collation_completed','independent_review']):
        raise ValueError('Numeric source table cannot grant glyph verification or reproduction')
    figures=acquisition.get('additional_figures',[])
    if not any(f['url']==table['consulted_figure_url'] and f['sha256']==table['consulted_figure_sha256'] and f['inspection_status']=='VISUALLY_INSPECTED' for f in figures):
        raise ValueError('Missing inspected high-resolution table identity')
    rows=table['rows']
    if [r['edition_sign_label'] for r in rows]!=LABELS:raise ValueError('Printed type rows changed or omitted')
    memberships=defaultdict(list)
    by_label={r['edition_sign_label']:r for r in rows}
    for row in rows:
        if set(row)!={'edition_sign_label','drawn_variant_position_groups','source_numbered_positions','variant_group_meaning','source_parenthetical_marker_positions'}:
            raise ValueError('Only numeric source metadata belongs in table rows')
        flat=[p for group in row['drawn_variant_position_groups'] for p in group]
        if flat!=row['source_numbered_positions'] or len(flat)!=len(set(flat)) or not flat:
            raise ValueError('Variant grouping differs from numeric assertion')
        if any(type(p)!=int or not 1<=p<=123 for p in flat):raise ValueError('Invalid source ordinal')
        if not set(row['source_parenthetical_marker_positions'])<=set(flat):raise ValueError('Marker without source ordinal')
        for p in flat:memberships[p].append(row['edition_sign_label'])
    collisions=[{'source_numbered_position':p,'type_labels':labels} for p,labels in sorted(memberships.items()) if len(labels)>1]
    declared=[{k:c[k] for k in ['source_numbered_position','type_labels']} for c in table['printed_conflicts']]
    if collisions!=declared:raise ValueError('Printed collisions were hidden or changed')
    for row in pilot['selected_source_groups']:
        if row['source_numbered_positions']!=by_label[row['edition_sign_label']]['source_numbered_positions']:
            raise ValueError('Selected native pilot disagrees with higher-resolution table')
    if any(facsimile[k] for k in ['glyph_collation_completed','verified_full_sequence','independent_review']):
        raise ValueError('Source number index cannot certify glyph transcription')
    if not any(f['sha256']==facsimile['figure_sha256'] and f['inspection_status']=='VISUALLY_INSPECTED' for f in figures):
        raise ValueError('Numbered facsimile lacks inspected figure identity')
    next_ordinal=1
    for line in facsimile['lines']:
        lo,hi=line['first_source_ordinal'],line['last_source_ordinal']
        if lo!=next_ordinal or hi<lo or line['source_ordinal_count']!=hi-lo+1:
            raise ValueError('Source line ordinals overlap, have gaps or drift in count')
        next_ordinal=hi+1
    if next_ordinal!=124 or [l['source_line_label'] for l in facsimile['lines']]!=LABELS[:10]:
        raise ValueError('Numbered facsimile scope differs from inspected ten lines / 123 ordinals')
    absent=[p for p in range(1,124) if p not in memberships]
    if [o['source_ordinal'] for o in facsimile['table_gap_observations']]!=absent:
        raise ValueError('Table gaps not represented in source number review')
    return {'format':'byblos-type-table-audit-v1',
        'input_hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in PATHS},
        'source_type_rows':len(rows),'drawn_variant_buckets':sum(len(r['drawn_variant_position_groups']) for r in rows),
        'numeric_membership_assertions':sum(len(r['source_numbered_positions']) for r in rows),
        'distinct_source_ordinals':len(memberships),'printed_collisions':collisions,
        'unassigned_ordinals_in_observed_number_range':absent,
        'facsimile_source_line_labels':len(facsimile['lines']),'facsimile_source_ordinals':next_ordinal-1,
        'selected_pilot_matches_table':True,'glyph_collation_completed':False,'verified_full_sequences_added':0,
        'boundary':'Unassigned ordinals are gaps in the printed numeric table, not newly created damaged or lost ancient signs. Multiple printed memberships remain conflicting source assertions. Variant buckets are drawn forms, not additional canonical types.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    out=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';target=ROOT/'research/stele-a-type-table-audit.json'
    if a.check:
        if target.read_text(encoding='utf-8')!=out:raise SystemExit('Type table audit stale')
        print('All 38 printed numeric rows replay with collisions retained.')
    else:print(out,end='')

if __name__=='__main__':main()
