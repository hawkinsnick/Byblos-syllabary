"""Self-contained catalogue reader; no network requests, images or imported fonts."""
from html import escape
import base64
import hashlib
import json
from urllib.parse import urlsplit
from .core import audit

STYLE = """:root{font-family:system-ui,sans-serif;color:#172b35;background:#f3f6f7}body{max-width:1050px;margin:auto;padding:24px}
h1{font-size:2rem;margin-bottom:8px}h2{margin-top:32px}a{color:#005a82}label{display:block;font-weight:600}
input,select{font:inherit;padding:10px;border:1px solid #82949d;border-radius:6px;max-width:100%;box-sizing:border-box}
input{width:100%}.filters{display:grid;grid-template-columns:2fr 1fr;gap:16px}.notice{background:#fff1d5;border-left:5px solid #916400;padding:16px}
details{background:white;border:1px solid #cad5da;border-radius:8px;margin:12px 0;padding:14px}summary{cursor:pointer;font-weight:650}
.tag{font-size:.8rem;padding:3px 6px;background:#e3edf1;border-radius:4px;display:inline-block;margin:4px}.meta{color:#405c69}
pre{font-size:.85rem;white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f6f7;padding:12px}li{margin:8px 0}
.digest{overflow-wrap:anywhere}footer{margin-top:36px;border-top:1px solid #cad5da;padding-top:16px}[hidden]{display:none!important}
@media(max-width:600px){body{padding:14px}.filters{grid-template-columns:1fr}h1{font-size:1.6rem}}
"""
SCRIPT = """const query=document.getElementById('query'),membership=document.getElementById('membership');
const rows=Array.from(document.querySelectorAll('[data-record]'));
function filter(){const term=query.value.trim().toLowerCase();let count=0;
for(const row of rows){const show=(!membership.value||row.dataset.membership===membership.value)&&row.dataset.search.includes(term);row.hidden=!show;if(show)count++;}
document.getElementById('result-count').textContent=count+' of '+rows.length+' catalogue records shown';}
query.addEventListener('input',filter);membership.addEventListener('change',filter);filter();
"""


def _hash(text):
    return base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode("ascii")


def _source_link(source):
    citation = escape(source["citation"])
    url = source.get("url")
    if isinstance(url, str) and urlsplit(url).scheme in {"http", "https"}:
        return '<a href="' + escape(url, quote=True) + '" rel="noreferrer">' + citation + '</a>'
    return citation


def explorer_html(bundle):
    report = audit(bundle)
    if not report["structure_valid"]:
        raise ValueError("Cannot render invalid corpus")
    sources = {s["id"]: s for s in bundle["sources"]["sources"]}
    version = escape(report["version"])
    csp = "default-src 'none'; style-src 'sha256-" + _hash(STYLE) + "'; script-src 'sha256-" + _hash(SCRIPT) + "'; base-uri 'none'; form-action 'none'"
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<meta http-equiv="Content-Security-Policy" content="' + escape(csp, quote=True) + '">',
             '<title>Byblos research catalogue ' + version + '</title><style>' + STYLE + '</style></head><body>',
             '<header><h1>Byblos research catalogue</h1><p class="meta">Development snapshot ' + version +
             ' · Evidence cutoff ' + escape(bundle["coverage"]["as_of"]) + '</p></header>',
             '<p class="notice"><strong>Scientific 1.0 ready: ' + str(report["scientific_1_0_ready"]) +
             '.</strong> Catalogue labels are not a count of distinct objects. Reported core membership remains attributed; disputed candidates are separate. Unknown fields remain null. Software validation is not specialist review.</p>',
             '<main><h2>Catalogue</h2><div class="filters"><label>Search records<input id="query" type="search" placeholder="ID, source, object or note"></label>',
             '<label>Membership<select id="membership"><option value="">All records</option><option value="reported_core">Reported core</option><option value="disputed">Disputed</option><option value="excluded">Excluded</option></select></label></div>',
             '<p id="result-count" aria-live="polite">All catalogue records shown</p>',
             '<noscript>Search requires JavaScript; all records and source details are readable below.</noscript>']
    for row in sorted(bundle["catalogue"]["records"], key=lambda r: r["id"]):
        search = json.dumps(row, ensure_ascii=False, sort_keys=True).lower()
        desc = row.get("display_name") or row.get("edition_label") or "Unknown description"
        parts += ['<details data-record="' + escape(row["id"], quote=True) + '" data-membership="' + escape(row["membership"], quote=True) +
                  '" data-search="' + escape(search, quote=True) + '"><summary>' + escape(row["id"]) + ' · ' + escape(desc) +
                  ' <span class="tag">' + escape(row["membership"].replace("_", " ")) + '</span></summary>',
                  '<p class="meta">Evidence: ' + escape(row["evidence_level"].replace("_", " ")) + ' · Review: ' + escape(row["review_status"]) + '</p>',
                  '<h3>Attributed evidence</h3><ul>']
        for ev in row["evidence"]:
            parts.append('<li>' + _source_link(sources[ev["source_id"]]) + ' — ' + escape(ev["locator"]) + '</li>')
        parts += ['</ul><h3>Complete record</h3><pre>' + escape(json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2)) + '</pre></details>']
    parts += ['<h2>Research gaps</h2><ul>']
    for gap in bundle["coverage"]["gaps"]:
        parts.append('<li><strong>' + escape(gap["id"]) + ' · ' + escape(gap["status"]) + '</strong>: ' + escape(gap["task"]) + '</li>')
    parts += ['</ul><h2>Source register</h2>']
    for source in sorted(sources.values(), key=lambda s: s["id"]):
        parts += ['<details><summary>' + escape(source["id"]) + '</summary><p>' + _source_link(source) + '</p>',
                  '<p>Consultation: ' + escape(source["consultation"]) + ' · Rights observation: ' + escape(source["rights"]["status"]) + '</p>',
                  '<pre>' + escape(json.dumps(source, ensure_ascii=False, sort_keys=True, indent=2)) + '</pre></details>']
    parts += ['<h2>Snapshot evidence</h2><p class="digest">SHA-256: ' + report["review_evidence_sha256"] + '</p>',
              '<p>Download <a href="bundle.json">bundle.json</a> for the lossless dataset or <a href="review_packet.json">review_packet.json</a> for pending review tasks. The packet grants no permission or approval.</p>',
              '<h2>Contribute evidence</h2><p>Start with the <a href="contribution_template.json">empty contribution form</a> or <a href="https://github.com/hawkinsnick/Byblos-syllabary/issues/new/choose">submit a correction or source lead</a>. Include exact citations and what you inspected. Proposals remain pending until assessed; opening this catalogue sends nothing.</p></main>',
              '<footer>Original catalogue viewer for hawkinsnick/Byblos-syllabary. Underlying assertions retain their source citations. No sign sequences, fonts, publication text or image bytes are bundled in this snapshot.</footer>',
              '<script>' + SCRIPT + '</script></body></html>\n']
    return "\n".join(parts)
