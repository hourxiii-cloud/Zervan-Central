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
    (
        "R6-C",
        "Premature-Analysis Rejection",
        "tools/validate_premature_analysis_rejection.py",
        "tests/test_premature_analysis_rejection.py",
    ),
    (
        "R6-D",
        "Proportional-Force Routing",
        "tools/validate_proportional_force_routing.py",
        "tests/test_proportional_force_routing.py",
    ),
    (
        "R6-E",
        "Qualification-Team Coherence",
        "tools/validate_qualification_team_coherence.py",
        "tests/test_qualification_team_coherence.py",
    ),
    (
        "R6-F",
        "Formation Re-Justification",
        "tools/validate_formation_rejustification.py",
        "tests/test_formation_rejustification.py",
    ),
    (
        "R6-G",
        "Distinct-Object Validation",
        "tools/validate_distinct_object_validation.py",
        "tests/test_distinct_object_validation.py",
    ),
    (
        "R6-H",
        "Hydration-On-Need",
        "tools/validate_hydration_on_need.py",
        "tests/test_hydration_on_need.py",
    ),
    (
        "R6-I",
        "Replay Fidelity",
        "tools/validate_replay_fidelity.py",
        "tests/test_replay_fidelity.py",
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
