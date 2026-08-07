#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AUTHORITY = ROOT / "DoctrineOps" / "AUTHORITY_RESOLUTION.md"

REQUIRED_LOCKS = [
    "Canonical implementation resolution and doctrinal authority are separate concerns.",
    "Runtime Authority: NONE",
    "Human Gate: ACTIVE",
    "Write capability is capability only.",
    "DEFAULT < VALID RESOLVED STATE",
    "No outer capability may redefine, merge, or locally override these dimensions.",
]

def validate():
    errors = []

    if not AUTHORITY.exists():
        return ["missing DoctrineOps/AUTHORITY_RESOLUTION.md"]

    text = AUTHORITY.read_text(encoding="utf-8")

    for lock in REQUIRED_LOCKS:
        if lock not in text:
            errors.append(
                f"missing R1-A authority lock: {lock}"
            )

    return errors


def main():
    errors = validate()

    if errors:
        print("R1-A AUTHORITY / CANONICAL RESOLUTION: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print("R1-A AUTHORITY / CANONICAL RESOLUTION: PASS")
    print("Canonical implementation and doctrinal authority: SEPARATE")
    print("Runtime Authority: NONE")
    print("Human Gate: ACTIVE")
    print("Write capability: NOT AUTHORITY")
    print("Default precedence: RESOLVED STATE WINS")
    print("Outer primitive redefinition: FORBIDDEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
