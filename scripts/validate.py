"""Command-line structural validation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from byblos.core import audit, load_bundle

def main():
    try:
        result = audit(load_bundle())
    except (ValueError, KeyError, TypeError, OSError) as exc:
        raise SystemExit(f"FAIL: malformed or missing input: {exc}")
    if not result["structure_valid"]:
        raise SystemExit("\n".join(result["errors"]))
    counts = result["counts"]
    print(f"PASS: {counts['catalogue_records']} catalogue records; "
          f"{counts['reported_core']} reported core; "
          f"{counts['disputed_candidates']} disputed candidates; "
          f"{counts['verified_core_sequences']} verified core sequences.")
    print("Scientific 1.0 ready:", result["scientific_1_0_ready"])

if __name__ == "__main__":
    main()
