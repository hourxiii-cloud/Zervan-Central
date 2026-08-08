#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

INIT = (
    ROOT
    / "candidate"
    / "RING7_INSTANTIATION_STATEMENT.md"
)

PLAY = (
    ROOT
    / "docs"
    / "deployment"
    / "RING7_DEPLOYMENT_PLAY.md"
)

CONTRACT = (
    ROOT
    / "contracts"
    / "promotion"
    / "RING7_DOCUMENTATION_PROMOTION_BOUNDARY_REGISTRY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "promotion"
    / "ring7_documentation_promotion_registry.schema.json"
)

R6P = (
    ROOT
    / "contracts"
    / "validation"
    / "RING6_AGGREGATE_AUDIT_CLOSURE.md"
)

LOSSLESS_RECEIPT = (
    ROOT
    / "schemas"
    / "validation"
    / "lossless_collapse_receipt.schema.json"
)

SECTIONS = {
    "R7-A":
        "Documentation / Promotion Boundary and Required-Surface Registry",

    "R7-B":
        "Question Contract",

    "R7-C":
        "README / Version Authority / Native-v41 Entry Surfaces",

    "R7-D":
        "User Manual",

    "R7-E":
        "Architecture Guide",

    "R7-F":
        "Developer Guide",

    "R7-G":
        "Audit Guide",

    "R7-H":
        "Operations Guide",

    "R7-I":
        "Transition Receipt",

    "R7-J":
        "Stability Receipt",

    "R7-K":
        "Completeness Receipt",

    "R7-L":
        "Promotion Receipt / Promotion-Readiness Record",

    "R7-M":
        "Fresh-Reader Final Package Validation",

    "R7-N":
        "Ring 7 Aggregate Documentation / Promotion Readiness Closure",
}

DOCUMENTATION_OWNERSHIP = {
    "README":
        "ORIENTATION",

    "USER_MANUAL":
        "UNDERSTANDING_AND_OPERATION",

    "ARCHITECTURE_GUIDE":
        "RATIONALE_AND_PRIMITIVES",

    "DEVELOPER_GUIDE":
        "IMPLEMENTATION_AND_EXTENSION",

    "AUDIT_GUIDE":
        "VERIFICATION_REPLACEMENT_RESILIENCE_PROVENANCE_COMPLETION",

    "OPERATIONS_GUIDE":
        "CONSISTENT_RUNTIME_OPERATION",
}

REQUIRED_MACHINE_SURFACES = [
    "QUESTION_CONTRACT",
    "TRANSITION_RECEIPT",
    "STABILITY_RECEIPT",
    "COMPLETENESS_RECEIPT",
    "PROMOTION_RECEIPT",
    "LOSSLESS_COLLAPSE_RECEIPT",
]

PROMOTION_BLOCKERS = [
    "QUESTION_CONTRACT_NOT_YET_VALIDATED",
    "NATIVE_V41_INITIATION_NOT_YET_VALIDATED",
    "NATIVE_V41_CANONICAL_ENTRY_NOT_YET_VALIDATED",
    "ACTIVE_VERSION_AUTHORITY_NOT_YET_RECONCILED",
    "USER_MANUAL_NOT_YET_VALIDATED",
    "ARCHITECTURE_GUIDE_NOT_YET_VALIDATED",
    "DEVELOPER_GUIDE_NOT_YET_VALIDATED",
    "AUDIT_GUIDE_NOT_YET_VALIDATED",
    "OPERATIONS_GUIDE_NOT_YET_VALIDATED",
    "TRANSITION_RECEIPT_NOT_YET_VALIDATED",
    "STABILITY_RECEIPT_NOT_YET_VALIDATED",
    "COMPLETENESS_RECEIPT_NOT_YET_VALIDATED",
    "PROMOTION_RECEIPT_NOT_YET_VALIDATED",
    "FINAL_FRESH_READER_NOT_YET_VALIDATED",
    "RING7_AGGREGATE_NOT_YET_VALIDATED",
    "HUMAN_GATE_AUTHORIZATION_NOT_GRANTED",
]


def normalized(path):
    text = path.read_text(
        encoding="utf-8"
    )

    for token in (
        "**",
        "__",
        "`",
    ):
        text = text.replace(
            token,
            ""
        )

    return " ".join(
        text.split()
    )


def make_registry():
    surface_states = {
        "QUESTION_CONTRACT":
            "DEFERRED_TO_R7_B",

        "NATIVE_V41_ENTRY":
            "DEFERRED_TO_R7_C",

        "USER_MANUAL":
            "DEFERRED_TO_R7_D",

        "ARCHITECTURE_GUIDE":
            "DEFERRED_TO_R7_E",

        "DEVELOPER_GUIDE":
            "DEFERRED_TO_R7_F",

        "AUDIT_GUIDE":
            "DEFERRED_TO_R7_G",

        "OPERATIONS_GUIDE":
            "DEFERRED_TO_R7_H",

        "TRANSITION_RECEIPT":
            "DEFERRED_TO_R7_I",

        "STABILITY_RECEIPT":
            "DEFERRED_TO_R7_J",

        "COMPLETENESS_RECEIPT":
            "DEFERRED_TO_R7_K",

        "PROMOTION_RECEIPT":
            "DEFERRED_TO_R7_L",

        "FINAL_FRESH_READER":
            "DEFERRED_TO_R7_M",

        "RING7_AGGREGATE":
            "DEFERRED_TO_R7_N",

        "LOSSLESS_COLLAPSE_RECEIPT": (
            "SATISFIED"
            if LOSSLESS_RECEIPT.exists()
            else "BLOCKED"
        ),
    }

    blockers = list(
        PROMOTION_BLOCKERS
    )

    if not LOSSLESS_RECEIPT.exists():
        blockers.append(
            "LOSSLESS_COLLAPSE_RECEIPT_MISSING"
        )

    return {
        "schema_version":
            "1.0",

        "ring":
            "R7-A",

        "domain":
            "DOCUMENTATION_AND_PROMOTION",

        "native_version":
            "vTemporal.41.0",

        "implementation_identity":
            "v41 Complete",

        "inherited_state":
            "R6-P VALIDATED_CANDIDATE",

        "sections":
            dict(
                SECTIONS
            ),

        "documentation_ownership":
            dict(
                DOCUMENTATION_OWNERSHIP
            ),

        "required_machine_surfaces":
            list(
                REQUIRED_MACHINE_SURFACES
            ),

        "surface_states":
            surface_states,

        "promotion_blockers":
            sorted(
                set(
                    blockers
                )
            ),

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",

        "promotion_state":
            "CANDIDATE",

        "target_state":
            "READY_FOR_HUMAN_GATE",

        "registry_disposition": (
            "VALIDATED"
            if LOSSLESS_RECEIPT.exists()
            else "BLOCKED"
        ),

        "provenance": [
            "candidate/RING7_INSTANTIATION_STATEMENT.md",
            "docs/deployment/RING7_DEPLOYMENT_PLAY.md",
            "contracts/validation/"
            "RING6_AGGREGATE_AUDIT_CLOSURE.md",
            "contracts/promotion/"
            "RING7_DOCUMENTATION_PROMOTION_BOUNDARY_REGISTRY.md",
        ],
    }


def validate():
    errors = []

    for path, label in (
        (
            INIT,
            "Ring 7 instantiation statement"
        ),
        (
            PLAY,
            "Ring 7 deployment play"
        ),
        (
            CONTRACT,
            "R7-A contract"
        ),
        (
            SCHEMA,
            "R7-A schema"
        ),
        (
            R6P,
            "Ring 6 closure"
        ),
        (
            LOSSLESS_RECEIPT,
            "Lossless-Collapse Receipt schema"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"invalid R7-A schema JSON: {exc}"
        ]

    if (
        schema.get(
            "$schema"
        )
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        errors.append(
            "R7-A schema must use JSON Schema Draft 2020-12"
        )

    contract = normalized(
        CONTRACT
    )

    locks = [
        "R7-A = Documentation / Promotion Boundary and Required-Surface Registry.",
        "Ring 7 = Documentation and Promotion.",
        "R6-P VALIDATED_CANDIDATE precedes R7-A.",
        "RING 6 RESULT: PASS is inherited.",
        "Ring 7 target = READY_FOR_HUMAN_GATE.",
        "README owns orientation.",
        "User Manual owns understanding and operation.",
        "Architecture Guide owns rationale and primitives.",
        "Developer Guide owns implementation and extension.",
        "Audit Guide owns verification, replacement, resilience, provenance, and completion criteria.",
        "Operations Guide owns consistent runtime operation.",
        "The README shall not carry the entire civilization.",
        "Question Contract is owned by R7-B.",
        "Native-v41 entry surfaces are owned by R7-C.",
        "Transition Receipt is owned by R7-I.",
        "Stability Receipt is owned by R7-J.",
        "Completeness Receipt is owned by R7-K.",
        "Promotion Receipt is owned by R7-L.",
        "Fresh-Reader final package validation is owned by R7-M.",
        "Aggregate promotion-readiness closure is owned by R7-N.",
        "Historical artifact != active native-v41 entry.",
        "Question != mutation.",
        "Receipt != authority.",
        "Implementation leads.",
        "Documentation follows.",
        "Deferred != forgotten.",
        "Registered != implemented.",
        "Implemented != validated.",
        "Validated != promoted.",
        "One dependency traversal is sufficient.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "R7-B owns Question Contract.",
    ]

    for lock in locks:
        if " ".join(
            lock.split()
        ) not in contract:
            errors.append(
                f"missing R7-A lock: {lock}"
            )

    init = normalized(
        INIT
    )

    for lock in (
        "RING 7 = DOCUMENTATION AND PROMOTION.",
        "READY_FOR_HUMAN_GATE",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE",
    ):
        if " ".join(
            lock.split()
        ) not in init:
            errors.append(
                f"Ring 7 instantiation missing required semantic: {lock}"
            )

    play = normalized(
        PLAY
    )

    for section in SECTIONS:
        if section not in play:
            errors.append(
                f"deployment play missing {section}"
            )

    r6p = normalized(
        R6P
    )

    for lock in (
        "R6-P = Ring 6 Aggregate Validation / Audit Closure.",
        "VALIDATED_CANDIDATE",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
    ):
        if " ".join(
            lock.split()
        ) not in r6p:
            errors.append(
                f"Ring 6 closure missing inherited semantic: {lock}"
            )

    registry = make_registry()

    if len(
        registry[
            "sections"
        ]
    ) != 14:
        errors.append(
            "R7-A must register R7-A through R7-N"
        )

    if (
        registry[
            "surface_states"
        ][
            "LOSSLESS_COLLAPSE_RECEIPT"
        ]
        != "SATISFIED"
    ):
        errors.append(
            "inherited Lossless-Collapse Receipt not satisfied"
        )

    if (
        registry[
            "authority_state"
        ]
        != "NONE"
    ):
        errors.append(
            "R7-A Authority must remain NONE"
        )

    if (
        registry[
            "human_gate_state"
        ]
        != "ACTIVE"
    ):
        errors.append(
            "R7-A Human Gate must remain ACTIVE"
        )

    if (
        registry[
            "promotion_state"
        ]
        != "CANDIDATE"
    ):
        errors.append(
            "R7-A Promotion State must remain CANDIDATE"
        )

    if (
        registry[
            "target_state"
        ]
        != "READY_FOR_HUMAN_GATE"
    ):
        errors.append(
            "R7-A target must be READY_FOR_HUMAN_GATE"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R7-A DOCUMENTATION / PROMOTION BOUNDARY AND REGISTRY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    registry = make_registry()

    print(
        "R7-A DOCUMENTATION / PROMOTION BOUNDARY AND REGISTRY: PASS"
    )
    print(
        "Inherited Ring 6 state: VALIDATED_CANDIDATE"
    )
    print(
        "Ring 7 domain: DOCUMENTATION AND PROMOTION"
    )
    print(
        "R7-A through R7-N: REGISTERED"
    )
    print(
        "Documentation ownership separation: PRESERVED"
    )
    print(
        "Required machine-readable promotion surfaces: REGISTERED"
    )
    print(
        "Lossless-Collapse Receipt: SATISFIED"
    )
    print(
        "Question Contract: DEFERRED_TO_R7_B"
    )
    print(
        "Native-v41 entry surfaces: DEFERRED_TO_R7_C"
    )
    print(
        "Five required guides: REGISTERED"
    )
    print(
        "Transition / Stability / Completeness / Promotion receipts: REGISTERED"
    )
    print(
        "Fresh-Reader final package validation: DEFERRED_TO_R7_M"
    )
    print(
        "Promotion blockers: EXPLICIT"
    )
    print(
        "Target state: READY_FOR_HUMAN_GATE"
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
        "R7-B Question Contract: NEXT"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
