# Evidence ledger and acquisition queue

`python -m byblos evidence-ledger` lists ten metadata fields for every catalogue
record. `python -m byblos acquisition-queue` lists source inspection tasks and
unexamined bibliography leads. Both reports are included in deterministic exports.

The field ledger distinguishes absent fields (`not_recorded`), explicit null
(`unknown`) and recorded values (`asserted`). Assertions preserve citation
locations, source IDs, consultation declarations and snapshot JSON pointers.
Repeated references to one source do not increase the distinct-source count.
Distinct authors or sources are not necessarily independent witnesses.

The ledger covers edition label, display name, material, object type, membership,
membership note, dimensions, discovery context, museum ID and reported excavation
identifier. Nested date, direction and museum hypotheses are preserved in their
original structure. It is not a universal ledger of every assertion. Record-level
independent approval uses the existing exact-snapshot review binding; no new review
or evidence grade is inferred.

The acquisition queue includes source records declared not consulted, metadata
only or abstract only. It orders tasks by unique records directly citing or linking
to each source, then source ID. This is a transparent workload ordering, not an
importance score. Sources examined in selected sections may still need extensive
collation. An absent queue entry never means acquisition or collation is complete.
Unexamined bibliography entries are listed separately and can overlap source tasks.

Generating these reports changes no evidence and sends no requests. Source
acquisition, appropriate reuse terms and independent expert evaluation remain
separate activities. Unknown object identities and absent sequences remain unknown.
