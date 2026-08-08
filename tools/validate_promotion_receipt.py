#!/usr/bin/env python3

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "contracts/promotion/PROMOTION_RECEIPT.md"
SCHEMA = ROOT / "schemas/promotion/promotion_receipt.schema.json"
RECEIPT = ROOT / "receipts/promotion/R7_L_PROMOTION_RECEIPT.json"
REGISTRY = ROOT / (
    "contracts/promotion/"
    "RING7_DOCUMENTATION_PROMOTION_BOUNDARY_REGISTRY.md"
)
TRANSITION = ROOT / "receipts/promotion/R7_I_TRANSITION_RECEIPT.json"
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"
COMPLETENESS = ROOT / "receipts/promotion/R7_K_COMPLETENESS_RECEIPT.json"


def validate():
    errors = []

    for path in (
        CONTRACT,
        SCHEMA,
        RECEIPT,
        REGISTRY,
        TRANSITION,
        STABILITY,
        COMPLETENESS,
    ):
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

    transition = json.loads(
        TRANSITION.read_text(encoding="utf-8")
    )

    stability = json.loads(
        STABILITY.read_text(encoding="utf-8")
    )

    completeness = json.loads(
        COMPLETENESS.read_text(encoding="utf-8")
    )

    registry = REGISTRY.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    if transition.get("transition_disposition") != "ACCOUNTED":
        errors.append(
            "R7-I transition state is not ACCOUNTED"
        )

    if stability.get("disposition") != "STABLE_BASELINE":
        errors.append(
            "R7-J stability state is not STABLE_BASELINE"
        )

    if completeness.get("disposition") != "COMPLETENESS_VALIDATED":
        errors.append(
            "R7-K completeness state is not COMPLETENESS_VALIDATED"
        )

    baseline = receipt.get("stability_baseline", "")

    if not re.fullmatch(r"[0-9a-f]{40}", baseline):
        errors.append(
            "invalid stability baseline"
        )

    if baseline != stability.get("baseline_commit"):
        errors.append(
            "promotion receipt stability baseline disagreement"
        )

    expected = {
        "schema_version": "1.0",
        "receipt_type": "PROMOTION_RECEIPT",
        "ring": "R7-L",
        "native_version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "source_branch": "candidate/v41-complete",
        "target_branch": "main",
        "transition_state": "ACCOUNTED",
        "stability_state": "STABLE_BASELINE",
        "completeness_state": "COMPLETENESS_VALIDATED",
        "fresh_reader_state": "PENDING_R7_M",
        "aggregate_state": "PENDING_R7_N",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "human_gate_authorization": "NOT_GRANTED",
        "promotion_state": "CANDIDATE",
        "promotion_readiness": "PRE_AUTHORIZATION_READY",
        "promoted": False,
        "canonical": False,
        "merged": False,
        "disposition": "PRE_AUTHORIZATION_READY",
    }

    for key, value in expected.items():
        if receipt.get(key) != value:
            errors.append(
                f"promotion receipt disagreement: {key}"
            )

    remaining = set(
        receipt.get("remaining_preconditions", [])
    )

    required_remaining = {
        "R7_M_FRESH_READER_FINAL_PACKAGE_VALIDATION",
        "R7_N_AGGREGATE_DOCUMENTATION_PROMOTION_READINESS_CLOSURE",
        "EXPLICIT_HUMAN_GATE_AUTHORIZATION_FOR_ACTUAL_PROMOTION",
    }

    if not required_remaining.issubset(remaining):
        errors.append(
            "required remaining preconditions are not preserved"
        )

    registry_markers = [
        "R7-L owns Promotion Receipt and pre-authorization promotion-readiness state.",
        "A Promotion Receipt before Human Gate authorization MUST NOT claim:",
        "- PROMOTED;",
        "- CANONICAL;",
        "- MERGED.",
        "Only explicit Human Gate authorization may permit candidate-to-main promotion.",
    ]

    for marker in registry_markers:
        if marker not in registry:
            errors.append(
                f"registry promotion marker missing: {marker}"
            )

    contract_markers = [
        "Promotion Receipt != promotion.",
        "Promotion readiness != canonical state.",
        "READY_FOR_HUMAN_GATE is a handoff state, not authorization.",
        "PRE_AUTHORIZATION_READY != READY_FOR_HUMAN_GATE.",
        "PRE_AUTHORIZATION_READY != PROMOTED.",
        "PRE_AUTHORIZATION_READY != CANONICAL.",
        "PRE_AUTHORIZATION_READY != MERGED.",
        "Receipt != authority.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "PRE-AUTHORIZATION PROMOTION READINESS RECORDED.",
    ]

    for marker in contract_markers:
        if marker not in contract:
            errors.append(
                f"promotion contract lock missing: {marker}"
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
        print("R7-L PROMOTION RECEIPT: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    receipt = json.loads(
        RECEIPT.read_text(encoding="utf-8")
    )

    print("R7-L PROMOTION RECEIPT: PASS")
    print(
        f"Stability baseline: {receipt['stability_baseline']}"
    )
    print("Transition accounting: ACCOUNTED")
    print("Stability: STABLE_BASELINE")
    print("Completeness: COMPLETENESS_VALIDATED")
    print("Promotion Receipt: SATISFIED")
    print("Source branch: candidate/v41-complete")
    print("Target branch: main")
    print("Fresh-Reader: PENDING_R7_M")
    print("Aggregate closure: PENDING_R7_N")
    print("Human Gate authorization: NOT_GRANTED")
    print("Promotion readiness: PRE_AUTHORIZATION_READY")
    print("Promoted: FALSE")
    print("Canonical: FALSE")
    print("Merged: FALSE")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    print("Promotion State: CANDIDATE")
    print("PRE-AUTHORIZATION PROMOTION READINESS RECORDED")
    print("R7-M Fresh-Reader Final Package Validation: NEXT")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
