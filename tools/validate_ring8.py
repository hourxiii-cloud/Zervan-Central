#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

print()
print("=" * 72)
print("ZERVAN RING 8 — HUMAN GATE / PROMOTION")
print("=" * 72)
print()
print("[R8-A] Human Gate / Promotion Boundary")

validation = subprocess.run(
    [
        sys.executable,
        str(
            ROOT
            / "tools"
            / "validate_ring8_human_gate_boundary.py"
        ),
    ],
    cwd=ROOT,
)

testing = subprocess.run(
    [
        sys.executable,
        "-m",
        "unittest",
        str(
            ROOT
            / "tests"
            / "test_ring8_human_gate_boundary.py"
        ),
    ],
    cwd=ROOT,
)

if validation.returncode or testing.returncode:
    print()
    print("RING 8 RESULT: FAIL")
    raise SystemExit(1)

print()
print("-" * 72)
print("RING 8 RECEIPT")
print("-" * 72)
print("R8-A PASS  Human Gate / Promotion Boundary")
print("-" * 72)
print("RING 8 RESULT: INSTANTIATED")
print("CURRENT: R8-A PASS")
print("Authority: NONE")
print("Human Gate: ACTIVE")
print("Promotion State: CANDIDATE")
raise SystemExit(0)
