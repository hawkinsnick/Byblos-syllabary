"""Compare consulted historical descriptions without certifying Dunand book pages."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = ['research/dhorme-1946-source-joins.json', 'research/dhorme-1946-acquisition.json',
         'research/core-count-assertions.json', 'research/core-edition-locators.json',
         'data/sources.json']


def build(root=ROOT):
    root = Path(root)
    joins, acquisition, survey, locators, sources = [json.loads((root / p).read_text(encoding='utf-8')) for p in PATHS]
    if joins['source_id'] != 'dhorme-1946' or joins['underlying_edition_source_id'] != 'dunand-1945':
        raise ValueError('Historical witness namespaces changed')
    if not any(s['id'] == joins['source_id'] and s['type'] == 'historical_decipherment_proposal' for s in sources['sources']):
        raise ValueError('Historical interpretation source must remain explicit')
    lineage = joins['source_lineage']
    if lineage['independent_physical_witness'] is not False or lineage['decipherment_and_phonetic_values_admitted'] is not False or joins['independent_expert_review_added'] is not False or joins['canonical_sequences_added'] != 0:
        raise ValueError('Historical redraws cannot admit decipherment or independent confirmation')
    if acquisition['underlying_dunand_1945_pages_inspected'] is not False:
        raise ValueError('Consulting a quote cannot promote book-page inspection')
    inspected = {p['printed_page'] for p in acquisition['pages'] if p['inspection_status'] == 'VISUALLY_INSPECTED_SELECTED_METADATA'}
    if lineage['article_printed_page'] not in inspected:
        raise ValueError('Copy-lineage footnote was not inspected')
    entries = joins['entries']
    if [e['dhorme_section_number'] for e in entries] != list(range(1, 11)) or [e['dhorme_figure_number'] for e in entries] != list(range(1, 11)):
        raise ValueError('Article section/figure order changed')
    expected_letters = 'cdaghjeifb'
    for e, letter in zip(entries, expected_letters):
        if e['record_id'] != 'BYB-' + letter.upper() or e['article_printed_page'] not in inspected:
            raise ValueError('Historical heading join changed or lacks inspected page')
        if any(e[k] for k in ['underlying_edition_directly_inspected', 'object_identity_verified', 'verified_sequence']):
            raise ValueError('Heading joins cannot verify objects, sequences or book pages')
        if letter != 'a' and (e['printed_heading_letter'] != letter or e['join_basis'] != 'EXPLICIT_PRINTED_LETTER'):
            raise ValueError('Explicit heading letter changed')
        if letter == 'a' and (e['printed_heading_letter'] is not None or e['join_basis'] != 'FIRST_STELE_AND_DUNAND_71_73_EDITION_LOCATOR'):
            raise ValueError('First-stele join cannot invent a printed letter')
    a_locator = next(e for e in locators['entries'] if e['record_id'] == 'BYB-A')
    if '71–73' not in a_locator['primary_edition_locator_reported']:
        raise ValueError('First-stele join lost its edition locator')
    surveyed = {e['record_id']: e for e in survey['entries']}
    comparison = []
    for claim in joins['count_records']:
        if claim['article_printed_page'] not in inspected or claim['claim_voice'] not in {'DUNAND_QUOTED_BY_DHORME', 'DHORME_DESCRIPTIVE_PROSE'}:
            raise ValueError('Historical count lacks inspected locator or claim voice')
        native = surveyed[claim['record_id']]
        faces = claim['face_sign_counts']
        derived = sum(faces.values()) if faces else None
        number = claim['reported_sign_count']
        if faces and number is not None and derived != number:
            raise ValueError('Quoted face counts differ from printed total')
        if number is None:
            number = derived
        if type(number) is not int or number < 1:
            raise ValueError('Historical source count missing or invalid')
        current = native['reported_visible_or_partly_visible_count']
        comparison.append({
            'record_id': claim['record_id'], 'article_locator': f"p. {claim['article_printed_page']}",
            'claim_voice': claim['claim_voice'], 'reported_sign_count': claim['reported_sign_count'],
            'face_count_sum_project_derived': derived, 'reported_type_count': claim['reported_type_count'],
            'survey_count_assertion': current, 'survey_type_assertion': native['reported_repertoire'],
            'historical_layout': claim['layout'], 'survey_layout': native['layout'],
            'count_comparison': 'UNRECONCILED_SOURCE_UNITS_AND_READING_CONVENTIONS',
            'native_count_changed': False, 'independent_confirmation': False,
        })
    if {r['record_id'] for r in comparison} != {'BYB-A','BYB-B','BYB-D','BYB-G','BYB-H','BYB-I'}:
        raise ValueError('Inspected historical count scope changed')
    j = joins['qualified_layout_records'][0]
    if j['article_printed_page'] not in inspected or j['possible_lower_line_is_certain'] is not False or j['native_line_count_changed'] is not False:
        raise ValueError('Possible extra line cannot be promoted')
    figure_assets = {f['figure_number']: f for f in acquisition['figures']}
    figure_reviews = joins['figure_layout_review']
    if [f['figure_number'] for f in figure_reviews] != list(range(1, 11)) or set(figure_assets) != set(range(1, 11)):
        raise ValueError('Historical figure inspection scope must retain all ten figures')
    for figure, entry in zip(figure_reviews, entries):
        asset = figure_assets[figure['figure_number']]
        if figure['record_id'] != entry['record_id'] or figure['asset_sha256'] != asset['sha256'] or figure['article_printed_page'] != asset['printed_page']:
            raise ValueError('Figure layout review lost its source asset or heading join')
        if asset['inspection_status'] != 'VISUALLY_INSPECTED_LAYOUT_ONLY' or asset['redistributed'] is not False or asset['glyph_sequence_collated'] is not False:
            raise ValueError('Layout-only source assets cannot become distributed full glyph witnesses')
        if any(figure[k] for k in ['face_identity_verified','full_sequence_verified','ancient_line_status_adjudicated']):
            raise ValueError('Source panel layout cannot certify ancient faces or sequences')
    h_figure = figure_reviews[4]['layout_observation']
    if h_figure['below_divider_trace_is_certified_extra_text_line'] is not False:
        raise ValueError('Below-divider trace cannot be admitted as an extra text line')
    f_figure = figure_reviews[8]
    if f_figure['standalone_crop_truncates_drawn_content'] is not True or not f_figure['crop_note']:
        raise ValueError('Standalone figure 9 crop limitation must remain visible')
    return {
        'format': 'byblos-dhorme-source-audit-v1',
        'input_hashes': {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in PATHS},
        'acquired_article_page_views': len(acquisition['pages']),
        'visually_inspected_page_views': len(inspected),
        'heading_joins': len(entries), 'explicit_letter_joins': 9, 'edition_locator_joins': 1,
        'historical_count_records': len(comparison), 'count_comparison': comparison,
        'historical_figures_layout_inspected': len(figure_reviews),
        'figure_layout_review': figure_reviews,
        'qualified_j_layout': j, 'copy_source_dependency': lineage,
        'verified_sequences_added': 0, 'direct_dunand_book_pages_added': 0,
        'independent_epigraphic_reviews_added': 0,
        'boundary': 'Ten historical headings are not ten certified objects. Article quotes and redraws depend on Dunand; proposed phonetics and translations are excluded. Count/layout disagreements are evidence targets, not automatically corrected readings.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = json.dumps(build(), ensure_ascii=False, indent=2) + '\n'
    target = ROOT / 'research/dhorme-1946-source-audit.json'
    if args.check:
        if target.read_text(encoding='utf-8') != output:
            raise SystemExit('Historical source audit stale')
        print('Ten historical heading joins and six count records replay without book-page/decipherment admission.')
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
