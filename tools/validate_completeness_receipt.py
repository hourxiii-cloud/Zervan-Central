#!/usr/bin/env python3

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "contracts/promotion/COMPLETENESS_RECEIPT.md"
SCHEMA = ROOT / "schemas/promotion/completeness_receipt.schema.json"
RECEIPT = ROOT / "receipts/promotion/R7_K_COMPLETENESS_RECEIPT.json"
REGISTRY = ROOT / (
    "contracts/promotion/"
    "RING7_DOCUMENTATION_PROMOTION_BOUNDARY_REGISTRY.md"
)
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"

DOCS = {
    "README": ROOT / "README.md",
    "USER_MANUAL": ROOT / "docs/USER_MANUAL.md",
    "ARCHITECTURE_GUIDE": ROOT / "docs/ARCHITECTURE_GUIDE.md",
    "DEVELOPER_GUIDE": ROOT / "docs/DEVELOPER_GUIDE.md",
    "AUDIT_GUIDE": ROOT / "docs/AUDIT_GUIDE.md",
    "OPERATIONS_GUIDE": ROOT / "docs/OPERATIONS_GUIDE.md",
}

MACHINE = {
    "QUESTION_CONTRACT":
        ROOT / "contracts/question/QUESTION_CONTRACT.md",
    "TRANSITION_RECEIPT":
        ROOT / "receipts/promotion/R7_I_TRANSITION_RECEIPT.json",
    "STABILITY_RECEIPT":
        ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json",
    "COMPLETENESS_RECEIPT":
        RECEIPT,
}


def validate():
    errors = []

    required_files = [
        CONTRACT,
        SCHEMA,
        RECEIPT,
        REGISTRY,
        STABILITY,
        *DOCS.values(),
        *MACHINE.values(),
    ]

    for path in required_files:
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    receipt = json.loads(
        RECEIPT.read_text(encoding="utf-8")
    )

    schema = json.loads(
        SCHEMA.read_text(encoding="utf-8")
    )

    stability = json.loads(
        STABILITY.read_text(encoding="utf-8")
    )

    registry = REGISTRY.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    if stability.get("disposition") != "STABLE_BASELINE":
        errors.append(
            "R7-J stability disposition is not STABLE_BASELINE"
        )

    baseline = receipt.get("stability_baseline", "")

    if not re.fullmatch(r"[0-9a-f]{40}", baseline):
        errors.append(
            "invalid stability baseline"
        )

    if baseline != stability.get("baseline_commit"):
        errors.append(
            "completeness baseline disagrees with R7-J"
        )

    expected = {
        "schema_version": "1.0",
        "receipt_type": "COMPLETENESS_RECEIPT",
        "ring": "R7-K",
        "native_version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "promotion_state": "CANDIDATE",
        "promotion_ready": False,
        "canonical": False,
        "disposition": "COMPLETENESS_VALIDATED",
    }

    for key, value in expected.items():
        if receipt.get(key) != value:
            errors.append(
                f"receipt disagreement: {key}"
            )

    documentation = receipt.get("documentation", {})

    for name, path in DOCS.items():
        if documentation.get(name) != "SATISFIED":
            errors.append(
                f"documentation not SATISFIED: {name}"
            )

        if not path.exists():
            errors.append(
                f"documentation missing: {name}"
            )

    machine = receipt.get(
        "machine_readable_surfaces",
        {},
    )

    for name, path in MACHINE.items():
        if machine.get(name) != "SATISFIED":
            errors.append(
                f"machine surface not SATISFIED: {name}"
            )

        if not path.exists():
            errors.append(
                f"machine surface missing: {name}"
            )

    if machine.get(
        "PROMOTION_RECEIPT"
    ) != "DEFERRED_TO_R7_L":
        errors.append(
            "Promotion Receipt is not explicitly deferred to R7-L"
        )

    if receipt.get("remaining_sections") != [
        "R7-L",
        "R7-M",
        "R7-N",
    ]:
        errors.append(
            "remaining Ring 7 sections are not explicit"
        )

    blockers = set(
        receipt.get("promotion_blockers", [])
    )

    required_blockers = {
        "PROMOTION_RECEIPT_PENDING_R7_L",
        "FRESH_READER_PENDING_R7_M",
        "AGGREGATE_CLOSURE_PENDING_R7_N",
        "EXPLICIT_HUMAN_GATE_AUTHORIZATION_REQUIRED",
    }

    if not required_blockers.issubset(blockers):
        errors.append(
            "required promotion blockers are not preserved"
        )

    registry_markers = [
        "R7-K owns Completeness Receipt.",
        "Promotion Receipt is owned by R7-L.",
        "Fresh-Reader final package validation is owned by R7-M.",
        "Aggregate promotion-readiness closure is owned by R7-N.",
        "Completeness != promotion.",
        "Deferred != forgotten.",
    ]

    for marker in registry_markers:
        if marker not in registry:
            errors.append(
                f"registry ownership marker missing: {marker}"
            )

    contract_markers = [
        "COMPLETENESS_VALIDATED != READY_FOR_HUMAN_GATE.",
        "COMPLETENESS_VALIDATED != PROMOTED.",
        "COMPLETENESS_VALIDATED != CANONICAL.",
        "Deferred != forgotten.",
        "Validated != promoted.",
        "Receipt != authority.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "COMPLETENESS VALIDATED.",
    ]

    for marker in contract_markers:
        if marker not in contract:
            errors.append(
                f"completeness contract lock missing: {marker}"
            )

    if (
        schema.get("$schema")
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        errors.append(
            "schema draft disagreement"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print("R7-K COMPLETENESS RECEIPT: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    receipt = json.loads(
        RECEIPT.read_text(encoding="utf-8")
    )

    print("R7-K COMPLETENESS RECEIPT: PASS")
    print(
        f"Stability baseline: {receipt['stability_baseline']}"
    )
    print("Documentation surfaces: SATISFIED")
    print("Question Contract: SATISFIED")
    print("Transition Receipt: SATISFIED")
    print("Stability Receipt: SATISFIED")
    print("Completeness Receipt: SATISFIED")
    print("Promotion Receipt: DEFERRED_TO_R7_L")
    print("Fresh-Reader validation: DEFERRED_TO_R7_M")
    print("Aggregate closure: DEFERRED_TO_R7_N")
    print("Promotion blockers: PRESERVED")
    print("Promotion ready: FALSE")
    print("Canonical: FALSE")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    print("Promotion State: CANDIDATE")
    print("COMPLETENESS VALIDATED")
    print("R7-L Promotion Receipt / Promotion-Readiness Record: NEXT")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
