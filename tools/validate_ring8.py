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
print("CURRENT: R8-B PASS")
print("NEXT: R8-C Promotion Candidate Binding")
print("Decision instance: NONE")
print("Human Gate Authorization: NOT_GRANTED")
print("Authority: NONE")
print("Human Gate: ACTIVE")
print("Promotion State: CANDIDATE")
raise SystemExit(0)
