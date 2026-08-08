#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

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

PROMOTION = ROOT / "receipts/promotion/R7_L_PROMOTION_RECEIPT.json"
COMPLETENESS = ROOT / "receipts/promotion/R7_K_COMPLETENESS_RECEIPT.json"
STABILITY = ROOT / "receipts/promotion/R7_J_STABILITY_RECEIPT.json"

CONTRACT = ROOT / (
    "contracts/validation/"
    "R7_M_FRESH_READER_FINAL_PACKAGE_VALIDATION.md"
)


def require(text, marker, label, errors):
    if marker not in text:
        errors.append(
            f"{label} missing required marker: {marker}"
        )


def validate():
    errors = []

    paths = [
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
        PROMOTION,
        COMPLETENESS,
        STABILITY,
        CONTRACT,
    ]

    for path in paths:
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    version = VERSION.read_text(
        encoding="utf-8"
    ).strip()

    version_json = json.loads(
        VERSION_JSON.read_text(
            encoding="utf-8"
        )
    )

    promotion = json.loads(
        PROMOTION.read_text(
            encoding="utf-8"
        )
    )

    completeness = json.loads(
        COMPLETENESS.read_text(
            encoding="utf-8"
        )
    )

    stability = json.loads(
        STABILITY.read_text(
            encoding="utf-8"
        )
    )

    readme = README.read_text(encoding="utf-8")
    authority = VERSION_AUTHORITY.read_text(encoding="utf-8")
    init = INIT.read_text(encoding="utf-8")
    entry = ENTRY.read_text(encoding="utf-8")
    user = USER.read_text(encoding="utf-8")
    arch = ARCH.read_text(encoding="utf-8")
    dev = DEV.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    ops = OPS.read_text(encoding="utf-8")
    question = QUESTION.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    # --------------------------------------------------------
    # VERSION RECOVERY
    # --------------------------------------------------------

    if version != "vTemporal.41.0":
        errors.append(
            "VERSION does not resolve to vTemporal.41.0"
        )

    expected_version_json = {
        "version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "promotion_state": "CANDIDATE",
        "canonical": False,
        "canonical_branch": "main",
        "development_branch": "candidate/v41-complete",
        "inferred_versioning_allowed": False,
        "mixed_version_identity_allowed": False,
    }

    for key, value in expected_version_json.items():
        if version_json.get(key) != value:
            errors.append(
                f"VERSION.json disagreement: {key}"
            )

    for marker in (
        "VERSION",
        "VERSION.json",
        "VERSION_AUTHORITY.md",
        "call/INITIATION_STATEMENT_V41_0.md",
        "canonical/ZERVAN_v41_0_CANONICAL_ENTRY.md",
        "vTemporal.41.0",
        "v41 Complete",
        "candidate/v41-complete",
        "CANDIDATE",
        "main",
    ):
        require(
            readme,
            marker,
            "README",
            errors,
        )

    require(
        authority,
        "vTemporal.41.0",
        "VERSION_AUTHORITY",
        errors,
    )

    require(
        init,
        "vTemporal.41.0",
        "initiation statement",
        errors,
    )

    require(
        entry,
        "vTemporal.41.0",
        "canonical entry",
        errors,
    )

    require(
        entry,
        "v41 Complete",
        "canonical entry",
        errors,
    )

    # --------------------------------------------------------
    # NO HISTORICAL INTERPRETIVE DEPENDENCY
    # --------------------------------------------------------

    require(
        readme,
        "Native v41 does not require prior v39 or v40 knowledge to initialize.",
        "README",
        errors,
    )

    require(
        entry,
        "Native v41 does not require v40 as an interpretive overlay.",
        "canonical entry",
        errors,
    )

    # --------------------------------------------------------
    # ROOM / GEOGRAPHY RECOVERY
    # --------------------------------------------------------

    for marker in (
        "THE ROOM IS ONE ANALYTICAL OBJECT.",
        "Perspective != Room.",
        "Zone != Room.",
        "Space != Room.",
        "TURN THE OBJECT. DO NOT CLONE THE WORLD.",
    ):
        require(
            entry,
            marker,
            "canonical entry",
            errors,
        )

    geography = (
        "Origin\n->\nIngress\n->\nGenesis\n->\nRoom\n->\n"
        "Territory\n->\nTerrain\n->\nZone\n->\nSpace\n->\n"
        "Representation Transform\n->\nCartography\n->\n"
        "Stick continuity"
    )

    require(
        entry,
        geography,
        "canonical entry",
        errors,
    )

    # --------------------------------------------------------
    # QUALIFICATION / QUESTION
    # --------------------------------------------------------

    require(
        entry,
        "QUALIFICATION PRECEDES ANALYSIS.",
        "canonical entry",
        errors,
    )

    require(
        entry,
        "contracts/question/QUESTION_CONTRACT.md",
        "canonical entry",
        errors,
    )

    for marker in (
        "Question != mutation.",
        "Question Contract != authority.",
    ):
        require(
            entry,
            marker,
            "canonical entry",
            errors,
        )

    for marker in (
        "read-only",
        "evidence boundary",
        "evidence ceiling",
        "Human Gate",
    ):
        require(
            question,
            marker,
            "Question Contract",
            errors,
        )

    # --------------------------------------------------------
    # ROUTING / HYDRATION
    # --------------------------------------------------------

    for marker in (
        "Need determines force.",
        "Question determines mission.",
        "Evidence determines escalation.",
        "Scale != formation.",
        "Identity travels.",
        "Payload rests.",
        "Hydration occurs on mission need.",
    ):
        require(
            entry,
            marker,
            "canonical entry",
            errors,
        )

    # --------------------------------------------------------
    # CONTINUITY
    # --------------------------------------------------------

    for marker in (
        "Collapse",
        "Landing",
        "Reflight",
        "Replay",
        "Scar",
        "Scar Replay",
        "Replay != new Room.",
    ):
        require(
            entry,
            marker,
            "canonical entry",
            errors,
        )

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    pipeline = (
        "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\n"
        "Human Gate"
    )

    require(
        entry,
        pipeline,
        "canonical entry",
        errors,
    )

    for marker in (
        "PMC performs bounded epistemic computation.",
        "CCR records deterministic candidate commitment.",
        "MC governs response / output admissibility.",
        "Raven reports.",
        "Human Gate decides.",
        "Approval != execution.",
    ):
        require(
            entry,
            marker,
            "canonical entry",
            errors,
        )

    # --------------------------------------------------------
    # DOCUMENTATION OWNERSHIP
    # --------------------------------------------------------

    documentation_markers = {
        user: (
            "Responsibility: UNDERSTANDING AND OPERATION",
            "USER MANUAL COMPLETE.",
        ),
        arch: (
            "Responsibility: RATIONALE AND PRIMITIVES",
            "ARCHITECTURE GUIDE COMPLETE.",
        ),
        dev: (
            "Responsibility: IMPLEMENTATION AND EXTENSION",
            "DEVELOPER GUIDE COMPLETE.",
        ),
        audit: (
            "Responsibility: VERIFICATION / REPLACEMENT / RESILIENCE / "
            "PROVENANCE / COMPLETION CRITERIA",
            "AUDIT GUIDE COMPLETE.",
        ),
        ops: (
            "Responsibility: CONSISTENT RUNTIME OPERATION",
            "OPERATIONS GUIDE COMPLETE.",
        ),
    }

    for text, markers in documentation_markers.items():
        for marker in markers:
            if marker not in text:
                errors.append(
                    f"documentation ownership/closure missing: {marker}"
                )

    require(
        readme,
        "README owns orientation.",
        "README",
        errors,
    )

    # --------------------------------------------------------
    # RUNTIME BOUNDARY
    # --------------------------------------------------------

    for marker in (
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "External Runtime remains DISABLED.",
        "External Action remains DISABLED.",
        "System Population remains DISALLOWED.",
    ):
        require(
            entry,
            marker,
            "canonical entry",
            errors,
        )

    # --------------------------------------------------------
    # PROMOTION STATE
    # --------------------------------------------------------

    expected_promotion = {
        "native_version": "vTemporal.41.0",
        "implementation_identity": "v41 Complete",
        "source_branch": "candidate/v41-complete",
        "target_branch": "main",
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

    for key, value in expected_promotion.items():
        if promotion.get(key) != value:
            errors.append(
                f"R7-L promotion state disagreement: {key}"
            )

    if (
        completeness.get("disposition")
        != "COMPLETENESS_VALIDATED"
    ):
        errors.append(
            "R7-K completeness is not validated"
        )

    if (
        stability.get("disposition")
        != "STABLE_BASELINE"
    ):
        errors.append(
            "R7-J stability baseline is not valid"
        )

    # --------------------------------------------------------
    # FRESH-READER CONTRACT BOUNDARY
    # --------------------------------------------------------

    for marker in (
        "PRIVATE_CONVERSATIONAL_PREREQUISITE = NONE",
        "V40_INTERPRETIVE_PREREQUISITE = NONE",
        "R7-M does not itself create READY_FOR_HUMAN_GATE.",
        "R7-N owns aggregate Documentation / Promotion Readiness closure.",
        "FRESH-READER FINAL PACKAGE VALIDATION COMPLETE.",
    ):
        require(
            contract,
            marker,
            "R7-M contract",
            errors,
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R7-M FRESH-READER FINAL PACKAGE VALIDATION: FAIL"
        )

        for error in errors:
            print(f" - {error}")

        return 1

    print(
        "R7-M FRESH-READER FINAL PACKAGE VALIDATION: PASS"
    )
    print("Native version recovery: PASS")
    print("Implementation identity recovery: PASS")
    print("Entry route recovery: PASS")
    print("Historical interpretive dependency: NONE")
    print("Room / operational geography recovery: PASS")
    print("Qualification / Question Contract recovery: PASS")
    print("Evidence controls recovery: PASS")
    print("Capability routing / hydration recovery: PASS")
    print("Continuity / Replay / Scar recovery: PASS")
    print("Pipeline recovery: PASS")
    print("Documentation ownership recovery: PASS")
    print("Runtime boundary recovery: PASS")
    print("Promotion posture recovery: PASS")
    print("Private conversational prerequisite: NONE")
    print("v40 interpretive prerequisite: NONE")
    print("Repository-only recovery: PASS")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    print("Promotion State: CANDIDATE")
    print("FRESH-READER FINAL PACKAGE: PASS")
    print("R7-N Aggregate Documentation / Promotion Readiness Closure: NEXT")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
