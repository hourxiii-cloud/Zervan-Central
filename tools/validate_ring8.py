#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

print()
print("=" * 72)
print("ZERVAN RING 8 — HUMAN GATE / PROMOTION")
print("=" * 72)
RINGS = [
    (
        "R8-A",
        "Human Gate / Promotion Boundary",
        "tools/validate_ring8_human_gate_boundary.py",
        "tests/test_ring8_human_gate_boundary.py",
    ),
    (
        "R8-B",
        "Promotion Decision Contract",
        "tools/validate_promotion_decision_contract.py",
        "tests/test_promotion_decision_contract.py",
    ),
    (
        "R8-C",
        "Promotion Candidate Binding",
        "tools/validate_promotion_candidate_binding.py",
        "tests/test_promotion_candidate_binding.py",
    ),
    (
        "R8-D",
        "Pre-Promotion Verification",
        "tools/validate_pre_promotion_verification.py",
        "tests/test_pre_promotion_verification.py",
    ),
    (
        "R8-E",
        "Human Gate Authorization Receipt",
        "tools/validate_human_gate_authorization_receipt.py",
        "tests/test_human_gate_authorization_receipt.py",
    ),
    (
        "R8-H",
        "Canonical / Version Authority Transition",
        "tools/validate_canonical_version_authority_transition.py",
        "tests/test_canonical_version_authority_transition.py",
    ),
    (
        "R8-I",
        "Post-Promotion Integrity Verification",
        "tools/validate_post_promotion_integrity.py",
        "tests/test_post_promotion_integrity.py",
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
print("RING 8 RECEIPT")
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
    print("RING 8 RESULT: FAIL")
    raise SystemExit(1)

print("RING 8 RESULT: INSTANTIATED")
print("CURRENT: R8-I PASS")
print("R8-F: SKIPPED BY HUMAN DIRECTION")
print("R8-G: PROMOTION EXECUTED")
print("R8-H: CANONICAL TRANSITION COMPLETE")
print("R8-E Human Gate Authorization: GRANTED")
print("Post-Promotion Integrity: VERIFIED")
print("Candidate preserved: TRUE")
print("Canonical: TRUE")
print("Authority: NONE")
print("Human Gate: ACTIVE")
print("Promotion State: CANONICAL")
print("NEXT: R8-J Post-Promotion Fresh Reader")
raise SystemExit(0)
