#!/usr/bin/env python3
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
    if re.search(r'vTemporal\.\d+\.\d+\.\d+|v\d+\.\d+\.\d+', readme):
        errors.append('README contains pinned release identity')
    if cfg.get('authority') != 'NONE' or cfg.get('human_gate') != 'ACTIVE' or cfg.get('no_compression_out') != 'ACTIVE':
        errors.append('release control fields disagree with authority contract')
    if cfg.get('inferred_versioning_allowed') is not False or cfg.get('mixed_version_identity_allowed') is not False:
        errors.append('release inference or mixed-version identity not disabled')
except (OSError, ValueError, KeyError) as exc:
    errors.append(str(exc))
if errors:
    print('FAIL: active release authority\n' + '\n'.join(' - ' + e for e in errors))
    sys.exit(1)
print('PASS: active release identity, authority controls, references, and README guard')
