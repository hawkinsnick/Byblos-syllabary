# Submit evidence and corrections

Contributions remain proposals until maintainers assess their evidence and obtain
the review required by the admission policy. This workflow checks structure, citations,
conflicting edits and snapshot identity. It does not determine archaeological truth,
verify contributor identity or grant reuse permission.

## Without programming

Open an issue in the [repository](https://github.com/hawkinsnick/Byblos-syllabary/issues)
using **Evidence correction** or **Source lead**. Include record IDs, exact citations,
page/plate locators, what you inspected and what remains uncertain. A source lead
can be submitted even if the publication has not been read. It cannot then support
a direct factual correction. Give links and bibliographic facts; source-access and
image/dataset permissions remain separate.

No issue or external correspondence is created automatically by these tools.

## Machine-readable proposals

Generate a form against the current snapshot:

```sh
python -m byblos proposal-template --record BYB-A > my-proposal.json
```

Or copy `exports/contribution_template.json`, which targets every catalogue record.
Fill `proposal_id`, `submitted_on` (YYYY-MM-DD), and a contributor name and stable
identifier. Submitters may choose an identifier they are willing to publish; no
email address is required. The empty form intentionally fails submission validation.

For each proposed field change, provide these keys:

| Key | Meaning |
|---|---|
| `record_id` | A known record within the form's target list |
| `field` | One of the permitted metadata fields below |
| `expected` | Current state: `{"present": false}` if absent, or `{"present": true, "value": ...}` |
| `value` | The proposed value; null means unknown, never deletion |
| `evidence` | Nonempty list of source IDs, precise locators and `fields: [field]` |

Permitted fields are display name, material, object type, membership, membership
note, museum ID, reported excavation identifier, discovery context and dimensions
in millimetres. Exact machine keys are listed in the generated form. Measurements
must be positive finite numbers; booleans do not count as measurements. Text values
must be nonempty or null. Membership must be reported_core, disputed or excluded.
Membership changes require scientific scrutiny, not merely a valid form.

Identity links, edition labels, sign sequences, evidence levels, approvals, asset
rights and release gates are deliberately outside this metadata intake format.
Submit proposals concerning these through an issue and the specialist workflow.
The tool does not silently expand the scope of a requested change.

## New sources

`new_sources` may contain unique new IDs, complete citation, consultation depth,
URL or null, DOI or null, notes, access date and a rights observation. Reuse rights
must remain `not_assessed`, with an explicit scope. Rights documentation needs
separate assessment before a licence or permission can enter accepted asset records.
Never equate access to a publication with permission to reproduce its media.

Consultation may be consulted_online, selected_pages, selected_sections,
abstract_only, metadata_only or not_consulted. Record actual depth, not the depth
planned for future work. Unread source leads are allowed without fact changes;
they cannot support corrections directly. A newly proposed, declared consulted
source can support a proposed correction, subject to human assessment of that claim.

## Check and stage

```sh
python -m byblos check-proposal my-proposal.json
python -m byblos stage-proposal my-proposal.json --output pending-submission
python -m byblos verify-proposal pending-submission
```

A valid check exits 0; invalid input exits 1. The assessment always says
`automatically_applied: false`. It prints the original and proposed values and
their evidence, making the request reviewable without editing corpus files.
Staging requires a new or empty directory. It writes proposal, assessment,
instructions and a SHA-256 manifest. It never writes a candidate corpus bundle.

Verification checks exact file inventory, regenerated content and the current
evidence digest. Extra files, altered assessments, symlinked files and stale
snapshots are rejected. A submission dated after the original snapshot is allowed;
the base digest must still match. If the corpus changes, generate a new form and
reconcile expected values against that new evidence.

## Admission remains manual

Maintainers must assess the sources and uncertainties, retain the proposal history,
make any justified corpus changes explicitly, and renew independent approvals
against the new evidence digest. A contributor's claimed citation or inspection is
not proof that the claim is correct. Validity does not imply acceptance. Source leads
do not become accepted sources merely because they appear in a pending packet.

No apply or auto-approve command exists. Follow [ADMISSION_POLICY.md](ADMISSION_POLICY.md)
and preserve attribution and source-specific rights in every admitted change.
