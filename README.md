# Byblos syllabary research corpus

Version: 1.3.3 — stable software workflow; provisional research catalogue.

An open research project working toward exhaustive, evidence-based coverage of the
undeciphered Byblos script. Its language affiliation is unresolved. The name
“syllabary” is conventional; proposed sound values are hypotheses.

## AI research skill

This corpus project includes a vendor-neutral, evidence-first AI research skill in [`ai-skill/`](ai-skill/). The corpus remains the scholarly source of truth; the skill is an interface to it, not a second corpus and not an independent authority.

Researchers using ChatGPT, Claude, Gemini, or another capable model can provide the repository (or its AI-ready bundle) together with [`ai-skill/SKILL.md`](ai-skill/SKILL.md). The skill requires the model to preserve provenance, uncertainty, exclusions, source dependence, rights, and this project's scientific gates. Before substantive use, check [`ai-skill/generated/source-state.json`](ai-skill/generated/source-state.json) and the generated research-bundle index for the corpus commit represented by the AI package.

For questions spanning multiple corpus projects, use the **Combined Corpus Research AI** documented in the Linear A repository under [`combined-ai-skill/`](https://github.com/hawkinsnick/Linear-A/tree/ai-skill-v0.1/combined-ai-skill). It orchestrates the registered individual skills while keeping their evidence models and rights separate. Membership in the combined system does **not** imply linguistic relationship, sign equivalence, chronology, decipherment, or independent replication.

## Current coverage

- 14 reported core entries plus 25 named disputed candidates; membership remains attributed.
- 51 registered sources/leads and 29 bibliography discovery entries; consultation depth recorded individually.
- 0 verified sign sequences, 0 imported images, 0 independently reviewed records; 18 sourced surface descriptions.
- Five edition-specific Dunand 1930 type groups record fourteen source-numbered positions; no shapes or sound values are certified.
- All fourteen core labels have attributed count records; all 43 OCBI entries have a pinned metadata-only structure inspection. See [the current checkpoint](docs/SOURCE-RECONCILIATION.md).
- A queryable stele a source review compares all 123 source drawing positions with literal table assertions and variant buckets, including 18 detailed marker/gap/collision inspections. [Read the source review](docs/STELE-A-SOURCE-REVIEW.md); its candidate erratum and count explanations remain unadopted.
- A consulted Dhorme 1946 witness adds ten qualified heading joins and six count comparisons; its copies depend on Dunand and its proposed decipherment remains unadmitted.
- Published corpus counts remain unresolved. This is not an exhaustive corpus.
- Identifiers refer to inscription records, not necessarily distinct physical objects.

43 OCBI entry labels are mapped provisionally by label or caption; entry counts include faces and variants. One licensed photograph is registered as an external reference, with credit and licence; its inscription identity remains unverified.

Start with [the ledger](data/coverage.json), [sources](data/sources.json),
and [method and roadmap](docs/METHOD.md).

## Verify locally

Requires Python 3.10+; no third-party dependencies.

```sh
python -m byblos validate
python -m unittest discover -s tests
python -m byblos audit
python -m byblos export --output my-snapshot
python -m byblos verify-export my-snapshot
```

Passing validation establishes structural consistency, not epigraphic correctness,
rights clearance, exhaustive coverage, or peer review.

## Research principles

Each assertion needs an attributable source and locator. Record unknowns as null.
Preserve damaged signs, edition differences, and alternative identifications.
Separate observed marks, editorial reconstruction, sign classification, sound
values, and translations. Never equate signs across scripts solely by appearance.
Track objects, surfaces, inscriptions, editions, and individual sign occurrences
separately as the data model expands.

Shared provenance and export conventions are intended to support the sister
corpus projects; compatibility with their current schemas has not been verified.

## Reuse and contributions

Licensing is component-specific: project-original software is PolyForm Noncommercial 1.0.0 and project-owned corpus content/documentation is CC BY-NC 4.0. Third-party and public-domain material retains its upstream status. Source access does not establish redistribution rights. See `LICENSE`, `LICENSE-CODE`, `LICENSE-CONTENT.md`, and `LICENSING.md`.
No photographs, plate drawings, or third-party transcriptions are redistributed.
See the rights fields in the source register.

Submit corrections with publication/page/plate references and distinguish direct
inspection from secondhand reporting. No specialist endorsement is claimed.

## Scientific release check

```sh
python -m byblos audit --require-1-0
```

Currently exits **2**, correctly reporting unmet scientific gates. Software 1.0
is a stable local validation, contribution and export workflow. The catalogue
remains provisional and incomplete; scientific 1.0 has not been released.

Run `python -m byblos release-check` to check version consistency, source links,
export integrity and exact agreement with repository data. Run the tests separately.


[Read the generated audit](exports/REPORT.md).
The JSON bundle is lossless; CSV is a convenience catalogue view.
`python -m byblos stats` returns no eligible sequences until verified sequences
exist. It does not treat reported sign totals as digitized observations.

[Scientific 1.0 status and required evidence](docs/RELEASE_STATUS.md) | [Research conflicts](docs/FINDINGS.md) | [Data model](docs/DATA_MODEL.md) | [Rights](docs/RIGHTS.md)

The [implemented admission policy](docs/ADMISSION_POLICY.md) binds reviews to the evidence snapshot and requires complete lines, attributed coverage decisions and count reconciliation. The [acquisition and review packet](docs/ACQUISITION_AND_REVIEW.md) supplies exact edition requests, permission scope and specialist acceptance criteria. No correspondence has been sent.

## Explore, prepare review and compare

Download and extract the repository ZIP, then open `exports/index.html` for a
searchable offline catalogue. No setup, remote assets or background requests.
The [user guide](docs/USER_GUIDE.md) explains the files and researcher workflow.

```sh
python -m byblos review-packet
python -m byblos compare old-snapshot new-snapshot
```

`exports/review_packet.json` has pending tasks for all 39 records and targets
for every reported surface line. Unknown inventories remain unknown; no sign
sequences or approvals are manufactured. Snapshot differences preserve missing
versus null, record identity, ordering and original token positions.

## Evidence contributions

Researchers can use the GitHub **Evidence correction** and **Source lead** issue
forms, or the [contribution workflow](docs/CONTRIBUTING.md). Machine-readable
proposals bind to a specific evidence snapshot, preserve expected current values,
and remain pending. No automatic apply or approval command exists.

```sh
python -m byblos proposal-template --record BYB-A
python -m byblos check-proposal my-proposal.json
python -m byblos stage-proposal my-proposal.json --output pending-submission
python -m byblos verify-proposal pending-submission
```

The exported `contribution_template.json` is intentionally incomplete until a
contributor fills identity, date and attributable changes or source leads.

Inspect source dependencies with `python -m byblos provenance` or filter with
`python -m byblos provenance --source mnamon-merlo`. See [provenance audit](docs/PROVENANCE.md).

## Inspect evidence and acquisition work

```sh
python -m byblos evidence-ledger
python -m byblos acquisition-queue
```

The [evidence ledger guide](docs/EVIDENCE_LEDGER.md) explains field unknowns,
citation bindings and the reproducible source inspection queue. These reports
organize existing evidence; they do not infer expert approval or missing readings.

## Continue with source references

While source reuse status is being established, use the [reference-only workflow](docs/REFERENCE_ONLY_WORKFLOW.md).
`python -m byblos reference-workflow` prints source-specific next actions.
`python -m byblos pilot-packet --record BYB-A` prepares one pending metadata review.
The exported pilot contains references and original catalogue metadata, with no
plates or sign sequences. Keep inspection PDFs outside the checkout; the current
release policy rejects known media files in the repository.

## Source reconciliation checkpoint

See [the 4 October 2026 evidence checkpoint](docs/SOURCE-RECONCILIATION.md) for new source-located evidence, reproducible checks, unresolved anomalies and the remaining primary-source work.

The final source pass adds [a focused review handoff](docs/EXPERT-REVIEW-HANDOFF.md), ten dependent stele line comparisons and 103 historical display targets. These are source locations, not certified ancient lines or glyph sequences. The 32/92 correction and count explanations remain unadopted.
