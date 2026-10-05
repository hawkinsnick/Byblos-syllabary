"""Inspect an attributed source ordinal or line, without producing a transcription."""
import argparse
import json
from pathlib import Path
from audit_facsimile_review import build, load_review

ROOT = Path(__file__).resolve().parents[1]


def select(ordinal=None, line=None, targets=False):
    audit = build(ROOT)
    review = load_review(ROOT)[0]
    rows = review['ordinals']
    if ordinal is not None:
        if type(ordinal) is not int or not 1 <= ordinal <= 123:
            raise ValueError('Source ordinal must be an integer from 1 through 123')
        rows = [r for r in rows if r['source_ordinal'] == ordinal]
    if line is not None:
        if line not in {'I','II','III','IV','V','VI','VII','VIII','IX','X'}:
            raise ValueError('Source line must be I through X')
        rows = [r for r in rows if r['source_line_label'] == line]
    if targets:
        rows = [r for r in rows if r['selected_marker_target']]
    return {'source_id': review['source_id'], 'edition_id': review['edition_id'],
            'records': rows, 'candidate_errata': review['candidate_errata'],
            'count_hypotheses': review['count_reconciliation_hypotheses'],
            'canonical_admission': False, 'verified_sequences_added': audit['verified_sequences_added'],
            'boundary': review['boundary']}


def report():
    data = select(targets=True)
    lines = ['# Stele a: selected source drawing review', '',
             'All 123 source drawing positions have explicit comparison dispositions against the unchanged printed table and its variant buckets. Eighteen detailed marker/gap/collision targets are listed below; 105 other outlined forms have compatibility dispositions. This source drawing comparison does not certify native glyph identities, direct ancient surface condition or a verified full sequence.', '',
             '| Ordinal | Source line | Literal table type labels | Drawing observation |',
             '| --- | --- | --- | --- |']
    for r in data['records']:
        labels = ', '.join(m['edition_sign_label'] for m in r['printed_table_memberships']) or 'Unassigned'
        lines.append(f"| {r['source_ordinal']} | {r['source_line_label']} | {labels} | {r['drawing_observation']['description']} |")
    lines += ['', '## Pending source-internal explanations', '',
              'Row VIII may have printed 32 for 92: the numbered drawing has a curved dotted form at 32 and a barred form at 92. This is a proposed erratum, not an adopted correction. The literal VIII/XIX collision at 32 remains intact.', '',
              'The hatched edge position 27 may explain why numbering ends at 123 while p. 3 reports 119 surviving and three certainly lost. Positions 40–42 have only minimal marks. These are drawing observations; no ancient loss identity or surviving-count convention is certified.', '',
              'Read `research/stele-a-facsimile-ordinal-review.json` and replay `python scripts/audit_facsimile_review.py --check`. Query a position with `python scripts/inspect_stele_a.py --ordinal 32` or a line with `--line VIII`.', '', data['boundary'], '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ordinal', type=int)
    parser.add_argument('--line')
    parser.add_argument('--targets', action='store_true')
    parser.add_argument('--report', action='store_true')
    parser.add_argument('--check-report', action='store_true')
    args = parser.parse_args()
    try:
        if args.report or args.check_report:
            output = report()
            if args.check_report:
                if (ROOT / 'docs/STELE-A-SOURCE-REVIEW.md').read_text(encoding='utf-8') != output:
                    raise ValueError('Stele a source review report stale')
                print('Selected source review report replays.')
            else:
                print(output, end='')
        else:
            print(json.dumps(select(args.ordinal, args.line, args.targets), ensure_ascii=False, indent=2))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
