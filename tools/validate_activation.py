#!/usr/bin/env python3

from __future__ import annotations

import os
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
]


def run_python(relative_path: str, *args: str) -> int:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [
            sys.executable,
            "-B",
            *args,
            str(ROOT / relative_path),
        ],
        cwd=ROOT,
        env=env,
    )

    return result.returncode


def main() -> int:
    print()
    print("=" * 72)
    print("ZERVAN ACTIVATION CONTROL VALIDATION")
    print("=" * 72)

    failed = False
    results = []

    for control, name, validator, test_path in CONTROLS:
        print()
        print(f"[{control}] {name}")

        validator_rc = run_python(
            validator,
        )

        test_rc = run_python(
            test_path,
            "-m",
            "unittest",
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
            "  Validator: "
            + (
                "PASS"
                if validator_rc == 0
                else "FAIL"
            )
        )

        print(
            "  Tests:     "
            + (
                "PASS"
                if test_rc == 0
                else "FAIL"
            )
        )

        if not passed:
            failed = True

    print()
    print("-" * 72)
    print("ACTIVATION CONTROL RECEIPT")
    print("-" * 72)

    for control, name, validator_rc, test_rc, passed in results:
        state = "PASS" if passed else "FAIL"
        print(
            f"{control:<6} {state:<4}  {name}"
        )

    print("-" * 72)

    if failed:
        print("ACTIVATION CONTROL RESULT: FAIL")
        print("Authority: NONE")
        print("Human Gate: ACTIVE")
        return 1

    print("ACTIVATION CONTROL RESULT: PASS")
    print("AC-10: ACTIVE")
    print("Evidence-Ceiling Semantic Enforcement: ENFORCED")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
