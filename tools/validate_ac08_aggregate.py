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
        "AC-08 Historical Fidelity — 18-test contract/implementation regression",
        (
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_historical_fidelity",
        ),
    ),
    Gate(
        "R4-F Replay Envelope",
        (
            sys.executable,
            "tools/validate_replay_envelope.py",
        ),
    ),
    Gate(
        "R6-I Replay Fidelity",
        (
            sys.executable,
            "tools/validate_replay_fidelity.py",
        ),
    ),
    Gate(
        "R4-I Runtime-State Continuity",
        (
            sys.executable,
            "tools/validate_runtime_state_continuity.py",
        ),
    ),
)


def run_gate(gate: Gate) -> tuple[str, int]:
    print()
    print("=" * 72)
    print(gate.name)
    print("=" * 72)

    result = subprocess.run(
        gate.command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout.rstrip())

    if result.stderr:
        print(result.stderr.rstrip())

    print(f"[return code: {result.returncode}]")

    return gate.name, result.returncode


def main() -> int:
    print()
    print("=" * 72)
    print("AC-08 — HISTORICAL FIDELITY AGGREGATE / BOUNDARY VALIDATION")
    print("=" * 72)

    results = tuple(run_gate(gate) for gate in GATES)

    print()
    print("=" * 72)
    print("AC-08 AGGREGATE RECEIPT")
    print("=" * 72)

    failed: list[str] = []

    for name, rc in results:
        passed = rc == 0
        state = "PASS" if passed else "FAIL"
        print(f"{state:<4} rc={rc:<3} {name}")

        if not passed:
            failed.append(name)

    print("-" * 72)

    if failed:
        print("AC-08 AGGREGATE / BOUNDARY VALIDATION: FAIL")
        print("No canonical or dependency repair inferred.")
        print("Failed gates:")

        for name in failed:
            print(f" - {name}")

        return 1

    print("AC-08 AGGREGATE / BOUNDARY VALIDATION: PASS")
    print("Historical-state proof regression: PASS")
    print("Replay Envelope integration: PASS")
    print("Replay Fidelity integration: PASS")
    print("Runtime continuity integration: PASS")
    print("Ring 6 full regression: PREVIOUSLY VERIFIED — NOT RE-RUN")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
