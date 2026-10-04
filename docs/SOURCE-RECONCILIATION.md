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
