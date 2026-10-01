# Byblos syllabary research corpus

Version: 0.2.0 — catalogue foundation.

An open research project working toward exhaustive, evidence-based coverage of the
undeciphered Byblos script. Its language affiliation is unresolved. The name
“syllabary” is conventional; proposed sound values are hypotheses.

## Current coverage

- 14 provisional catalogue records (a–n), reported in Mnamon's scholarly guide.
- 14 registered sources/leads and 15 bibliography discovery entries; consultation depth recorded individually.
- 0 verified sign sequences, 0 imported images, 0 independently reviewed records.
- Published corpus counts remain unresolved. This is not an exhaustive corpus.
- Identifiers refer to inscription records, not necessarily distinct physical objects.

Start with [the ledger](data/coverage.json), [sources](data/sources.json),
and [method and roadmap](docs/METHOD.md).

## Verify locally

Requires Python 3.10+; no third-party dependencies.

```sh
python scripts/validate.py
python -m unittest discover -s tests
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
