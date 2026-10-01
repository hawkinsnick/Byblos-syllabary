"""Field-level evidence inventory and acquisition queue; no scientific scoring."""
import copy
from collections import Counter
from .core import audit
from .admission import approved, evidence_digest
from .provenance import provenance_report

FIELDS = ('edition_label', 'display_name', 'material', 'object_type', 'membership',
          'membership_note', 'dimensions_mm', 'discovery_context', 'museum_id',
          'reported_excavation_identifier')


def evidence_ledger(bundle):
    report = audit(bundle)
    if not report['structure_valid']:
        raise ValueError('Evidence ledger requires structurally valid data')
    sources = {s['id']: s for s in bundle['sources']['sources']}
    records = []
    counts = Counter()
    for index, record in sorted(enumerate(bundle['catalogue']['records']), key=lambda pair: pair[1]['id']):
        claims = []
        for field in FIELDS:
            value = record.get(field)
            status = 'not_recorded' if field not in record else 'unknown' if value is None else 'asserted'
            citations = []
            if status == 'asserted':
                for i, evidence in enumerate(record['evidence']):
                    if field in evidence['fields']:
                        source = sources[evidence['source_id']]
                        citations.append(dict(source_id=source['id'], locator=evidence['locator'],
                                              consultation=source['consultation'],
                                              evidence_path=f'/catalogue/records/{index}/evidence/{i}'))
            counts[status] += 1
            claims.append(dict(field=field, path=f'/catalogue/records/{index}/{field}',
                               status=status, value=copy.deepcopy(value), citations=citations,
                               distinct_cited_sources=len({c['source_id'] for c in citations})))
        records.append(dict(record_id=record['id'], membership=record['membership'],
                            evidence_level=record['evidence_level'],
                            current_independent_record_approval=approved(bundle, 'records', record['id']),
                            claims=claims,
                            nested_claims=copy.deepcopy({k: record.get(k) for k in
                                ('date_claims', 'direction_claims', 'reported_museum_identifier')})))
    return dict(format='byblos-evidence-ledger-v1', version=report['version'],
                evidence_sha256=evidence_digest(bundle), field_status_counts=dict(sorted(counts.items())),
                records=records,
                interpretation='Fixed catalogue field inventory, not all scientific assertions. '
                'Not recorded differs from explicit null/unknown. Nested hypotheses retain their original evidence. '
                'Distinct cited sources are not necessarily independent. Attribution and approval declarations '
                'do not prove truth; no credibility or decipherment score is computed.')


def acquisition_queue(bundle):
    provenance = provenance_report(bundle)
    tasks = []
    for source in provenance['sources']:
        records = sorted({u['owner'].split(':', 1)[1] for u in source['uses']
                          if u['owner'].startswith('/catalogue/records:')})
        if source['consultation'] in {'not_consulted', 'metadata_only', 'abstract_only'}:
            tasks.append(dict(source_id=source['source_id'], citation=source['citation'],
                              consultation=source['consultation'], linked_record_ids=records,
                              linked_record_count=len(records), status='pending_acquisition_or_inspection',
                              source_usage_paths=[u['path'] for u in source['uses']],
                              required_outputs=['Record lawful access and exact edition/version.',
                                  'Record inspected pages/plates and precise field-level citations.',
                                  'Assess separate reuse terms before importing images or sequences.']))
    tasks.sort(key=lambda task: (-task['linked_record_count'], task['source_id']))
    bibliography = [copy.deepcopy(e) for e in bundle['bibliography']['entries']
                    if e.get('primary_text_examined') is not True]
    bibliography.sort(key=lambda row: row['id'])
    return dict(format='byblos-acquisition-queue-v1', version=bundle['coverage']['version'],
                evidence_sha256=evidence_digest(bundle), source_tasks=tasks,
                unexamined_bibliography_leads=bibliography,
                interpretation='Ordering uses direct catalogue citation/lead linkage counts, then source ID. '
                'Counts are workload reach, not scientific importance or independent corroboration. '
                'Sources consulted only in selected sections may still require more inspection; absence from '
                'this queue does not mean fully collated. Bibliography and source tasks may overlap. '
                'No acquisition, permission request or expert approval is performed by generating this queue.')
