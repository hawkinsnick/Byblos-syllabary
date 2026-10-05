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
from scripts.audit_type_table import build as table_audit
from scripts.audit_facsimile_review import build as drawing_audit
from scripts.audit_dhorme_source_joins import build as historical_audit


def build():
    native=audit(load_bundle(ROOT));source=source_audit(ROOT);numbered=numbering_audit(ROOT);table=table_audit(ROOT);drawing=drawing_audit(ROOT);historical=historical_audit(ROOT)
    if not native['structure_valid']:raise ValueError('Native corpus structure invalid')
    return {'schema_version':'1.0','project':'Byblos-syllabary','repository_version':native['version'],
        'checked':'2026-10-05','date_basis':'UTC','milestone':'SOURCE_DRAWING_TYPE_TABLE_COMPARISON_AND_UNADOPTED_CORRECTIONS',
        'native_evidence_counts':native['counts'],
        'source_scoped_evidence':{'survey_core_count_records':source['core_count_assertion_records'],
            'provider_entries_structurally_inspected':source['provider_entries'],
            'acquired_primary_page_views':source['acquired_primary_page_views'],
            'visually_inspected_primary_views_this_checkpoint':source['visually_inspected_primary_views_this_checkpoint'],
            'selected_primary_type_groups':numbered['source_type_groups'],
            'selected_source_numbered_positions':numbered['source_numbered_position_assertions'],
            'complete_printed_type_rows_numerically_registered':table['source_type_rows'],
            'printed_numeric_membership_assertions':table['numeric_membership_assertions'],
            'distinct_source_ordinals_in_table':table['distinct_source_ordinals'],
            'facsimile_numbered_line_spans':table['facsimile_source_line_labels'],
            'facsimile_source_ordinals':table['facsimile_source_ordinals'],
            'source_facsimile_positions_compared':drawing['source_drawing_positions_compared'],
            'selected_facsimile_drawing_markers_inspected':drawing['selected_marker_targets_inspected'],
            'drawing_table_comparison_dispositions':drawing['drawing_table_comparison_counts'],
            'number_table_join_only_positions':drawing['number_and_table_join_only_positions'],
            'unadopted_source_internal_erratum_candidates':len(drawing['candidate_erratum_scenarios']),
            'historical_article_heading_joins':historical['heading_joins'],
            'historical_article_visually_inspected_page_views':historical['visually_inspected_page_views'],
            'historical_article_count_records':historical['historical_count_records'],
            'historical_figures_layout_inspected':historical['historical_figures_layout_inspected'],
            'source_recurrence_assertions_numerically_checked':len(numbered['recurrence_assertions_checked'])},
        'scientific_results':{'scientific_1_0_ready':native['scientific_1_0_ready'],
            'complete_verified_sequences':native['counts']['verified_core_sequences'],
            'sequence_frequency_allowed':False,'independent_epigraphic_review_completed':False,
            'source_numbering_consistency':'PASS_SELECTED_ASSERTIONS_ONLY'},
        'unresolved_source_conflicts':{'layout':['BYB-G','BYB-H'],'direction':['BYB-M'],
            'count_conventions':['BYB-A','BYB-B','BYB-D','BYB-G','BYB-H','BYB-I'],'first_line_reading':['BYB-N'],
            'qualified_possible_extra_line':['BYB-J'],
            'printed_type_membership':table['printed_collisions'],
            'ordinals_unassigned_in_table':table['unassigned_ordinals_in_observed_number_range'],
            'candidate_errata_unadopted':drawing['candidate_erratum_scenarios']},
        'source_redistribution':{'scans':False,'OCBI_readings':False,'OCBI_code_or_fonts':False,
            'selected_primary_numeric_metadata':'Original attributed factual assertions only'},
        'next_work':['Cross-collate the source drawing/type comparisons against the later edition, physical images and independent readings; source drawing compatibility does not certify native glyph identity.',
            'Test the unadopted VIII 32/92 erratum and edge-position 27 count hypothesis against the later edition and survey.',
            'Compare the ten dependent Dhorme figure witnesses with the original editions; retain source count policies and h/j physical uncertainty.',
            'Acquire lawful Dunand 1945 and 1978 edition/plate access for complete source sequences.',
            'Resolve provider face/variant/object identities and g/h/m/n source discrepancies.',
            'Obtain applicable upstream terms before distributing provider readings or images.'],
        'evidence':['research/core-count-assertions.json','research/source-comparison-audit.json',
            'research/stele-a-numbering-audit.json','research/stele-a-count-comparison.json',
            'research/dunand-1930-acquisition.json','research/stele-a-type-table-audit.json',
            'research/stele-a-facsimile-review-audit.json','docs/STELE-A-SOURCE-REVIEW.md',
            'research/dhorme-1946-source-audit.json'],
        'boundary':'Five edition-specific type labels and fourteen numbered-position assertions are a selected primary-source pilot, not five certified native sign identities or a verified full sequence. Source counts, provider rows and ancient occurrences remain distinct.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    out=json.dumps(build(),ensure_ascii=False,indent=2)+'\n';target=ROOT/'analysis/current-status.json'
    if a.check:
        if target.read_text(encoding='utf-8')!=out:raise SystemExit('Current status stale')
        print('Current evidence counts and scientific gates replay.')
    else:print(out,end='')


if __name__=='__main__':main()
