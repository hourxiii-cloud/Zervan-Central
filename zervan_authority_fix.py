#!/usr/bin/env python3
"""Idempotent Zervan active release authority repair and validator installation."""
import json
import re
from pathlib import Path

root = Path.cwd()
version_json = root / 'VERSION.json'
version_file = root / 'VERSION'
authority_file = root / 'VERSION_AUTHORITY.md'
readme_file = root / 'README.md'
assert all(p.is_file() for p in (version_json, version_file, authority_file, readme_file)), 'STOP: required root files missing'
config = json.loads(version_json.read_text(encoding='utf-8'))
assert config['version'] == version_file.read_text(encoding='utf-8').strip(), 'STOP: VERSION and VERSION.json disagree'
for field in ('initiation_call', 'canonical_entry', 'authority_contract'):
    value = config.get(field)
    assert isinstance(value, str) and value and (root / value).is_file(), f'STOP: unresolved {field}: {value}'
assert config['authority_contract'] == 'VERSION_AUTHORITY.md', 'STOP: unexpected authority contract'

start = '<!-- BEGIN GENERATED ACTIVE RELEASE AUTHORITY CONTRACT -->'
end = '<!-- END GENERATED ACTIVE RELEASE AUTHORITY CONTRACT -->'
header = f'''{start}
# Active release authority contract

**Current release identity is selected exclusively by `VERSION.json`.**
`VERSION` must match `VERSION.json.version` exactly. The active initiation,
canonical entry, admission, and verification paths are read from `VERSION.json`
and the referenced current initiation contract; none are selected from the
historical sections below.

This document preserves historical release authority declarations as provenance.
Older statements such as “Active Version”, “Active initiation path”, or
“Promotion State” are **historical within their originating release scope**;
they do not compete with the current `VERSION.json` selection.

Any current-release mismatch, missing required target, or inconsistent control
is a **hard validation failure**, not an opportunity to infer a release from
this document, the README, or conversation state.

Authority NONE. Human Gate ACTIVE. No Compression Out ACTIVE.
{end}
'''
original = authority_file.read_text(encoding='utf-8')
if start in original:
    assert end in original, 'STOP: malformed existing generated contract'
    original = original.split(end, 1)[1].lstrip('\n')
authority_file.write_text(header + '\n---\n\n' + original, encoding='utf-8')

script = root / 'scripts' / 'validate_active_release_authority.py'
script.parent.mkdir(exist_ok=True)
script.write_text('''#!/usr/bin/env python3
"""Fail closed on conflicting active Zervan release identity and paths."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
errors = []
try:
    cfg = json.loads((root / 'VERSION.json').read_text(encoding='utf-8'))
    version = (root / 'VERSION').read_text(encoding='utf-8').strip()
    if cfg.get('version') != version:
        errors.append('VERSION != VERSION.json.version')
    for key in ('initiation_call', 'canonical_entry', 'authority_contract',
                'human_gate_decision_reference', 'integration_receipt',
                'component_registry', 'skyfall_admission'):
        path = cfg.get(key)
        if not isinstance(path, str) or not path or Path(path).is_absolute() or '..' in Path(path).parts:
            errors.append(f'{key}: invalid or absent path')
        elif not (root / path).is_file():
            errors.append(f'{key}: target missing: {path}')
    authority = (root / 'VERSION_AUTHORITY.md').read_text(encoding='utf-8')
    readme = (root / 'README.md').read_text(encoding='utf-8')
    marker = '<!-- END GENERATED ACTIVE RELEASE AUTHORITY CONTRACT -->'
    if marker not in authority or 'selected exclusively by `VERSION.json`' not in authority.split(marker)[0]:
        errors.append('active authority contract missing or altered')
    if re.search(r'vTemporal\.\d+\.\d+\.\d+|\bv\d+\.\d+\.\d+\b', readme):
        errors.append('README contains pinned release identity')
    if cfg.get('authority') != 'NONE' or cfg.get('human_gate') != 'ACTIVE' or cfg.get('no_compression_out') != 'ACTIVE':
        errors.append('release control fields disagree with authority contract')
    if cfg.get('inferred_versioning_allowed') is not False or cfg.get('mixed_version_identity_allowed') is not False:
        errors.append('release inference or mixed-version identity not disabled')
except (OSError, ValueError, KeyError) as exc:
    errors.append(str(exc))
if errors:
    print('FAIL: active release authority\\n' + '\\n'.join(' - ' + e for e in errors))
    sys.exit(1)
print('PASS: active release identity, authority controls, references, and README guard')
''', encoding='utf-8')
print('Updated VERSION_AUTHORITY.md (historical text retained)')
print('Installed scripts/validate_active_release_authority.py')
