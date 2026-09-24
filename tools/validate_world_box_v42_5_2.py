#!/usr/bin/env python3
"""Candidate record operations for World/Box boundaries; not an ontology engine.

All mutations return a new JSON record. History and the originating Question
are immutable through this API. Receipt linkage is checked, not receipt truth.
"""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys

PROFILE = {
    'null_space': 'Null Space is the consideration of unavailability.',
    'possibility': 'The condition of possibility creates pre-existing Boxes as superposition.',
    'box_condition': 'The condition of The Box, itself, collapses into REALITY and is simply OBSERVED.',
    'mechanism': 'UNRESOLVED',
    'world_reality_identity': 'UNRESOLVED',
    'authority': 'NONE',
    'human_gate': 'ACTIVE',
}
UNRESOLVED = [f'U{i:02}' for i in range(1, 25)]
RANK = {'UNRESOLVED': 0, 'SUPPORTED': 1, 'ESTABLISHED': 2}
ROLES = {'CONTRIBUTION', 'FRAME', 'NEED', 'FUNCTION', 'SOURCE', 'QUALIFICATION'}


class InvalidRecord(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidRecord(message)


def shape(value, keys, at):
    require(type(value) is dict, f'{at}: expected object')
    require(set(value) == set(keys.split()), f'{at}: missing or unexpected fields')


def text(value, at):
    require(type(value) is str and bool(value.strip()), f'{at}: expected nonempty string')


def strings(value, at):
    require(type(value) is list, f'{at}: expected list')
    for s in value:
        text(s, at)
    require(len(set(value)) == len(value), f'{at}: duplicate references')


def receipt_map(receipts):
    require(type(receipts) is list, 'receipts: expected list')
    result = {}
    for r in receipts:
        shape(r, 'id role detail ceiling', 'receipt')
        for key in ('id', 'role', 'detail'):
            text(r[key], 'receipt.' + key)
        require(r['role'] in ROLES, 'receipt: unknown role')
        require(r['id'] not in result, 'receipt: duplicate id')
        if r['role'] == 'QUALIFICATION':
            require(type(r['ceiling']) is str and r['ceiling'] in RANK,
                    'receipt: invalid evidence ceiling')
        else:
            require(r['ceiling'] is None, 'receipt: only qualification sets a ceiling')
        result[r['id']] = r
    return result


def replay(record):
    shape(record, 'format origin profile unresolved receipts events', 'record')
    require(record['format'] == 'WORLD_BOX_CANDIDATE_1', 'record: unsupported format')
    require(record['profile'] == PROFILE, 'source profile changed or mechanism invented')
    require(record['unresolved'] == UNRESOLVED, 'source unresolved surface changed')
    origin = record['origin']
    shape(origin, 'operation_id governed_object_id root_box_id question world_ref', 'origin')
    for k, v in origin.items():
        text(v, 'origin.' + k)
    receipts = receipt_map(record['receipts'])

    def ref(value, role):
        text(value, role + ' reference')
        require(value in receipts and receipts[value]['role'] == role,
                f'{role}: reference not present with required role')
        return receipts[value]

    def frames(values):
        strings(values, 'frame_refs')
        for value in values:
            ref(value, 'FRAME')

    require(type(record['events']) is list, 'events: expected list')
    ids, representations, observations, standings = set(), {}, {}, {}
    for e in record['events']:
        require(type(e) is dict, 'event: expected object')
        kind = e.get('type')
        require(type(kind) is str, 'event: type must be a string')
        common = 'id type contribution_ref '
        if kind in {'REPRESENT', 'TRANSFORM'}:
            shape(e, common + 'surface referent_id content frame_refs need_ref parents' +
                  (' function_ref' if kind == 'TRANSFORM' else ''), kind)
        elif kind == 'OBSERVE':
            shape(e, common + 'subject_ref observation_kind source_ref content frame_refs', kind)
        elif kind == 'QUALIFY':
            shape(e, common + 'representation_id standing observation_ids discriminating_ids qualification_ref', kind)
        else:
            raise InvalidRecord('unsupported event; no object mutation, ontology or collapse operation')
        text(e['id'], 'event.id')
        require(e['id'] not in ids, 'duplicate event id')
        ref(e['contribution_ref'], 'CONTRIBUTION')
        if kind in {'REPRESENT', 'TRANSFORM'}:
            require(type(e['surface']) is str and e['surface'] in {'WORLD', 'BOX'}, 'invalid surface')
            expected = origin['world_ref'] if e['surface'] == 'WORLD' else origin['root_box_id']
            require(e['referent_id'] == expected, 'representation substituted its referent')
            text(e['content'], 'representation.content')
            frames(e['frame_refs'])
            ref(e['need_ref'], 'NEED')
            strings(e['parents'], 'parents')
            for parent in e['parents']:
                require(parent in representations, 'parent missing or not earlier')
                require(representations[parent]['surface'] == e['surface'],
                        'transformation must not silently equate World and Box')
            if kind == 'TRANSFORM':
                require(bool(e['parents']), 'transformation requires earlier representation')
                ref(e['function_ref'], 'FUNCTION')
            representations[e['id']] = deepcopy(e)
            standings[e['id']] = 'UNRESOLVED'
        elif kind == 'OBSERVE':
            text(e['subject_ref'], 'observation.subject_ref')
            require(type(e['observation_kind']) is str and
                    e['observation_kind'] in {'ORDINARY', 'REALITY_RELATION'}, 'invalid observation kind')
            ref(e['source_ref'], 'SOURCE')
            text(e['content'], 'observation.content')
            frames(e['frame_refs'])
            observations[e['id']] = deepcopy(e)
            # Observation records do not select a Box, erase alternatives, infer
            # cause, alter Question identity, or promote any representation.
        else:
            text(e['representation_id'], 'qualification.representation_id')
            require(e['representation_id'] in representations, 'qualification: unknown representation')
            text(e['standing'], 'qualification.standing')
            require(e['standing'] in RANK or e['standing'] == 'REJECTED', 'unsupported standing')
            strings(e['observation_ids'], 'observation_ids')
            strings(e['discriminating_ids'], 'discriminating_ids')
            require(set(e['observation_ids']) <= observations.keys(), 'observation missing or not earlier')
            require(set(e['discriminating_ids']) <= set(e['observation_ids']),
                    'discriminating references must be observations used in qualification')
            qualification = ref(e['qualification_ref'], 'QUALIFICATION')
            if e['standing'] != 'UNRESOLVED':
                require(bool(e['discriminating_ids']), 'change of standing needs discriminating observation linkage')
            if e['standing'] in RANK:
                require(RANK[e['standing']] <= RANK[qualification['ceiling']], 'standing exceeds receipt ceiling')
            standings[e['representation_id']] = e['standing']
        ids.add(e['id'])
    return {'question': origin['question'], 'representations': representations,
            'observations': observations, 'standings': standings}


def validate(record, previous=None):
    try:
        replay(record)
        if previous is not None:
            replay(previous)
            for key in ('format', 'origin', 'profile', 'unresolved'):
                require(record[key] == previous[key], f'{key}: historical mutation')
            for key in ('events', 'receipts'):
                require(record[key][:len(previous[key])] == previous[key], f'{key}: history rewritten')
        return []
    except InvalidRecord as exc:
        return [str(exc)]


def checked(record, previous=None):
    failures = validate(record, previous)
    if failures:
        raise InvalidRecord('; '.join(failures))
    return record


def start(origin, receipts):
    return checked({'format': 'WORLD_BOX_CANDIDATE_1', 'origin': deepcopy(origin),
                    'profile': deepcopy(PROFILE), 'unresolved': UNRESOLVED.copy(),
                    'receipts': deepcopy(receipts), 'events': []})


def append_event(record, event, new_receipts=()):
    checked(record)
    result = deepcopy(record)
    result['receipts'].extend(deepcopy(list(new_receipts)))
    result['events'].append(deepcopy(event))
    return checked(result, record)


def recover_question(record):
    checked(record)
    return record['origin']['question']


def apply_function(record, source_id, transform_event, function):
    """Run a warranted callback on a detached representation; retain input.

    This is an application boundary, not a sandbox for hostile Python code.
    Validate warrant/target before executing the callback.
    """
    checked(record)
    probe = deepcopy(transform_event)
    probe['content'] = 'preflight'
    require(probe.get('type') == 'TRANSFORM', 'function requires TRANSFORM event')
    require(probe.get('parents') == [source_id], 'function parent mismatch')
    append_event(record, probe)  # permission linkage before execution
    source = replay(record)['representations'][source_id]
    output = function(deepcopy(source))
    text(output, 'function output')
    event = deepcopy(transform_event)
    event['content'] = output
    return append_event(record, event)


def validate_composition(envelope, previous=None):
    """Bind the new state to the original increment's Q+R validator."""
    try:
        shape(envelope, 'box_question_return world_development', 'composition')
        record = envelope['world_development']
        checked(record, previous)
        returned = envelope['box_question_return']
        require(type(returned) is dict, 'box_question_return: expected object')
        original = record['origin']
        for key, other in [('operation_id', 'operation_id'), ('governed_object_id', 'governed_object_id'),
                           ('root_box_id', 'root_box_id'), ('question', 'original_question')]:
            require(original[key] == returned.get(other), 'Q+R origin mismatch: ' + key)
        path = Path(__file__).with_name('validate_box_question_return_v42_5_2.py')
        require(path.is_file(), 'install the Box Question Return increment first')
        spec = importlib.util.spec_from_file_location('_box_return_v4252', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            failures = module.validate(returned)
        except (TypeError, ValueError, KeyError, AttributeError) as exc:
            # Fail closed if the earlier validator encounters malformed input.
            raise InvalidRecord('Q+R malformed input: ' + type(exc).__name__) from exc
        require(not failures, 'Q+R validation: ' + '; '.join(failures))
        return []
    except InvalidRecord as exc:
        return [str(exc)]


def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('record', type=Path)
    p.add_argument('--previous', type=Path, help='trusted earlier World record for continuity comparison')
    p.add_argument('--composition', action='store_true', help='validate Q+R and World together')
    args = p.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding='utf-8'))
        previous = json.loads(args.previous.read_text(encoding='utf-8')) if args.previous else None
        failures = (validate_composition if args.composition else validate)(record, previous)
    except (OSError, ValueError) as exc:
        failures = [str(exc)]
    print(json.dumps({'record_validation': 'BLOCKED' if failures else 'PASS',
                      'failures': failures, 'canonical_promotion': 'NONE'}, indent=2))
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
