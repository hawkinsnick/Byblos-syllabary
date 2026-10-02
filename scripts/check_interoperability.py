"""Fail CI if the shared collection interoperability safeguards drift."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
c = json.loads((ROOT / "schemas" / "interoperability-contract.json").read_text(encoding="utf-8"))
required = {
    "source_attribution_required": True,
    "source_integrity_hash_required": True,
    "uncertainty_preserved": True,
    "unknown_physical_object_count_is_null": True,
    "cross_language_pooling_default": False,
    "cross_project_links_create_independent_witnesses": False,
    "language_or_script_identity_inferred_from_links": False,
    "decipherment_claimed": False,
}
assert c.get("contract") == "hawkinsnick-epigraphic-corpus-interoperability"
assert c.get("version") == "1.1.0"
assert c.get("profile") == "provisional_research_catalogue"
assert c.get("principles") == required
print("Interoperability contract 1.1 safeguards passed.")
