#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

RINGS = [
    (
        "R4-A",
        "Restriction / Constriction Record",
        "tools/validate_restriction_constriction.py",
        "tests/test_restriction_constriction.py",
    ),
    (
        "R4-B",
        "Collapse Boundary",
        "tools/validate_collapse_boundary.py",
        "tests/test_collapse_boundary.py",
    ),

    (
        "R4-C",
        "Landing Witness",
        "tools/validate_landing_witness.py",
        "tests/test_landing_witness.py",
    ),

    (
        "R4-D",
        "Reflight Trigger",
        "tools/validate_reflight_trigger.py",
        "tests/test_reflight_trigger.py",
    ),

    (
        "R4-E",
        "Post-Convergence Closure / Closing Witness",
        "tools/validate_closing_witness.py",
        "tests/test_closing_witness.py",
    ),

]

print()
print("=" * 72)
print("ZERVAN RING 4 — RUNTIME STATE OPERATIONS")
print("=" * 72)

print()
print("[DEPENDENCY] Rings 1, 2, and 3")

for ring_number in (
    1,
    2,
    3,
):
    dependency = subprocess.run(
        [
            sys.executable,
            str(
                ROOT
                / f"tools/validate_ring{ring_number}.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if dependency.returncode != 0:
        print(
            f"  Ring {ring_number} substrate: FAIL"
        )

        if dependency.stdout.strip():
            print(
                dependency.stdout.rstrip()
            )

        if dependency.stderr.strip():
            print(
                dependency.stderr.rstrip()
            )

        print()
        print("RING 4 RESULT: FAIL")
        raise SystemExit(1)

    print(
        f"  Ring {ring_number} substrate: PASS"
    )

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
print("RING 4 RECEIPT")
print("-" * 72)
print("R1    PASS  Required authority / identity substrate")
print("R2    PASS  Required Room / operational geography substrate")
print("R3    PASS  Required qualification / occupation substrate")

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
    print("RING 4 RESULT: FAIL")
    raise SystemExit(1)

print("RING 4 RESULT: PASS")
raise SystemExit(0)
