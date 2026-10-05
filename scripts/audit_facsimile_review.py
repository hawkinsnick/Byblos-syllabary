"""Replay source-number review while keeping observations and hypotheses separate."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    'research/stele-a-facsimile-ordinal-review.json',
    'research/stele-a-facsimile-number-index.json',
    'research/stele-a-type-table.json',
    'research/dunand-1930-acquisition.json',
    'research/stele-a-count-comparison.json',
]
TARGETS = {7, 14, 16, 27, 32, 34, 38, 40, 41, 42, 44, 81, 92, 95, 96, 111, 113, 114}
CATEGORIES = {
    'HATCHED_DRAWN_FORM', 'DRAWN_FORM_PRESENT',
    'EDGE_HATCHING_WITHOUT_ASSIGNABLE_FORM',
    'MINIMAL_MARKS_NO_ASSIGNABLE_CONTOUR', 'DOTTED_OR_FRAGMENTARY_DRAWN_FORM',
    'OUTLINED_DRAWN_FORM_PRESENT',
}
ROW_KEYS = {
    'source_ordinal', 'source_line_label', 'printed_table_memberships',
    'review_status', 'drawing_observation', 'canonical_type_admitted',
    'verified_glyph', 'analysis_eligible',
    'selected_marker_target', 'drawing_table_comparison',
}


def load_review(root=ROOT):
    root = Path(root)
    return [json.loads((root / p).read_text(encoding='utf-8')) for p in PATHS]


def build(root=ROOT):
    root = Path(root)
    review, index, table, acquisition, counts = load_review(root)
    for key in ['record_id', 'edition_id', 'source_id']:
        if review[key] != index[key] or review[key] != table[key]:
            raise ValueError('Source review has drifted across edition namespaces')
    if review['source_instances_not_independent'] is not True:
        raise ValueError('Same-article witnesses cannot become independent evidence')
    for key, expected in [('drawing_figure_sha256', index['figure_sha256']),
                          ('table_figure_sha256', table['consulted_figure_sha256'])]:
        if review[key] != expected:
            raise ValueError('Source review figure pin changed')
        if not any(f['sha256'] == expected and f['inspection_status'] == 'VISUALLY_INSPECTED'
                   and f['redistributed'] is False for f in acquisition['additional_figures']):
            raise ValueError('Review requires an inspected, unredistributed source figure')
    memberships = defaultdict(list)
    for row in table['rows']:
        for bucket, positions in enumerate(row['drawn_variant_position_groups'], 1):
            for ordinal in positions:
                memberships[ordinal].append({
                    'edition_sign_label': row['edition_sign_label'],
                    'drawn_variant_bucket': bucket,
                    'parenthetical_marker_present': ordinal in row['source_parenthetical_marker_positions'],
                })
    lines = {p: line['source_line_label'] for line in index['lines']
             for p in range(line['first_source_ordinal'], line['last_source_ordinal'] + 1)}
    rows = review['ordinals']
    if [r['source_ordinal'] for r in rows] != list(range(1, 124)):
        raise ValueError('Review must retain all 123 source ordinals exactly once')
    examined = set()
    observations = Counter()
    comparisons = Counter()
    for row in rows:
        p = row['source_ordinal']
        if set(row) != ROW_KEYS or type(p) is not int:
            raise ValueError('Only bounded source-review fields belong in ordinal records')
        if row['source_line_label'] != lines[p] or row['printed_table_memberships'] != memberships[p]:
            raise ValueError('Source review changed literal numbering/table claims')
        if row['canonical_type_admitted'] is not None or row['verified_glyph'] is not False or row['analysis_eligible'] is not False:
            raise ValueError('Drawing review cannot promote native glyphs or eligible sequences')
        observation = row['drawing_observation']
        if observation is None:
            raise ValueError('Every source position requires its drawing comparison disposition')
        if set(observation) != {'category', 'description', 'locator', 'ancient_surface_status_adjudicated'}:
            raise ValueError('Only attributed drawing observations belong in this review')
        if row['review_status'] != 'SOURCE_DRAWING_AND_TABLE_INSPECTED' or observation['category'] not in CATEGORIES:
            raise ValueError('Unknown source-drawing review disposition')
        if observation['ancient_surface_status_adjudicated'] is not False or not observation['description'] or not observation['locator']:
            raise ValueError('Drawing markers cannot certify ancient damage status')
        if type(row['selected_marker_target']) is not bool:
            raise ValueError('Marker target flag must be explicit')
        if row['selected_marker_target']:
            examined.add(p)
        elif observation['category'] != 'OUTLINED_DRAWN_FORM_PRESENT':
            raise ValueError('Detailed marker observation lacks selected target scope')
        labels = [m['edition_sign_label'] for m in memberships[p]]
        expected_status = ('TABLE_TYPE_UNASSIGNED' if not labels else
                           'CONFLICTING_PRINTED_TYPES' if len(labels) > 1 else
                           'PARTIAL_DRAWING_COMPATIBLE_WITH_PRINTED_TYPE' if row['selected_marker_target'] else
                           'DRAWING_TABLE_FORM_COMPATIBLE')
        comparison = row['drawing_table_comparison']
        if set(comparison) != {'status','literal_type_labels','native_identity_certified','independent_confirmation'} or comparison['status'] != expected_status or comparison['literal_type_labels'] != labels:
            raise ValueError('Source drawing comparison changed or silently resolved literal type claims')
        if comparison['native_identity_certified'] is not False or comparison['independent_confirmation'] is not False:
            raise ValueError('Same-source drawing compatibility cannot certify native glyph identities')
        comparisons[comparison['status']] += 1
        observations[observation['category']] += 1
    if examined != TARGETS:
        raise ValueError('Selected inspection scope changed; inspect and revise the source audit explicitly')
    proposals = []
    for proposal in review['candidate_errata']:
        literal = proposal['literal_table_claim']
        old, new = literal['source_ordinal'], proposal['candidate_replacement_ordinal']
        label = literal['edition_sign_label']
        if old not in examined or new not in examined or not any(m['edition_sign_label'] == label for m in memberships[old]):
            raise ValueError('Candidate erratum lacks inspected endpoints and a literal source claim')
        if proposal['status'] != 'PROPOSED_SOURCE_INTERNAL_ERRATUM_NOT_ADOPTED' or proposal['canonical_change_applied'] is not False or proposal['source_independent_confirmation'] is not False:
            raise ValueError('Candidate source erratum was silently adopted or independently certified')
        if proposal['counterfactual_counts_are_not_observed'] is not True or not proposal['evidence']:
            raise ValueError('Erratum scenario must retain its evidentiary limits')
        scenario = {p: [m['edition_sign_label'] for m in ms] for p, ms in memberships.items()}
        scenario[old].remove(label)
        scenario.setdefault(new, []).append(label)
        proposals.append({
            'id': proposal['id'], 'status': proposal['status'],
            'hypothetical_replacement': {'type_label': label, 'from_ordinal': old, 'to_ordinal': new},
            'counterfactual_only': {
                'distinct_table_ordinals': sum(bool(ms) for ms in scenario.values()),
                'collisions': [p for p, ms in sorted(scenario.items()) if len(ms) > 1],
                'unassigned_ordinals': [p for p in range(1, 124) if not scenario.get(p)],
            },
            'literal_register_changed': False,
        })
    claims = {a['id']: a for a in counts['assertions']}
    extra = len(rows) - claims['BYB-A-D1930-SURVIVING']['value'] - claims['BYB-A-D1930-LOST']['value']
    for hypothesis in review['count_reconciliation_hypotheses']:
        if hypothesis['status'] != 'UNRESOLVED_SOURCE_INTERNAL_HYPOTHESIS' or hypothesis['canonical_count_change_applied'] is not False:
            raise ValueError('Count hypothesis cannot become a source-count correction')
    return {
        'format': 'byblos-facsimile-review-audit-v2',
        'input_hashes': {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in PATHS},
        'source_ordinals_joined': len(rows), 'source_drawing_positions_compared': len(rows),
        'selected_marker_targets_inspected': len(examined),
        'other_drawn_form_comparisons': len(rows) - len(examined),
        'number_and_table_join_only_positions': 0,
        'drawing_table_comparison_counts': dict(sorted(comparisons.items())),
        'drawing_observation_counts': dict(sorted(observations.items())),
        'all_table_gaps_have_drawing_review': {o['source_ordinal'] for o in index['table_gap_observations']} <= examined,
        'candidate_erratum_scenarios': proposals,
        'source_count_arithmetic': {
            'numbered_facsimile_positions': len(rows),
            'reported_surviving_signs': claims['BYB-A-D1930-SURVIVING']['value'],
            'reported_certainly_lost_positions': claims['BYB-A-D1930-LOST']['value'],
            'arithmetic_difference': extra, 'ancient_count_reconciliation_established': False,
        },
        'canonical_types_added': 0, 'verified_sequences_added': 0,
        'independent_reviews_added': 0, 'frequency_inference_allowed': False,
        'boundary': 'Source drawing/table comparisons and arithmetic only. Literal table assertions remain intact. Candidate errata, ancient damage, native glyph normalization, independent collation and the later survey count remain unadjudicated.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = json.dumps(build(), ensure_ascii=False, indent=2) + '\n'
    target = ROOT / 'research/stele-a-facsimile-review-audit.json'
    if args.check:
        if target.read_text(encoding='utf-8') != output:
            raise SystemExit('Facsimile review audit stale')
        print('123 source drawing/table comparisons replay with 18 detailed marker targets and no admission.')
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
