"""Reconcile source units without treating source serialization as ancient text."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PATHS = ['research/ocbi-structure-inspection.json', 'data/external_crosswalk.json',
         'research/core-edition-locators.json', 'research/core-count-assertions.json',
         'research/stele-a-count-comparison.json', 'research/dunand-1930-acquisition.json']
ENTRY_KEYS = {'id','provider_label','provider_source','provider_group','provider_direction',
              'provider_plate_path','source_line','encoded_nonempty_rows',
              'reading_payload_sha256','reading_redistributed'}


def build(root=ROOT):
    root = Path(root)
    data = [json.loads((root/p).read_text(encoding='utf-8')) for p in PATHS]
    inspection, crosswalk, locators, counts, comparison, acquisition = data
    if inspection['source_blob'] != '3c3224f32596b493fd5bb634fff3b8000e591b14':
        raise ValueError('Unknown provider source pin')
    entries = inspection['entries']
    cross = {e['id']: e for e in crosswalk['entries']}
    if len(entries) != 43 or len(cross) != 43 or {e['id'] for e in entries} != set(cross):
        raise ValueError('Provider entry denominator changed')
    for e in entries:
        if set(e) != ENTRY_KEYS or e['reading_redistributed'] is not False:
            raise ValueError('Only bounded metadata belongs in the provider inspection')
        for key in ['provider_label','provider_source','provider_group','provider_direction','provider_plate_path']:
            if e[key] != cross[e['id']][key]:
                raise ValueError('Provider metadata disagrees with the native crosswalk')
        if not re.fullmatch('[0-9a-f]{64}',e['reading_payload_sha256']):
            raise ValueError('Missing payload identity')
        if type(e['encoded_nonempty_rows']) is not int or e['encoded_nonempty_rows'] < 1:
            raise ValueError('Invalid row count')
    located = {e['record_id']: e for e in locators['entries']}
    asserted = {e['record_id']: e for e in counts['entries']}
    if len(asserted) != 14 or set(asserted) != set(located):
        raise ValueError('Core count assertions must cover all native core labels exactly once')
    for e in counts['entries']:
        if e['source_id'] != 'vita-zamora-2018' or not e['locator']:
            raise ValueError('Count assertion lacks inspected survey attribution')
        if e['layout'] != located[e['record_id']]['layout'] or e['direction_claim'] != located[e['record_id']]['direction_claim']:
            raise ValueError('Count assertion disagrees with retained source layout')
        if e['verified_sign_sequence'] is not False or e['independent_review'] is not False:
            raise ValueError('Reported counts cannot become verified readings')
        c = e['reported_visible_or_partly_visible_count']
        if type(c['value']) is not int or c['value'] < 1 or type(c['approximate']) is not bool:
            raise ValueError('Invalid attributed count or approximation')
        components = c['components']
        if components and components[0]['source_category'] != 'numerals_additional':
            if sum(x['value'] for x in components) != c['value']:
                raise ValueError('Explicit included components disagree with source total')
    grouped = defaultdict(list)
    for e in entries:
        grouped[cross[e['id']]['proposed_project_record']].append(e)
    core_rows = []
    for ident, native in located.items():
        found = grouped.get(ident, [])
        encoded = sum(e['encoded_nonempty_rows'] for e in found)
        layout = native['layout']
        if ident == 'BYB-G':
            unit = 'columns'; reported = layout['reported_columns']
            state = 'ROW_COLUMN_DIFFERENCE_UNRESOLVED'
        else:
            unit = 'lines'; reported = layout['reported_lines']
            state = 'NUMERIC_LAYOUT_MATCH_ONLY' if encoded == reported else 'ROW_LINE_DIFFERENCE_UNRESOLVED'
        row = {'record_id':ident,'provider_entry_ids':[e['id'] for e in found],
               'encoded_nonempty_rows':encoded,'survey_reported_layout_count':reported,
               'survey_layout_unit':unit,'layout_comparison':state,
               'physical_identity_verified':False,'sequence_verified':False,
               'face_correspondence':'LABEL_LAYOUT_COMPATIBILITY_ONLY' if ident=='BYB-F' else 'UNADJUDICATED'}
        if ident == 'BYB-G':
            row['certainly_textual_columns_reported']=layout['certainly_textual_columns']
            row['caution']='Five encoded rows numerically match five certainly textual columns; the sixth reported column is still unresolved.'
        if ident == 'BYB-H':
            row['certainly_textual_lines_reported']=layout['certainly_textual_lines']
            row['caution']='Three encoded rows numerically match three certainly textual lines; retain the fourth reported line as a review target.'
        if ident == 'BYB-M':
            row['direction_comparison']={'provider':'RTL','survey':'left_to_right',
                'survey_qualification':'conditional_on_sign_orientation','status':'UNRESOLVED_OPPOSING_CLAIMS'}
        if ident == 'BYB-N':
            row['caution']='Both sources represent five rows, but the survey reports no noticeable signs in the first preserved line. Numeric row agreement does not validate its reading.'
        core_rows.append(row)
    assertions = {a['id']:a for a in comparison['assertions']}
    if assertions['BYB-A-D1930-SURVIVING']['value']!=119 or assertions['BYB-A-D1930-LOST']['value']!=3 or assertions['BYB-A-VZ2018-VISIBLE']['value']!=asserted['BYB-A']['reported_visible_or_partly_visible_count']['value']:
        raise ValueError('Stele A source count assertions disagree')
    if comparison['verified_sequence'] or comparison['independent_review']:
        raise ValueError('Source count comparison cannot certify a sequence')
    if len(acquisition['pages'])!=12 or any(p.get('image_redistributed') is not False for p in acquisition['pages']):
        raise ValueError('Acquisition scope changed or scan redistribution detected')
    return {'format':'byblos-source-comparison-audit-v1',
        'input_hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in PATHS},
        'provider_entries':len(entries),'provider_groups':dict(sorted(Counter(e['provider_group'] for e in entries).items())),
        'provider_entries_mapped_to_core_labels':sum(len(grouped[x]) for x in located),
        'distinct_core_labels_targeted':len(located),
        'core_count_assertion_records':len(asserted),
        'all_provider_entry_dispositions':[{'entry_id':e['id'],'proposed_project_record':cross[e['id']]['proposed_project_record'],'mapping_status':cross[e['id']]['mapping_status'],'identity_verified':False,'sequence_redistribution':'UNRESOLVED','count_as_independent_object':False} for e in entries],
        'core_layout_comparison':core_rows,
        'unresolved_core_layout_differences':['BYB-G','BYB-H'],
        'unresolved_direction_conflicts':['BYB-M'],
        'acquired_primary_page_views':len(acquisition['pages']),
        'visually_inspected_primary_views_this_checkpoint':sum(p['inspection_status']=='VISUALLY_INSPECTED' for p in acquisition['pages']),
        'verified_sequences_added':0,'independent_reviews_added':0,
        'boundary':'Metadata replay and source-conditional comparisons. Numeric agreement is neither sign-level collation nor physical-object certification; candidate variants, faces and native source directions are preserved. No glyph frequencies or corpus-wide sign total is inferred.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    output=json.dumps(build(),ensure_ascii=False,indent=2)+'\n'
    target=ROOT/'research/source-comparison-audit.json'
    if a.check:
        if target.read_text(encoding='utf-8')!=output:raise SystemExit('Source comparison audit stale')
        print('43 provider entries and 14 source-count records replay with explicit unit conflicts.')
    else:print(output,end='')


if __name__=='__main__':main()
