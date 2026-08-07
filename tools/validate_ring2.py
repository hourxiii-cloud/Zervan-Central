#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

RINGS = [
    (
        "R2-A",
        "Canonical Room Object Identity / Singularity",
        "tools/validate_canonical_room_object_identity.py",
        "tests/test_canonical_room_object_identity.py",
    ),
    (
        "R2-B",
        "Origin Establishment / Object Binding",
        "tools/validate_origin_establishment_object_binding.py",
        "tests/test_origin_establishment_object_binding.py",
    ),
    (
        "R2-C",
        "Terrain / Territory",
        "tools/validate_terrain_territory.py",
        "tests/test_terrain_territory.py",
    ),
    (
        "R2-D",
        "Bounded Zone",
        "tools/validate_bounded_zone.py",
        "tests/test_bounded_zone.py",
    ),
    (
        "R2-E",
        "Bounded Space",
        "tools/validate_bounded_space.py",
        "tests/test_bounded_space.py",
    ),
    (
        "R2-F",
        "Perspective / Representation Transform",
        "tools/validate_representation_transform.py",
        "tests/test_representation_transform.py",
    ),

    (
        "R2-G",
        "Orientation / Coordinates",
        "tools/validate_orientation_coordinates.py",
        "tests/test_orientation_coordinates.py",
    ),

]

print()
print("=" * 72)
print("ZERVAN RING 2 — CANONICAL ROOM OBJECT / OPERATIONAL GEOGRAPHY")
print("=" * 72)

print()
print("[DEPENDENCY] Ring 1")

ring1 = subprocess.run(
    [
        sys.executable,
        str(ROOT / "tools/validate_ring1.py"),
    ],
    cwd=ROOT,
    capture_output=True,
    text=True,
)

if ring1.returncode != 0:
    print("  Ring 1 substrate: FAIL")

    if ring1.stdout.strip():
        print(
            ring1.stdout.rstrip()
        )

    if ring1.stderr.strip():
        print(
            ring1.stderr.rstrip()
        )

    print()
    print("RING 2 RESULT: FAIL")
    raise SystemExit(1)

print("  Ring 1 substrate: PASS")

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
print("RING 2 RECEIPT")
print("-" * 72)
print("R1    PASS  Required inner substrate")

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
    print("RING 2 RESULT: FAIL")
    raise SystemExit(1)

print("RING 2 RESULT: PASS")
raise SystemExit(0)
