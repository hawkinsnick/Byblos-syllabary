# Research while copyright status is being established

Current project publication policy: factual catalogue metadata, bibliographic
references and original attributed annotations. Full scans, copied publication
prose, plates, fonts and third-party sign sequences remain outside this workflow.
This is a scoped publication policy, not a determination of any source's legal status.

## Work that can proceed

1. Locate authorized access routes to original editions, including library holdings
   and user-supplied copies with known provenance. Do not bypass access controls.
2. Inspect available sources, recording exact edition, page, plate and consultation
   depth. Keep inspection files outside the Git checkout. The publication tools
   neither fetch nor upload those files.
3. Record factual metadata and original analysis with per-assertion citations.
   Preserve competing identities and readings as attributed hypotheses. Do not
   treat independent retyping, tracing or redrawing as automatic rights clearance.
4. Prepare a small metadata pilot for a reviewer, then make evidence-bound
   proposals for specific corrections. No response is automatically admitted.
5. Assess proposed reuse item by item before adding images or sequences. A source
   licence and an asset-specific licence can have different scope.

## Tools and concrete deliverables

```sh
python -m byblos reference-workflow
python -m byblos pilot-packet --record BYB-A
python -m byblos release-check
```

`exports/reference_workflow.json` contains all registered sources, their recorded
consultation and rights scope, linked records, scoped asset declarations and
reference-only next actions. It grants no new rights or permissions.

`exports/pilot_packet.json` is a pending metadata packet for inscription A. It
includes the recorded facts, field-level citations, primary-edition lead and
unknowns. Sources are limited to citations in the record and line inventory.
Its reported ten-line surface inventory now cites Dunand 1930 pp. 2–3; its transcription remains null. A
reviewer can assess citation fidelity without being asked to endorse decipherment.
Use the CLI to prepare a different record; reported line targets remain reported.

The release check reports known media extensions found in the checkout and fails
the current media-free publication policy if any are present. Git internals,
virtual environments and Python caches are excluded. This includes uppercase
extensions and nested files. The check does not inspect text for copying, establish
legal clearance or detect disguised media. A future intentional media release
needs an explicit policy change and scoped evidence, not renaming a file.

## Rights investigation record

For each proposed item, record these questions with evidence:

| Question | Evidence to obtain |
|---|---|
| Which work and edition? | Title page, author, publisher, publication date and version |
| Which material will be reused? | Exact pages, images, drawings, sequence data or encoding map |
| Who holds relevant rights? | Item-specific credits, ownership records or explicit response |
| Which jurisdictions and terms apply? | Publication history, intended distribution and source access terms |
| Is an applicable licence or permission available? | Exact text, scope, conditions, date and grantor authority |
| Is another legal basis established? | Documented analysis for the particular work and intended use |
| What attribution is required? | Creator, source, licence link, modification notice and other conditions |

Keep the result pending until supported. Silence, refusal, inability to identify a
holder and an unassessed status are distinct; none is recorded as a grant.
No contact messages have been sent by this workflow.

## Legal reference boundary

The U.S. Copyright Office distinguishes facts and ideas from their protected
expression: https://www.copyright.gov/help/faq/faq-protect.html . It also explains
that research/noncommercial purpose does not by itself establish fair use:
https://www.copyright.gov/fair-use/ . These general U.S. references do not resolve
Dunand's copyright status, another jurisdiction's rules, database rights or the
terms attached to a particular access route. No public-domain finding is claimed.

## Scientific boundary

This pathway preserves useful research and attribution while specific assets are
unavailable. It does not close missing primary inspection, complete transcription,
object identity, coverage reconciliation or independent scientific review gates.
