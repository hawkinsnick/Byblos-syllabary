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
