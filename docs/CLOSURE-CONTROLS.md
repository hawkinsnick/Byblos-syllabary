# Safe printed-type lookup for the 1930 source

The lookup covers 123 printed ordinal positions. It excludes ordinal 32, which appears under both VIII and XIX, and eight unassigned ordinals: 14,27,34,40,41,42,92,95. Their `unambiguous_printed_type` is null. The remaining 114 entries are unambiguous memberships in the literal source table; they are not 114 certified surviving signs.

```sh
python scripts/evidence_query.py --record BYB-A --collection catalogue
python scripts/evidence_query.py --record BYB-A-D1930-ordinal-032 --collection closure-controls
python scripts/evidence_query.py --record BYB-A-D1930-ordinal-092 --collection closure-controls
```

No 32-to-92 erratum is adopted. The literal type table, facsimile numbering and source assertions remain unchanged. This completes ACD-017's exclusion criterion; resolving the publication discrepancy or assigning signs requires separate source evidence and review. Canonical sign identity admission remains false for every row.

## Replay and scope

```sh
python scripts/closure_controls.py --check
python scripts/test_closure_controls.py
```

The tests exercise actual researcher queries, exclusions/nulls and source-pin integrity, and reject inconsistent input evidence. Software controls establish no new expert approval, source reading, material determination or physical identity.
