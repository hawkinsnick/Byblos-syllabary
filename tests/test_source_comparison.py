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
F=module('audit_facsimile_review')
D=module('audit_dhorme_source_joins')

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
    def test_drawing_review_preserves_literal_and_counterfactual_counts(self):
        x=F.build();self.assertEqual(x['selected_marker_targets_inspected'],18)
        self.assertEqual(x['source_drawing_positions_compared'],123)
        self.assertEqual(x['number_and_table_join_only_positions'],0)
        self.assertTrue(x['all_table_gaps_have_drawing_review'])
        self.assertEqual(x['candidate_erratum_scenarios'][0]['counterfactual_only']['distinct_table_ordinals'],116)
        self.assertFalse(x['candidate_erratum_scenarios'][0]['literal_register_changed'])
        self.assertEqual(T.build()['distinct_source_ordinals'],115)
    def test_source_ordinal_review_cannot_enable_frequency(self):
        self.mutate('research/stele-a-facsimile-ordinal-review.json',lambda x:x['ordinals'][0].update(analysis_eligible=True),F.build)
    def test_missing_drawing_review_cannot_count_as_inspected(self):
        self.mutate('research/stele-a-facsimile-ordinal-review.json',lambda x:x['ordinals'][0].update(drawing_observation=None),F.build)
    def test_source_drawing_is_not_direct_surface_inspection(self):
        def change(x):x['ordinals'][6]['drawing_observation']['ancient_surface_status_adjudicated']=True
        self.mutate('research/stele-a-facsimile-ordinal-review.json',change,F.build)
    def test_same_article_is_not_independent_confirmation(self):
        self.mutate('research/stele-a-facsimile-ordinal-review.json',lambda x:x.update(source_instances_not_independent=False),F.build)
    def test_source_erratum_cannot_be_silently_adopted(self):
        self.mutate('research/stele-a-facsimile-ordinal-review.json',lambda x:x['candidate_errata'][0].update(canonical_change_applied=True),F.build)
    def test_source_count_hypothesis_cannot_be_silently_adopted(self):
        self.mutate('research/stele-a-facsimile-ordinal-review.json',lambda x:x['count_reconciliation_hypotheses'][0].update(canonical_count_change_applied=True),F.build)
    def test_printed_membership_cannot_be_repaired_in_review(self):
        self.mutate('research/stele-a-facsimile-ordinal-review.json',lambda x:x['ordinals'][31].update(printed_table_memberships=[]),F.build)
    def test_historical_join_scope_and_derived_count_are_explicit(self):
        x=D.build();self.assertEqual(x['heading_joins'],10)
        self.assertEqual(x['explicit_letter_joins'],9)
        self.assertEqual(x['edition_locator_joins'],1)
        self.assertEqual(x['direct_dunand_book_pages_added'],0)
        i=next(r for r in x['count_comparison'] if r['record_id']=='BYB-I')
        self.assertIsNone(i['reported_sign_count']);self.assertEqual(i['face_count_sum_project_derived'],84)
    def test_quoted_book_cannot_be_marked_directly_inspected(self):
        self.mutate('research/dhorme-1946-acquisition.json',lambda x:x.update(underlying_dunand_1945_pages_inspected=True),D.build)
    def test_historical_proposed_phonetics_cannot_be_admitted(self):
        self.mutate('research/dhorme-1946-source-joins.json',lambda x:x['source_lineage'].update(decipherment_and_phonetic_values_admitted=True),D.build)
    def test_first_stele_join_cannot_invent_a_printed_letter(self):
        self.mutate('research/dhorme-1946-source-joins.json',lambda x:x['entries'][2].update(printed_heading_letter='a'),D.build)
    def test_possible_extra_line_cannot_become_certain(self):
        self.mutate('research/dhorme-1946-source-joins.json',lambda x:x['qualified_layout_records'][0].update(possible_lower_line_is_certain=True),D.build)
    def test_crop_limitation_cannot_be_hidden(self):
        self.mutate('research/dhorme-1946-source-joins.json',lambda x:x['figure_layout_review'][8].update(standalone_crop_truncates_drawn_content=False),D.build)
    def test_source_trace_cannot_become_a_certified_line(self):
        self.mutate('research/dhorme-1946-source-joins.json',lambda x:x['figure_layout_review'][4]['layout_observation'].update(below_divider_trace_is_certified_extra_text_line=True),D.build)
