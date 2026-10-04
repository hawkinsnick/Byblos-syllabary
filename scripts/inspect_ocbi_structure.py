"""Inspect a separately acquired pinned OCBI source without exporting readings."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BLOB = '3c3224f32596b493fd5bb634fff3b8000e591b14'
SOURCE_COMMIT = '69b4cc2822493146045cb9969586bf5bd9195380'
SOURCE_URL = f'https://github.com/elamicon/elamicon/blob/{SOURCE_COMMIT}/src/Scripts/Byblos.elm'
PATTERN = re.compile(
    r'\{ id = "([^"\n]+)", source = "([^"\n]+)", group = "([^"\n]+)", '
    r'dir = (\w+), plate = Just "([^"\n]+)", link = Nothing, text =\s*"""(.*?)"""', re.S)


def inspect(source_bytes, require_pin=True):
    blob = hashlib.sha1(b'blob ' + str(len(source_bytes)).encode() + b'\0' + source_bytes).hexdigest()
    if require_pin and blob != SOURCE_BLOB:
        raise ValueError('Source blob differs from the inspected pin; review a changed source explicitly')
    text = source_bytes.decode('utf-8')
    marker = 'fragments = List.map'
    if text.count(marker) != 1:
        raise ValueError('Expected exactly one fragment-definition section')
    section = text.split(marker, 1)[1].split('\nbyblos :', 1)[0]
    matches = list(PATTERN.finditer(section))
    if len(matches) != section.count('{ id ='):
        raise ValueError('Unparsed fragment definition; do not silently drop a record')
    if not matches:
        raise ValueError('No fragment definitions')
    rows = []
    labels = set()
    for i, match in enumerate(matches, 1):
        label, source, group, direction, plate, reading = match.groups()
        if label in labels or direction not in {'RTL', 'LTR', 'TDR', 'TDL', 'BTL', 'BTR'}:
            raise ValueError('Duplicate label or unsupported direction')
        labels.add(label)
        source_line = text[:text.index(marker) + len(marker) + match.start()].count('\n') + 1
        rows.append({
            'id': f'OCBI-ENTRY-{i:02}', 'provider_label': label,
            'provider_source': source, 'provider_group': group,
            'provider_direction': direction, 'provider_plate_path': plate,
            'source_line': source_line,
            'encoded_nonempty_rows': sum(bool(line.strip()) for line in reading.strip().splitlines()),
            'reading_payload_sha256': hashlib.sha256(reading.encode()).hexdigest(),
            'reading_redistributed': False,
        })
    return {
        'format': 'byblos-ocbi-structure-v1', 'checked': '2026-10-04',
        'source_id': 'ocbi-source', 'source_url': SOURCE_URL,
        'source_commit': SOURCE_COMMIT, 'source_blob': blob,
        'source_sha256': hashlib.sha256(source_bytes).hexdigest(), 'source_bytes': len(source_bytes),
        'inspection_scope': 'Pinned fragment metadata and encoded row structure; no glyph sequence or source code exported.',
        'rights': {'source_code_redistribution': 'UNRESOLVED',
                   'sequence_redistribution': 'UNRESOLVED',
                   'readme_observation': 'Pinned README promises a future permissive licence but says its text is unsettled.',
                   'readme_url': f'https://github.com/elamicon/elamicon/blob/{SOURCE_COMMIT}/README.md'},
        'entries': rows,
        'boundary': 'Encoded rows are source serialization units, not certified ancient lines or columns. Glyphs, code, fonts, plates and proposed sound values are excluded. Entry order is pinned; labels preserve original whitespace.',
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-file', type=Path, required=True,
                   help='Local lawful copy of the exact pinned Byblos.elm; kept outside this repository')
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    result = json.dumps(inspect(args.source_file.read_bytes()), ensure_ascii=False, indent=2) + '\n'
    target = ROOT / 'research/ocbi-structure-inspection.json'
    if args.check:
        if target.read_text(encoding='utf-8') != result:
            raise SystemExit('OCBI inspection is stale')
        print('Pinned OCBI metadata and row structure replay; no readings exported.')
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
