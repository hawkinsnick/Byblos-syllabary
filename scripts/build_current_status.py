"""Build a current Byblos evidence summary from native and source-scoped audits."""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from byblos.core import audit,load_bundle
from scripts.audit_source_comparison import build as source_audit
from scripts.audit_numbered_assertions import build as numbering_audit


def build():
    native=audit(load_bundle(ROOT));source=source_audit(ROOT);numbered=numbering_audit(ROOT)
    if not native['structure_valid']:raise ValueError('Native corpus structure invalid')
    return {'schema_version':'1.0','project':'Byblos-syllabary','repository_version':native['version'],
        'checked':'2026-10-04','milestone':'SOURCE_SCOPED_PRIMARY_NUMBERING_AND_PROVIDER_RECONCILIATION',
        'native_evidence_counts':native['counts'],
        'source_scoped_evidence':{'survey_core_count_records':source['core_count_assertion_records'],
            'provider_entries_structurally_inspected':source['provider_entries'],
            'acquired_primary_page_views':source['acquired_primary_page_views'],
            'visually_inspected_primary_views_this_checkpoint':source['visually_inspected_primary_views_this_checkpoint'],
            'selected_primary_type_groups':numbered['source_type_groups'],
            'selected_source_numbered_positions':numbered['source_numbered_position_assertions'],
            'source_recurrence_assertions_numerically_checked':len(numbered['recurrence_assertions_checked'])},
        'scientific_results':{'scientific_1_0_ready':native['scientific_1_0_ready'],
            'complete_verified_sequences':native['counts']['verified_core_sequences'],
            'sequence_frequency_allowed':False,'independent_epigraphic_review_completed':False,
            'source_numbering_consistency':'PASS_SELECTED_ASSERTIONS_ONLY'},
        'unresolved_source_conflicts':{'layout':['BYB-G','BYB-H'],'direction':['BYB-M'],
            'count_conventions':['BYB-A'],'first_line_reading':['BYB-N']},
        'source_redistribution':{'scans':False,'OCBI_readings':False,'OCBI_code_or_fonts':False,
            'selected_primary_numeric_metadata':'Original attributed factual assertions only'},
        'next_work':['Collate the rest of stele a numbering and type table with explicit damage/variant status.',
            'Acquire lawful Dunand 1945 and 1978 edition/plate access for complete source sequences.',
            'Resolve provider face/variant/object identities and g/h/m/n source discrepancies.',
            'Obtain applicable upstream terms before distributing provider readings or images.'],
        'evidence':['research/core-count-assertions.json','research/source-comparison-audit.json',
            'research/stele-a-numbering-audit.json','research/stele-a-count-comparison.json',
            'research/dunand-1930-acquisition.json'],
        'boundary':'Five edition-specific type labels and fourteen numbered-position assertions are a selected primary-source pilot, not five certified native sign identities or a verified full sequence. Source counts, provider rows and ancient occurrences remain distinct.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    out=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';target=ROOT/'analysis/current-status.json'
    if a.check:
        if target.read_text(encoding='utf-8')!=out:raise SystemExit('Current status stale')
        print('Current evidence counts and scientific gates replay.')
    else:print(out,end='')


if __name__=='__main__':main()
