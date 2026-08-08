#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

# ----------------------------------------------------------------
# R5 VERSION REFERENCE PREFLIGHT
#
# Ring 1-B owns the repository-wide generated version-reference
# invariant. Ring 5 development adds/changes candidate artifacts,
# so synchronize that generated inventory ONCE before invoking
# inner-ring dependency validation.
#
# This does not weaken R1-B. It ensures R1-B evaluates the current
# repository surface rather than a stale generated inventory.
# ----------------------------------------------------------------

regeneration = subprocess.run(
    [
        sys.executable,
        str(
            ROOT
            / "tools"
            / "regenerate_version_references.py"
        ),
    ],
    cwd=ROOT,
    capture_output=True,
    text=True,
)

if regeneration.returncode != 0:
    print("R5 VERSION REFERENCE PREFLIGHT: FAIL")

    if regeneration.stdout.strip():
        print(regeneration.stdout.rstrip())

    if regeneration.stderr.strip():
        print(regeneration.stderr.rstrip())

    raise SystemExit(1)

print("R5 VERSION REFERENCE PREFLIGHT: SYNCHRONIZED")

RINGS = [
    (
        "R5-A",
        "Pipeline Integration Boundary / Existing-Semantics Lock",
        "tools/validate_pipeline_integration_boundary.py",
        "tests/test_pipeline_integration_boundary.py",
    ),
    (
        "R5-B",
        "Room-Bound Evidence -> PMC Intake Binding",
        "tools/validate_room_bound_evidence_pmc_intake.py",
        "tests/test_room_bound_evidence_pmc_intake.py",
    ),
    (
        "R5-C",
        "PMC -> CCR Candidate Commitment Lineage",
        "tools/validate_pmc_ccr_candidate_commitment_lineage.py",
        "tests/test_pmc_ccr_candidate_commitment_lineage.py",
    ),
    (
        "R5-D",
        "CCR -> MC Response / Output Admissibility Binding",
        "tools/validate_ccr_mc_response_output_admissibility.py",
        "tests/test_ccr_mc_response_output_admissibility.py",
    ),
    (
        "R5-E",
        "MC -> Raven Representation / Report Binding",
        "tools/validate_mc_raven_representation_binding.py",
        "tests/test_mc_raven_representation_binding.py",
    ),
    (
        "R5-F",
        "Raven -> Human Gate Publication / Action Boundary",
        "tools/validate_raven_human_gate_publication_action_boundary.py",
        "tests/test_raven_human_gate_publication_action_boundary.py",
    ),
    (
        "R5-G",
        "Decision Option Lineage",
        "tools/validate_decision_option_lineage.py",
        "tests/test_decision_option_lineage.py",
    ),
]

print()
print("=" * 72)
print("ZERVAN RING 5 — EXISTING PIPELINE INTEGRATION")
print("=" * 72)

print()
print("[DEPENDENCY] Rings 1, 2, 3, and 4")

for ring_number in (
    1,
    2,
    3,
    4,
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
        print("RING 5 RESULT: FAIL")
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
print("RING 5 RECEIPT")
print("-" * 72)
print("R1    PASS  Required authority / identity substrate")
print("R2    PASS  Required Room / operational geography substrate")
print("R3    PASS  Required qualification / occupation substrate")
print("R4    PASS  Required runtime-state substrate")

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
    print("RING 5 RESULT: FAIL")
    raise SystemExit(1)

print("RING 5 RESULT: PASS")
raise SystemExit(0)
