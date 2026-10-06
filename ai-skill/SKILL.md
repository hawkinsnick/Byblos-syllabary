---
name: byblos-syllabary-research
description: Evidence-first AI research skill for the Byblos syllabary corpus.
version: 0.3.1
---

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
