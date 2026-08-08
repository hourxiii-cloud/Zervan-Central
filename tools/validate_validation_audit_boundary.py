#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "validation_audit_registry.schema.json"
)

R5J = (
    ROOT
    / "contracts"
    / "pipeline"
    / "RING5_EXISTING_PIPELINE_INTEGRATION_AGGREGATE_CLOSURE.md"
)

FAMILIES = [
    "UNIT",
    "SCHEMA",
    "LIFECYCLE",
    "PERSPECTIVE_ROTATION",
    "ONE_OBJECT_CONVERGENCE",
    "DISTINCT_OBJECT",
    "PERTURBATION",
    "ORTHOGONAL_TRANSITION",
    "REPLAY",
    "REPLACEMENT",
    "REPRESENTATION_INDEPENDENCE",
    "LOSSLESS_COLLAPSE",
]

VECTORS = [
    "ONE_OBJECT_PERSPECTIVE_ROTATION",
    "PREMATURE_ANALYSIS_REJECTION",
    "PROPORTIONAL_FORCE_ROUTING",
    "QUALIFICATION_TEAM_COHERENCE",
    "FORMATION_REJUSTIFICATION",
    "DISTINCT_OBJECT_TEST",
    "HYDRATION_ON_NEED",
    "REPLAY_FIDELITY",
    "PMC_CCR_MC_COMPATIBILITY",
    "ORTHOGONAL_TRANSITION",
    "RBT_001",
    "FRESH_READER_TEST",
]

REQUIRED_CONTRACT_SURFACES = [
    "QUESTION_CONTRACT",
    "PROMOTION_RECEIPT",
    "LOSSLESS_COLLAPSE_RECEIPT",
]

FAILURE_CLASSES = [
    "INNER_INVARIANT_CONTRADICTION",
    "OUTER_IMPLEMENTATION_DEFECT",
    "VALIDATOR_DEFECT",
    "COVERAGE_GAP",
    "SOURCE_COLLISION",
    "UNRESOLVED_REQUIRED_SURFACE",
]


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


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


def make_valid_record():
    return {
        "schema_version":
            "1.0",

        "native_version":
            "vTemporal.41.0",

        "implementation_identity":
            "v41 Complete",

        "ring":
            "R6-A",

        "source_tranche":
            "TRANCHE_8_VALIDATION_AND_AUDIT",

        "ring5_dependency":
            "R5-J",

        "required_validation_families":
            list(FAMILIES),

        "named_validation_vectors":
            list(VECTORS),

        "required_contract_audit_surfaces":
            list(REQUIRED_CONTRACT_SURFACES),

        "failure_classes":
            list(FAILURE_CLASSES),

        "registry_disposition":
            "REGISTERED",

        "promotion_state":
            "CANDIDATE",

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",

        "lineage_reference":
            "ring6:r6-a:vTemporal.41.0",

        "provenance_route": [
            "R5-J",
            "TRANCHE_8",
            "R6-A",
        ],
    }


def validate_record(record):
    errors = []

    if record.get(
        "native_version"
    ) != "vTemporal.41.0":
        errors.append(
            "native version must remain vTemporal.41.0"
        )

    if record.get(
        "implementation_identity"
    ) != "v41 Complete":
        errors.append(
            "implementation identity must remain v41 Complete"
        )

    if record.get(
        "ring"
    ) != "R6-A":
        errors.append(
            "registry ring must remain R6-A"
        )

    if record.get(
        "source_tranche"
    ) != "TRANCHE_8_VALIDATION_AND_AUDIT":
        errors.append(
            "R6-A must remain bound to Tranche 8 Validation and Audit"
        )

    if record.get(
        "ring5_dependency"
    ) != "R5-J":
        errors.append(
            "R6-A must depend on closed Ring 5 R5-J"
        )

    if record.get(
        "required_validation_families"
    ) != FAMILIES:
        errors.append(
            "required validation-family inventory is incomplete or reordered"
        )

    if record.get(
        "named_validation_vectors"
    ) != VECTORS:
        errors.append(
            "named validation-vector inventory is incomplete or reordered"
        )

    if record.get(
        "required_contract_audit_surfaces"
    ) != REQUIRED_CONTRACT_SURFACES:
        errors.append(
            "required contract audit-surface inventory is incomplete"
        )

    if record.get(
        "failure_classes"
    ) != FAILURE_CLASSES:
        errors.append(
            "Ring 6 failure classification inventory is incomplete"
        )

    if record.get(
        "registry_disposition"
    ) not in {
        "REGISTERED",
        "BLOCKED",
    }:
        errors.append(
            "invalid R6-A registry disposition"
        )

    if record.get(
        "promotion_state"
    ) != "CANDIDATE":
        errors.append(
            "R6-A promotion state must remain CANDIDATE"
        )

    if record.get(
        "authority_state"
    ) != "NONE":
        errors.append(
            "R6-A authority state must remain NONE"
        )

    if record.get(
        "human_gate_state"
    ) != "ACTIVE":
        errors.append(
            "R6-A Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "lineage_reference"
    ):
        errors.append(
            "R6-A requires lineage reference"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-A requires provenance route"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-A contract"
        ),
        (
            SCHEMA,
            "R6-A schema"
        ),
        (
            R5J,
            "R5-J closure contract"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    text = normalized(
        CONTRACT
    )

    locks = [
        "Ring 6 = Validation and Audit.",
        "R6-A establishes the validation boundary and vector registry.",
        "R6-A does not claim that every registered validation vector has already been implemented.",
        "R6-A does not create a new analytical primitive.",
        "R6-A does not redefine Rings 1 through 5.",
        "Audit != mutation.",
        "Validation != authority.",
        "Test success != truth.",
        "Development ring transition != system-state transition.",
        "One dependency traversal is sufficient.",
        "Reduced redundant execution != reduced validation coverage.",
        "Validation does not repair implementation state silently.",
        "Validator failure != permission to rewrite doctrine.",
        "Test convenience != implementation mutation.",
        "No family absorbs another family.",
        "Turn the object.",
        "Do not clone the world.",
        "Qualification precedes analysis.",
        "Need determines force.",
        "Question determines mission.",
        "Evidence determines escalation.",
        "Formation change != object change.",
        "Replay != reconstruction.",
        "Replay != new Room.",
        "Orthogonal transition != perspective rotation.",
        "Return != reconstruction.",
        "Humor does not reduce test rigor.",
        "Representation independence != semantic looseness.",
        "Replacement != redefinition.",
        "Local change should produce local consequence.",
        "Schema != truth.",
        "Validator observes state-transition law.",
        "Validator does not own state.",
        "Green output != complete audit trail.",
        "R6-A does not silently claim required contracts already exist.",
        "R6-A does not assign their implementation ownership by inference.",
        "Missing required surface != nonexistent requirement.",
        "REGISTERED != implemented.",
        "IMPLEMENTED != validated.",
        "VALIDATED != canonical promotion.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Validation completion != Human Gate approval.",
        "R6-B owns the first implemented extended validation vector after the boundary registry is established.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-A lock: {lock}"
            )

    r5j = normalized(
        R5J
    )

    r5_locks = [
        "Ring 5 — Existing Pipeline Integration: COMPLETE.",
        "Closure state: VALIDATED_CANDIDATE.",
        "Promotion state: CANDIDATE.",
        "Authority: NONE.",
        "Human Gate: ACTIVE.",
        "It is not canonical promotion.",
    ]

    for lock in r5_locks:
        if (
            " ".join(
                lock.split()
            )
            not in r5j
        ):
            errors.append(
                f"Ring 5 handoff missing required state: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-A schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "test_execution_authority",
        "canonical_promotion",
        "doctrine_rewrite",
        "room_lifecycle_transition",
        "evidence_boundary_override",
        "evidence_ceiling_override",
        "human_gate_bypass",
        "automatic_repair",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R6-A improperly absorbs implementation/authority semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    errors.extend(
        validate_record(
            make_valid_record()
        )
    )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-A VALIDATION / AUDIT BOUNDARY "
            "AND VECTOR REGISTRY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-A VALIDATION / AUDIT BOUNDARY "
        "AND VECTOR REGISTRY: PASS"
    )
    print(
        "Ring 5 -> Ring 6 development handoff: BOUND"
    )
    print(
        "Required validation families: REGISTERED"
    )
    print(
        "Named native validation vectors: REGISTERED"
    )
    print(
        "Question / Promotion / Lossless-Collapse contract surfaces: AUDIT-REGISTERED"
    )
    print(
        "Implementation / validator / invariant failure classes: SEPARATED"
    )
    print(
        "Validation mutation / authority / promotion: NOT ABSORBED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-B first extended validation vector: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
