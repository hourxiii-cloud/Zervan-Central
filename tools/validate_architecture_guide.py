#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

GUIDE = ROOT / "docs/ARCHITECTURE_GUIDE.md"
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"
ENTRY = ROOT / "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md"
MANUAL = ROOT / "docs/USER_MANUAL.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose",
    "## 2. Architectural Problem",
    "## 3. One Analytical Object",
    "## 4. Why the Room Exists",
    "## 5. Origin, Ingress, and Genesis",
    "## 6. Revision and Branch",
    "## 7. Operational Geography",
    "## 8. Territory and Terrain",
    "## 9. Zone",
    "## 10. Space",
    "## 11. Representation Transform",
    "## 12. Cartography",
    "## 13. Stick Continuity",
    "## 14. Qualification Before Analysis",
    "## 15. Request State and Room State",
    "## 16. Occupancy",
    "## 17. Question Contract",
    "## 18. Evidence Boundary",
    "## 19. Evidence Ceiling",
    "## 20. Capability Routing",
    "## 21. Scale and Formation",
    "## 22. Hydration",
    "## 23. Restriction and Constriction",
    "## 24. Collapse",
    "## 25. Landing",
    "## 26. Reflight",
    "## 27. Replay",
    "## 28. Scar",
    "## 29. Scar Replay",
    "## 30. Distinct Object Test",
    "## 31. Passageways",
    "## 32. Analytical Pipeline",
    "## 33. PMC",
    "## 34. CCR",
    "## 35. MC",
    "## 36. Raven",
    "## 37. Human Gate",
    "## 38. Validation Architecture",
    "## 39. Failure Taxonomy",
    "## 40. Stability Before Documentation",
    "## 41. Documentation Separation",
    "## 42. Version and Promotion Separation",
    "## 43. Authority Model",
    "## 44. Architecture Closure",
]


def validate():
    errors = []

    for path in (
        GUIDE,
        STABILITY,
        ENTRY,
        MANUAL,
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
            "Architecture Guide is not bound to R7-J baseline"
        )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(
                f"Architecture Guide missing section: {section}"
            )

    if "Responsibility: RATIONALE AND PRIMITIVES" not in text:
        errors.append(
            "Architecture Guide responsibility mismatch"
        )

    required_references = [
        "vTemporal.41.0",
        "Origin",
        "Ingress",
        "Genesis",
        "Room",
        "Territory",
        "Terrain",
        "Zone",
        "Space",
        "Representation Transform",
        "Cartography",
        "Stick continuity",
        "Question Contract",
        "Evidence Boundary",
        "Evidence Ceiling",
        "SAME_OBJECT",
        "DISTINCT_OBJECT",
        "UNRESOLVED",
        "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
        "INNER_INVARIANT_CONTRADICTION",
        "OUTER_IMPLEMENTATION_DEFECT",
        "VALIDATOR_DEFECT",
        "COVERAGE_GAP",
        "SOURCE_COLLISION",
        "UNRESOLVED_REQUIRED_SURFACE",
        "Implementation leads.",
        "Documentation follows.",
        "ARCHITECTURE GUIDE COMPLETE.",
    ]

    for marker in required_references:
        if marker not in text:
            errors.append(
                f"Architecture Guide missing required reference: {marker}"
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
                f"Architecture Guide contains prohibited state: {marker}"
            )

    entry = ENTRY.read_text(encoding="utf-8")

    if "vTemporal.41.0" not in entry:
        errors.append(
            "native-v41 entry identity missing"
        )

    if "THE ROOM IS ONE ANALYTICAL OBJECT." not in entry:
        errors.append(
            "native-v41 Room primitive missing"
        )

    manual = MANUAL.read_text(encoding="utf-8")

    if "USER MANUAL COMPLETE." not in manual:
        errors.append(
            "R7-D User Manual is not complete"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print("R7-E ARCHITECTURE GUIDE: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    stability = json.loads(
        STABILITY.read_text(encoding="utf-8")
    )

    print("R7-E ARCHITECTURE GUIDE: PASS")
    print(
        f"Stability baseline: {stability['baseline_commit']}"
    )
    print(
        "Documentation responsibility: RATIONALE AND PRIMITIVES"
    )
    print(
        "One-object architecture: DOCUMENTED"
    )
    print(
        "Operational geography: DOCUMENTED"
    )
    print(
        "Qualification / occupancy: DOCUMENTED"
    )
    print(
        "Question / evidence controls: DOCUMENTED"
    )
    print(
        "Routing / hydration / representation: DOCUMENTED"
    )
    print(
        "Collapse / Landing / Reflight / Replay / Scar: DOCUMENTED"
    )
    print(
        "Distinct-object / Passageway architecture: DOCUMENTED"
    )
    print(
        "PMC / CCR / MC / Raven / Human Gate separation: DOCUMENTED"
    )
    print(
        "Validation / failure taxonomy: DOCUMENTED"
    )
    print(
        "Architecture guide as alternate implementation: REJECTED"
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
        "ARCHITECTURE GUIDE COMPLETE"
    )
    print(
        "R7-F Developer Guide: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
