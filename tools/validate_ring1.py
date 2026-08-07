#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

RINGS = [
    (
        "R1-A",
        "Authority / Canonical Resolution",
        "tools/validate_authority_resolution.py",
        "tests/test_authority_resolution.py",
    ),
    (
        "R1-B",
        "Version Identity / Promotion",
        "tools/validate_version_identity.py",
        "tests/test_version_identity.py",
    ),
    (
        "R1-C",
        "Identity / Integrity / Provenance",
        "tools/validate_identity_integrity_provenance.py",
        "tests/test_identity_integrity_provenance.py",
    ),
    (
        "R1-D",
        "Manifest Architecture",
        "tools/validate_manifest_architecture.py",
        "tests/test_manifest_architecture.py",
    ),
]

OPTIONAL_RINGS = [
    (
        "R1-E",
        "State Roots / Authorized Views",
        "tools/validate_state_roots_authorized_views.py",
        "tests/test_state_roots_authorized_views.py",
    ),
    (
        "R1-F",
        "Revision / Branch / Merge",
        "tools/validate_revision_branch_merge.py",
        "tests/test_revision_branch_merge.py",
    ),
]

for optional in OPTIONAL_RINGS:
    if (ROOT / optional[2]).exists():
        RINGS.append(optional)

results = []

print()
print("=" * 68)
print("ZERVAN RING 1 — INNER CORE VALIDATION")
print("=" * 68)

for ring, name, validator, tests in RINGS:
    print()
    print(f"[{ring}] {name}")

    validation = subprocess.run(
        [sys.executable, str(ROOT / validator)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    testing = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            str(ROOT / tests),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    passed = (
        validation.returncode == 0
        and testing.returncode == 0
    )

    results.append((ring, name, passed))

    print(
        f"  Contract: {'PASS' if validation.returncode == 0 else 'FAIL'}"
    )
    print(
        f"  Tests:    {'PASS' if testing.returncode == 0 else 'FAIL'}"
    )

    if not passed:
        if validation.stdout.strip():
            print(validation.stdout.rstrip())
        if validation.stderr.strip():
            print(validation.stderr.rstrip())
        if testing.stdout.strip():
            print(testing.stdout.rstrip())
        if testing.stderr.strip():
            print(testing.stderr.rstrip())

print()
print("-" * 68)
print("RING 1 RECEIPT")
print("-" * 68)

failed = False

for ring, name, passed in results:
    state = "PASS" if passed else "FAIL"
    print(f"{ring:<5} {state:<4}  {name}")
    if not passed:
        failed = True

print("-" * 68)

if failed:
    print("RING 1 RESULT: FAIL")
    raise SystemExit(1)

print("RING 1 RESULT: PASS")
raise SystemExit(0)
