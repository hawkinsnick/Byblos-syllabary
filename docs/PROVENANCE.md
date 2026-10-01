# Provenance audit

Run `python -m byblos provenance` for the complete citation inventory, or
`python -m byblos provenance --source dunand-1945` to inspect one registered source.
The same report is included as `provenance.json` in each deterministic export.

Each usage preserves its source ID, role, JSON pointer, owning record or container,
citation locator and field bindings when recorded. JSON pointers address the exact
snapshot identified by its evidence digest. Owners use container namespaces so
a bibliography entry and source with the same ID remain distinct.

| Role | Meaning |
|---|---|
| field_evidence | Recorded source attribution with locator and field bindings |
| source_reference | Other source_id link, including counts, assets and access attempts |
| primary_edition_lead | Edition proposed for acquisition; no implied inspection |
| discovery_source | Citation through which a bibliography lead was found |
| context_source | Source listed as context for a research gap |
| metadata_source_id | Source supplying provider metadata |
| project_evidence_source_id | Project-selected source pointer for external mapping evidence |

Nested evidence, including direction claims and future token assertions, is walked
recursively. Unresolved source IDs are listed separately; they are diagnostics,
not silently substituted. Unknown source filters fail. Invalid corpus bundles
are rejected. The command does not change records or grant approvals.

This is a source-link inventory, not a complete graph of object identity or review
dependencies. It cannot detect uncited copying, determine whether two authors are
independent, or prove a cited claim. Repeated uses of one source are repeated uses,
not corroboration. Consultation and rights values are the project's recorded
declarations. No numeric quality score is inferred. Filtered reports retain the
whole-bundle unresolved-reference diagnostics.
