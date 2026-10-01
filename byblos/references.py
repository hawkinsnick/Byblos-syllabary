"""Reference-only research planning while publication rights remain unresolved."""
import copy
from .core import audit, rights_supported
from .admission import evidence_digest
from .provenance import provenance_report
from .workflow import review_packet
from .evidence import evidence_ledger


def reference_workflow(bundle):
    report = audit(bundle)
    if not report['structure_valid']:
        raise ValueError('Reference workflow requires structurally valid data')
    uses = {s['source_id']: s for s in provenance_report(bundle)['sources']}
    rows = []
    for source in sorted(bundle['sources']['sources'], key=lambda s: s['id']):
        linked = sorted({u['owner'].split(':', 1)[1] for u in uses[source['id']]['uses']
                         if u['owner'].startswith('/catalogue/records:')})
        assets = [dict(asset_id=a['id'], kind=a.get('kind'), delivery=a.get('delivery'),
                       rights=copy.deepcopy(a.get('rights')), declared_rights_supported=rights_supported(a))
                  for a in bundle['research_entities']['assets'] if a.get('source_id') == source['id']]
        rows.append(dict(source_id=source['id'], citation=source['citation'], url=source.get('url'),
                         consultation=source['consultation'], recorded_rights=copy.deepcopy(source['rights']),
                         linked_record_ids=linked, assets=assets,
                         publication_plan='references_and_original_metadata_only',
                         copyright_determination='not_determined_by_this_report',
                         actions=['Preserve source/version and exact locators.',
                                  'Inspect only through an authorized access route.',
                                  'Record attributable factual observations and original analysis.',
                                  'Keep scans, plates, copied prose, fonts and third-party sequences out of this publication workflow.',
                                  'Assess each proposed reuse separately before changing delivery.']))
    return dict(format='byblos-reference-workflow-v1', version=report['version'],
                evidence_sha256=evidence_digest(bundle), sources=rows,
                scientific_1_0_ready=report['scientific_1_0_ready'],
                interpretation='A project publication plan, not a legal clearance or finding of infringement. '
                'Unknown, denied and unanswered permissions are not grants. Access and attribution do not '
                'establish redistribution rights. An asset declaration applies only to its recorded scope; '
                'this report never transfers that scope to other media or sequences.')


def pilot_packet(bundle, record_id='BYB-A'):
    packet = review_packet(bundle)
    tasks = [t for t in packet['tasks'] if t['record_id'] == record_id]
    if not tasks:
        raise ValueError('Unknown pilot record: ' + str(record_id))
    task = tasks[0]
    source_ids = set()
    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {'source_id', 'primary_edition_lead'} and isinstance(item, str):
                    source_ids.add(item)
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(task['record'])
    walk(task['line_targets'])
    ledger = next(r for r in evidence_ledger(bundle)['records'] if r['record_id'] == record_id)
    return dict(format='byblos-metadata-pilot-v1', version=packet['version'],
                evidence_sha256=packet['reviewed_bundle_sha256'], record_id=record_id,
                task=task, field_ledger=ledger,
                sources=[copy.deepcopy(s) for s in bundle['sources']['sources'] if s['id'] in source_ids],
                publication_plan='metadata_and_source_references_only',
                requested_review=['Check that citations support the stated metadata.',
                                  'Distinguish reported inscription labels from verified physical identity.',
                                  'Identify missing primary-edition evidence and uncertain coverage.',
                                  'Return scoped corrections; no endorsement of decipherment requested.'],
                limitations=['No scans, plates or sign sequences included.',
                             'Existing statements retain their recorded evidence levels.',
                             'Empty line targets mean unknown inventory, not zero lines.',
                             'Pending review fields are not approvals; no response is automatically admitted.'])
