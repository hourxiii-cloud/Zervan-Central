#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

GUIDE = ROOT / "docs/OPERATIONS_GUIDE.md"
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"
AUDIT = ROOT / "docs/AUDIT_GUIDE.md"
DEV = ROOT / "docs/DEVELOPER_GUIDE.md"
ARCH = ROOT / "docs/ARCHITECTURE_GUIDE.md"
MANUAL = ROOT / "docs/USER_MANUAL.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose",
    "## 2. Current Runtime Posture",
    "## 3. Startup Identity Check",
    "## 4. Repository State Check",
    "## 5. Operating Object",
    "## 6. Orientation",
    "## 7. Qualification Gate",
    "## 8. Occupancy",
    "## 9. Question Intake",
    "## 10. Evidence Boundary Check",
    "## 11. Evidence Ceiling Check",
    "## 12. Capability Routing",
    "## 14. Hydration",
    "## 15. Restriction and Constriction",
    "## 16. Perspective Rotation",
    "## 17. Distinct Object Handling",
    "## 18. Analysis Route",
    "## 24. Collapse Operation",
    "## 25. Landing Operation",
    "## 26. Reflight Operation",
    "## 27. Replay Operation",
    "## 28. Scar Operation",
    "## 34. Failure Classification",
    "## 36. Fast Gate",
    "## 37. Commit Discipline",
    "## 39. Return to Existing Work",
    "## 40. Runtime Restart",
    "## 42. Resilience Operation",
    "## 43. Provenance Operation",
    "## 45. Stability Boundary",
    "## 46. Transition Boundary",
    "## 47. Promotion Boundary",
    "## 49. Normal Operational Sequence",
    "## 50. Operational Stop Conditions",
    "## 51. Operational Recovery",
    "## 52. No-Default Drift",
    "## 53. External Runtime Boundary",
    "## 54. External Action Boundary",
    "## 55. System Population Boundary",
    "## 56. Canonical Mutation Boundary",
    "## 57. Operations Closure",
]


def validate():
    errors = []

    for path in (
        GUIDE,
        STABILITY,
        AUDIT,
        DEV,
        ARCH,
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
            "Operations Guide is not bound to R7-J baseline"
        )

    if "Responsibility: CONSISTENT RUNTIME OPERATION" not in text:
        errors.append(
            "Operations Guide responsibility mismatch"
        )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(
                f"Operations Guide missing section: {section}"
            )

    required = [
        "vTemporal.41.0",
        "v41 Complete",
        "candidate/v41-complete",
        "contracts/question/QUESTION_CONTRACT.md",
        "SAME_OBJECT",
        "DISTINCT_OBJECT",
        "UNRESOLVED",
        "Need determines force.",
        "Question determines mission.",
        "Evidence determines escalation.",
        "Restricted != nonexistent.",
        "Turn the object.",
        "Do not clone the world.",
        "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
        "INNER_INVARIANT_CONTRADICTION",
        "OUTER_IMPLEMENTATION_DEFECT",
        "VALIDATOR_DEFECT",
        "COVERAGE_GAP",
        "SOURCE_COLLISION",
        "UNRESOLVED_REQUIRED_SURFACE",
        "git diff --check",
        "git diff --cached --check",
        "VERSION_REFERENCES.json",
        "Transition accounting != promotion.",
        "Stability != completeness.",
        "Historical artifact != active implementation.",
        "READY_FOR_HUMAN_GATE is not CANONICAL.",
        "OPERATIONS GUIDE COMPLETE.",
    ]

    for marker in required:
        if marker not in text:
            errors.append(
                f"Operations Guide missing required reference: {marker}"
            )

    prohibited = [
        "Promotion State: CANONICAL",
        "Authority: WRITE",
        "Human Gate: DISABLED",
        "External Runtime: ENABLED",
        "External Action: ENABLED",
        "System Population: ALLOWED",
    ]

    for marker in prohibited:
        if marker in text:
            errors.append(
                f"Operations Guide contains prohibited state: {marker}"
            )

    if "AUDIT GUIDE COMPLETE." not in AUDIT.read_text(
        encoding="utf-8"
    ):
        errors.append(
            "R7-G Audit Guide is not complete"
        )

    if "DEVELOPER GUIDE COMPLETE." not in DEV.read_text(
        encoding="utf-8"
    ):
        errors.append(
            "R7-F Developer Guide is not complete"
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

    return errors


def main():
    errors = validate()

    if errors:
        print("R7-H OPERATIONS GUIDE: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    stability = json.loads(
        STABILITY.read_text(encoding="utf-8")
    )

    print("R7-H OPERATIONS GUIDE: PASS")
    print(
        f"Stability baseline: {stability['baseline_commit']}"
    )
    print(
        "Documentation responsibility: CONSISTENT RUNTIME OPERATION"
    )
    print(
        "Identity / orientation / qualification: DOCUMENTED"
    )
    print(
        "Question / evidence controls: DOCUMENTED"
    )
    print(
        "Routing / hydration / restriction: DOCUMENTED"
    )
    print(
        "Pipeline operation: DOCUMENTED"
    )
    print(
        "Collapse / Landing / Reflight / Replay / Scar: DOCUMENTED"
    )
    print(
        "Failure / recovery procedure: DOCUMENTED"
    )
    print(
        "Runtime boundaries: PRESERVED"
    )
    print(
        "External action: DISABLED"
    )
    print(
        "Promotion by operations: REJECTED"
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
        "OPERATIONS GUIDE COMPLETE"
    )
    print(
        "R7-K Completeness Receipt: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
