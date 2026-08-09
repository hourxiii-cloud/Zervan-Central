#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Gate:
    name: str
    command: tuple[str, ...]


GATES = (
    Gate(
        "AC-07 contract/schema",
        (
            sys.executable,
            "-m",
            "tools.validate_cross_stage_integrity",
        ),
    ),
    Gate(
        "AC-07 integration boundary",
        (
            sys.executable,
            "-m",
            "tools.validate_cross_stage_integration",
        ),
    ),
    Gate(
        "AC-07 regression",
        (
            sys.executable,
            "-m",
            "unittest",
            "tests.test_cross_stage_integrity",
            "-v",
        ),
    ),
)


def run_gate(gate: Gate) -> bool:
    print()
    print("=" * 72)
    print(gate.name)
    print("=" * 72)

    result = subprocess.run(
        gate.command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.stdout:
        print(result.stdout.rstrip())

    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)

    state = "PASS" if result.returncode == 0 else "FAIL"

    print()
    print(f"{gate.name}: {state}")
    print(f"return code: {result.returncode}")

    return result.returncode == 0


def main() -> int:
    print("=== AC-07 AGGREGATE / BOUNDARY VALIDATION ===")

    results = [
        (gate.name, run_gate(gate))
        for gate in GATES
    ]

    print()
    print("=" * 72)
    print("AC-07 AGGREGATE RECEIPT")
    print("=" * 72)

    for name, passed in results:
        print(f"{'PASS' if passed else 'FAIL':<4}  {name}")

    failed = [
        name
        for name, passed in results
        if not passed
    ]

    print("-" * 72)

    if failed:
        print("AC-07 AGGREGATE / BOUNDARY VALIDATION: FAIL")
        print("Failed gates:")
        for name in failed:
            print(f" - {name}")
        return 1

    print("AC-07 AGGREGATE / BOUNDARY VALIDATION: PASS")
    print("Dedicated regression: PASS")
    print("Cross-stage integration: PASS")
    print("Aggregate composition: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
