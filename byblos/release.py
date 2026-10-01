"""Repository consistency checks, distinct from scientific admission."""
import re
from pathlib import Path
from .core import load_bundle, audit, ROOT
from .export import export_texts, verify_export
from .provenance import provenance_report

MEDIA_SUFFIXES = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.tif', '.tiff',
                  '.bmp', '.svg', '.eps', '.ps', '.woff', '.woff2', '.ttf', '.otf', '.zip'}


def media_files(root):
    """Known media extensions under the repository; no legal/content inference."""
    root = Path(root)
    ignored = {'.git', '.venv', '__pycache__'}
    return sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                  if not ignored.intersection(p.relative_to(root).parts)
                  and p.is_file() and p.suffix.lower() in MEDIA_SUFFIXES)


def release_check(root=ROOT):
    root = Path(root)
    bundle = load_bundle(root)
    report = audit(bundle)
    checks = {'structure': report['structure_valid']}
    version = bundle['coverage']['version']
    checks['version_format'] = bool(re.fullmatch(r'\d+\.\d+\.\d+', version))
    checks['package_version'] = (root / 'byblos/__init__.py').read_text(encoding='utf-8').strip() == '__version__ = "' + version + '"'
    checks['citation_version'] = 'version: "' + version + '"' in (root / 'CITATION.cff').read_text(encoding='utf-8').splitlines()
    checks['readme_version'] = ('Version: ' + version + ' —') in (root / 'README.md').read_text(encoding='utf-8')
    checks['status_version'] = ('Current software snapshot: ' + version + '.') in (root / 'docs/RELEASE_STATUS.md').read_text(encoding='utf-8')
    readme = (root / 'README.md').read_text(encoding='utf-8')
    counts = report['counts']
    checks['readme_coverage_counts'] = all(label in readme for label in (
        str(counts['reported_core']) + ' reported core entries plus ' + str(counts['disputed_candidates']) + ' named disputed candidates',
        str(counts['sources_and_leads']) + ' registered sources/leads and ' + str(len(bundle['bibliography']['entries'])) + ' bibliography discovery entries'))
    errors = []
    bundled_media = media_files(root)
    checks['reference_only_media_inventory'] = not bundled_media
    if report['structure_valid']:
        checks['source_links_resolve'] = not provenance_report(bundle)['unresolved_references']
        try:
            verify_export(root / 'exports')
            checks['snapshot_integrity'] = True
        except (ValueError, OSError, TypeError, KeyError) as exc:
            checks['snapshot_integrity'] = False
            errors.append(str(exc))
        texts = export_texts(bundle)
        checks['snapshot_matches_repository'] = all(
            (root / 'exports' / name).is_file() and
            (root / 'exports' / name).read_bytes() == text.encode('utf-8')
            for name, text in texts.items())
    return {'format': 'byblos-release-check-v1', 'version': version,
            'repository_consistent': all(checks.values()), 'checks': checks, 'errors': errors,
            'bundled_media_files': bundled_media,
            'scientific_1_0_ready': report['scientific_1_0_ready'],
            'interpretation': 'Repository consistency only. Run the regression suite separately. '
            'Software version numbers do not certify scientific completeness, rights or independent review.'}
