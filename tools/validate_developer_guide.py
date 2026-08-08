#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

GUIDE = ROOT / "docs/DEVELOPER_GUIDE.md"
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"
ARCH = ROOT / "docs/ARCHITECTURE_GUIDE.md"
MANUAL = ROOT / "docs/USER_MANUAL.md"
ENTRY = ROOT / "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose",
    "## 2. Development Rule",
    "## 3. Repository Entry",
    "## 4. Repository Structure",
    "## 5. Contracts",
    "## 6. Schemas",
    "## 7. Validators",
    "## 8. Tests",
    "## 9. Aggregate Runners",
    "## 10. Identity Implementation",
    "## 11. SHA-512",
    "## 12. One-Object Preservation",
    "## 13. Operational Geography",
    "## 14. Qualification",
    "## 15. Occupancy",
    "## 16. Question Contract Extension",
    "## 17. Evidence Boundary",
    "## 18. Evidence Ceiling",
    "## 19. Capability Routing",
    "## 20. Scale and Formation",
    "## 21. Hydration",
    "## 22. Restriction and Constriction",
    "## 23. Collapse",
    "## 24. Landing",
    "## 25. Reflight",
    "## 26. Replay",
    "## 27. Scar",
    "## 28. Distinct Objects and Passageways",
    "## 29. Analytical Pipeline",
    "## 30. PMC Development Boundary",
    "## 31. CCR Development Boundary",
    "## 32. MC Development Boundary",
    "## 33. Raven Development Boundary",
    "## 34. Human Gate Boundary",
    "## 35. Provenance",
    "## 36. Extension Rule",
    "## 37. New Contract Rule",
    "## 38. New Schema Rule",
    "## 39. New Validator Rule",
    "## 40. New Test Rule",
    "## 41. Failure Classification",
    "## 42. INNER_INVARIANT_CONTRADICTION",
    "## 43. OUTER_IMPLEMENTATION_DEFECT",
    "## 44. VALIDATOR_DEFECT",
    "## 45. COVERAGE_GAP",
    "## 46. SOURCE_COLLISION",
    "## 47. UNRESOLVED_REQUIRED_SURFACE",
    "## 48. Git Discipline",
    "## 49. VERSION_REFERENCES.json",
    "## 50. Fast-Gate Discipline",
    "## 51. Backward Compatibility",
    "## 52. Documentation After Change",
    "## 53. Promotion Boundary for Developers",
    "## 54. Developer Closure",
]


def validate():
    errors = []

    for path in (
        GUIDE,
        STABILITY,
        ARCH,
        MANUAL,
        ENTRY,
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    text = GUIDE.read_text(encoding="utf-8")

    stability = json.loads(
        STABILITY.read_text(encoding="utf-8")
    )

    if stability.get("disposition") != "STABLE_BASELINE":
        errors.append(
            "R7-J stability disposition is not STABLE_BASELINE"
        )

    baseline = stability.get("baseline_commit")

    if not baseline or baseline not in text:
        errors.append(
            "Developer Guide is not bound to R7-J baseline"
        )

    if "Responsibility: IMPLEMENTATION AND EXTENSION" not in text:
        errors.append(
            "Developer Guide responsibility mismatch"
        )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(
                f"Developer Guide missing section: {section}"
            )

    required = [
        "VERSION",
        "VERSION.json",
        "VERSION_AUTHORITY.md",
        "candidate/v41-complete",
        "contracts/",
        "schemas/",
        "receipts/",
        "tools/",
        "tests/",
        "docs/",
        "JSON Schema Draft 2020-12",
        "SHA-512",
        "SAME_OBJECT",
        "DISTINCT_OBJECT",
        "UNRESOLVED",
        "contracts/question/QUESTION_CONTRACT.md",
        "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
        "INNER_INVARIANT_CONTRADICTION",
        "OUTER_IMPLEMENTATION_DEFECT",
        "VALIDATOR_DEFECT",
        "COVERAGE_GAP",
        "SOURCE_COLLISION",
        "UNRESOLVED_REQUIRED_SURFACE",
        "git diff --check",
        "VERSION_REFERENCES.json",
        "Implementation leads.",
        "Documentation follows.",
        "DEVELOPER GUIDE COMPLETE.",
    ]

    for marker in required:
        if marker not in text:
            errors.append(
                f"Developer Guide missing required reference: {marker}"
            )

    prohibited = [
        "Promotion State: CANONICAL",
        "Authority: WRITE",
        "Human Gate: DISABLED",
        "External Runtime: ENABLED",
        "System Population: ALLOWED",
    ]

    for marker in prohibited:
        if marker in text:
            errors.append(
                f"Developer Guide contains prohibited state: {marker}"
            )

    if "ARCHITECTURE GUIDE COMPLETE." not in ARCH.read_text(
        encoding="utf-8"
    ):
        errors.append(
            "R7-E Architecture Guide is not complete"
        )

    if "USER MANUAL COMPLETE." not in MANUAL.read_text(
        encoding="utf-8"
    ):
        errors.append(
            "R7-D User Manual is not complete"
        )

    if "vTemporal.41.0" not in ENTRY.read_text(
        encoding="utf-8"
    ):
        errors.append(
            "native-v41 entry identity missing"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print("R7-F DEVELOPER GUIDE: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    stability = json.loads(
        STABILITY.read_text(encoding="utf-8")
    )

    print("R7-F DEVELOPER GUIDE: PASS")
    print(
        f"Stability baseline: {stability['baseline_commit']}"
    )
    print(
        "Documentation responsibility: IMPLEMENTATION AND EXTENSION"
    )
    print(
        "Repository structure: DOCUMENTED"
    )
    print(
        "Contracts / schemas / validators / tests: DOCUMENTED"
    )
    print(
        "Identity / SHA-512 / provenance: DOCUMENTED"
    )
    print(
        "Extension rules: DOCUMENTED"
    )
    print(
        "Failure classification: DOCUMENTED"
    )
    print(
        "Git / fast-gate discipline: DOCUMENTED"
    )
    print(
        "Authority boundary: PRESERVED"
    )
    print(
        "Alternate architecture creation: REJECTED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Promotion State: CANDIDATE"
    )
    print(
        "DEVELOPER GUIDE COMPLETE"
    )
    print(
        "R7-G Audit Guide: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
