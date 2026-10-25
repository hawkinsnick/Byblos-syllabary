---
name: byblos-syllabary-research
description: Evidence-first AI research skill for the Byblos syllabary corpus.
version: 0.3.1
---

## Load and validate this repository-bound skill

Use this file as the canonical individual skill. Load the complete matching
repository checkout or give the AI access to its files; this Markdown file alone
contains instructions, not the corpus. Do not claim that supplying a GitHub URL
installs a skill or makes private/local files available to an AI platform.
Resolve the paths below from the repository root. With Python 3.10+ available,
run `python scripts/validate_ai_skill.py` before describing this skill as
operational on the supplied checkout. Read `docs/AI-SKILL-VALIDATION.md` for the
exact workflow, examples, dependencies, validation scope and limitations.
If execution or source access is unavailable, say which step was not run and
make no fresh validation claim. Preserve all native source/rights restrictions.

Discover exact IDs with `python scripts/evidence_query.py --coverage` and
`python scripts/evidence_query.py --list COLLECTION`. Retrieve evidence with
`python scripts/evidence_query.py --record ID --collection COLLECTION`;
use `python scripts/research_delivery.py --dossier ID --collection COLLECTION`
for its evidence-only answer frame. Return the exact source path/hash/pointer,
attribution, uncertainty and native evidence unit. A missing ID means absent
from the selected view; never invent a replacement or infer global absence.


# Byblos syllabary Research Skill

This skill is an interface to the corpus in this repository. The corpus remains the canonical source of truth. Never maintain an independent scholarly dataset inside the skill.

## Governing rules
1. Separate physical/epigraphic observation, source transcription, normalization, computational derivation, scholarly interpretation, and AI-derived analysis.
2. Prefer canonical machine-readable corpus records over prose summaries for record-level questions.
3. Preserve identifiers, provenance, uncertainty, disagreements, corrections, negative results, and superseded analyses.
4. Never invent missing signs, readings, restorations, provenience, bibliography, source independence, or rights.
5. Label calculations performed by the AI and state enough method for reproduction.
6. Respect record/source-specific licensing and attribution. Repository-level licensing must not erase upstream restrictions.
7. For cross-corpus claims, establish comparability and source independence before interpreting similarity.
8. Report blocked or missing evidence rather than filling gaps.

## Corpus-specific caution
Undeciphered script: proposed sign values and Semitic interpretations are hypotheses unless the corpus explicitly records stronger evidence; preserve edition and provenance distinctions.

## Default research response
Give the direct answer, followed as relevant by Evidence; Evidentiary status; Uncertainty/limitations; Reproducibility; Rights/attribution.

## Synchronization
Read `ai-skill/generated/source-state.json` before substantive work. It records the corpus commit from which the AI-facing package was synchronized. Generated files are rebuildable views; canonical corpus files govern if a discrepancy is found.

## Academic-scrutiny gates
- Software maturity is distinct from scientific corpus maturity.
- Do not perform sequence-frequency inference without verified sequences.
- Reported counts with incompatible units remain separate.
- Proposed sound values remain hypotheses.
- Rights remain source-specific.

## Source reconciliation checkpoint
Read `docs/SOURCE-RECONCILIATION.md` and the indexed source-reconciliation artifacts before comparing versions, counting identities, or preparing specialist review.
- Eighteen reported surfaces cover thirteen core labels; BYB-G remains a column layout rather than an invented line inventory.
- Primary edition locators reported by the survey do not establish direct primary collation. Keep j entry page-range/caption anomalies unresolved.
- The field-provenance audit distinguishes BYB-A's selected Dunand 1930 factual metadata from later corpus-edition and sign-sequence collation; the latter remain zero for all fourteen core labels.
- The publication genealogy is 10 labels in the 1945 cohort plus 4 in the 1978 cohort; this is a label count, while h/j possible coreference keeps the physical-monument denominator unresolved.
- The counting-unit ledger keeps 14 publication labels, 18 surfaces, 126 line targets, BYB-G's 6/5 reported/certainly-textual columns, zero verified sequences and an unknown physical-monument count as separate denominators.
- Exact catalogue routes identify the 1945 edition through OL6188790M / bybliagrammatado0000duna / LCCN 55042246 / OCLC 1191221 / Google Books RnYtAAAAMAAJ, and the later article through KEI00067546 / KeiBi 43:205. Borrow restrictions, snippets and bibliographic metadata are discovery evidence only: zero primary pages or sequences have been collated through these routes.
- Dunand 1978 pagination remains unresolved: Mnamon 52–58 versus KeiBi 51–59, with 1981 appearance reported only by KeiBi. Use 51–59 solely as an acquisition target until the physical article is inspected.


## Linear A parity / pre-expert gate (2026-10-06)

Use `docs/LINEAR-A-PARITY-GATE.md` as the governing readiness target. Do not collapse rights/access blockers, unresolved scholarly questions, and independent-review requirements into one category.

Before declaring a Byblos task blocked:
- exhaust lawful public metadata and inspected evidence;
- preserve incompatible count units rather than forcing reconciliation;
- distinguish source disagreement from missing access;
- isolate the exact edition/page/plate or provider permission needed;
- never manufacture a sequence, glyph identity, object identity, or reviewer approval.

Parity with Linear A means methodological and evidentiary-control parity, not equal surviving evidence.


## Rights-dominant pre-expert readiness (2026-10-06)

Read `analysis/preexpert-residual-ledger.json` and `docs/RIGHTS-DOMINANT-READINESS.md` before proposing further corpus-growth work. Under currently lawfully admitted evidence, no identified non-rights machine/source task remains intentionally deferred. The dominant evidence-growth dependencies are lawful access to Dunand 1945/1978 and authoritative object/accession witnesses, plus applicable upstream terms for OCBI sequence/encoding reuse.

This is not scientific completion. Independent epigraphic review remains downstream of source acquisition. Never turn the rights-dominant milestone into permission to infer missing signs, sequences, object identities, directions, or reviewer decisions.

## Offline corpus browser
Run `python scripts/build_corpus_browser.py` to generate `workbench/corpus-browser.html`. The browser is self-contained and searches only the explicitly allowlisted files in `research/browser-sources.json`. Adding a file to the browser requires a rights/provenance check; never recursively ingest repository data or restricted upstream material. Browser display does not establish decipherment, source independence, or expert validation.

## Enforced assertion, dependency and bundle integrity

Read `docs/AI-INTEGRITY.md` and the required `research/cross-corpus-dependencies.json` before source counts or cross-corpus analysis. Use qualified assertion views when provided; original source literals must travel with their reconciliation, uncertainty and identity context. The dependency register does not certify physical identity or linguistic affinity. Shared catalogue references and duplicated digital sources are not independent witnesses. Missing links mean unknown, not independent. `scripts/check_cross_corpus_dependencies.py` screens declared record selections and rejects pooled physical/witness counts and phonetic transfer. Native AI bundle validation checks the dependency projection and local evidence hashes. Bundle publication validates the exact source parent and never rebases or force-pushes the validated artifact. Software and packaging checks do not establish expert or model-behavior acceptance.

## Source delivery checkpoint

Read `research/source-access-delivery-2026-10-12.json` and `docs/DUNAND-SOURCE-REQUEST.md` when planning source acquisition. Preserve contact-verification and routing uncertainty. Distinguish drafted requests from sent correspondence and explicit permissions. Log edition/version, IDs, coverage and rights per delivered component before reconciliation. Do not admit an inaccessible edition, invented word-ID join or photograph as certified gold; no scientific gate is closed by this checkpoint.

## Available source evidence

Read `docs/FULL-AVAILABLE-SOURCE-LAYERS.md` when querying the expanded source layer. Preserve native sampling units, unresolved source classifications, replica/derivative dependence and component rights. Source rectangles, facsimile ordinals and table rows are not automatically ancient objects, certified glyphs or independent witnesses.

## Count and assignment partition — 14 October 2026

Read `research/count-assignment-checkpoint-2026-10-14.json`, `research/count-assignment-partition.json` and `docs/COUNT-ASSIGNMENT-RECONCILIATION.md`. All 123 numbered positions partition into 119 form-bearing source drawings, three minimal-mark positions and one edge-only position. This numerical match does not certify ancient surviving/lost categories. Keep 114 single literal assignments, the 32 collision and eight unassigned ordinals distinct. The 32-to-92 hypothesis remains unadopted; direct 1945/1978 collation and expert acceptance remain open. No new canonical type or sequence is added.

## Corpus-native evidence and alternatives

Read `docs/EVIDENCE-AND-ALTERNATIVES.md`, `research/evidence-query-profile.json` and `analysis/evidence-query-coverage.json` for evidence or competing-reading questions. Use `scripts/evidence_query.py` with exact native IDs and an explicit collection when ambiguous. Preserve `native_record`, every uncertainty/editorial mark, source attribution, locator, inspection status and rights. Cite artifact path, JSON pointer and SHA-256; hashes certify bytes only. Treat explicitly linked records as declared ID associations, not physical certification or independent witnesses. Context resources have corpus-level scope and are not automatically about the queried record. Distinguish a named source reading from a legacy queue label, uninspected bibliographic lead, count convention or hypothesis. Do not infer a count of collated alternative pairs or independent witnesses from searchable rows; those metrics remain unknown. Report the native units and scope of each view separately, and defer to the corpus-specific limits. No new readings, expert acceptance or decipherment follows from this interface.

## Bounded attribution review (2026-10-15)

Read `docs/ATTRIBUTION-REVIEW.md` and `research/attribution-review.json` before describing a dispute or source comparison. Run `python scripts/attribution_review.py --case ID` with the referenced evidence available. Preserve complete native evidence and distinguish reading, interpretation, classification, count, identity and representation questions. This checkpoint reviews pinned repository packets; it does not repeat their primary consultation or grant independent review. Inherit the exact author/publication, locator, consultation limits and dependence from each pointer; missing fields remain unknown. Use the case-specific remaining work. Do not count register entries or apparatus notes as fully attributed pairs, physical objects or independent witnesses.

Stele A counting units, drawing partitions, Dunand-through-Dhorme voice and all fourteen core layout comparisons remain qualified. Numeric agreement does not validate signs.

## Research delivery, evidence answers and feedback

Read `docs/RESEARCH-DELIVERY.md` and verify `analysis/research-delivery.json`
with `python scripts/research_delivery.py --check` before using delivery claims.
Use `--dossier ID --collection COLLECTION` for exact evidence-bound answers;
preserve the complete native payload, citations, categories and limitations.
Use `--search TEXT` for source-record retrieval. Do not convert file pointers
into missing primary-edition citations, catalogue rows into unique objects,
source dependence into independent confirmation, or review forms into acceptance.
Prepare bounded review drafts with `--review-template`; validate submissions with
`--validate-review`, then require native human-maintainer acceptance. Treat delivery
and deterministic answer tests as engineering checks, not empirical LLM validation
or completion of scholarly/source-permission work. Local packaging grants no new
redistribution rights. Label any model-generated analysis separately and cite it.

## Apply scoped closure controls

Read `docs/CLOSURE-CONTROLS.md` and retrieve linked `closure-controls` before using a missing locator, conflicting material or printed type membership in a claim. Respect explicit nulls and exclusions. A completed control does not recover a source, adjudicate a conflict, establish sign identity or grant expert acceptance. Raw source literals remain available with their original qualifications.

## Preserve review provenance

Reject malformed JSON-pointer escapes and negative or leading-zero array indices
when verifying source citations; literal object keys retain their own spelling.
Read the [master hostile-review report](https://github.com/hawkinsnick/Master-Corpus-AI-Skill/blob/main/references/hostile-review-2026-10-25.md)
for this member's pinned retrieval scope and the limits of the source-fidelity
and development checks. Complete retrieval-view traversal does not certify
corpus completeness, accepted readings, independent witnesses or expert review.
