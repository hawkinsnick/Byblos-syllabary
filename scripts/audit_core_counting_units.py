"""Build a denominator ledger without collapsing Byblos unit types."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATHS=["data/catalogue.json","data/surfaces.json","research/core-publication-genealogy-audit.json","research/core-edition-locators.json"]
def build(root=ROOT):
 root=Path(root);read=lambda p:json.loads((root/p).read_text(encoding="utf-8"));catalogue=read(PATHS[0]);surfaces=read(PATHS[1])["surfaces"];genealogy=read(PATHS[2]);locators=read(PATHS[3]);core=[r for r in catalogue["records"] if r["membership"]=="reported_core"];ids={r["id"] for r in core};surface_ids={s["inscription_id"] for s in surfaces}
 if len(core)!=14 or len({r["edition_label"] for r in core})!=14:raise ValueError("core publication-label denominator changed")
 if not surface_ids<=ids or len(surfaces)!=18 or sum(s["line_count"] for s in surfaces)!=126:raise ValueError("surface/line denominator changed")
 if surface_ids!=ids-{"BYB-G"}:raise ValueError("surface coverage denominator changed")
 if genealogy["conventional_core_label_count"]!=14 or genealogy["verified_sequence_count"]!=0:raise ValueError("genealogy denominator or verification state changed")
 g=next(x for x in locators["entries"] if x["record_id"]=="BYB-G")
 if g["layout"]["reported_columns"]!=6 or g["layout"]["certainly_textual_columns"]!=5:raise ValueError("BYB-G column denominator changed")
 return {"format":"byblos-core-counting-unit-ledger-v1","input_hashes":{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in PATHS},"denominators":{"publication_labels":14,"publication_cohorts":2,"core_labels_with_line_surfaces":13,"reported_surfaces":18,"reported_line_targets":126,"column_only_core_labels":1,"BYB_G_reported_columns":6,"BYB_G_certainly_textual_columns":5,"verified_sign_sequences":0,"certified_distinct_physical_monuments":None},"excluded_from_arithmetic":[{"unit":"physical monuments","reason":"BYB-H and BYB-J may be one stele; no certified physical-object crosswalk exists."},{"unit":"approximate corpus texts","reason":"The survey's approximate fifteen-text scope is not the same denominator as the fourteen explicitly enumerated Dunand labels."},{"unit":"sign occurrences","reason":"Reported lines and columns are review targets, not collated sign sequences."}],"boundary":"Publication labels, publication cohorts, project surfaces, reported lines, reported columns, possible physical monuments and verified sign sequences are incompatible units. This ledger exposes each denominator and performs no conversion among them."}
if __name__=="__main__":
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--check",action="store_true");a=p.parse_args();output=json.dumps(build(),ensure_ascii=False,indent=2)+"\n";target=ROOT/"research/core-counting-unit-ledger.json"
 if a.check:
  if target.read_text(encoding="utf-8")!=output:raise SystemExit("Core counting-unit ledger stale")
  print("Byblos counting denominators replay without physical-object inflation.")
 else:print(output,end="")
