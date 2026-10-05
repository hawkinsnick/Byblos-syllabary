# Scientific 1.0 assessment

Current software snapshot: 1.3.2. Scientific 1.0 is **not released**.

Software 1.0 stabilizes the dependency-free local workflow and current output
formats. It does not promote catalogue assertions to verified archaeological facts.
Breaking output-format changes will use new format identifiers. Additive fields
and new export files can be introduced in minor software versions.

`python -m byblos release-check` checks repository and export consistency.
Regression tests remain a separate required check; neither replaces expert review.

The complete available-work pipeline was exercised: structural validation,
regression tests, deterministic export, checksum verification, lossless bundle
reconstruction, and analysis with no eligible sequences. The generated audit
lists the concrete evidence gaps. Tests cannot supply missing archaeological data.

## Evidence needed to close the gates

1. Inspect original editions (especially Dunand 1945 and 1978), relevant later
   studies, museum identifiers and images. Record exact page/plate references.
2. Establish objects and surfaces and resolve possible joins, count policies,
   direction assumptions and candidate duplicates.
3. Obtain an explicit licence/permission for reused OCBI sequences and their
   encoding map, or create documented independent transcriptions from evidence
   with appropriate source rights.
4. Collate every in-scope sequence and register signs without collapsing disputed
   variants or introducing canonical phonetic interpretations.
5. Obtain documented independent specialist review of both metadata and
   transcriptions. No review or permission has been invented.
6. Audit bibliography and candidate coverage against a dated, reproducible source
   inventory. Resolve gaps or document justified scope decisions with evidence.
7. Complete the evidence required by the implemented [admission policy](ADMISSION_POLICY.md)
   and obtain independent admission review before enabling the exhaustiveness flag.

## Prepared permission scope

For OCBI, establish permission to redistribute machine-readable sign sequences,
preserve edition and variant identifiers, distribute the encoding map if permitted,
publish corrections as separate attributed readings, and include the data in
public downloadable research exports. Ask separately about slide photographs,
published drawings, and fonts. Record the exact attribution and licence text.

This is a checklist for future correspondence, not a sent message or a permission
grant. No third-party communication has been sent.

## Reproduce

```sh
python -m byblos validate
python -m unittest discover -s tests
python -m byblos export --output new-snapshot
python -m byblos verify-export new-snapshot
python -m byblos audit --require-1-0
```

The final command currently exits 2. That honest blocked result preserves the
scientific standard specified for this project.

## Blocker work completed in 0.6

- The admission-policy implementation blocker is closed: a fully synthetic
  complete case passes, while missing lines, stale approvals, self-review,
  unreconciled counts and missing encoding-map rights are rejected.
- The project O-3c evidence-pointer discrepancy is resolved. Archaeological mapping
  remains provisional and the upstream provider path is retained.
- One photograph has a documented creator licence and an external asset record.
  That clears this source's declared reuse basis only; it does not clear OCBI,
  original plates or other media, and no image bytes are included.
- Source history and bibliography improved; an arrowhead candidate and additional
  chronology, volume and count conflicts are now traceable.

Original editions, item-level fragment identities, full sequences, their reuse
terms, complete coverage dispositions and actual independent specialist review
remain external evidence dependencies. The [acquisition and review packet](ACQUISITION_AND_REVIEW.md)
contains exact requests and review deliverables. Nothing was sent to third parties.

## Work continuing while external dependencies are deferred

0.7 adds an offline inspection catalogue, deterministic review-task packet and
lossless snapshot comparison. These make the current evidence and remaining work
reviewable without access to additional editions. They do not close acquisition,
sequence rights or specialist-review gates. See USER_GUIDE.md.

0.8 adds pending metadata/source proposal intake, assessment and verification,
plus GitHub issue forms. This strengthens contributor collaboration while source
permissions and specialist review remain deferred. No proposals, reviews or
new historical assertions were admitted merely by implementing this workflow.

0.9 adds exact citation tracing. Software 1.0 adds strict JSON ingestion, rejects
export symlinks and detects stale version labels or exports from a different bundle.

Software 1.1 adds field attribution and acquisition work inventories. These make
evidence dependencies easier to inspect without granting scientific approval.

1.2 extends publication discovery through publisher-checked 2026 metadata and
distinguishes partial bibliography inspection from no inspection. No new sign
sequences, archaeological identities or independent expert approvals are claimed.

1.3 adds a source-specific reference-only work plan and a pending metadata pilot
for inscription A. A media inventory enforces the current publication policy;
it is not a legal clearance. Copyright investigation and scientific gates remain open.
