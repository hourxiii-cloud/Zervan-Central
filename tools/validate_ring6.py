#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

print()
print("=" * 72)
print("ZERVAN RING 6 — VALIDATION AND AUDIT")
print("=" * 72)

# ------------------------------------------------------------
# RING 5 DEPENDENCY
#
# Ring 5 already traverses Rings 1 through 4.
# Do not redundantly invoke Rings 1-4 here.
# This validates the entire inner implementation exactly once.
# ------------------------------------------------------------

print()
print("[DEPENDENCY] Ring 5 — Existing Pipeline Integration")

ring5 = subprocess.run(
    [
        sys.executable,
        str(
            ROOT
            / "tools"
            / "validate_ring5.py"
        ),
    ],
    cwd=ROOT,
    capture_output=True,
    text=True,
)

if ring5.returncode != 0:
    print("  Ring 5 substrate: FAIL")

    if ring5.stdout.strip():
        print(
            ring5.stdout.rstrip()
        )

    if ring5.stderr.strip():
        print(
            ring5.stderr.rstrip()
        )

    print()
    print("RING 6 RESULT: FAIL")
    raise SystemExit(1)

print("  Ring 5 substrate: PASS")

RINGS = [
    (
        "R6-A",
        "Validation / Audit Boundary and Vector Registry",
        "tools/validate_validation_audit_boundary.py",
        "tests/test_validation_audit_boundary.py",
    ),
    (
        "R6-B",
        "One-Object Perspective Rotation",
        "tools/validate_one_object_perspective_rotation.py",
        "tests/test_one_object_perspective_rotation.py",
    ),
]

results = []

for ring, name, validator, tests in RINGS:
    print()
    print(
        f"[{ring}] {name}"
    )

    validation = subprocess.run(
        [
            sys.executable,
            str(
                ROOT
                / validator
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    testing = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            str(
                ROOT
                / tests
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    passed = (
        validation.returncode == 0
        and testing.returncode == 0
    )

    results.append(
        (
            ring,
            name,
            passed,
        )
    )

    print(
        f"  Contract: "
        f"{'PASS' if validation.returncode == 0 else 'FAIL'}"
    )

    print(
        f"  Tests:    "
        f"{'PASS' if testing.returncode == 0 else 'FAIL'}"
    )

    if not passed:
        if validation.stdout.strip():
            print(
                validation.stdout.rstrip()
            )

        if validation.stderr.strip():
            print(
                validation.stderr.rstrip()
            )

        if testing.stdout.strip():
            print(
                testing.stdout.rstrip()
            )

        if testing.stderr.strip():
            print(
                testing.stderr.rstrip()
            )

print()
print("-" * 72)
print("RING 6 RECEIPT")
print("-" * 72)
print(
    "R1-R5 PASS  Validated through Ring 5 dependency traversal"
)

failed = False

for ring, name, passed in results:
    state = (
        "PASS"
        if passed
        else "FAIL"
    )

    print(
        f"{ring:<5} {state:<4}  {name}"
    )

    if not passed:
        failed = True

print("-" * 72)

if failed:
    print("RING 6 RESULT: FAIL")
    raise SystemExit(1)

print("RING 6 RESULT: PASS")
raise SystemExit(0)
