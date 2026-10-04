#!/usr/bin/env python3
"""Validate document admission and preservation, not live host enforcement."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def binding(item):
    path = Path(item['path'])
    assert not path.is_absolute() and '..' not in path.parts, 'unsafe binding'
    data = (ROOT / path).read_bytes()
    assert len(data) == item['size_bytes'], f'byte mismatch: {path}'
    assert hashlib.sha256(data).hexdigest() == item['sha256'], f'hash mismatch: {path}'


def main():
    identity = json.loads((ROOT / 'VERSION.json').read_text())
    admission_path = identity['middleware_admission']
    admission = json.loads((ROOT / admission_path).read_text())
    receipt = json.loads((ROOT / admission['promotion_receipt']).read_text())
    assert admission['release'] == identity['version'] == (ROOT / 'VERSION').read_text().strip()
    assert admission['canonical'] is True
    assert admission['authority'] == receipt['authority'] == 'NONE'
    assert admission['human_gate'] == receipt['human_gate'] == 'ACTIVE'
    assert admission['no_compression_out'] == 'ACTIVE'
    assert admission['originating_data_mutation'] == 'DISALLOWED'
    assert admission['runtime_validation'] == 'NOT PERFORMED'
    assert admission['component_credentials_issued_by_this_change'] is False
    assert receipt['independent_component_execution'] is False
    assert admission['load_order'] == [item['path'] for item in admission['payloads']]
    assert receipt['source'] == admission['preserved_source']
    assert receipt['payload'] == admission['payloads'][0]
    assert receipt['frozen_dependencies'] == admission['frozen_dependencies']
    for item in admission['payloads'] + admission['frozen_dependencies'] + [admission['preserved_source'], receipt['admission']]:
        binding(item)
    entry = (ROOT / identity['canonical_entry']).read_text()
    for path in [admission_path, *admission['load_order'], admission['promotion_receipt']]:
        assert '/' + path in entry, f'missing required load path: {path}'
    print('MIDDLEWARE ADMISSION: PASS (payload, source, frozen dependencies, receipt, entry)')
    print('Live host enforcement and component credentials: NOT VALIDATED')


if __name__ == '__main__':
    main()
