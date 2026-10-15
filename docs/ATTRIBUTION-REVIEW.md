# Attribution review

Stele A counting units, drawing partitions, Dunand-through-Dhorme voice and all fourteen core layout comparisons remain qualified. Numeric agreement does not validate signs.

Existing source consultation receipts and limits are inherited exactly from the referenced native packets. This pass inspects those packets, not the underlying publications afresh. No exhaustive literature search, new autopsy or independent review is claimed.

The complete selections below name the finite native collections reviewed. Other repository records and the broader literature are outside this checkpoint. Case counts are review tasks, not inscriptions, independent witnesses or fully attributed alternative pairs.

| Complete native selection | Rows |
|---|---:|
| `research/source-comparison-audit.json/core_layout_comparison` | 14 |

Use the case query to read the finding together with the complete native evidence, including any named author/publication, source locator, inspection state, qualification and source dependence. Missing metadata stays missing; a source ID alone is not proof of direct consultation.

```sh
python scripts/attribution_review.py --check
python scripts/attribution_review.py --case 'BYB-A-SIGN-COUNT'
python scripts/evidence_query.py --list attribution-review
```

| Review ID | Type | Finding | Remaining work |
|---|---|---|---|
| BYB-A-SIGN-COUNT | COUNT_OR_IDENTITY | Dunand1930 pp.3–4 and the Vita–Zamora2018 survey p.79 use different sign/repertoire units;119 surviving plus3 lost cannot silently become123 visible. | The survey side is not directly primary-page inspected in this comparison. Resolve each partly visible/lost partition and type convention. |
| BYB-A-DRAWING-PARTITION | REPRESENTATION | The drawing-partition audit does not itself establish ancient damage or a verified sign sequence. | Retain the literal label collision/gaps and unadopted relabelling hypothesis; do not convert graphic partition arithmetic into epigraphic certainty. |
| BYB-DHORME-VOICE | SOURCE_ROLE | Dhorme’s reported counts and redrawn figures depend on Dunand; the copy preparer and underlying photograph lineage are explicit. | Direct Dunand book comparison and full graphic collation remain open; proposed decipherment values are not admitted. |
| BYB-A-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-B-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-C-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-D-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-E-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-F-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-G-LAYOUT | REPRESENTATION | BYB-G retains row/column differences. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-H-LAYOUT | REPRESENTATION | BYB-H retains row/line differences. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-I-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-J-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-K-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-L-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-M-LAYOUT | REPRESENTATION | BYB-M retains opposed direction claims; matching row counts do not reconcile direction. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |
| BYB-N-LAYOUT | REPRESENTATION | Numeric layout compatibility is documentary evidence only; it does not validate signs or certify object identity. | Inspect exact source units, faces and sign contexts; label/layout agreement cannot provide independent confirmation. |

`research/attribution-review.json` pins every referenced native artifact by SHA-256 and records exact JSON pointers. `analysis/attribution-review-audit.json` is replayed by the checker. Queries reject changed input bytes before returning any case. The earlier native records remain unchanged.

Pair-attribution states describe documentary limitations, not scientific acceptance. A partial located comparison can be a real scholarly alternative without full typographic, physical-position or independent collation. `NOT_APPLICABLE` marks controls and interpretations for which a two-reading pair is not the appropriate unit. No unknown pair/witness total is replaced with zero.
