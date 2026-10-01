# Scientific 1.0 admission policy

Implemented in `byblos/admission.py`; exercised by synthetic positive and negative
cases in `tests/test_admission.py`. The actual corpus remains blocked.

An exhaustive claim means complete **within a stated, independently reviewed scope
and cutoff date**. It cannot mean no future discoveries or publications are possible.
The software checks declarations and their consistency; reviewers must assess truth,
research adequacy, rights and epigraphic quality.

## Required evidence

`coverage.admission_audit` must contain policy version 1, a cutoff no later than
the snapshot date, inclusion and exclusion criteria, scope evidence, and contributor
identities. `source_dispositions`, `bibliography_dispositions` and
`count_reconciliations` must cover every registered ID exactly once. Each disposition
needs `id`, `status` (`collated` or `excluded`), a rationale and attributable evidence.
Calling an unread source collated is rejected. An exclusion is a documented scope
decision, subject to independent review, not evidence that its contents are irrelevant.

The search protocol must record databases, queries, languages, date range,
citation chaining, limitations and evidence. A hit list alone does not establish
systematic coverage. Review every catalogue membership decision, including disputed
and excluded records. Complete every core object's identification, its surface
inventory, direct edition collation and every recorded line of its linked sequence.
All crosswalk entries require evidence for verification or explicit exclusion with
a reason. All research gaps require evidenced resolutions.

Verified transcriptions require documented origin (`independent_collation` or
`imported`), `creator_ids`, `source_version`, and `normalization_log` (an explicit
empty list means no normalization). Imported sequences require a separately registered,
rights-supported `encoding_map` asset. Asset permission and source access remain
separate. Font licences cannot supply a dataset licence.

## Independent review records

A record must include a stable reviewer identity, name, expertise, review date,
durable report or correspondence reference, exact scope, independence declaration,
decision, attributable evidence and `reviewed_bundle_sha256`. Contributor identities
must be declared; self-review cannot satisfy independent approval. A specialist must
check independence and suitability beyond these declarations. AI verification does
not constitute independent specialist review.

Obtain the current digest from `python -m byblos audit` (`review_evidence_sha256`).
It uses SHA-256 over compact, sorted-key UTF-8 JSON (`ensure_ascii=False`). The digest
binds the entire data bundle, including versions, sources, tokens and scope decisions,
except review rows, release counters/claim flags, catalogue `review_status`, and
transcription `status`. These exceptions allow approval to promote reviewed flags
without invalidating itself. Any other data change requires new approval. Retain
the reviewed Git commit in the durable report too. A checksum is not a signature.

Scopes are individual `records`, individual `transcriptions`, and
`{"entity_type": "admission", "id": "scientific-1.0"}` for the final coverage
assessment. Populate real review records only after review occurs. Declarations in
synthetic tests are fixtures, never evidence for this project.

## Enable the claim

Set `exhaustive_claim_allowed` only after all admission requirements are met.
Structural validation rejects premature claims. `audit --require-1-0` returns 2
until every gate passes, including structure, complete sequences, independent review,
objects, surfaces, crosswalk, resolved research gaps and admission evidence.

The positive test proves that this policy has an attainable admission path. It
does not prove the real corpus meets it. Publication must retain scope, cutoff,
limitations, underlying citations, asset rights and correction history.
