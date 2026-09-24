import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('world_box', ROOT / 'tools/validate_world_box_v42_5_2.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
Q = 'Could presently observed Reality be another availability relative to a containing Zervan test?'


def seed():
    origin = dict(operation_id='op:world', governed_object_id='object:inquiry',
                  root_box_id='box:question', question=Q, world_ref='world:referent')
    receipts = [dict(id=role.lower(), role=role, detail='Synthetic fixture; ' + role,
                     ceiling='SUPPORTED' if role == 'QUALIFICATION' else None)
                for role in sorted(M.ROLES)]
    return M.start(origin, receipts)


def representation(rid='r1', surface='BOX'):
    return dict(id=rid, type='REPRESENT', contribution_ref='contribution', surface=surface,
                referent_id='box:question' if surface == 'BOX' else 'world:referent',
                content='Representable; not observed; not established.', frame_refs=['frame'],
                need_ref='need', parents=[])


def observation(oid='o1'):
    return dict(id=oid, type='OBSERVE', contribution_ref='contribution', subject_ref='r1',
                observation_kind='REALITY_RELATION', source_ref='source',
                content='Synthetic observation receipt; not evidence for the containing-test proposition.',
                frame_refs=['frame'])


def qualification(qid='q1', standing='SUPPORTED'):
    return dict(id=qid, type='QUALIFY', contribution_ref='contribution', representation_id='r1',
                standing=standing, observation_ids=['o1'], discriminating_ids=['o1'],
                qualification_ref='qualification')


def represented():
    return M.append_event(seed(), representation())


def observed():
    return M.append_event(represented(), observation())


def composed(world=None):
    world = represented() if world is None else world
    o = world['origin']
    returned = dict(schema_version='1.0', operation_id=o['operation_id'],
                    governed_object_id=o['governed_object_id'], root_box_id=o['root_box_id'],
                    original_question=o['question'], question_scope='OTHER', representations=[],
                    collapse=dict(disposition='UNRESOLVED', standing_refs=[],
                                  unresolved_scope=['Containing relation not established'],
                                  retained_possibilities=[], paradox_trigger=False),
                    authority_state='NONE', human_gate_state='ACTIVE')
    returned['return'] = dict(question=o['question'], result='Representable; not observed; not established.',
                              answer_scope='NONE', root_box_id=o['root_box_id'],
                              governed_object_id=o['governed_object_id'],
                              identity_receipt=dict(question=o['question'], root_box_id=o['root_box_id'],
                                                    governed_object_id=o['governed_object_id']),
                              traversal_receipts=[], opened=True, observed=True, qualified=False)
    return dict(box_question_return=returned, world_development=world)


class WorldBoxTests(unittest.TestCase):
    def test_primitive_without_enumeration(self):
        self.assertEqual(M.recover_question(seed()), Q)
        self.assertEqual(M.replay(seed())['representations'], {})

    def test_plural_representations_one_referent(self):
        state = M.append_event(seed(), representation('w1', 'WORLD'))
        state = M.append_event(state, representation('w2', 'WORLD'))
        self.assertEqual({r['referent_id'] for r in M.replay(state)['representations'].values()}, {'world:referent'})
        self.assertEqual(M.recover_question(state), Q)

    def test_referent_substitution_blocked(self):
        e = representation('w1', 'WORLD')
        e['referent_id'] = 'world:manufactured'
        with self.assertRaises(M.InvalidRecord):
            M.append_event(seed(), e)

    def test_origin_mutation_against_previous_blocked(self):
        before = represented()
        after = copy.deepcopy(before)
        after['origin']['question'] = 'Derived analysis substituted for Question'
        self.assertTrue(M.validate(after, before))

    def test_analysis_cannot_enter_box_content(self):
        after = represented()
        after['origin']['analysis'] = 'environment'
        self.assertTrue(M.validate(after))

    def test_no_collapse_or_world_creation_operations(self):
        for kind in ['COLLAPSE', 'CREATE_WORLD', 'SELECT_BOX', 'DESTROY_BOX', 'INFER_CONTAINER', 'MUTATE_QUESTION']:
            with self.subTest(kind=kind), self.assertRaises(M.InvalidRecord):
                M.append_event(seed(), dict(type=kind))

    def test_profile_preserves_unknown_mechanism(self):
        state = observed()
        self.assertEqual(state['profile']['mechanism'], 'UNRESOLVED')
        self.assertEqual(len(M.replay(state)['observations']), 1)

    def test_imported_mechanism_blocked(self):
        for field, value in [('mechanism', 'OBSERVER_CAUSED'), ('possibility', 'QUANTUM'),
                             ('world_reality_identity', 'IDENTICAL'), ('authority', 'META_LEVEL')]:
            state = seed()
            state['profile'][field] = value
            self.assertTrue(M.validate(state), field)

    def test_observation_does_not_promote_representation(self):
        self.assertEqual(M.replay(observed())['standings']['r1'], 'UNRESOLVED')

    def test_observation_cause_field_rejected(self):
        e = observation()
        e['caused_collapse'] = True
        with self.assertRaises(M.InvalidRecord):
            M.append_event(represented(), e)

    def test_warranted_function_executes_without_mutating_origin(self):
        before = represented()
        snapshot = copy.deepcopy(before)
        event = representation('r2')
        event.update(type='TRANSFORM', parents=['r1'], function_ref='function')
        def function(detached):
            detached['content'] = 'Qualified external analysis result'
            detached['referent_id'] = 'attempted mutation of input copy'
            return detached['content']
        after = M.apply_function(before, 'r1', event, function)
        self.assertEqual(before, snapshot)
        self.assertEqual(after['origin'], before['origin'])
        self.assertEqual(M.replay(after)['representations']['r2']['content'], 'Qualified external analysis result')
        self.assertEqual(M.replay(after)['representations']['r1']['content'], representation()['content'])

    def test_missing_function_warrant_blocks_before_execution(self):
        event = representation('r2')
        event.update(type='TRANSFORM', parents=['r1'], function_ref='missing')
        called = []
        with self.assertRaises(M.InvalidRecord):
            M.apply_function(represented(), 'r1', event, lambda r: called.append(True))
        self.assertEqual(called, [])

    def test_function_cannot_return_object_as_question(self):
        event = representation('r2')
        event.update(type='TRANSFORM', parents=['r1'], function_ref='function')
        before = represented()
        with self.assertRaises(M.InvalidRecord):
            M.apply_function(before, 'r1', event, lambda r: {'question': 'replacement'})
        self.assertEqual(M.recover_question(before), Q)

    def test_world_box_transform_not_silently_equated(self):
        e = representation('r2', 'WORLD')
        e.update(type='TRANSFORM', parents=['r1'], function_ref='function')
        with self.assertRaises(M.InvalidRecord):
            M.append_event(represented(), e)

    def test_no_representation_required_after_observation(self):
        state = M.append_event(seed(), observation())
        self.assertEqual(M.replay(state)['representations'], {})

    def test_need_reference_required(self):
        e = representation()
        e['need_ref'] = 'function'
        with self.assertRaises(M.InvalidRecord):
            M.append_event(seed(), e)

    def test_missing_frame_reference_blocked(self):
        e = representation()
        e['frame_refs'] = ['missing']
        with self.assertRaises(M.InvalidRecord):
            M.append_event(seed(), e)

    def test_future_parents_and_duplicate_ids_blocked(self):
        e = representation()
        e['parents'] = ['future']
        with self.assertRaises(M.InvalidRecord):
            M.append_event(seed(), e)
        with self.assertRaises(M.InvalidRecord):
            M.append_event(represented(), representation())

    def test_representations_not_accepted_as_observations(self):
        e = qualification()
        e.update(observation_ids=['r1'], discriminating_ids=['r1'])
        with self.assertRaises(M.InvalidRecord):
            M.append_event(represented(), e)

    def test_compatibility_without_discrimination_does_not_raise_standing(self):
        e = qualification()
        e['discriminating_ids'] = []
        with self.assertRaises(M.InvalidRecord):
            M.append_event(observed(), e)

    def test_ceiling_blocks_establishment(self):
        with self.assertRaises(M.InvalidRecord):
            M.append_event(observed(), qualification(standing='ESTABLISHED'))

    def test_qualification_does_not_make_reality(self):
        for value in ['REALITY', 'TRUE', 'FALSE', 'ACTUAL', 'AUTHORITY']:
            with self.subTest(value=value), self.assertRaises(M.InvalidRecord):
                M.append_event(observed(), qualification(standing=value))

    def test_later_standing_does_not_rewrite_history(self):
        before = observed()
        after = M.append_event(before, qualification())
        self.assertEqual(M.replay(before)['standings']['r1'], 'UNRESOLVED')
        self.assertEqual(M.replay(after)['standings']['r1'], 'SUPPORTED')
        self.assertEqual(after['events'][:len(before['events'])], before['events'])
        self.assertEqual(M.validate(after, before), [])

    def test_rejection_retains_original_representation(self):
        after = M.append_event(observed(), qualification(standing='REJECTED'))
        self.assertEqual(M.replay(after)['representations']['r1'], representation())

    def test_unknown_not_immune_to_future_qualification(self):
        after = M.append_event(observed(), qualification())
        self.assertEqual(M.replay(after)['standings']['r1'], 'SUPPORTED')
        self.assertEqual(M.recover_question(after), Q)

    def test_history_rewrite_detected_against_previous(self):
        before = observed()
        for field in ['content', 'source_ref']:
            after = copy.deepcopy(before)
            after['events'][-1][field] = 'rewritten'
            self.assertTrue(M.validate(after, before))

    def test_observations_not_erased_by_meta_representation(self):
        before = observed()
        after = M.append_event(before, representation('meta'))
        self.assertEqual(M.replay(after)['observations'], M.replay(before)['observations'])

    def test_unresolved_surface_cannot_be_silently_closed(self):
        state = seed()
        state['unresolved'].remove('U05')
        self.assertTrue(M.validate(state))

    def test_all_24_unresolved_questions_preserved(self):
        path = ROOT / 'verification/v42.5.2/WORLD_UNRESOLVED_REGISTER.json'
        register = json.loads(path.read_text())
        self.assertEqual([r['id'] for r in register], M.UNRESOLVED)
        self.assertTrue(all(r['standing'] == 'UNRESOLVED' for r in register))

    def test_all_50_source_sections_preserved(self):
        import re
        path = ROOT / 'change_requests/CR_WORLD_REPRESENTATIONAL_MULTIPLICITY_BOX_SUPERPOSITION_REALITY_OBSERVATION.md'
        headings = re.findall(r'^(\d+)\. [A-Z][A-Z /—-]+$', path.read_text(), re.M)
        self.assertEqual([int(n) for n in headings], list(range(1, 51)))

    def test_malformed_json_shapes_fail_closed(self):
        values = [None, [], {}, True, 7, 'text']
        for value in values:
            self.assertTrue(M.validate(value))
        base = represented()
        paths = [('origin',), ('profile',), ('unresolved',), ('receipts',), ('events',),
                 ('origin', 'question'), ('events', 0, 'id'), ('events', 0, 'surface'),
                 ('events', 0, 'parents'), ('events', 0, 'frame_refs'), ('receipts', 0, 'role')]
        for path in paths:
            for value in values:
                with self.subTest(path=path, value=value):
                    state = copy.deepcopy(base)
                    cursor = state
                    for key in path[:-1]:
                        cursor = cursor[key]
                    cursor[path[-1]] = value
                    result = M.validate(state)
                    self.assertIsInstance(result, list)
                    # Empty optional event/receipt arrays can legitimately validate.

    def test_composition_with_first_increment(self):
        self.assertEqual(M.validate_composition(composed()), [])

    def test_composition_detects_question_drift(self):
        envelope = composed()
        envelope['world_development']['origin']['question'] = 'shrunk Q'
        self.assertTrue(M.validate_composition(envelope))

    def test_composition_invokes_return_validator(self):
        envelope = composed()
        envelope['box_question_return']['return']['question'] = 'wrong return'
        self.assertTrue(M.validate_composition(envelope))

    def test_composition_malformed_earlier_input_fails_closed(self):
        envelope = composed()
        envelope['box_question_return']['representations'] = [dict(id=[])]
        self.assertTrue(M.validate_composition(envelope))


if __name__ == '__main__':
    unittest.main()
