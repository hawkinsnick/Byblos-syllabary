# Byblos syllabary research corpus

Version: 0.6.0 — research catalogue and reproducible tooling.

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

Currently exits **2**, correctly reporting unmet scientific gates. This project
has progressed through development snapshots 0.2–0.6; the original
scientific milestones are not all complete. 1.0 has not been released.

[Read the generated audit](exports/REPORT.md).
The JSON bundle is lossless; CSV is a convenience catalogue view.
`python -m byblos stats` returns no eligible sequences until verified sequences
exist. It does not treat reported sign totals as digitized observations.

[Scientific 1.0 status and required evidence](docs/RELEASE_STATUS.md) | [Research conflicts](docs/FINDINGS.md) | [Data model](docs/DATA_MODEL.md) | [Rights](docs/RIGHTS.md)

The [implemented admission policy](docs/ADMISSION_POLICY.md) binds reviews to the evidence snapshot and requires complete lines, attributed coverage decisions and count reconciliation. The [acquisition and review packet](docs/ACQUISITION_AND_REVIEW.md) supplies exact edition requests, permission scope and specialist acceptance criteria. No correspondence has been sent.
