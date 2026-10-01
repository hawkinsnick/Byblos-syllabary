# Byblos syllabary research corpus

Version: 1.1.0 — stable software workflow; provisional research catalogue.

An open research project working toward exhaustive, evidence-based coverage of the
undeciphered Byblos script. Its language affiliation is unresolved. The name
“syllabary” is conventional; proposed sound values are hypotheses.

## Current coverage

- 14 reported core entries plus 25 named disputed candidates; membership remains attributed.
- 47 registered sources/leads and 25 bibliography discovery entries; consultation depth recorded individually.
- 0 verified sign sequences, 0 imported images, 0 independently reviewed records; 6 sourced surface descriptions.
- Published corpus counts remain unresolved. This is not an exhaustive corpus.
- Identifiers refer to inscription records, not necessarily distinct physical objects.

43 OCBI entry labels are mapped provisionally by label or caption; entry counts include faces and variants. One licensed photograph is registered as an external reference, with credit and licence; its inscription identity remains unverified.

Start with [the ledger](data/coverage.json), [sources](data/sources.json),
and [method and roadmap](docs/METHOD.md).

## Verify locally

Requires Python 3.10+; no third-party dependencies.

```sh
python -m byblos validate
python -m unittest discover -s tests
python -m byblos audit
python -m byblos export --output my-snapshot
python -m byblos verify-export my-snapshot
```

Passing validation establishes structural consistency, not epigraphic correctness,
rights clearance, exhaustive coverage, or peer review.

## Research principles

Each assertion needs an attributable source and locator. Record unknowns as null.
Preserve damaged signs, edition differences, and alternative identifications.
Separate observed marks, editorial reconstruction, sign classification, sound
values, and translations. Never equate signs across scripts solely by appearance.
Track objects, surfaces, inscriptions, editions, and individual sign occurrences
separately as the data model expands.

Shared provenance and export conventions are intended to support the sister
corpus projects; compatibility with their current schemas has not been verified.

## Reuse and contributions

No blanket licence is granted in this initial snapshot. Third-party material
retains its own rights. Source access does not establish redistribution rights.
No photographs, plate drawings, or third-party transcriptions are redistributed.
See the rights fields in the source register.

Submit corrections with publication/page/plate references and distinguish direct
inspection from secondhand reporting. No specialist endorsement is claimed.

## Scientific release check

```sh
python -m byblos audit --require-1-0
```

Currently exits **2**, correctly reporting unmet scientific gates. Software 1.0
is a stable local validation, contribution and export workflow. The catalogue
remains provisional and incomplete; scientific 1.0 has not been released.

Run `python -m byblos release-check` to check version consistency, source links,
export integrity and exact agreement with repository data. Run the tests separately.


[Read the generated audit](exports/REPORT.md).
The JSON bundle is lossless; CSV is a convenience catalogue view.
`python -m byblos stats` returns no eligible sequences until verified sequences
exist. It does not treat reported sign totals as digitized observations.

[Scientific 1.0 status and required evidence](docs/RELEASE_STATUS.md) | [Research conflicts](docs/FINDINGS.md) | [Data model](docs/DATA_MODEL.md) | [Rights](docs/RIGHTS.md)

The [implemented admission policy](docs/ADMISSION_POLICY.md) binds reviews to the evidence snapshot and requires complete lines, attributed coverage decisions and count reconciliation. The [acquisition and review packet](docs/ACQUISITION_AND_REVIEW.md) supplies exact edition requests, permission scope and specialist acceptance criteria. No correspondence has been sent.

## Explore, prepare review and compare

Download and extract the repository ZIP, then open `exports/index.html` for a
searchable offline catalogue. No setup, remote assets or background requests.
The [user guide](docs/USER_GUIDE.md) explains the files and researcher workflow.

```sh
python -m byblos review-packet
python -m byblos compare old-snapshot new-snapshot
```

`exports/review_packet.json` has pending tasks for all 39 records and targets
for every reported surface line. Unknown inventories remain unknown; no sign
sequences or approvals are manufactured. Snapshot differences preserve missing
versus null, record identity, ordering and original token positions.

## Evidence contributions

Researchers can use the GitHub **Evidence correction** and **Source lead** issue
forms, or the [contribution workflow](docs/CONTRIBUTING.md). Machine-readable
proposals bind to a specific evidence snapshot, preserve expected current values,
and remain pending. No automatic apply or approval command exists.

```sh
python -m byblos proposal-template --record BYB-A
python -m byblos check-proposal my-proposal.json
python -m byblos stage-proposal my-proposal.json --output pending-submission
python -m byblos verify-proposal pending-submission
```

The exported `contribution_template.json` is intentionally incomplete until a
contributor fills identity, date and attributable changes or source leads.

Inspect source dependencies with `python -m byblos provenance` or filter with
`python -m byblos provenance --source mnamon-merlo`. See [provenance audit](docs/PROVENANCE.md).

## Inspect evidence and acquisition work

```sh
python -m byblos evidence-ledger
python -m byblos acquisition-queue
```

The [evidence ledger guide](docs/EVIDENCE_LEDGER.md) explains field unknowns,
citation bindings and the reproducible source inspection queue. These reports
organize existing evidence; they do not infer expert approval or missing readings.
