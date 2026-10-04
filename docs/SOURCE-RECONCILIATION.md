# Source reconciliation checkpoint — 4 October 2026

Fourteen Dunand core labels now have precise primary-edition locators **as reported by Vita and Zamora (2018)**. Their pages have not all been inspected directly in the original editions. The survey and the original edition are linked sources, not independent confirmations.

## Evidence growth

The native surface register grows from seven to eighteen reported surfaces, covering thirteen of fourteen core labels. It now supplies 126 reported line targets for pending review. All sign sequences remain unverified. Blank, damaged, uncertain and nontextual rows must be resolved when collating the original plates.

`research/core-edition-locators.json` records the survey page, reported edition pages, material, line/face layout and qualified direction for every core label. `research/edition-locator-audit.json` binds that table to the native catalogue and surface register by byte hashes.

`research/core-field-provenance-audit.json` now separates direct primary inspection from reported locators at field level. All fourteen core labels have survey-reported edition locators. Only BYB-A presently has directly inspected primary metadata (selected factual fields from Dunand 1930); no core label has a directly collated corpus-edition sequence, verified sign sequence, or established museum/object identifier. Direct metadata inspection is not promoted into sign-level verification.

```sh
python scripts/check_edition_locators.py --check
python scripts/audit_core_provenance.py --check
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

Inspect lawful copies of Dunand's original editions and plates; establish museum/object identities; resolve provider face/variant crosswalks; collate sign sequences and uncertain directions. Software integrity and expanded review targets do not establish scientific corpus 1.0 or exhaustive coverage.
