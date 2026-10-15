#!/usr/bin/env python3
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
                      paths['canonical_entry'],paths['human_gate_decision_reference'],paths['integration_receipt'],
                      'canonical/architecture_friction/ARCHITECTURE_FRICTION_CR_ADMISSION.json',
                      'verification/v48.1.3/ARCHITECTURE_FRICTION_CLOSURE_RECEIPT.json']
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
        # Mandatory Architecture Friction canonical dependency closure.
        import hashlib
        af_path = 'canonical/architecture_friction/ARCHITECTURE_FRICTION_CR_ADMISSION.json'
        af = json.loads(read(af_path))
        components = registry.get('components', {})
        # Seven components form the Architecture Friction baseline.
        # Canonically admitted additive components may extend that registry.
        required_components = {
            'spider_persona',
            'middleware',
            'relational_flow_math',
            'jumping_spider_persona',
            'skyfall_buffer_leap',
            'azimuth_cr001_rev3',
            'architecture_friction_cr',
        }
        missing_components = required_components - set(components)
        if missing_components:
            fail(
                'architecture friction baseline components missing: '
                + ', '.join(sorted(missing_components))
            )

        # CR-2026-10-15-v4813-GOLD is now an admitted additive component.
        if 'cr_2026_10_15_v4813_gold' not in components:
            fail('canonical GOLD additive component missing from registry')
        comp = components.get('architecture_friction_cr', {})
        actual = hashlib.sha256((ROOT / af_path).read_bytes()).hexdigest()
        if comp.get('admission') != {'path': af_path, 'sha256': actual}:
            fail('architecture friction admission not correctly registered')
        if af.get('canonical') is not True or af.get('human_gate_decision') != 'APPROVE':
            fail('architecture friction approval missing')
        if set(af.get('qualified_scope', {})) != {'AF-01','AF-02','AF-03','AF-04'}:
            fail('architecture friction scope mismatch')
        source = comp.get('frozen_source', {})
        if source.get('sha256') != af.get('source_sha256'):
            fail('architecture friction frozen source mismatch')
        if hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() != source['sha256']:
            fail('architecture friction frozen archive integrity mismatch')
        if af_path not in entry or not all(x in entry for x in ('AF-01','AF-02','AF-03','AF-04')):
            fail('architecture friction missing from canonical entry')
        closure = json.loads(read('verification/v48.1.3/ARCHITECTURE_FRICTION_CLOSURE_RECEIPT.json'))
        if closure.get('admission') != {'path': af_path, 'sha256': actual}:
            fail('architecture friction closure receipt mismatch')
        if closure.get('human_gate_decision') != 'APPROVE':
            fail('architecture friction closure approval missing')
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
