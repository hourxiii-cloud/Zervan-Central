#!/usr/bin/env python3
"""Install a fail-closed release authority validator and GitHub Actions guard.
Run from the repository root. Does not commit or promote anything.
"""
from pathlib import Path
import subprocess

root = Path.cwd()
assert (root / 'VERSION.json').is_file() and (root / 'VERSION_AUTHORITY.md').is_file(), 'Run in Zervan-Central root'
validator = r'''#!/usr/bin/env python3
"""Check the active release contract, not historical release declarations."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []

def fail(msg):
    errors.append(msg)

def read(path):
    p = ROOT / path
    if not p.is_file():
        fail(f'missing: {path}')
        return ''
    return p.read_text(encoding='utf-8')

def target(cfg, key):
    value = cfg.get(key)
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts or '\\' in value:
        fail(f'invalid {key} path: {value!r}')
        return ''
    read(value)
    return value

try:
    cfg = json.loads(read('VERSION.json'))
    version = cfg.get('version')
    if not isinstance(version, str) or not re.fullmatch(r'vTemporal\.\d+\.\d+\.\d+', version):
        fail('invalid VERSION.json.version')
    if read('VERSION').strip() != version:
        fail('VERSION does not match VERSION.json.version')
    if cfg.get('canonical_branch') != 'main':
        fail('canonical branch is not main')
    for key, expected in {'authority':'NONE','human_gate':'ACTIVE','no_compression_out':'ACTIVE',
                          'inferred_versioning_allowed':False,'mixed_version_identity_allowed':False}.items():
        if cfg.get(key) != expected:
            fail(f'control mismatch: {key}')
    paths = {k:target(cfg,k) for k in ('initiation_call','canonical_entry','authority_contract',
            'human_gate_decision_reference','integration_receipt','component_registry','skyfall_admission',
            'spider_admission','middleware_admission','jumping_spider_admission','flow_math_admission')}
    if paths['authority_contract'] != 'VERSION_AUTHORITY.md':
        fail('authority_contract does not select VERSION_AUTHORITY.md')
    authority = read('VERSION_AUTHORITY.md')
    marker = '<!-- END GENERATED ACTIVE RELEASE AUTHORITY CONTRACT -->'
    header = authority.split(marker)[0] if marker in authority else ''
    if marker not in authority or 'selected exclusively by `VERSION.json`' not in header:
        fail('active authority contract missing or altered')
    readme = read('README.md')
    if re.search(r'vTemporal\.\d+\.\d+\.\d+|\bv\d+\.\d+\.\d+\b', readme):
        fail('README pins a release identity')
    if '`VERSION.json`' not in readme:
        fail('README does not identify VERSION.json')
    initiation = read(paths['initiation_call']) if paths['initiation_call'] else ''
    entry = read(paths['canonical_entry']) if paths['canonical_entry'] else ''
    # Current initiation contract must identify the selected release and enumerate
    # the current entry and all explicitly ordered active release dependencies.
    if version and version not in initiation and version.replace('vTemporal.', 'v') not in initiation:
        fail('initiation statement does not identify active release')
    if version and version not in entry:
        fail('canonical entry does not identify active release')
    required_order = ['VERSION','VERSION.json','VERSION_AUTHORITY.md',
                      paths['initiation_call'],paths['component_registry'],paths['skyfall_admission'],
                      paths['canonical_entry'],paths['human_gate_decision_reference'],paths['integration_receipt']]
    listed = re.findall(r'^\s*\d+\.\s+/?(\S+)\s*$', initiation, re.MULTILINE)
    if listed != required_order:
        fail('initiation load order disagrees with VERSION.json or expected active contract')
    for control in ('Authority NONE', 'Human Gate ACTIVE', 'No Compression Out ACTIVE'):
        for name, content in [('initiation', initiation),('canonical entry', entry)]:
            if not re.search(re.escape(control).replace(r'\ ', r'\s+') + r'\b', content, re.I):
                fail(f'{name} missing control: {control}')
    registry_path = paths['component_registry']
    if registry_path:
        registry = json.loads(read(registry_path))
        if registry.get('active_release') != version:
            fail('component registry active_release disagrees with VERSION.json')
        if registry.get('canonical_branch') != cfg.get('canonical_branch'):
            fail('component registry branch mismatch')
        if registry.get('parent_release') != cfg.get('parent_canonical_identity'):
            fail('component registry parent release mismatch')
        if registry.get('canonical_parent_commit') != cfg.get('parent_canonical_commit'):
            fail('component registry parent commit mismatch')
except (OSError, ValueError, TypeError) as exc:
    fail(f'validation error: {exc}')
if errors:
    print('FAIL: active release authority')
    for error in errors:
        print(' -', error)
    sys.exit(1)
print('PASS: active release identity, references, initiation order, canonical entry, registry, controls, README')
'''
workflow = '''name: Active release authority
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Validate active release contract
        run: python3 scripts/validate_active_release_authority.py
'''
p = root / 'scripts/validate_active_release_authority.py'
p.parent.mkdir(exist_ok=True)
p.write_text(validator, encoding='utf-8')
w = root / '.github/workflows/validate-release-authority.yml'
w.parent.mkdir(parents=True, exist_ok=True)
w.write_text(workflow, encoding='utf-8')
subprocess.run(['python3', str(p)], check=True)
print('Installed validator and CI workflow. Review diff before committing.')
