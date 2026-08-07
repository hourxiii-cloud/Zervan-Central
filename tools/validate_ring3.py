#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

RINGS = [
    (
        "R3-A",
        "Qualification Request / Mission Fitness",
        "tools/validate_qualification_request.py",
        "tests/test_qualification_request.py",
    ),
    (
        "R3-B",
        "Qualification Record / Disposition",
        "tools/validate_qualification_record.py",
        "tests/test_qualification_record.py",
    ),

]

print()
print("=" * 72)
print("ZERVAN RING 3 — QUALIFICATION / OCCUPATION")
print("=" * 72)

print()
print("[DEPENDENCY] Rings 1 and 2")

for ring_number in (
    1,
    2,
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
        print("RING 3 RESULT: FAIL")
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
            str(ROOT / validator),
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
print("RING 3 RECEIPT")
print("-" * 72)
print("R1    PASS  Required authority / identity substrate")
print("R2    PASS  Required Room / operational geography substrate")

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
    print("RING 3 RESULT: FAIL")
    raise SystemExit(1)

print("RING 3 RESULT: PASS")
raise SystemExit(0)
