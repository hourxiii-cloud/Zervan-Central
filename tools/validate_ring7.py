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
    (
        "R7-E",
        "Architecture Guide",
        "tools/validate_architecture_guide.py",
        "tests/test_architecture_guide.py",
    ),
    (
        "R7-F",
        "Developer Guide",
        "tools/validate_developer_guide.py",
        "tests/test_developer_guide.py",
    ),
    (
        "R7-G",
        "Audit Guide",
        "tools/validate_audit_guide.py",
        "tests/test_audit_guide.py",
    ),
    (
        "R7-H",
        "Operations Guide",
        "tools/validate_operations_guide.py",
        "tests/test_operations_guide.py",
    ),
    (
        "R7-K",
        "Completeness Receipt",
        "tools/validate_completeness_receipt.py",
        "tests/test_completeness_receipt.py",
    ),
    (
        "R7-L",
        "Promotion Receipt / Promotion-Readiness Record",
        "tools/validate_promotion_receipt.py",
        "tests/test_promotion_receipt.py",
    ),
    (
        "R7-M",
        "Fresh-Reader Final Package Validation",
        "tools/validate_fresh_reader_final_package.py",
        "tests/test_fresh_reader_final_package.py",
    ),
    (
        "R7-N",
        "Aggregate Documentation / Promotion Readiness Closure",
        "tools/validate_ring7_aggregate_closure.py",
        "tests/test_ring7_aggregate_closure.py",
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

print("-" * 72)

if failed:
    print("RING 7 RESULT: FAIL")
    raise SystemExit(1)

print("RING 7 RESULT: PASS")
print("DOCUMENTATION COMPLETE")
print("QUESTION CONTRACT COMPLETE")
print("NATIVE-v41 ENTRY COMPLETE")
print("TRANSITION ACCOUNTING COMPLETE")
print("STABILITY VALIDATED")
print("COMPLETENESS VALIDATED")
print("FRESH-READER VALIDATED")
print("PROMOTION PACKAGE COMPLETE")
print("PROMOTION READINESS READY_FOR_HUMAN_GATE")
print("AUTHORITY: NONE")
print("HUMAN GATE: ACTIVE")
print("PROMOTION STATE: CANDIDATE")
print("CANONICAL: FALSE")
print("PROMOTED: FALSE")
print("MERGED: FALSE")
print("HUMAN GATE AUTHORIZATION: NOT_GRANTED")
raise SystemExit(0)
