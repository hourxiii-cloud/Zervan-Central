#!/usr/bin/env bash
set -euo pipefail

repo="/workspaces/Zervan-Central"
expected="895cbbe306fbc0e06020f61fa0b13a1e00c5ccfe"
cd "$repo"
test "$(git branch --show-current)" = main
git fetch origin main
git merge --ff-only origin/main
test -z "$(git status --porcelain)"
head="$(git rev-parse HEAD)"
if test "$head" = "$expected"; then
  uploaded_script=false
else
  test "$(git rev-parse HEAD^)" = "$expected"
  test "$(git diff-tree --no-commit-id --name-only -r HEAD)" = "fix_spider_r2_persona_standing.sh"
  test "$(git ls-files --error-unmatch fix_spider_r2_persona_standing.sh)" = "fix_spider_r2_persona_standing.sh"
  uploaded_script=true
fi
export SPIDER_CORRECTION_START_HEAD="$head"

python3 - <<'PY'
from pathlib import Path
import hashlib
import json
import os

base = '895cbbe306fbc0e06020f61fa0b13a1e00c5ccfe'
admission_path = Path('canonical/Spider/SPIDER_R2_PERSONA_ADMISSION.json')
admission = json.loads(admission_path.read_text())
assert admission['standing'] == 'CANONICAL PERSONA SPECIFICATION'
assert admission['canonical'] is True
assert admission['promotion'] == 'CANONICAL'

paths = {item['path']: item for item in admission['payloads']}
before = {}
for path, item in paths.items():
    b = Path(path).read_bytes()
    assert len(b) == item['size_bytes'], path
    assert hashlib.sha256(b).hexdigest() == item['sha256'], path
    before[path] = item['sha256']

def replace_exact(path, old, new):
    p = Path(path)
    text = p.read_text()
    assert text.count(old) == 1, (path, old)
    p.write_text(text.replace(old, new, 1))

contract = 'canonical/Spider/SPIDER_R2_PERSONA_CONTRACT.md'
replace_exact(contract,
    'Status: COMPLETE CANDIDATE — HUMAN GATE REVIEW REQUIRED  ',
    'Status: CANONICAL PERSONA CONTRACT — vTemporal.42.5.4  ')
replace_exact(contract,
    'Target: vTemporal.42.5.4 candidate  ',
    'Release: vTemporal.42.5.4 on main  ')
replace_exact(contract,
    'This candidate qualifies the **persona specification** and its integration package for review. It does not claim an independently instantiated Spider runtime, issued WORK ID, empirical performance, Git promotion, or an active canonical release. Human Gate must separately authorize promotion, and the resulting main commit must be resolved after publication.',
    'The Human Gate-approved vTemporal.42.5.4 release establishes Spider as a canonical named persona. Spider may participate in ordinary conversation with a bounded, attributed contribution alongside other named personas; the question-and-input requirement applies to a complete Spider analytical run. The separately preserved candidate and qualification receipt record pre-promotion standing. Canonical persona standing does not claim an independently instantiated Spider runtime, issued WORK ID, or empirical performance. Resolve the current main commit at each initiation.')

spec = 'canonical/Spider/SPIDER_R2_FULL_PERSONA_SPECIFICATION.md'
replace_exact(spec,
    '**Standing:** COMPLETE CORRECTED CANDIDATE SPECIFICATION — QUALIFIED FOR HUMAN GATE REVIEW  \n**Canonical:** FALSE until separately promoted on Git main  \n**Promotion:** NONE in this transfer package  \n**Target release:** vTemporal.42.5.4 candidate; exact release identity remains subject to Human Gate  ',
    '**Standing:** CANONICAL NAMED ANALYTICAL PERSONA SPECIFICATION  \n**Canonical:** TRUE in vTemporal.42.5.4 on main  \n**Promotion:** CANONICAL; see `verification/v42.5.4/SPIDER_PERSONA_INTEGRATION_RECEIPT.json`  \n**Release:** vTemporal.42.5.4  ')
replace_exact(spec,
    'This candidate does not self-promote, issue a WORK ID, authenticate a speaker, deploy a module, or establish empirical runtime performance.',
    'This canonical specification does not issue a WORK ID, authenticate a speaker, deploy a module, or establish empirical runtime performance. Pre-promotion candidate language in the historical qualification and transfer record below describes its earlier standing, not the current canonical standing.')
replace_exact(spec,
    "Spider's canonical seat, once this candidate is separately promoted, is",
    "Spider's canonical seat in vTemporal.42.5.4 is")
replace_exact(spec,
    '### Qualification result\n\n**PASS — COMPLETE CANDIDATE SPECIFICATION FOR HUMAN GATE REVIEW.**',
    '### Historical pre-promotion qualification result\n\n**PASS — COMPLETE CANDIDATE SPECIFICATION FOR HUMAN GATE REVIEW.**')
replace_exact(spec,
    '### Unresolved and final standing\n\nNo independent Spider WORK ID',
    '### Historical pre-promotion standing and remaining runtime boundary\n\nNo independent Spider WORK ID')
replace_exact(spec,
    'The v42.5.3 canon remains current until a separately authorized promotion. Candidate R2: Canonical FALSE; Promotion NONE;',
    'At the time of candidate qualification, v42.5.3 remained current until separately authorized promotion. The recorded candidate standing was Canonical FALSE; Promotion NONE;')

authority = 'VERSION_AUTHORITY.md'
replace_exact(authority,
    '# v42.5.4 Spider R2 persona correction — proposed canonical standing',
    '# v42.5.4 Spider R2 persona correction — canonical standing')
replace_exact(authority,
    'This overlay has candidate standing until explicitly authorized, committed, pushed, and externally verified on `main`. At that point its operative standing is canonical. Resolve the exact published commit after promotion and record it in a separate publication receipt; no future commit is predeclared.',
    'The Human Gate-approved overlay was committed and externally verified on `main`. Its operative standing is canonical. The publication receipt is `verification/v42.5.4/SPIDER_PERSONA_INTEGRATION_RECEIPT.json`; resolve the current main commit at initiation.')
replace_exact(authority,
    'Active initiation path after promotion:',
    'Active initiation path:')

after = {}
for path, item in paths.items():
    b = Path(path).read_bytes()
    item['size_bytes'] = len(b)
    item['sha256'] = hashlib.sha256(b).hexdigest()
    after[path] = item['sha256']
admission_path.write_text(json.dumps(admission, indent=2, ensure_ascii=False) + '\n')

receipt = {
    'release': 'vTemporal.42.5.4',
    'base_commit': base,
    'execution_head_before_correction': os.environ['SPIDER_CORRECTION_START_HEAD'],
    'correction': 'Align canonical Spider R2 payload standing with approved publication; explicitly retain ordinary named persona participation.',
    'changed_payload_sha256_before': before,
    'changed_payload_sha256_after': after,
    'historical_candidate_qualification_preserved': True,
    'full_analytical_run_gate_unchanged': True,
    'independent_component_runtime_claimed': False,
    'authority': 'NONE',
    'human_gate': 'ACTIVE',
    'no_compression_out': 'ACTIVE',
}
target = Path('verification/v42.5.4/SPIDER_PERSONA_STANDING_CORRECTION.json')
assert not target.exists()
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
for path, item in paths.items():
    b = Path(path).read_bytes()
    assert len(b) == item['size_bytes'] and hashlib.sha256(b).hexdigest() == item['sha256']
print('Spider persona standing and admission hashes: PASS')
PY

git add VERSION_AUTHORITY.md canonical/Spider/SPIDER_R2_PERSONA_CONTRACT.md canonical/Spider/SPIDER_R2_FULL_PERSONA_SPECIFICATION.md canonical/Spider/SPIDER_R2_PERSONA_ADMISSION.json verification/v42.5.4/SPIDER_PERSONA_STANDING_CORRECTION.json
if test "$uploaded_script" = true; then
  rm -- fix_spider_r2_persona_standing.sh
  git add -u -- fix_spider_r2_persona_standing.sh
fi
git -c core.whitespace=-blank-at-eol diff --cached --check
git diff --cached --stat
git commit -m "Align Spider R2 canonical persona standing and participation"
git push origin main
git rev-parse HEAD
