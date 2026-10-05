"""Audit dependent drawing comparisons and display targets without glyph admission."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = ['research/historical-layout-targets.json',
         'research/stele-a-dependent-drawing-comparison.json',
         'research/dhorme-1946-source-joins.json',
         'research/dhorme-1946-acquisition.json',
         'research/stele-a-facsimile-number-index.json',
         'research/dhorme-1946-source-audit.json']


def build(root=ROOT):
    root = Path(root)
    targets, comparison, joins, acquisition, numbering, historical = [
        json.loads((root / p).read_text(encoding='utf-8')) for p in PATHS]
    assets = {f['figure_number']: f for f in acquisition['figures']}
    full_page = next(p for p in acquisition['pages'] if p.get('printed_page') == 33)
    expected = []
    for f in joins['figure_layout_review']:
        layout = f['layout_observation']
        panels = layout.get('panels', [{'display_position': 'single',
            'drawn_line_bands': layout.get('drawn_line_bands', layout.get(
                'main_drawn_line_bands', layout.get('drawn_columns')))}])
        for panel in panels:
            for i in range(1, panel['drawn_line_bands'] + 1):
                expected.append((f, panel['display_position'], i,
                                 'column' if 'drawn_columns' in layout else 'line_band'))
    rows = targets['segments']
    if len(rows) != len(expected) or len({r['id'] for r in rows}) != len(rows):
        raise ValueError('Layout targets must be complete and uniquely identified')
    for row, (f, panel, i, kind) in zip(rows, expected):
        crop = f['figure_number'] == 9 and panel == 'left' and i == 1
        asset = assets[f['figure_number']]
        sha = full_page['image_sha256'] if crop else asset['sha256']
        url = full_page['image_url'] if crop else asset['url']
        if (row['id'], row['record_label_join'], row['figure_number'],
            row['printed_page'], row['display_panel'], row['display_order'],
            row['segment_kind'], row['asset_sha256'], row['inspection_url'],
            row['standalone_asset_truncates_this_target']) != (
                f"D1946-F{f['figure_number']:02d}-{panel}-{i:02d}", f['record_id'],
                f['figure_number'], f['article_printed_page'], panel, i, kind, sha, url, crop):
            raise ValueError('Display target lost source locator, order or crop correction')
        if row['order_basis'] != ('LEFT_TO_RIGHT' if kind == 'column' else 'TOP_TO_BOTTOM'):
            raise ValueError('Display order is not ancient reading order')
        if row['physical_face_id'] is not None or row['source_glyph_count'] is not None or row['verified_sequence'] or row['ancient_reading_order_admitted']:
            raise ValueError('Layout target cannot certify face, count, direction or sequence')
    if any(targets[k] != 0 for k in ['canonical_surfaces_added', 'canonical_lines_added', 'verified_sequences_added']) or targets['independent_confirmation']:
        raise ValueError('Dependent layout indexing cannot add native evidence')
    if any(x['certified_extra_text_line'] for x in targets['excluded_qualified_traces']):
        raise ValueError('Qualified traces cannot become textual lines')
    if comparison['earlier_asset_sha256'] != numbering['figure_sha256'] or comparison['later_asset_sha256'] != assets[3]['sha256']:
        raise ValueError('Drawing comparison asset pins changed')
    if comparison['later_has_source_ordinal_labels'] or any(comparison[k] for k in ['erratum_adopted', 'surviving_count_reconciled', 'independent_confirmation', 'physical_identity_certified', 'verified_sequences_added']):
        raise ValueError('Dependent unnumbered drawing cannot resolve native claims')
    if [(x['earlier_source_line_label'], x['later_display_line_band']) for x in comparison['line_comparisons']] != [(x['source_line_label'], i) for i, x in enumerate(numbering['lines'], 1)]:
        raise ValueError('Broad ten-line correspondence changed')
    if any(x['one_to_one_glyph_alignment_certified'] or x['status'] != 'BROAD_LAYOUT_CORRESPONDENCE_ONLY' for x in comparison['line_comparisons']):
        raise ValueError('Broad layout cannot promote exact glyph alignment')
    if [x['earlier_source_ordinals'] for x in comparison['focused_targets']] != [[32], [92], [27], [40, 41, 42]]:
        raise ValueError('Focused comparison scope changed')
    if [x['disposition'] for x in comparison['focused_targets']] != [
            'EXACT_FORM_JOIN_UNRESOLVED', 'MOTIF_COMPATIBLE_ERRATUM_NOT_RESOLVED',
            'COUNT_POLICY_UNRESOLVED', 'LOSS_AND_SLOT_ALIGNMENT_UNRESOLVED']:
        raise ValueError('Focused source uncertainties cannot be silently resolved')
    return {'format': 'byblos-final-source-pass-audit-v1',
        'input_hashes': {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in PATHS},
        'source_display_targets': len(rows),
        'horizontal_line_band_targets': sum(r['segment_kind'] == 'line_band' for r in rows),
        'column_targets': sum(r['segment_kind'] == 'column' for r in rows),
        'display_panels': len({(r['figure_number'], r['display_panel']) for r in rows}),
        'figure_coverage': sorted({r['figure_number'] for r in rows}),
        'crop_corrected_targets': sum(r['standalone_asset_truncates_this_target'] for r in rows),
        'broad_stele_line_comparisons': len(comparison['line_comparisons']),
        'focused_drawing_comparisons': len(comparison['focused_targets']),
        'count_policy_review_targets': historical['count_comparison'],
        'canonical_lines_added': 0, 'verified_sequences_added': 0,
        'independent_reviews_added': 0,
        'disposition': 'AGREED_FINAL_PASS_COMPLETE_SCOPED_PAUSE_NOT_TERMINAL_READINESS',
        'boundary': targets['boundary']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = ROOT / 'research/final-source-pass-audit.json'
    content = json.dumps(build(), indent=2, ensure_ascii=False) + '\n'
    if args.check:
        if output.read_text(encoding='utf-8') != content:
            raise SystemExit('Final source pass audit is stale')
    else:
        output.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    main()
