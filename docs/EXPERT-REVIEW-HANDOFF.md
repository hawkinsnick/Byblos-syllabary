# Byblos source-review handoff

Snapshot 1.3.3, 5 October 2026 UTC. This is a focused review packet, not a certified corpus or a claim that all accessible scholarship has been exhausted. No independent reviewer has completed these checks.

## What the final pass established

Ten broad line correspondences connect the Dunand 1930 stele drawing to Dhorme 1946 figure 3. The later drawing has no ordinal labels, and its copies depend on Dunand photographs. Four focused comparisons cover 32, 92, 27 and 40–42. The barred motif is compatible in the later eighth band, while central damage prevents a certified counterpart for 32. Neither the proposed 32/92 correction nor the lost/surviving count explanation is adopted.

The historical target register identifies 103 display segments: 98 horizontal bands and five columns in fifteen display panels across ten figures. IDs express project display order only. They add no canonical ancient lines, surfaces, sign counts or sequences. Figure 9 upper-left inspection uses the full p. 33 image because the standalone crop truncates that panel. Qualified h/j traces remain outside the main target count.

## Count questions for source collation

| Label | Historical article count | Survey count convention | Requested determination |
|---|---|---|---|
| BYB-A | 119; Dhorme p. 23 | 123 | Does the later edition explain ordinal 27, the 119 surviving plus three lost convention, or the VIII 32/92 collision? Inspect original table, numbered drawing, later plate and physical image. |
| BYB-B | 41; Dhorme p. 34 | 43 = 39 signs + 4 dividers | Identify which dividers each source includes: historical 41 and three divider positions versus survey 39 signs plus four dividers. Do not assume that 41 includes or excludes the historical dividers. |
| BYB-D | 461; Dhorme p. 12 | approximately 457; 3 numerals additional | Identify the three additional numeral marks and the later reading/count policy. Survey approximately 457 plus three numerals is not exactly the historical 461; approximation prevents an exact one-sign discrepancy claim. |
| BYB-G | 38; Dhorme p. 27 | 40 | Separate remaining signs, damaged traces and columns counted as textual. Five drawn columns do not settle six reported columns / five certainly textual. |
| BYB-H | 6; Dhorme p. 28 | 7 | Distinguish six qualified forms, seven survey signs, three main drawn bands and the trace below the lowest divider. Do not certify the trace as an extra text line. |
| BYB-I | 84 (derived face sum); Dhorme p. 31 | approximately 96 | Check face inventories and damaged-form inclusion. Historical 33 + 51 = 84 is a derived sum; survey approximately 96 uses an unreconciled convention. |

Historical count voices are recorded in `research/dhorme-1946-source-joins.json`: g is Dhorme descriptive prose; the other five are Dunand statements quoted by Dhorme. These are not six directly inspected Dunand book pages. Source type totals are also separate; no merged sign repertoire is admitted.

## Review beyond counts

1. Verify the 1930 VIII table entry and the unnumbered later motif against the actual 1945 plate and an authorized photograph. Record whether the evidence supports 92, 32 or another explanation; retain source assertions even if a correction is eventually adopted.
2. Establish physical identity and faces using museum records. In particular, h/j may be one stele; fifteen drawing panels do not certify fifteen surfaces. Left/right panel display order must not silently become recto/verso.
3. Resolve g/h layout, m direction and n first-line discrepancies at their exact source locators. Dhorme figures cover a–j only and cannot settle later k–n readings.
4. Review candidate inscription membership, damage and sign identity before admitting any continuous native sequence. Historical phonetic values and translations remain excluded.

## Evidence and replay

- `research/stele-a-dependent-drawing-comparison.json`: ten broad line comparisons and four focused targets, with pinned source assets.
- `research/historical-layout-targets.json`: unique figure/panel/band targets and crop-corrected inspection route.
- `research/final-source-pass-audit.json`: reproducible scope, source hashes and count-policy questions.
- `docs/STELE-A-SOURCE-REVIEW.md`: earlier literal table and marker review.
- `docs/SOURCE-RECONCILIATION.md`: source lineage, rights and unresolved catalogue joins.

Run `python scripts/audit_final_source_pass.py --check`, the existing source audits, and `python -m unittest discover -s tests`. These checks validate structured evidence and prevent inappropriate promotion; they do not substitute for independent epigraphic review.

Source routes: [Dunand 1930](https://www.persee.fr/doc/syria_0039-7946_1930_num_11_1_3456) and [Dhorme 1946](https://www.persee.fr/doc/syria_0039-7946_1946_num_25_1_4447). Source copies remain private; use publisher access. Consult `research/core-primary-access-routes.json` for Dunand edition discovery routes.

## Disposition and pivot

The agreed additional pass is complete. Pause Byblos at this scoped checkpoint and assess another thin corpus. Direct Dunand 1945/1978 plate access, lawful physical images, source permissions and independent review are concrete dependencies for stronger readings. Further accessible literature and provider identity work remain open; no terminal pre-expert maximum, exhaustive coverage or scientific 1.0 claim is granted.
