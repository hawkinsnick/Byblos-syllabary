# Explore and review the corpus

## Read without installing software

1. On the [GitHub repository](https://github.com/hawkinsnick/Byblos-syllabary),
   choose **Code → Download ZIP**.
2. Extract the ZIP. Open `exports/index.html` in a web browser.
3. Search by record ID, object, source or note. Filter reported core, disputed
   or excluded entries. Expand a record to read its citations and complete data.
4. Read the source register and open gaps below the catalogue.

The catalogue works offline. It makes no background requests and loads no remote
images or fonts. Clicking a source link opens that external source. With JavaScript
disabled, all records remain readable; search and filtering are unavailable.
GitHub displays HTML as source code, so download and extract it to use the viewer.

Unknown fields display as `null` in the complete record. An unverified or disputed
entry is not a proven addition to the corpus. Fourteen core labels do not necessarily
represent fourteen distinct objects. The viewer does not grant rights to linked sources.

## Files for researchers

| File in `exports` | Purpose |
|---|---|
| `index.html` | Searchable offline catalogue and source register |
| `bundle.json` | Full, lossless snapshot of every data table |
| `catalogue.jsonl` | One complete catalogue record per line |
| `catalogue.csv` | Convenience catalogue view; use JSON for complete data and exact types |
| `review_packet.json` | Pending tasks for every record, with known line targets and evidence |
| `contribution_template.json` | Unfilled form for attributed metadata corrections or source leads |
| `audit.json` / `REPORT.md` | Release checks, evidence gaps and scope limitations |
| `manifest.json` | Checksums for every exported file and canonical data inputs |

The review packet copies the current records, sources, external mappings, assets
and gaps. It supplies one task per record and a target for each **reported** surface
line. An empty target list means the surface inventory is unknown. It does not mean
that the inscription has no lines. No placeholder tokens or sign sequences are created.

Response fields begin pending and unknown. Filling them in does not automatically
change the corpus or create an approved review. Submit findings with exact evidence,
reviewer identity and the reviewed evidence digest. Follow the
[admission policy](ADMISSION_POLICY.md) before admitting review results.

## Generate and check a new snapshot

From the extracted repository directory, using Python 3.10 or later:

```sh
python -m byblos validate
python -m byblos export --output my-snapshot
python -m byblos verify-export my-snapshot
python -m byblos review-packet
```

Choose a new or empty export directory; existing files are not overwritten.
Use the matching repository version to regenerate and verify an older export.
The final command prints a review packet without changing any corpus files.

## Compare snapshots

```sh
python -m byblos compare old-snapshot new-snapshot
python -m byblos compare old-snapshot/bundle.json new-snapshot/bundle.json --fail-on-change
```

The result lists every recorded change with a JSON-pointer path and before/after
values. `present: false` means a field did not exist; `present: true, value: null`
means it existed but was unknown. Lists of records match by ID, and `@order`
separately records changes in their ordering. Token lists compare recorded positions;
the tool does not infer sign equivalences, align editions or decide which reading
is correct. Both input bundles must pass structural validation.

Without `--fail-on-change`, a valid comparison exits 0 even when differences exist.
With the flag, differences exit 3. Invalid input exits 1. A change to the evidence
digest means earlier approvals must be renewed; changes to review records or derived
review flags are also displayed even when they leave that digest unchanged.

## Help and permissions

Use the [acquisition and review packet](ACQUISITION_AND_REVIEW.md) for exact source
requests, permission scope and specialist deliverables. Development continues while
these dependencies remain open. No unverified sequence is promoted merely to meet
a version target, and no outreach is sent by generating these files.

## Propose a correction or source

Use the repository's Evidence correction or Source lead issue form, or start from
`exports/contribution_template.json`. See [CONTRIBUTING.md](CONTRIBUTING.md) for
expected-value checks, source requirements and read-only staging commands.
Pending proposal packets are distinct from accepted corpus exports.
