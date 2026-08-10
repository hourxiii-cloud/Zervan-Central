#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

CONTROLS = [
    (
        "AC-10",
        "Evidence-Ceiling Semantic Enforcement",
        "tools/validate_evidence_ceiling_semantics.py",
        "tests/test_ac10_evidence_ceiling_semantics.py",
    ),
    (
        "AC-11",
        "Human-Gate / Authority Semantic Enforcement",
        "tools/validate_human_gate_authority_semantics.py",
        "tests/test_ac11_human_gate_authority_semantics.py",
    ),
    (
        "AC-12",
        "Activation Aggregate Closure",
        "tools/validate_activation_aggregate_closure.py",
        "tests/test_ac12_activation_aggregate_closure.py",
    ),
]


def run_command(args):
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
    ).returncode


def main():
    print()
    print("=" * 72)
    print("ZERVAN ACTIVATION CONTROL VALIDATION")
    print("=" * 72)

    results = []

    for control, name, validator, test_path in CONTROLS:
        print()
        print(f"[{control}] {name}")

        validator_rc = run_command(
            [
                sys.executable,
                "-B",
                str(ROOT / validator),
            ]
        )

        test_rc = run_command(
            [
                sys.executable,
                "-B",
                "-m",
                "unittest",
                str(ROOT / test_path),
            ]
        )

        passed = (
            validator_rc == 0
            and test_rc == 0
        )

        results.append(
            (
                control,
                name,
                validator_rc,
                test_rc,
                passed,
            )
        )

        print(
            f"  Validator: "
            f"{'PASS' if validator_rc == 0 else 'FAIL'}"
        )
        print(
            f"  Tests:     "
            f"{'PASS' if test_rc == 0 else 'FAIL'}"
        )

    print()
    print("-" * 72)
    print("ACTIVATION CONTROL RECEIPT")
    print("-" * 72)

    failed = False

    for (
        control,
        name,
        validator_rc,
        test_rc,
        passed,
    ) in results:
        state = "PASS" if passed else "FAIL"

        print(
            f"{control:<5} {state:<4}  {name}"
        )

        if not passed:
            failed = True

    print("-" * 72)

    if failed:
        print("ACTIVATION CONTROL RESULT: FAIL")
        print("Authority: NONE")
        print("Human Gate: ACTIVE")
        return 1

    print("ACTIVATION CONTROL RESULT: PASS")
    print("AC-10: ACTIVE")
    print("AC-11: ACTIVE")
    print("AC-12: ACTIVE")
    print("Evidence-Ceiling Semantic Enforcement: ENFORCED")
    print("Human-Gate / Authority Semantic Enforcement: ENFORCED")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
