# Source reconciliation checkpoint — 4 October 2026

Fourteen Dunand core labels now have precise primary-edition locators **as reported by Vita and Zamora (2018)**. Their pages have not all been inspected directly in the original editions. The survey and the original edition are linked sources, not independent confirmations.

## Evidence growth

The native surface register grows from seven to eighteen reported surfaces, covering thirteen of fourteen core labels. It now supplies 126 reported line targets for pending review. All sign sequences remain unverified. Blank, damaged, uncertain and nontextual rows must be resolved when collating the original plates.

`research/core-edition-locators.json` records the survey page, reported edition pages, material, line/face layout and qualified direction for every core label. `research/edition-locator-audit.json` binds that table to the native catalogue and surface register by byte hashes.

`research/core-field-provenance-audit.json` now separates direct primary inspection from reported locators at field level. All fourteen core labels have survey-reported edition locators. Only BYB-A presently has directly inspected primary metadata (selected factual fields from Dunand 1930); no core label has a directly collated corpus-edition sequence, verified sign sequence, or established museum/object identifier. Direct metadata inspection is not promoted into sign-level verification.

`research/core-publication-genealogy-audit.json` reconciles the institutional Mnamon genealogy against the native catalogue: ten labels (`a`–`j`) belong to the 1945 publication cohort and four (`k`–`n`) to the 1978 cohort. The resulting fourteen publication labels are not asserted to be fourteen monuments because `h` and `j` may belong to one stele. The audit deliberately leaves physical-monument bounds unset.

`research/core-counting-unit-ledger.json` unifies the incompatible denominators without collapsing them: 14 publication labels in two cohorts; 13 labels represented by 18 line surfaces; 126 reported line targets; one column-only label (`g`) with six reported columns, only five certainly textual; zero verified sequences; and no certified physical-monument count.

`research/core-primary-access-routes.json` resolves catalogue-level access identities for both core editions without claiming page inspection. Dunand's 1945 *Byblia Grammata* is cross-identified as Open Library **OL6188790M**, Internet Archive item **bybliagrammatado0000duna**, LCCN **55042246**, OCLC **1191221**, and Google Books **RnYtAAAAMAAJ** (xix + 200 pages); the available Internet Archive route is access-restricted/borrow and Google Books exposes metadata/snippets, not a collated edition. Dunand's later article is Tübingen KeiBi **KEI00067546 / KeiBi 43:205**, *Bulletin du Musée de Beyrouth* 30, pp. 51–59, four figures and two plates, nominally 1978 but recorded as appearing in 1981. `research/core-primary-access-route-audit.json` binds these three catalogue records to all ten 1945 labels and four 1978 labels. It adds zero inspected primary pages, verified sequences, or physical identities.

`research/dunand-1978-bibliographic-conflict-audit.json` preserves a narrower unresolved conflict: Mnamon reports pp. 52–58, while KeiBi reports pp. 51–59 and an appearance year of 1981 for the nominal 1978 article. The shared span is 52–58; boundary pages 51 and 59 are disputed. The union 51–59 is an acquisition target only, not a resolved citation. No appearance year, content, plate, or sequence is independently certified until the physical article is inspected.

```sh
python scripts/check_edition_locators.py --check
python scripts/audit_core_provenance.py --check
python scripts/audit_core_genealogy.py --check
python scripts/audit_core_counting_units.py --check
python scripts/audit_core_access_routes.py --check
python scripts/audit_dunand_1978_bibliography.py --check
python -m byblos validate
python -m byblos release-check
python -m byblos review-packet
python -m unittest discover -s tests
```

## Preserve these distinctions

- **g:** six reported columns, only five certainly textual. Do not invent six lines to fit the current line-based surface model.
- **f:** reported direction differs by face: A right-to-left, B left-to-right. Preserve the authors' inferential qualification.
- **m:** left-to-right is conditional on sign orientation, not independently reviewed certainty.
- **h/j:** possible parts of one inscription; fourteen edition labels are not fourteen certified physical objects.
- **j:** the survey prints a descending edition-page range and a figure caption referring to f. Those source anomalies remain visible pending primary-plate inspection.
- **counts:** fourteen explicitly enumerated Dunand labels differ in scope from the survey's approximate fifteen-text summary and additional candidate discussion. This explains a possible scope distinction; it does not settle every provider discrepancy or admit a fifteenth core object.

Source: Juan-Pablo Vita and José-Ángel Zamora, “The Byblos Script,” in *Paths into Script Formation in the Ancient Mediterranean*, SMEA NS Supplemento 1 (2018), pp. 75–102, especially pp. 76–85. This project publishes factual metadata and original summaries with source locators. The supplied article and its images are not redistributed.

## Remaining frontier

Inspect lawful copies of Dunand's original editions and plates; the exact catalogue routes now distinguish borrow-restricted, metadata/snippet-only and bibliographic-only access states. Establish museum/object identities; resolve provider face/variant crosswalks; collate sign sequences and uncertain directions. Software integrity, catalogue discovery and expanded review targets do not establish scientific corpus 1.0 or exhaustive coverage.

## Digital catalogue access check

WorldCat digital record **OCLC 1244511616** (eBook, 1945 [i.e. 1946]) is distinct from the print record OCLC 1191221. Its “Access free” link leads to the same Internet Archive item **bybliagrammatado0000duna**, whose public metadata reports `Access-restricted-item: true`. The 264 scan-page count is distinct from xix + 200 printed pages and from inscription counts. Checked 4 October 2026 at https://search.worldcat.org/oclc/1244511616 and https://archive.org/details/bybliagrammatado0000duna . This route supplies no collated edition pages or plates; lawful delivery remains the barrier.

## Primary numbering and source structure — 4 October 2026

The openly accessible Dunand 1930 article supplies a bounded primary-source pilot for stele a. Twelve page views were acquired privately, including plate I and its verso; all twelve were visually inspected in this checkpoint. The registered selected sign groups I, II, IV, V and VI contain fourteen source-numbered position assertions. One repeated three-position span is numerically consistent with those groups. This does not establish independently verified glyph identities, a complete transcription, or a reading.

The article reports 119 surviving signs, three certainly lost positions and 38 grouped types. Vita and Zamora report 123 visible or partly visible signs and a qualified type count of 34+3. These are retained as source-specific claims with unresolved counting conventions. All 38 numeric table rows are now registered separately, retaining 55 drawn-variant buckets. The table has 116 memberships across 115 distinct ordinals, a duplicated position 32 and eight unassigned ordinals (14, 27, 34, 40, 41, 42, 92, 95). These require numbered-facsimile reconciliation, not automatic loss classification. Four parenthetical markers remain unnormalized.

All fourteen survey core entries now have typed count assertions, retaining approximate counts, numerals and dividers. A pinned OCBI source inspection covers all 43 provider entries using metadata only. Its 15 core entries map provisionally to 14 labels because f has separate faces. Provider row counts disagree with the survey's total layout for g and h; m has a direction conflict; n's numeric line agreement does not certify the first line's reading. These discrepancies are explicit review targets.

No primary scans, provider readings, code or fonts are redistributed. Applicable OCBI corpus terms remain unresolved. The five native sign records are edition-specific type labels with source ordinals, no encoded shapes or sound values, and no independent certification. Verified full sequences remain zero.

Replay the new checkpoint:

```sh
python scripts/audit_source_comparison.py --check
python scripts/audit_numbered_assertions.py --check
python scripts/audit_type_table.py --check
python scripts/build_current_status.py --check
```

`inspect_ocbi_structure.py --source-file PRIVATE_PATH --check` additionally reproduces the provider metadata from the exact upstream Git blob recorded in `research/ocbi-structure-inspection.json`. The private source is deliberately absent from the repository. Acquisition digests document consulted copies; they do not grant rights or establish independent review.

The original 710-pixel page led to two pilot row-IV number misreads (67/104); the advertised original figure resolved them to 61/110 before merge. The full table audit now cross-checks the native pilot, and a regression test rejects the earlier values. The correction is retained in the numeric table register.

`research/stele-a-facsimile-number-index.json` now indexes all ten source line spans, from ordinal 1 through 123, directly from the advertised p. 2 facsimile. All eight table gaps have source-line review targets. This source numbering includes damaged/empty indicated positions and does not equal the reported surviving-sign count. The numbered facsimile, the original table figure and plate photograph have private acquisition digests; none of those image bytes is redistributed. Glyph identities, damaged traces and the position-32 conflict still require reading-specific collation.

## Selected facsimile review — 5 October 2026 UTC

The source ordinal review joins all 123 numbered positions to the unchanged literal type table. Eighteen selected drawing-marker targets were inspected: all eight unassigned table numbers, the position-32 conflict, the four parenthetically marked table positions and additional hatched/dotted forms. The review was then extended through all ten lines: 105 other outlined forms have drawing/table-variant compatibility dispositions. The aggregate dispositions are 105 ordinary compatibility, nine partial-form compatibility, one printed-type conflict and eight unassigned. Drawing comparisons do not certify native glyph identities, ancient surface condition or independent review.

A candidate source-internal erratum proposes that row VIII's 32 may refer to the barred drawing at 92; the curved dotted form at 32 also has a row-XIX assertion. This candidate is not adopted. Its counterfactual would remove the duplicate and reduce eight table gaps to seven; the literal table remains at 115 distinct ordinals and retains duplicate 32. Another unadopted hypothesis tests whether the edge-only drawing at 27 accounts for the extra source ordinal beyond the reported 119 surviving plus three certainly lost. No count or loss identity is thereby resolved.

The [source review](STELE-A-SOURCE-REVIEW.md) provides a human-readable target list. Query `python scripts/inspect_stele_a.py --ordinal 32`, `--line VIII` or `--targets`. Replay `python scripts/audit_facsimile_review.py --check` and `python scripts/inspect_stele_a.py --check-report`. Proposed corrections, source drawings and ancient glyphs remain distinct.

## Historical copied witness — Dhorme 1946

Thirty-seven advertised page views were acquired privately; eleven page images were visually inspected for selected metadata. Sections/figures 1–10 map to c, d, first stele (qualified a join), g, h, j, e, i, f, b. Nine letters are printed in headings; a is an edition-locator join using pp. 71–73. The p. 5 footnote attributes the copies to Decamps de Mertzenfeld, from Dunand photographs. This is a dependent graphical witness, not independent object confirmation or inspection of Byblia Grammata.

The source records quoted counts for a (119; 38 types), b (41; faces 26+15), d (461; 64 types), h (six qualified signs; three lines, two yielding signs), i (faces 33+51; derived sum 84) and Dhorme's descriptive g count (38; 17 types; five columns). These differ from the survey's conventions and remain unreconciled. j has three complete horizontal lines, an upper partial line and a possible lower fifth line; no native line count changes. Phonetics and translations remain unadmitted.

Read `research/dhorme-1946-source-joins.json`; replay `python scripts/audit_dhorme_source_joins.py --check`. The citation of Syria X/1929 remains a source error/conflict against the inspected XI/1930 article. No historical count, heading or copied figure creates a certified archaeological identity, independent reading or verified sequence.

All ten historical figures now have layout-only inspection records. Panel display order stays separate from face labels: d is displayed 19-line panel left / 22 right; i is displayed five-line panel left / four right. These count joins do not certify physical face identity. The h drawing has traces below its lowest main divider; their textual status is unresolved. Standalone figure 9 truncates upper left-panel strokes, so the full p. 33 image is the appropriate review asset. No source figure bytes are included in the repository.

## Final agreed pass — 5 October 2026 UTC

`research/stele-a-dependent-drawing-comparison.json` records ten broad line correspondences and four focused comparisons against the unnumbered Dhorme figure. It does not settle the 32/92 or ordinal-27 hypotheses. `research/historical-layout-targets.json` expands source locations across all ten historical figures: 98 horizontal bands and five columns. IDs indicate display order; faces, sign counts and ancient reading order remain unadmitted. The full p. 33 image supplies the truncated figure-9 upper-left target. Run `python scripts/audit_final_source_pass.py --check` and consult `docs/EXPERT-REVIEW-HANDOFF.md` for the six count-policy questions and remaining dependencies. This scoped pause is not terminal pre-expert readiness.
