"""Derived citation inventory; counts describe usage, never confidence."""
from collections import Counter
from .core import audit
from .admission import evidence_digest


def provenance_report(bundle, source_id=None):
    if not audit(bundle)['structure_valid']:
        raise ValueError('Provenance requires structurally valid data')
    sources = {s['id']: s for s in bundle['sources']['sources']}
    if source_id is not None and source_id not in sources:
        raise ValueError('Unknown source: ' + str(source_id))
    uses = []

    def walk(value, path, owner):
        if isinstance(value, dict):
            # Evidence objects carry explicit field bindings. Other source links
            # describe context, counts or leads, not field-bound observations.
            if 'source_id' in value and isinstance(value['source_id'], str):
                sid = value['source_id']
                role = 'field_evidence' if 'fields' in value and 'locator' in value else 'source_reference'
                uses.append(dict(source_id=sid, role=role, owner=owner,
                                 path=path + '/source_id', locator=value.get('locator'),
                                 fields=value.get('fields', [])))
            for key, item in value.items():
                pointer = path + '/' + key.replace('~', '~0').replace('/', '~1')
                if key in ('primary_edition_lead', 'discovery_source', 'project_evidence_source_id', 'metadata_source_id') and isinstance(item, str):
                    uses.append(dict(source_id=item, role=key, owner=owner, path=pointer,
                                     locator=value.get('discovery_locator') if key == 'discovery_source' else value.get('locator'), fields=[]))
                elif key == 'source_ids' and isinstance(item, list):
                    for i, sid in enumerate(item):
                        uses.append(dict(source_id=sid, role='context_source', owner=owner,
                                         path=pointer + '/' + str(i), locator=None, fields=[]))
                walk(item, pointer, owner)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                child_owner = owner
                if isinstance(item, dict) and isinstance(item.get('id'), str):
                    # Full container path namespaces equal IDs in different tables.
                    child_owner = path + ':' + item['id']
                walk(item, path + '/' + str(i), child_owner)

    for key, value in sorted(bundle.items()):
        walk(value, '/' + key, '/' + key)
    uses.sort(key=lambda u: (u['source_id'], u['path'], u['role']))
    unresolved = [u for u in uses if u['source_id'] not in sources]
    inventory = []
    for sid, source in sorted(sources.items()):
        linked = [u for u in uses if u['source_id'] == sid]
        inventory.append(dict(source_id=sid, citation=source['citation'],
                              consultation=source['consultation'], rights=source['rights'],
                              role_counts=dict(sorted(Counter(u['role'] for u in linked).items())),
                              uses=linked))
    if source_id is not None:
        inventory = [row for row in inventory if row['source_id'] == source_id]
    return dict(format='byblos-provenance-v1', evidence_sha256=evidence_digest(bundle),
                selected_source=source_id, sources=inventory, unresolved_references=unresolved,
                interpretation='Derived links only. Field evidence records attribution, not correctness. '
                'Source references, discovery citations and edition leads are not independent corroboration. '
                'Consultation depth and rights are recorded declarations; usage counts are not confidence scores. '
                'Paths address this exact snapshot; owners are namespaced by their container.')
