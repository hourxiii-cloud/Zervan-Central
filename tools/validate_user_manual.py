#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

MANUAL = ROOT / "docs/USER_MANUAL.md"
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"
ENTRY = ROOT / "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md"
QUESTION = ROOT / "contracts/question/QUESTION_CONTRACT.md"


REQUIRED_SECTIONS = [
    "## 1. Purpose",
    "## 2. Start Native v41",
    "## 3. Understand the Room",
    "## 4. Understand Operational Geography",
    "## 5. Preserve Identity",
    "## 6. Qualify Before Analysis",
    "## 7. Occupancy",
    "## 8. Ask a Question",
    "## 9. Read-Only Inquiry",
    "## 10. Evidence Boundary and Evidence Ceiling",
    "## 11. Route Capability Proportionally",
    "## 12. Hydrate on Need",
    "## 13. Restriction and Constriction",
    "## 14. Perspective and Representation",
    "## 15. Distinct Objects and Passageways",
    "## 16. Collapse",
    "## 17. Landing",
    "## 18. Reflight",
    "## 19. Replay",
    "## 20. Scar and Scar Replay",
    "## 21. Analytical Pipeline",
    "## 22. Reports and Renderings",
    "## 23. Decision Support",
    "## 24. Blocked, Provisional, Degraded, and Rejected Operation",
    "## 25. Uncertainty",
    "## 26. Failure Handling",
    "## 27. Returning to Existing Work",
    "## 28. Normal User Operating Sequence",
    "## 29. Runtime Boundary",
    "## 30. Promotion Boundary",
    "## 31. Documentation Boundary",
    "## 32. Quick Operational Reference",
    "## 33. User Manual Closure",
]


def validate():
    errors = []

    for path in (
        MANUAL,
        STABILITY,
        ENTRY,
        QUESTION,
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    text = MANUAL.read_text(
        encoding="utf-8"
    )

    stability = json.loads(
        STABILITY.read_text(
            encoding="utf-8"
        )
    )

    if stability.get("disposition") != "STABLE_BASELINE":
        errors.append(
            "R7-J stability disposition is not STABLE_BASELINE"
        )

    if stability.get("documentation_freeze") is not True:
        errors.append(
            "R7-J documentation freeze is not established"
        )

    baseline = stability.get(
        "baseline_commit"
    )

    if not baseline or baseline not in text:
        errors.append(
            "User Manual is not bound to the R7-J baseline commit"
        )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(
                f"User Manual missing section: {section}"
            )

    required_references = [
        "VERSION",
        "VERSION.json",
        "VERSION_AUTHORITY.md",
        "call/INITIATION_STATEMENT_V41_0.md",
        "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md",
        "contracts/question/QUESTION_CONTRACT.md",
        "vTemporal.41.0",
        "v41 Complete",
        "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate",
        "INNER_INVARIANT_CONTRADICTION",
        "OUTER_IMPLEMENTATION_DEFECT",
        "VALIDATOR_DEFECT",
        "COVERAGE_GAP",
        "SOURCE_COLLISION",
        "UNRESOLVED_REQUIRED_SURFACE",
        "USER MANUAL COMPLETE.",
    ]

    for reference in required_references:
        if reference not in text:
            errors.append(
                f"User Manual missing required reference: {reference}"
            )

    # Documentation-state checks, not doctrine-by-literal-prose checks.
    if "Responsibility: UNDERSTANDING AND OPERATION" not in text:
        errors.append(
            "User Manual responsibility is not UNDERSTANDING AND OPERATION"
        )

    if "Authority: NONE" not in text:
        errors.append(
            "User Manual authority state missing"
        )

    if "Human Gate: ACTIVE" not in text:
        errors.append(
            "User Manual Human Gate state missing"
        )

    if "Promotion State: CANDIDATE" not in text:
        errors.append(
            "User Manual candidate state missing"
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
                f"User Manual contains prohibited state: {marker}"
            )

    # Source existence and identity are required; the manual is not forced
    # to reproduce source contracts sentence-for-sentence.
    entry_text = ENTRY.read_text(
        encoding="utf-8"
    )

    question_text = QUESTION.read_text(
        encoding="utf-8"
    )

    if "vTemporal.41.0" not in entry_text:
        errors.append(
            "native-v41 entry version missing"
        )

    if "Question Contract" not in question_text:
        errors.append(
            "Question Contract source unavailable"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print("R7-D USER MANUAL: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    stability = json.loads(
        STABILITY.read_text(
            encoding="utf-8"
        )
    )

    print("R7-D USER MANUAL: PASS")
    print(
        f"Stability baseline: {stability['baseline_commit']}"
    )
    print(
        "Documentation responsibility: UNDERSTANDING AND OPERATION"
    )
    print(
        "Repository-only operation: DOCUMENTED"
    )
    print(
        "Room / geography / qualification: DOCUMENTED"
    )
    print(
        "Question / evidence boundaries: DOCUMENTED"
    )
    print(
        "Routing / hydration / representation: DOCUMENTED"
    )
    print(
        "Collapse / Landing / Reflight / Replay / Scar: DOCUMENTED"
    )
    print(
        "Pipeline / reporting / decision support: DOCUMENTED"
    )
    print(
        "Blocked / degraded / uncertainty behavior: DOCUMENTED"
    )
    print(
        "Failure handling: DOCUMENTED"
    )
    print(
        "Runtime / promotion boundary: DOCUMENTED"
    )
    print(
        "Private conversational prerequisite: NONE"
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
        "USER MANUAL COMPLETE"
    )
    print(
        "R7-E Architecture Guide: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
