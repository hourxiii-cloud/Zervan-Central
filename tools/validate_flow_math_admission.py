"""Verify the additive math object's binding and required loading, not physical truth."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    admission_path = 'canonical/geometry/FLOW_MATH_ADMISSION.json'
    a = json.loads((root / admission_path).read_text())
    version = json.loads((root / 'VERSION.json').read_text())
    if a['release'] != version['version'] or version['flow_math_admission'] != admission_path:
        raise ValueError('release or admission route mismatch')
    if (a['authority'], a['human_gate'], a['originating_data_mutation']) != ('NONE', 'ACTIVE', 'DISALLOWED'):
        raise ValueError('control drift')
    if a['runtime_validation'] != 'NOT PERFORMED' or a['independent_component_execution'] is not False:
        raise ValueError('unsupported runtime claim')
    if a['load_order'] != [a['frozen_parent']['path'], a['payloads'][0]['path']]:
        raise ValueError('parent-first full load required')
    for item in [a['frozen_parent'], *a['payloads']]:
        path = Path(item['path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('unsafe binding')
        b = (root / path).read_bytes()
        if len(b) != item['size_bytes'] or hashlib.sha256(b).hexdigest() != item['sha256']:
            raise ValueError(f'bound artifact mismatch: {path}')
    entry = (root / version['canonical_entry']).read_text()
    for path in [admission_path, *a['load_order']]:
        if '/' + path not in entry:
            raise ValueError(f'required entry load missing: {path}')
    return a


if __name__ == '__main__':
    validate()
    print('FLOW MATH ADMISSION: PASS — frozen parent, full supplement, code, tests, required loading')
    print('Physical applicability and deployed independent runtime: NOT VALIDATED')
