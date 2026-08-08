#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

R7 = ROOT / (
    "contracts/validation/"
    "RING7_AGGREGATE_DOCUMENTATION_PROMOTION_READINESS_CLOSURE.md"
)

R8 = ROOT / (
    "contracts/promotion/"
    "RING8_HUMAN_GATE_PROMOTION_BOUNDARY.md"
)


def normalized(text):
    return " ".join(text.split())


def validate():
    errors = []

    for path in (R7, R8):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    r7 = normalized(
        R7.read_text(encoding="utf-8")
    )

    r8 = normalized(
        R8.read_text(encoding="utf-8")
    )

    for marker in (
        "RING 7 RESULT: PASS",
        "PROMOTION READINESS READY_FOR_HUMAN_GATE",
        "Authority: NONE",
        "Human Gate: ACTIVE",
        "Promotion State: CANDIDATE",
        "Canonical: FALSE",
        "Promoted: FALSE",
        "Merged: FALSE",
        "Human Gate Authorization: NOT_GRANTED",
    ):
        if marker not in r7:
            errors.append(
                f"Ring 7 handoff missing: {marker}"
            )

    for marker in (
        "R8-A = Human Gate / Promotion Boundary.",
        "R7-N precedes R8-A.",
        "Ring 7 state = READY_FOR_HUMAN_GATE.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "Canonical remains FALSE.",
        "Promoted remains FALSE.",
        "Merged remains FALSE.",
        "Human Gate Authorization remains NOT_GRANTED.",
        "No promotion has occurred.",
        "No merge has occurred.",
        "No canonical mutation has occurred.",
        "R8-A INSTANTIATED.",
    ):
        if marker not in r8:
            errors.append(
                f"R8-A lock missing: {marker}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print("R8-A HUMAN GATE / PROMOTION BOUNDARY: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print("R8-A HUMAN GATE / PROMOTION BOUNDARY: PASS")
    print("Ring 7 handoff: READY_FOR_HUMAN_GATE")
    print("Human Gate authorization: NOT_GRANTED")
    print("Promotion executed: FALSE")
    print("Canonical mutation: FALSE")
    print("Merge executed: FALSE")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    print("Promotion State: CANDIDATE")
    print("R8-A INSTANTIATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
