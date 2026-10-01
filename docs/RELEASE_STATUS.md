# Scientific 1.0 assessment

Current development snapshot: 0.5.0. Scientific 1.0 is **not released**.

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
7. Implement and test an audited 1.0 admission policy before enabling the
   exhaustiveness flag. The prerelease schema deliberately rejects that flag.

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
