#!/usr/bin/env python3

from pathlib import Path
import argparse
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

RING6 = ROOT / "tools/validate_ring6.py"

REGISTRY = ROOT / (
    "contracts/promotion/"
    "RING7_DOCUMENTATION_PROMOTION_BOUNDARY_REGISTRY.md"
)
TRANSITION = ROOT / "receipts/promotion/R7_I_TRANSITION_RECEIPT.json"
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"
COMPLETENESS = ROOT / "receipts/promotion/R7_K_COMPLETENESS_RECEIPT.json"
PROMOTION = ROOT / "receipts/promotion/R7_L_PROMOTION_RECEIPT.json"
FRESH_READER = ROOT / (
    "contracts/validation/"
    "R7_M_FRESH_READER_FINAL_PACKAGE_VALIDATION.md"
)
CLOSURE = ROOT / (
    "contracts/validation/"
    "RING7_AGGREGATE_DOCUMENTATION_PROMOTION_READINESS_CLOSURE.md"
)

VERSION = ROOT / "VERSION"
VERSION_JSON = ROOT / "VERSION.json"
VERSION_AUTHORITY = ROOT / "VERSION_AUTHORITY.md"
README = ROOT / "README.md"
INIT = ROOT / "call/INITIATION_STATEMENT_V41_0.md"
ENTRY = ROOT / "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md"

USER = ROOT / "docs/USER_MANUAL.md"
ARCH = ROOT / "docs/ARCHITECTURE_GUIDE.md"
DEV = ROOT / "docs/DEVELOPER_GUIDE.md"
AUDIT = ROOT / "docs/AUDIT_GUIDE.md"
OPS = ROOT / "docs/OPERATIONS_GUIDE.md"
QUESTION = ROOT / "contracts/question/QUESTION_CONTRACT.md"


def run_ring6():
    return subprocess.run(
        [
            sys.executable,
            str(RING6),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def validate(run_dependency=True):
    errors = []

    required = [
        RING6,
        REGISTRY,
        TRANSITION,
        STABILITY,
        COMPLETENESS,
        PROMOTION,
        FRESH_READER,
        CLOSURE,
        VERSION,
        VERSION_JSON,
        VERSION_AUTHORITY,
        README,
        INIT,
        ENTRY,
        USER,
        ARCH,
        DEV,
        AUDIT,
        OPS,
        QUESTION,
    ]

    for path in required:
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    if run_dependency:
        ring6 = run_ring6()
        combined = ring6.stdout + ring6.stderr

        if ring6.returncode != 0:
            errors.append(
                "Ring 6 aggregate dependency failed\n"
                + combined.rstrip()
            )
        elif "RING 6 RESULT: PASS" not in combined:
            errors.append(
                "Ring 6 aggregate did not emit RING 6 RESULT: PASS\n"
                + combined.rstrip()
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
    promotion = json.loads(
        PROMOTION.read_text(encoding="utf-8")
    )
    version_json = json.loads(
        VERSION_JSON.read_text(encoding="utf-8")
    )

    fresh = FRESH_READER.read_text(
        encoding="utf-8"
    )
    closure = CLOSURE.read_text(
        encoding="utf-8"
    )
    registry = REGISTRY.read_text(
        encoding="utf-8"
    )

    if (
        transition.get("transition_disposition")
        != "ACCOUNTED"
    ):
        errors.append(
            "R7-I transition accounting is not ACCOUNTED"
        )

    if (
        stability.get("disposition")
        != "STABLE_BASELINE"
    ):
        errors.append(
            "R7-J stability is not STABLE_BASELINE"
        )

    if (
        completeness.get("disposition")
        != "COMPLETENESS_VALIDATED"
    ):
        errors.append(
            "R7-K completeness is not COMPLETENESS_VALIDATED"
        )

    if (
        promotion.get("disposition")
        != "PRE_AUTHORIZATION_READY"
    ):
        errors.append(
            "R7-L disposition is not PRE_AUTHORIZATION_READY"
        )

    if (
        promotion.get("human_gate_authorization")
        != "NOT_GRANTED"
    ):
        errors.append(
            "Human Gate authorization was unexpectedly granted"
        )

    for key in (
        "promoted",
        "canonical",
        "merged",
    ):
        if promotion.get(key) is not False:
            errors.append(
                f"R7-L historical receipt unexpectedly sets {key}=true"
            )

    expected_version = {
        "version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "promotion_state": "CANDIDATE",
        "canonical": False,
        "canonical_branch": "main",
        "development_branch": "candidate/v41-complete",
    }

    for key, value in expected_version.items():
        if version_json.get(key) != value:
            errors.append(
                f"VERSION.json disagreement: {key}"
            )

    if VERSION.read_text(
        encoding="utf-8"
    ).strip() != "vTemporal.41.0":
        errors.append(
            "VERSION disagreement"
        )

    documentation = {
        README: "README owns orientation.",
        USER: "USER MANUAL COMPLETE.",
        ARCH: "ARCHITECTURE GUIDE COMPLETE.",
        DEV: "DEVELOPER GUIDE COMPLETE.",
        AUDIT: "AUDIT GUIDE COMPLETE.",
        OPS: "OPERATIONS GUIDE COMPLETE.",
    }

    for path, marker in documentation.items():
        text = path.read_text(encoding="utf-8")

        if marker not in text:
            errors.append(
                f"documentation closure missing: {path.relative_to(ROOT)}"
            )

    if (
        "FRESH-READER FINAL PACKAGE VALIDATION COMPLETE."
        not in fresh
    ):
        errors.append(
            "R7-M Fresh-Reader closure missing"
        )

    fresh_markers = [
        "FRESH_READER_FINAL_PACKAGE = PASS",
        "REPOSITORY_ONLY_RECOVERY = PASS",
        "PRIVATE_CONVERSATIONAL_PREREQUISITE = NONE",
        "V40_INTERPRETIVE_PREREQUISITE = NONE",
    ]

    for marker in fresh_markers:
        if marker not in fresh:
            errors.append(
                f"R7-M Fresh-Reader marker missing: {marker}"
            )

    normalized_registry = " ".join(
        registry.split()
    )

    registry_markers = [
        "R7-N owns Ring 7 aggregate Documentation / Promotion Readiness closure.",
        "Ring 7 aggregate SHALL traverse Ring 6 exactly once.",
        "Ring 7 SHALL NOT separately rerun Rings 1 through 5.",
        "One dependency traversal is sufficient.",
        "Ring 7 target = READY_FOR_HUMAN_GATE.",
    ]

    for marker in registry_markers:
        if marker not in normalized_registry:
            errors.append(
                f"R7-A aggregate rule missing: {marker}"
            )

    closure_markers = [
        "RING 7 RESULT: PASS",
        "DOCUMENTATION COMPLETE",
        "QUESTION CONTRACT COMPLETE",
        "NATIVE-v41 ENTRY COMPLETE",
        "TRANSITION ACCOUNTING COMPLETE",
        "STABILITY VALIDATED",
        "COMPLETENESS VALIDATED",
        "FRESH-READER VALIDATED",
        "PROMOTION PACKAGE COMPLETE",
        "PROMOTION READINESS READY_FOR_HUMAN_GATE",
        "Authority: NONE",
        "Human Gate: ACTIVE",
        "Promotion State: CANDIDATE",
        "Canonical: FALSE",
        "Promoted: FALSE",
        "Merged: FALSE",
        "Human Gate Authorization: NOT_GRANTED",
        "READY_FOR_HUMAN_GATE != authorization.",
        "READY_FOR_HUMAN_GATE != PROMOTED.",
        "READY_FOR_HUMAN_GATE != CANONICAL.",
        "READY_FOR_HUMAN_GATE != MERGED.",
        "RING 7 AGGREGATE DOCUMENTATION / PROMOTION READINESS CLOSURE COMPLETE.",
    ]

    for marker in closure_markers:
        if marker not in closure:
            errors.append(
                f"R7-N closure marker missing: {marker}"
            )

    prohibited = [
        "Promotion State: CANONICAL",
        "Authority: WRITE",
        "Human Gate: DISABLED",
        "Human Gate Authorization: GRANTED",
        "Canonical: TRUE",
        "Promoted: TRUE",
        "Merged: TRUE",
    ]

    for marker in prohibited:
        if marker in closure:
            errors.append(
                f"R7-N closure contains prohibited state: {marker}"
            )

    return errors


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Validate R7-N aggregate closure. "
            "Use --full for the single heavyweight Ring 6 dependency traversal."
        )
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="run Ring 6 aggregate dependency exactly once",
    )

    args = parser.parse_args()

    errors = validate(
        run_dependency=args.full
    )

    if errors:
        print(
            "R7-N AGGREGATE DOCUMENTATION / PROMOTION READINESS: FAIL"
        )

        for error in errors:
            print(f" - {error}")

        return 1

    print(
        "R7-N AGGREGATE DOCUMENTATION / PROMOTION READINESS: PASS"
    )

    if args.full:
        print("Ring 6 dependency traversal: PASS / EXACTLY ONCE")
    else:
        print("Ring 6 dependency traversal: DEFERRED TO --full")

    print("Rings 1-5 separate traversal: NOT PERFORMED")
    print("Documentation: COMPLETE")
    print("Question Contract: COMPLETE")
    print("Native-v41 entry: COMPLETE")
    print("Transition accounting: COMPLETE")
    print("Stability: VALIDATED")
    print("Completeness: VALIDATED")
    print("Fresh-Reader: VALIDATED")
    print("Promotion package: COMPLETE")
    print("Promotion Readiness: READY_FOR_HUMAN_GATE")
    print("Human Gate authorization: NOT_GRANTED")
    print("Promoted: FALSE")
    print("Canonical: FALSE")
    print("Merged: FALSE")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    print("Promotion State: CANDIDATE")
    print("RING 7 RESULT: PASS")
    print(
        "RING 7 AGGREGATE DOCUMENTATION / "
        "PROMOTION READINESS CLOSURE COMPLETE"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
