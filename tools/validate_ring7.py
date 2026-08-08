#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

print()
print("=" * 72)
print("ZERVAN RING 7 — DOCUMENTATION AND PROMOTION")
print("=" * 72)

RINGS = [
    (
        "R7-A",
        "Documentation / Promotion Boundary and Required-Surface Registry",
        "tools/validate_ring7_documentation_promotion_boundary.py",
        "tests/test_ring7_documentation_promotion_boundary.py",
    ),
    (
        "R7-B",
        "Question Contract",
        "tools/validate_question_contract.py",
        "tests/test_question_contract.py",
    ),
    (
        "R7-C",
        "README / Version Authority / Native-v41 Entry Surfaces",
        "tools/validate_native_v41_entry.py",
        "tests/test_native_v41_entry.py",
    ),
    (
        "R7-I",
        "Transition Receipt",
        "tools/validate_transition_receipt.py",
        "tests/test_transition_receipt.py",
    ),
    (
        "R7-J",
        "Stability Receipt",
        "tools/validate_stability_receipt.py",
        "tests/test_stability_receipt.py",
    ),
    (
        "R7-D",
        "User Manual",
        "tools/validate_user_manual.py",
        "tests/test_user_manual.py",
    ),
]

results = []

for ring, name, validator, tests in RINGS:
    print()
    print(f"[{ring}] {name}")

    validation = subprocess.run(
        [
            sys.executable,
            str(ROOT / validator),
        ],
        cwd=ROOT,
    )

    testing = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            str(ROOT / tests),
        ],
        cwd=ROOT,
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

print()
print("-" * 72)
print("RING 7 RECEIPT")
print("-" * 72)

failed = False

for ring, name, passed in results:
    state = "PASS" if passed else "FAIL"

    print(
        f"{ring:<5} {state:<4}  {name}"
    )

    if not passed:
        failed = True

for ring, name in (
    ("R7-E", "Architecture Guide"),
    ("R7-F", "Developer Guide"),
    ("R7-G", "Audit Guide"),
    ("R7-H", "Operations Guide"),
    ("R7-K", "Completeness Receipt"),
    ("R7-L", "Promotion Receipt / Promotion-Readiness Record"),
    ("R7-M", "Fresh-Reader Final Package Validation"),
    ("R7-N", "Aggregate Documentation / Promotion Readiness Closure"),
):
    print(
        f"{ring:<5} DEFER  {name}"
    )

print("-" * 72)

if failed:
    print("RING 7 RESULT: FAIL")
    raise SystemExit(1)

print("RING 7 RESULT: INSTANTIATED")
print("CURRENT: R7-A PASS")
print("NEXT: R7-B Question Contract")
raise SystemExit(0)
