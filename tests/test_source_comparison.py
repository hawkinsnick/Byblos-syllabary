import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

R=Path(__file__).resolve().parents[1]
def module(name):
    s=importlib.util.spec_from_file_location(name,R/'scripts'/f'{name}.py')
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=module('audit_source_comparison');N=module('audit_numbered_assertions');I=module('inspect_ocbi_structure');T=module('audit_type_table')

class SourceEvidenceTests(unittest.TestCase):
    def mutate(self,path,change,builder):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
            p=root/path;x=json.loads(p.read_text(encoding='utf-8'));change(x);p.write_text(json.dumps(x),encoding='utf-8')
            with self.assertRaises(ValueError):builder(root)
    def test_complete_provider_reconciliation_preserves_conflicts(self):
        x=M.build();self.assertEqual(x['provider_entries'],43)
        self.assertEqual(x['provider_entries_mapped_to_core_labels'],15)
        self.assertEqual(x['distinct_core_labels_targeted'],14)
        self.assertEqual(x['unresolved_core_layout_differences'],['BYB-G','BYB-H'])
        m=next(r for r in x['core_layout_comparison'] if r['record_id']=='BYB-M')
        self.assertEqual(m['direction_comparison']['status'],'UNRESOLVED_OPPOSING_CLAIMS')
        self.assertEqual(x['verified_sequences_added'],0)
    def test_readings_cannot_leak_into_metadata(self):
        self.mutate('research/ocbi-structure-inspection.json',lambda x:x['entries'][0].update(text='reading'),M.build)
    def test_crosswalk_metadata_drift_is_rejected(self):
        self.mutate('data/external_crosswalk.json',lambda x:x['entries'][0].update(provider_direction='LTR'),M.build)
    def test_reported_counts_cannot_become_verified(self):
        self.mutate('research/core-count-assertions.json',lambda x:x['entries'][0].update(verified_sign_sequence=True),M.build)
    def test_inspector_rejects_unpinned_source(self):
        with self.assertRaises(ValueError):I.inspect(b'changed source')
    def test_inspector_rejects_duplicate_or_unparsed_records(self):
        f='{ id = "a", source = "BYBL", group = "BYBL", dir = RTL, plate = Just "a.jpg", link = Nothing, text = """x""" }'
        with self.assertRaises(ValueError):I.inspect(('fragments = List.map\n'+f+'\n'+f+'\nbyblos : Script').encode(),require_pin=False)
        with self.assertRaises(ValueError):I.inspect(('fragments = List.map\n'+f+'\n{ id = "lost", unsupported = True }\nbyblos : Script').encode(),require_pin=False)
    def test_selected_numbering_supports_only_source_consistency(self):
        x=N.build();self.assertEqual(x['source_type_groups'],5)
        self.assertEqual(x['source_numbered_position_assertions'],14)
        self.assertEqual(x['recurrence_assertions_checked'][0]['source_type_labels'],['IV','V','VI'])
        self.assertFalse(x['full_sequence_verified'])
    def test_uninspected_number_cannot_support_recurrence(self):
        self.mutate('research/stele-a-numbered-assertions.json',lambda x:x['recurrence_assertions'][0]['source_position_groups'][0].__setitem__(0,999),N.build)
    def test_numbered_assertions_cannot_gain_sound_values(self):
        self.mutate('data/research_entities.json',lambda x:x['signs'][0].update(sound_value='ka'),N.build)
    def test_source_number_cannot_be_assigned_two_type_labels(self):
        def change(x):x['signs'][1]['source_numbered_positions'].append(1)
        self.mutate('data/research_entities.json',change,N.build)
    def test_complete_printed_table_retains_ambiguous_membership(self):
        x=T.build();self.assertEqual(x['source_type_rows'],38)
        self.assertEqual(x['printed_collisions'],[{'source_numbered_position':32,'type_labels':['VIII','XIX']}])
        self.assertEqual(x['unassigned_ordinals_in_observed_number_range'],[14,27,34,40,41,42,92,95])
    def test_pilot_misread_cannot_survive_full_table_check(self):
        def change(x):
            row=next(r for r in x['selected_source_groups'] if r['edition_sign_label']=='IV')
            row['source_numbered_positions']=[4,37,67,70,104,119]
        self.mutate('research/stele-a-numbered-assertions.json',change,T.build)
    def test_printed_collision_cannot_be_erased(self):
        self.mutate('research/stele-a-type-table.json',lambda x:x.update(printed_conflicts=[]),T.build)
    def test_shapes_cannot_leak_into_numeric_table(self):
        self.mutate('research/stele-a-type-table.json',lambda x:x['rows'][0].update(sound_value='a'),T.build)
    def test_facsimile_line_overlap_is_rejected(self):
        self.mutate('research/stele-a-facsimile-number-index.json',lambda x:x['lines'][1].update(first_source_ordinal=7),T.build)
