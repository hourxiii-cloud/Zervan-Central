#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

GUIDE = ROOT / "docs/AUDIT_GUIDE.md"
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"
DEV = ROOT / "docs/DEVELOPER_GUIDE.md"
ARCH = ROOT / "docs/ARCHITECTURE_GUIDE.md"
MANUAL = ROOT / "docs/USER_MANUAL.md"

REQUIRED_SECTIONS = [
    "## 1. Purpose",
    "## 2. Audit Objective",
    "## 3. Evidence First",
    "## 4. Audit Source Order",
    "## 5. Version Verification",
    "## 6. Authority Verification",
    "## 7. Room Identity Verification",
    "## 8. Distinct Object Verification",
    "## 9. Genesis and Revision Verification",
    "## 10. Cryptographic Verification",
    "## 11. Operational Geography Verification",
    "## 12. Qualification Verification",
    "## 13. Occupancy Verification",
    "## 14. Question Contract Verification",
    "## 15. Evidence Boundary Verification",
    "## 16. Evidence Ceiling Verification",
    "## 17. Capability Routing Verification",
    "## 18. Formation Verification",
    "## 19. Hydration Verification",
    "## 20. Restriction Verification",
    "## 21. Collapse Verification",
    "## 22. Landing Verification",
    "## 23. Reflight Verification",
    "## 24. Replay Verification",
    "## 25. Scar Verification",
    "## 26. Representation Independence Verification",
    "## 27. Replacement Verification",
    "## 28. Resilience Verification",
    "## 29. Pipeline Verification",
    "## 35. Provenance Verification",
    "## 39. Failure Classification",
    "## 47. Completion Criteria",
    "## 49. Fresh-Reader Criterion",
    "## 50. Lossless-Collapse Criterion",
    "## 54. Audit Independence",
    "## 56. Promotion Audit Boundary",
    "## 57. Audit Closure",
]


def validate():
    errors = []

    for path in (
        GUIDE,
        STABILITY,
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
            "Audit Guide is not bound to R7-J baseline"
        )

    if (
        "Responsibility: VERIFICATION / REPLACEMENT / RESILIENCE / "
        "PROVENANCE / COMPLETION CRITERIA"
        not in text
    ):
        errors.append(
            "Audit Guide responsibility mismatch"
        )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(
                f"Audit Guide missing section: {section}"
            )

    required = [
        "vTemporal.41.0",
        "v41 Complete",
        "SAME_OBJECT",
        "DISTINCT_OBJECT",
        "UNRESOLVED",
        "SHA-512",
        "Hash != truth.",
        "Signature != correctness.",
        "Integrity != semantic correctness.",
        "Question != authority.",
        "Need determines force.",
        "Question determines mission.",
        "Evidence determines escalation.",
        "Restricted != nonexistent.",
        "Landing != Replay.",
        "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
        "INNER_INVARIANT_CONTRADICTION",
        "OUTER_IMPLEMENTATION_DEFECT",
        "VALIDATOR_DEFECT",
        "COVERAGE_GAP",
        "SOURCE_COLLISION",
        "UNRESOLVED_REQUIRED_SURFACE",
        "Transition accounting != promotion.",
        "Stability != completeness.",
        "Completion != promotion.",
        "Historical artifact != active implementation.",
        "VERSION_REFERENCES.json",
        "AUDIT GUIDE COMPLETE.",
    ]

    for marker in required:
        if marker not in text:
            errors.append(
                f"Audit Guide missing required reference: {marker}"
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
                f"Audit Guide contains prohibited state: {marker}"
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
        print("R7-G AUDIT GUIDE: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    stability = json.loads(
        STABILITY.read_text(encoding="utf-8")
    )

    print("R7-G AUDIT GUIDE: PASS")
    print(
        f"Stability baseline: {stability['baseline_commit']}"
    )
    print(
        "Documentation responsibility: VERIFICATION / REPLACEMENT / "
        "RESILIENCE / PROVENANCE / COMPLETION CRITERIA"
    )
    print(
        "Identity / geography / qualification: AUDITABLE"
    )
    print(
        "Question / evidence controls: AUDITABLE"
    )
    print(
        "Routing / hydration / restriction: AUDITABLE"
    )
    print(
        "Replay / Scar / replacement / resilience: AUDITABLE"
    )
    print(
        "Pipeline / provenance: AUDITABLE"
    )
    print(
        "Completion criteria: DOCUMENTED"
    )
    print(
        "Audit as implementation owner: REJECTED"
    )
    print(
        "Promotion by audit: REJECTED"
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
        "AUDIT GUIDE COMPLETE"
    )
    print(
        "R7-H Operations Guide: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
