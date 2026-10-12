"""Verify the additive math object's binding and required loading, not physical truth."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    admission_path = 'canonical/geometry/FLOW_MATH_ADMISSION.json'
    a = json.loads((root / admission_path).read_text())
    version = json.loads((root / 'VERSION.json').read_text())
    registry = json.loads((root / version['component_registry']).read_text())
    component = registry['components']['relational_flow_math']
    if registry.get('active_release') != version['version']:
        raise ValueError('component registry active release mismatch')
    if component['source_release'] != a['release'] or component['admission']['path'] != admission_path:
        raise ValueError('flow-math component registry lineage mismatch')
    for key in ('admission', 'origin_contract', 'promotion_receipt', 'port_record'):
        item = component[key]
        actual = hashlib.sha256((root / item['path']).read_bytes()).hexdigest()
        if actual != item['sha256']:
            raise ValueError(f'registered flow-math {key} hash mismatch')
    if component['originating_candidate_commit'] != a['originating_candidate_commit'] or component['transport_artifact_sha256'] != a['transport_artifact_sha256']:
        raise ValueError('originating candidate or transport digest registry mismatch')
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
    origin_sha = a.get('originating_candidate_commit')
    transport_sha = a.get('transport_artifact_sha256')
    contract_path = a.get('origin_contract')
    receipt_path = a.get('promotion_receipt')
    payloads = {item['path']: item for item in a['payloads']}
    if not origin_sha or not transport_sha or contract_path not in payloads or receipt_path not in payloads:
        raise ValueError('origin contract or receipt binding missing')
    contract_text = (root / contract_path).read_text()
    receipt = json.loads((root / receipt_path).read_text())
    contract_item = payloads[contract_path]
    if f"Originating candidate commit SHA: `{origin_sha}`" not in contract_text:
        raise ValueError('originating candidate SHA mismatch')
    if f"Transport artifact SHA-256: `{transport_sha}`" not in contract_text:
        raise ValueError('transport artifact SHA mismatch')
    if receipt.get('originating_candidate_commit') != origin_sha:
        raise ValueError('receipt originating SHA mismatch')
    if receipt.get('transport_artifact', {}).get('sha256') != transport_sha:
        raise ValueError('receipt transport SHA mismatch')
    if receipt.get('origin_contract') != {'path': contract_path, 'sha256': contract_item['sha256']}:
        raise ValueError('receipt contract binding mismatch')
    entry = (root / version['canonical_entry']).read_text()
    for path in [admission_path, *a['load_order'], contract_path, receipt_path]:
        if '/' + path not in entry:
            raise ValueError(f'required entry load missing: {path}')
    return a


if __name__ == '__main__':
    validate()
    print('FLOW MATH ADMISSION: PASS — frozen parent, full supplement, code, tests, required loading')
    print('Physical applicability and deployed independent runtime: NOT VALIDATED')
