# Data model 0.4

Catalogue IDs identify inscription entries. Objects and surfaces have separate
identities; object IDs remain null until established. Edition labels remain
edition-specific. The research entities file currently has empty object, sign,
edition, transcription, review and asset arrays. Empty arrays are genuine gaps.

Evidence entries contain source_id, a precise locator, and supported fields.
An unconsulted bibliographic lead cannot support an assertion as if read directly.
Consultation of a survey supports an attributed survey report, not claimed autopsy.

## Sequence representation

An edition links source and inscription. A sign links edition and its original
sign label. A transcription links edition, inscription and a rights-supported
transcription asset. Each line links surface, explicit direction, numbered line
and ordered tokens. Tokens record position, sign_id (possibly null), alternatives,
status and evidence. Status distinguishes observed, uncertain, restored,
unreadable, gap, divider and numeral. Restorations require rationale.

Independent approval records have reviewer identity, independence declaration,
scope, status and evidence. Assertions of review are checked against these
records. The software cannot establish whether a recorded review actually occurred.

The importer/exporter must preserve this structure; it must not reverse arrays
when displaying right-to-left texts or collapse alternatives into certainty.

## Rights

Assets require scope, creator, attribution, reference and an explicit rights
status: licensed, permission_granted or original. Licenced assets need a licence
identifier; permission grants need a permission record. Software checks presence
and consistency, not legal validity.

## Gates

The scientific release audit derives counts from entities instead of accepting
hand-entered progress totals. A 1.0 audit fails when core transcriptions, core
review, object identity, surfaces, verified external mappings or research gaps
are incomplete. Exhaustiveness is admitted only when the implemented evidence policy passes.
See ADMISSION_POLICY.md for required dispositions, review digest and completeness checks.

## Compatibility

This is a Byblos-specific schema. Cross-project compatibility remains a planned
adapter, not a tested claim. Shared IDs and provenance principles do not imply
that other projects have identical schemas.

Review rows now require stable reviewer IDs, expertise, date, durable report reference and the current evidence digest. Every evidence edit invalidates old approvals. Verified sequences require explicit origin, creators, source version and normalization log; imported sequences also need a rights-supported encoding map.

## Review packet and differences (0.7)

`byblos-review-packet-v1` is a derived task format, outside the corpus research
entities. It carries the evidence digest, copied source records and pending
responses. Known lines are tasks; unknown inventories are explicitly marked.

`byblos-snapshot-diff-v1` compares complete bundles. Every change has a pointer
and before/after presence and value. ID-bearing lists match by ID; `@order`
records list-order changes. Positional token differences are not sign alignments.
