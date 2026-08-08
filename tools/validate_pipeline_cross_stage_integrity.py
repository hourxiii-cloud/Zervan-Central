#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "PIPELINE_CROSS_STAGE_INTEGRITY_NO_RESPONSIBILITY_ABSORPTION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "pipeline_cross_stage_integrity.schema.json"
)

CONTRACTS = {
    "R5-A": (
        ROOT
        / "contracts"
        / "pipeline"
        / "PIPELINE_INTEGRATION_BOUNDARY_EXISTING_SEMANTICS_LOCK.md"
    ),
    "R5-B": (
        ROOT
        / "contracts"
        / "pipeline"
        / "ROOM_BOUND_EVIDENCE_PMC_INTAKE_BINDING.md"
    ),
    "R5-C": (
        ROOT
        / "contracts"
        / "pipeline"
        / "PMC_CCR_CANDIDATE_COMMITMENT_LINEAGE.md"
    ),
    "R5-D": (
        ROOT
        / "contracts"
        / "pipeline"
        / "CCR_MC_RESPONSE_OUTPUT_ADMISSIBILITY_BINDING.md"
    ),
    "R5-E": (
        ROOT
        / "contracts"
        / "pipeline"
        / "MC_RAVEN_REPRESENTATION_REPORT_BINDING.md"
    ),
    "R5-F": (
        ROOT
        / "contracts"
        / "pipeline"
        / "RAVEN_HUMAN_GATE_PUBLICATION_ACTION_BOUNDARY.md"
    ),
    "R5-G": (
        ROOT
        / "contracts"
        / "pipeline"
        / "DECISION_OPTION_LINEAGE.md"
    ),
    "R5-H": (
        ROOT
        / "contracts"
        / "pipeline"
        / "REPORT_RENDERING_CONTRACT.md"
    ),
}

PIPELINE_ROUTE = [
    "ROOM_BOUND_EVIDENCE",
    "PMC_INTAKE",
    "PMC",
    "CCR",
    "MC",
    "RAVEN",
    "HUMAN_GATE",
]

REQUIRED_OWNERSHIP_CHECKS = {
    "ROOM_IDENTITY_NOT_ABSORBED",
    "REGISTRY_NOT_ABSORBED",
    "GOVERNANCE_NOT_ABSORBED",
    "AUDIT_NOT_ABSORBED",
    "CARTOGRAPHY_NOT_ABSORBED",
    "PMC_NOT_ABSORBED",
    "CCR_NOT_ABSORBED",
    "MC_NOT_ABSORBED",
    "RAVEN_NOT_ABSORBED",
    "HUMAN_GATE_NOT_ABSORBED",
}

REQUIRED_AUTHORITY_CHECKS = {
    "PMC_NO_ACTION_AUTHORITY",
    "CCR_NO_ACTION_AUTHORITY",
    "MC_NO_ACTION_AUTHORITY",
    "RAVEN_NO_ACTION_AUTHORITY",
    "DECISION_OPTION_NO_ACTION_AUTHORITY",
    "REPORT_NO_ACTION_AUTHORITY",
    "HUMAN_GATE_APPROVAL_NOT_EXECUTION",
    "ZERVAN_AUTHORITY_NONE",
    "HUMAN_GATE_ACTIVE",
}

REQUIRED_COLLISIONS = {
    "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION",
    "MC_EPHEMERALITY_LINEAGE_COLLISION",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_cross_stage_integrity_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "cross_stage_integrity_id"
    }

    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(preimage)
        ).hexdigest()
    )


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


def validate_record(record):
    errors = []

    if (
        record.get("cross_stage_integrity_id")
        != compute_cross_stage_integrity_id(record)
    ):
        errors.append(
            "cross_stage_integrity_id does not recompute from record"
        )

    for field in (
        "pipeline_route",
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "coordinate_reference",
        "pmc_intake_binding_id",
        "pmc_run_id",
        "ccr_id",
        "mc_evaluation_id",
        "raven_representation_id",
        "collision_states",
        "ownership_checks",
        "authority_checks",
        "lineage_reference",
        "provenance_route",
        "integrity_disposition",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Cross-stage integrity requires {field}"
            )

    if (
        record.get("pipeline_route")
        != PIPELINE_ROUTE
    ):
        errors.append(
            "native Ring 5 pipeline route is invalid or reordered"
        )

    ownership = set(
        record.get(
            "ownership_checks",
            []
        )
    )

    missing_ownership = (
        REQUIRED_OWNERSHIP_CHECKS
        - ownership
    )

    if missing_ownership:
        errors.append(
            "missing ownership checks: "
            + ", ".join(
                sorted(
                    missing_ownership
                )
            )
        )

    authority = set(
        record.get(
            "authority_checks",
            []
        )
    )

    missing_authority = (
        REQUIRED_AUTHORITY_CHECKS
        - authority
    )

    if missing_authority:
        errors.append(
            "missing authority checks: "
            + ", ".join(
                sorted(
                    missing_authority
                )
            )
        )

    collisions = set(
        record.get(
            "collision_states",
            []
        )
    )

    missing_collisions = (
        REQUIRED_COLLISIONS
        - collisions
    )

    if missing_collisions:
        errors.append(
            "known Ring 5 collision state was silently removed: "
            + ", ".join(
                sorted(
                    missing_collisions
                )
            )
        )

    disposition = record.get(
        "integrity_disposition"
    )

    if disposition not in {
        "VALID",
        "BLOCKED",
    }:
        errors.append(
            "invalid cross-stage integrity disposition"
        )

    if (
        disposition == "BLOCKED"
        and not record.get(
            "blocking_reasons"
        )
    ):
        errors.append(
            "BLOCKED integrity disposition requires blocking reasons"
        )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "cross-stage authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "cross-stage Human Gate state must remain ACTIVE"
        )

    return errors


def validate_contract_surface():
    errors = []

    for ring, path in CONTRACTS.items():
        if not path.exists():
            errors.append(
                f"missing {ring} contract"
            )

    if errors:
        return errors

    surfaces = {
        ring: normalized(path)
        for ring, path in CONTRACTS.items()
    }

    expected = {
        "R5-A": [
            "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate.",
            "Binding != ownership.",
            "Binding != authority.",
            "No pipeline component may silently absorb:",
            "Convenience != ownership.",
        ],
        "R5-B": [
            "PMC may not bypass CCR.",
            "PMC may not bypass MC.",
            "PMC does not become the owner of that context.",
            "Coordinate reference != Cartography ownership.",
        ],
        "R5-C": [
            "CCR may not reinterpret PMC output.",
            "CCR does not select the world.",
            "PMC selects or denies.",
            "CCR records.",
            "CCR is mandatory between PMC and MC in Ring 5.",
        ],
        "R5-D": [
            "Native-v41 MC integration MUST receive a CCR reference.",
            "MC does not rewrite it.",
            "Receipt != MC memory.",
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION.",
            "MC_EPHEMERALITY_LINEAGE_COLLISION.",
        ],
        "R5-E": [
            "Raven MUST NOT bypass MC.",
            "Raven may not manufacture MC disposition.",
            "Raven cannot authorize publication.",
            "The Unkindness is not a separate pipeline stage.",
        ],
        "R5-F": [
            "Human Gate decision != execution.",
            "No default approval exists.",
            "Approval != execution.",
            "Prior approval != standing approval.",
        ],
        "R5-G": [
            "Decision option != decision.",
            "Decision option != approval.",
            "Decision option != execution.",
            "Option lineage MUST NOT begin at Raven alone.",
        ],
        "R5-H": [
            "Report != truth authority.",
            "Report != publication authority.",
            "Report != certification.",
            "Supported meaning may not.",
            "R5-I owns Pipeline Cross-Stage Integrity / No-Responsibility-Absorption.",
        ],
    }

    for ring, locks in expected.items():
        surface = surfaces[
            ring
        ]

        for lock in locks:
            normalized_lock = " ".join(
                lock.split()
            )

            if normalized_lock not in surface:
                errors.append(
                    f"{ring} missing expected cross-stage lock: {lock}"
                )

    return errors


def validate_schema_surface():
    errors = []

    schema_paths = [
        ROOT
        / "schemas"
        / "pipeline"
        / "room_bound_evidence_pmc_intake.schema.json",

        ROOT
        / "schemas"
        / "pipeline"
        / "canonical_commitment_record.schema.json",

        ROOT
        / "schemas"
        / "pipeline"
        / "mc_response_output_admissibility.schema.json",

        ROOT
        / "schemas"
        / "pipeline"
        / "raven_representation_binding.schema.json",

        ROOT
        / "schemas"
        / "pipeline"
        / "human_gate_transition_decision.schema.json",

        ROOT
        / "schemas"
        / "pipeline"
        / "decision_option_lineage.schema.json",

        ROOT
        / "schemas"
        / "pipeline"
        / "report_rendering_record.schema.json",
    ]

    forbidden_by_stage = {
        "room_bound_evidence_pmc_intake.schema.json": {
            "selected_world_id",
            "ccr_record",
            "mc_admissibility",
            "publication_authorization",
            "execution_authorization",
        },
        "canonical_commitment_record.schema.json": {
            "mc_admissibility",
            "raven_report",
            "publication_authorization",
            "execution_authorization",
        },
        "mc_response_output_admissibility.schema.json": {
            "raw_telemetry",
            "new_evidence",
            "publication_authorization",
            "execution_authorization",
            "mc_internal_working_state",
        },
        "raven_representation_binding.schema.json": {
            "new_evidence",
            "mc_disposition_override",
            "publication_authorization",
            "execution_authorization",
            "decision_authority",
        },
        "human_gate_transition_decision.schema.json": {
            "execution_result",
            "external_side_effect",
            "canonical_truth",
            "system_authority",
        },
        "decision_option_lineage.schema.json": {
            "execution_authorization",
            "publication_authorization",
            "decision_authority",
            "preferred_option",
            "automatic_selection",
        },
        "report_rendering_record.schema.json": {
            "new_evidence",
            "decision_authority",
            "execution_authorization",
            "publication_execution",
            "canonical_promotion",
        },
    }

    for path in schema_paths:
        if not path.exists():
            errors.append(
                f"missing schema {path.name}"
            )
            continue

        try:
            schema = load(
                path
            )
        except Exception as exc:
            errors.append(
                f"invalid schema {path.name}: {exc}"
            )
            continue

        properties = set(
            schema.get(
                "properties",
                {}
            )
        )

        leaked = (
            properties
            & forbidden_by_stage[
                path.name
            ]
        )

        if leaked:
            errors.append(
                f"{path.name} absorbs forbidden responsibility: "
                + ", ".join(
                    sorted(
                        leaked
                    )
                )
            )

    return errors


def make_valid_record():
    record = {
        "schema_version":
            "1.0",

        "pipeline_route":
            list(
                PIPELINE_ROUTE
            ),

        "object_id":
            "sha512:"
            + "1" * 128,

        "room_revision_id":
            "revision:a",

        "room_state_root":
            "sha512:"
            + "2" * 128,

        "authorized_view_root":
            "sha512:"
            + "3" * 128,

        "evidence_boundary_reference":
            "boundary:a",

        "evidence_ceiling_reference":
            "ceiling:a",

        "coordinate_reference":
            "coordinate:a",

        "pmc_intake_binding_id":
            "sha512:"
            + "4" * 128,

        "pmc_run_id":
            "pmc-run:a",

        "ccr_id":
            "sha512:"
            + "5" * 128,

        "mc_evaluation_id":
            "sha512:"
            + "6" * 128,

        "raven_representation_id":
            "sha512:"
            + "7" * 128,

        "human_gate_decision_reference":
            None,

        "decision_option_references": [
            "decision-option:a"
        ],

        "report_references": [
            "report:a"
        ],

        "collision_states": sorted(
            REQUIRED_COLLISIONS
        ),

        "ownership_checks": sorted(
            REQUIRED_OWNERSHIP_CHECKS
        ),

        "authority_checks": sorted(
            REQUIRED_AUTHORITY_CHECKS
        ),

        "lineage_reference":
            "lineage:a",

        "provenance_route": [
            "room:a",
            "pmc-intake:a",
            "pmc:a",
            "ccr:a",
            "mc:a",
            "raven:a",
            "human-gate:a",
        ],

        "integrity_disposition":
            "VALID",

        "blocking_reasons": [],

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",
    }

    record[
        "cross_stage_integrity_id"
    ] = compute_cross_stage_integrity_id(
        record
    )

    return record


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-I contract"
        ),
        (
            SCHEMA,
            "R5-I schema"
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
        "R5-I does not create another analytical stage.",
        "R5-I does not redefine any stage.",
        "Cross-stage validation != stage ownership.",
        "Integration integrity != analytical authority.",
        "No native route may omit CCR.",
        "No native route may bypass MC before Raven.",
        "No native route may bypass Human Gate for governed authority-bearing movement.",
        "R5-I validates the chain.",
        "R5-I does not absorb the chain.",
        "No stage may silently absorb another stage's responsibility.",
        "Convenience != ownership.",
        "Binding != ownership.",
        "Pipeline binding != Room ownership.",
        "Room context consumption != Room mutation.",
        "Stage transition != Room identity transition.",
        "Renderer change != Room identity change.",
        "Human Gate decision != Room identity change.",
        "PMC confidence does not raise the claim ceiling.",
        "CCR commitment does not raise the claim ceiling.",
        "MC admissibility does not raise the claim ceiling.",
        "Raven prose does not raise the claim ceiling.",
        "Decision Option usefulness does not raise the claim ceiling.",
        "Human Gate approval does not raise the claim ceiling.",
        "Report polish does not raise the claim ceiling.",
        "Restricted != nonexistent.",
        "Unavailable to a stage != nonexistent in the Room.",
        "Coordinate reference != Cartography ownership.",
        "Coordinate propagation != spatial mutation.",
        "Presentation change != truth change.",
        "PMC selects or denies.",
        "CCR records.",
        "Direct raw PMC -> MC routing is not a valid native-v41 execution route.",
        "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION remains explicit.",
        "Receipt != MC memory.",
        "MC_EPHEMERALITY_LINEAGE_COLLISION remains explicit.",
        "Raven reporting != MC ownership.",
        "Approval != execution.",
        "Prior approval != standing approval.",
        "Raven output != Human Gate decision.",
        "Decision option != decision.",
        "Decision option != approval.",
        "Decision option != execution.",
        "Report != truth.",
        "Report != publication.",
        "Report != certification.",
        "Report != execution.",
        "Zervan Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Human authorization != system authority.",
        "Collision suppression is invalid.",
        "Historical artifact != active native route.",
        "Surface collisions.",
        "Do not normalize them away.",
        "No Compression Out applies end-to-end.",
        "Receipt identity != truth.",
        "Receipt != promotion.",
        "Receipt != authority.",
        "VALID != analytical truth.",
        "VALID != Human Gate approval.",
        "VALID != publication.",
        "VALID != promotion.",
        "Missing ownership check is not assumed PASS.",
        "Missing authority check is not assumed PASS.",
        "Pipeline shortcut != optimization.",
        "Transport != ownership.",
        "Fail closed.",
        "Do not repair a stage by absorbing another stage's function.",
        "R5-J owns Ring 5 Aggregate Closure.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R5-I lock: {lock}"
            )

    errors.extend(
        validate_contract_surface()
    )

    errors.extend(
        validate_schema_surface()
    )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-I schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "pmc_selected_world_override",
        "ccr_generation",
        "mc_disposition_override",
        "raven_rendering_override",
        "human_gate_approval_override",
        "execution_authorization",
        "publication_execution",
        "canonical_promotion",
        "room_lifecycle_transition",
        "cartography_mutation",
        "evidence_boundary_override",
        "evidence_ceiling_override",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-I improperly absorbs stage responsibility: "
            + ", ".join(
                sorted(
                    leaked
                )
            )
        )

    record = make_valid_record()

    errors.extend(
        validate_record(
            record
        )
    )

    # --------------------------------------------------------
    # Route skip: CCR
    # --------------------------------------------------------

    skipped_ccr = json.loads(
        json.dumps(
            record
        )
    )

    skipped_ccr[
        "pipeline_route"
    ] = [
        "ROOM_BOUND_EVIDENCE",
        "PMC_INTAKE",
        "PMC",
        "MC",
        "RAVEN",
        "HUMAN_GATE",
    ]

    skipped_ccr[
        "cross_stage_integrity_id"
    ] = compute_cross_stage_integrity_id(
        skipped_ccr
    )

    if not any(
        "pipeline route is invalid"
        in error
        for error in validate_record(
            skipped_ccr
        )
    ):
        errors.append(
            "R5-I incorrectly permitted CCR route bypass"
        )

    # --------------------------------------------------------
    # Missing ownership control
    # --------------------------------------------------------

    missing_owner = json.loads(
        json.dumps(
            record
        )
    )

    missing_owner[
        "ownership_checks"
    ].remove(
        "CARTOGRAPHY_NOT_ABSORBED"
    )

    missing_owner[
        "cross_stage_integrity_id"
    ] = compute_cross_stage_integrity_id(
        missing_owner
    )

    if not any(
        "missing ownership checks"
        in error
        for error in validate_record(
            missing_owner
        )
    ):
        errors.append(
            "R5-I incorrectly assumed missing ownership check PASS"
        )

    # --------------------------------------------------------
    # Missing authority control
    # --------------------------------------------------------

    missing_authority = json.loads(
        json.dumps(
            record
        )
    )

    missing_authority[
        "authority_checks"
    ].remove(
        "HUMAN_GATE_APPROVAL_NOT_EXECUTION"
    )

    missing_authority[
        "cross_stage_integrity_id"
    ] = compute_cross_stage_integrity_id(
        missing_authority
    )

    if not any(
        "missing authority checks"
        in error
        for error in validate_record(
            missing_authority
        )
    ):
        errors.append(
            "R5-I incorrectly assumed missing authority check PASS"
        )

    # --------------------------------------------------------
    # Collision suppression
    # --------------------------------------------------------

    suppressed_collision = json.loads(
        json.dumps(
            record
        )
    )

    suppressed_collision[
        "collision_states"
    ].remove(
        "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION"
    )

    suppressed_collision[
        "cross_stage_integrity_id"
    ] = compute_cross_stage_integrity_id(
        suppressed_collision
    )

    if not any(
        "collision state was silently removed"
        in error
        for error in validate_record(
            suppressed_collision
        )
    ):
        errors.append(
            "R5-I incorrectly permitted known collision suppression"
        )

    # --------------------------------------------------------
    # BLOCKED requires reason
    # --------------------------------------------------------

    blocked = json.loads(
        json.dumps(
            record
        )
    )

    blocked[
        "integrity_disposition"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = []

    blocked[
        "cross_stage_integrity_id"
    ] = compute_cross_stage_integrity_id(
        blocked
    )

    if not any(
        "BLOCKED integrity disposition requires blocking reasons"
        in error
        for error in validate_record(
            blocked
        )
    ):
        errors.append(
            "R5-I incorrectly permitted unexplained BLOCKED state"
        )

    # --------------------------------------------------------
    # Authority promotion
    # --------------------------------------------------------

    promoted = json.loads(
        json.dumps(
            record
        )
    )

    promoted[
        "authority_state"
    ] = "AUTONOMOUS"

    promoted[
        "cross_stage_integrity_id"
    ] = compute_cross_stage_integrity_id(
        promoted
    )

    if not any(
        "authority_state must remain NONE"
        in error
        for error in validate_record(
            promoted
        )
    ):
        errors.append(
            "R5-I incorrectly permitted autonomous authority promotion"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-I PIPELINE CROSS-STAGE INTEGRITY / "
            "NO-RESPONSIBILITY-ABSORPTION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-I PIPELINE CROSS-STAGE INTEGRITY / "
        "NO-RESPONSIBILITY-ABSORPTION: PASS"
    )
    print(
        "Room-Bound Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate: INTACT"
    )
    print(
        "Room identity / view / boundary / claim ceiling / coordinate: CONTINUOUS"
    )
    print(
        "PMC / CCR / MC / Raven / Human Gate ownership: SEPARATED"
    )
    print(
        "Registry / Governance / Audit / Cartography ownership: NOT ABSORBED"
    )
    print(
        "Decision Option / Report authority: NONE"
    )
    print(
        "CCR-preservation / MC-ephemerality collisions: SURFACED"
    )
    print(
        "Human Gate approval / execution: SEPARATED"
    )
    print(
        "No Compression Out / lineage / provenance: PRESERVED"
    )
    print(
        "R5-J Ring 5 Aggregate Closure: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
