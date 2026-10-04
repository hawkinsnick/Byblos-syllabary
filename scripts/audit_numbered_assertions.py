"""Check a bounded primary-edition numbering pilot without certifying glyphs."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATHS=['data/research_entities.json','research/stele-a-numbered-assertions.json',
       'research/dunand-1930-acquisition.json','data/sources.json']


def build(root=ROOT):
    root=Path(root)
    read=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
    entities,assertions,acquisition,sources=map(read,PATHS)
    edition=assertions['edition_id']
    eds=[e for e in entities['editions'] if e['id']==edition]
    if len(eds)!=1 or eds[0]['source_id']!=assertions['source_id'] or eds[0]['inscription_id']!=assertions['record_id']:
        raise ValueError('Numbering pilot lacks a unique source-bound edition')
    if assertions['verified_full_sequence'] or assertions['independent_review']:
        raise ValueError('Numbering metadata cannot certify full glyph transcription')
    if not any(s['id']==assertions['source_id'] and s['type']=='primary_edition' for s in sources['sources']):
        raise ValueError('Numbering pilot must cite the registered primary edition')
    inspected={p['printed_page'] for p in acquisition['pages'] if p['inspection_status']=='VISUALLY_INSPECTED'}
    if not {4,5,8,9}<=inspected:raise ValueError('Numbering, sign table and recurrence pages were not inspected')
    signs=[s for s in entities['signs'] if s['edition_id']==edition]
    native={s['edition_sign_label']:s for s in signs}
    if len(native)!=len(signs):raise ValueError('Duplicate source type label')
    selected={s['edition_sign_label']:s['source_numbered_positions'] for s in assertions['selected_source_groups']}
    if len(selected)!=len(assertions['selected_source_groups']) or set(selected)!=set(native):
        raise ValueError('Selected and native source type identities disagree')
    positions={}
    for label,ordinals in selected.items():
        s=native[label]
        if s['source_numbered_positions']!=ordinals or s['shape_encoded'] or s['independently_reviewed'] or s['sound_value'] is not None:
            raise ValueError('Source grouping promoted, altered or shape/sound assertions added')
        if not s['evidence'] or not all(e['source_id']==assertions['source_id'] and e['locator'] for e in s['evidence']):
            raise ValueError('Missing source type locator')
        if not ordinals or len(set(ordinals))!=len(ordinals):raise ValueError('Duplicate or empty source ordinals')
        for ordinal in ordinals:
            if type(ordinal)!=int or ordinal<1 or ordinal in positions:
                raise ValueError('Source ordinal must occur in exactly one selected type assertion')
            positions[ordinal]=label
    checked=[]
    for recurrence in assertions['recurrence_assertions']:
        groups=recurrence['source_position_groups']
        if recurrence['source_id']!=assertions['source_id'] or not recurrence['locator']:
            raise ValueError('Recurrence lacks primary-source attribution')
        if recurrence['glyph_collation_completed'] or recurrence['semantic_interpretation_admitted']:
            raise ValueError('Numerical source consistency cannot grant glyph or semantic verification')
        if len(groups)<2 or any(not group or len(group)!=len(groups[0]) for group in groups):
            raise ValueError('Repeated source spans require equal, nonempty lengths')
        if any(type(p)!=int or p not in positions for group in groups for p in group):
            raise ValueError('Uninspected ordinal used by recurrence')
        labels=[[positions[p] for p in group] for group in groups]
        if any(label!=labels[0] for label in labels[1:]):
            raise ValueError('Printed recurrence disagrees with selected source type memberships')
        checked.append({'id':recurrence['id'],'status':'NUMERICAL_SOURCE_ASSERTIONS_CONSISTENT',
                        'source_spans':groups,'source_type_labels':labels[0],
                        'glyph_or_linguistic_confirmation':False})
    return {'format':'byblos-numbering-audit-v1',
        'input_hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in PATHS},
        'source_type_groups':len(native),'source_numbered_position_assertions':len(positions),
        'recurrence_assertions_checked':checked,'full_sequence_verified':False,
        'independent_review':False,'global_sign_equivalence_allowed':False,
        'boundary':'Only the selected source numbering/grouping assertions are checked. A source type label and Arabic ordinal are not glyph coordinates, normalized sign identity, phonetic value, a certified ancient occurrence or a complete transcription.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    out=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';target=ROOT/'research/stele-a-numbering-audit.json'
    if a.check:
        if target.read_text(encoding='utf-8')!=out:raise SystemExit('Numbering audit stale')
        print('Selected primary numbering assertions replay without glyph/semantic promotion.')
    else:print(out,end='')


if __name__=='__main__':main()
