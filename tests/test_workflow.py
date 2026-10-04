"""Review preparation, data differences and safe offline rendering."""
import copy
from html.parser import HTMLParser
import json
import re
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from byblos.admission import evidence_digest
from byblos.core import ROOT, load_bundle
from byblos.explorer import explorer_html
from byblos.workflow import review_packet, compare_snapshots


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.records, self.links, self.scripts = [], [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-record" in attrs:
            self.records.append(attrs["data-record"])
        if tag == "a":
            self.links.append(attrs.get("href"))
        if tag == "script":
            self.scripts.append(attrs)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle()
    def test_packet_covers_records_and_reported_lines_without_approval(self):
        original = copy.deepcopy(self.bundle)
        packet = review_packet(self.bundle)
        self.assertEqual(self.bundle, original)
        self.assertEqual(packet["reviewed_bundle_sha256"], evidence_digest(self.bundle))
        self.assertEqual({t["record_id"] for t in packet["tasks"]},
                         {r["id"] for r in self.bundle["catalogue"]["records"]})
        targets = [(x["surface_id"], x["line"]) for t in packet["tasks"] for x in t["line_targets"]]
        expected = [(s["id"], n) for s in self.bundle["surfaces"]["surfaces"] for n in range(1, s["line_count"] + 1)]
        self.assertEqual(sorted(targets), sorted(expected))
        self.assertTrue(all(t["response"]["decision"] is None and t["response"]["status"] == "pending" for t in packet["tasks"]))
        unknown = next(t for t in packet["tasks"] if t["record_id"] == "BYB-G")
        self.assertEqual(unknown["surface_inventory_status"], "not_established")
        self.assertEqual(unknown["line_targets"], [])
    def test_identical_snapshot_has_no_changes(self):
        self.assertEqual(compare_snapshots(self.bundle, copy.deepcopy(self.bundle))["changes"], [])
    def test_missing_and_null_are_distinct(self):
        after = copy.deepcopy(self.bundle)
        after["catalogue"]["records"][0]["annotation"] = None
        diff = compare_snapshots(self.bundle, after)
        self.assertEqual(len(diff["changes"]), 1)
        self.assertEqual(diff["changes"][0]["before"], {"present": False})
        self.assertEqual(diff["changes"][0]["after"], {"present": True, "value": None})
        self.assertTrue(diff["evidence_changed"])
    def test_reordering_is_reported_without_false_record_edits(self):
        after = copy.deepcopy(self.bundle)
        after["catalogue"]["records"].reverse()
        changes = compare_snapshots(self.bundle, after)["changes"]
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]["path"], "/catalogue/records/@order")
    def test_type_change_bool_and_integer_is_not_lost(self):
        before, after = copy.deepcopy(self.bundle), copy.deepcopy(self.bundle)
        before["search_log"]["test_only"] = 0
        after["search_log"]["test_only"] = False
        self.assertEqual(compare_snapshots(before, after)["change_count"], 1)
    def test_pointer_escapes_keys(self):
        after = copy.deepcopy(self.bundle)
        after["search_log"]["a/b~c"] = "test"
        self.assertEqual(compare_snapshots(self.bundle, after)["changes"][0]["path"], "/search_log/a~1b~0c")
    def test_changed_record_is_matched_by_id(self):
        after = copy.deepcopy(self.bundle)
        after["catalogue"]["records"][0]["annotation"] = "needs inspection"
        after["catalogue"]["records"].reverse()
        paths = {x["path"] for x in compare_snapshots(self.bundle, after)["changes"]}
        self.assertEqual(paths, {"/catalogue/records/BYB-A/annotation", "/catalogue/records/@order"})
    def test_invalid_data_is_not_packaged_or_compared(self):
        bad = copy.deepcopy(self.bundle)
        bad["catalogue"]["records"][0]["evidence"] = []
        for func in (review_packet, explorer_html):
            with self.assertRaises(ValueError):
                func(bad)
        with self.assertRaises(ValueError):
            compare_snapshots(self.bundle, bad)
    def test_explorer_contains_every_record_and_only_safe_source_links(self):
        page = Page(explorer_html(self.bundle))
        self.assertEqual(set(page.records), {r["id"] for r in self.bundle["catalogue"]["records"]})
        self.assertEqual(len(page.records), len(self.bundle["catalogue"]["records"]))
        self.assertTrue(all(link.startswith(("https://", "http://")) or link in {"bundle.json", "review_packet.json", "contribution_template.json"} for link in page.links))
        self.assertEqual(page.scripts, [{}])
    def test_source_content_cannot_add_scripts_or_active_url(self):
        self.bundle["sources"]["sources"][0]["citation"] = '</script><script>alert("test")</script>'
        self.bundle["sources"]["sources"][0]["url"] = 'javascript:alert("test")'
        html = explorer_html(self.bundle)
        page = Page(html)
        self.assertEqual(page.scripts, [{}])
        self.assertNotIn('javascript:alert("test")', page.links)
        self.assertIn("&lt;script&gt;", html)
    @unittest.skipUnless(shutil.which("node"), "Node is optional for JavaScript execution checks")
    def test_exported_javascript_search_and_membership_filters(self):
        script = re.search(r"<script>(.*?)</script>", explorer_html(self.bundle), re.S).group(1)
        harness = r'''
const vm=require('node:vm'),assert=require('node:assert/strict');
const query={value:'',addEventListener(type,fn){this[type]=fn}},membership={value:'',addEventListener(type,fn){this[type]=fn}},count={textContent:''};
const rows=[{dataset:{membership:'reported_core',search:'byb-c bronze tablet'}},{dataset:{membership:'reported_core',search:'byb-d bronze tablet'}},{dataset:{membership:'disputed',search:'arrowhead 13104'}}];
const document={getElementById(id){return {query,membership,'result-count':count}[id]},querySelectorAll(){return rows}};
vm.runInNewContext(SCRIPT_PLACEHOLDER,{document});
assert.equal(count.textContent,'3 of 3 catalogue records shown');
query.value='  TABLET  ';query.input();assert.equal(count.textContent,'2 of 3 catalogue records shown');assert.equal(rows[2].hidden,true);
membership.value='disputed';membership.change();assert.equal(count.textContent,'0 of 3 catalogue records shown');
query.value='';query.input();assert.equal(count.textContent,'1 of 3 catalogue records shown');assert.equal(rows[2].hidden,false);
membership.value='';membership.change();assert.equal(count.textContent,'3 of 3 catalogue records shown');
'''.replace("SCRIPT_PLACEHOLDER", json.dumps(script))
        p = subprocess.run([shutil.which("node"), "-"], input=harness, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
    def test_cli_compare_exit_code_for_changes(self):
        with tempfile.TemporaryDirectory() as d:
            before, after = Path(d)/"before.json", Path(d)/"after.json"
            before.write_text(json.dumps(self.bundle), encoding="utf-8")
            self.bundle["search_log"]["annotation"] = "test"
            after.write_text(json.dumps(self.bundle), encoding="utf-8")
            p = subprocess.run([sys.executable, "-m", "byblos", "compare", str(before), str(after), "--fail-on-change"],
                               cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(p.returncode, 3)
            self.assertEqual(json.loads(p.stdout)["change_count"], 1)
