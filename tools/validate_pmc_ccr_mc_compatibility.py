#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "PMC_CCR_MC_COMPATIBILITY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "pmc_ccr_mc_compatibility.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R5A = (
    ROOT
    / "contracts"
    / "pipeline"
    / "PIPELINE_INTEGRATION_BOUNDARY_EXISTING_SEMANTICS_LOCK.md"
)

R5B = (
    ROOT
    / "contracts"
    / "pipeline"
    / "ROOM_BOUND_EVIDENCE_PMC_INTAKE_BINDING.md"
)

R5C = (
    ROOT
    / "contracts"
    / "pipeline"
    / "PMC_CCR_CANDIDATE_COMMITMENT_LINEAGE.md"
)

R5D = (
    ROOT
    / "contracts"
    / "pipeline"
    / "CCR_MC_RESPONSE_OUTPUT_ADMISSIBILITY_BINDING.md"
)

LEGACY_INTERFACE = (
    ROOT
    / "Doctrine"
    / "PMC_MC_INTERFACE.md"
)

NAMING_LOCK = (
    ROOT
    / "Doctrine"
    / "PMC_MC_NAMING_LOCK.md"
)

NATIVE_ROUTE = [
    "EVIDENCE",
    "PMC",
    "CCR",
    "MC",
    "RAVEN",
    "HUMAN_GATE",
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


def evaluate_record(record):
    reasons = []

    if record.get(
        "pipeline_route"
    ) != NATIVE_ROUTE:
        reasons.append(
            "PIPELINE_ORDER_CHANGED"
        )

        route = record.get(
            "pipeline_route",
            []
        )

        if (
            "PMC" in route
            and "MC" in route
            and (
                "CCR" not in route
                or route.index("CCR")
                > route.index("MC")
            )
        ):
            reasons.append(
                "CCR_BYPASSED"
            )

    room_ids = {
        record.get(
            "room_object_id"
        ),
        record.get(
            "pmc_room_object_id"
        ),
        record.get(
            "ccr_room_object_id"
        ),
        record.get(
            "mc_room_object_id"
        ),
    }

    if len(room_ids) != 1:
        reasons.append(
            "ROOM_IDENTITY_CHANGED"
        )

    if (
        record.get(
            "pmc_selected_world_id"
        )
        != record.get(
            "ccr_selected_world_id"
        )
    ):
        reasons.append(
            "PMC_SELECTION_REINTERPRETED"
        )

    if (
        record.get(
            "pmc_candidate_ordering"
        )
        != record.get(
            "ccr_candidate_ordering"
        )
    ):
        reasons.append(
            "PMC_CANDIDATE_ORDER_CHANGED"
        )

    if (
        record.get(
            "pmc_rejection_references"
        )
        != record.get(
            "ccr_rejection_references"
        )
    ):
        reasons.append(
            "PMC_REJECTION_HISTORY_LOST"
        )

    pmc_uncertainty = record.get(
        "pmc_uncertainty_references",
        []
    )

    ccr_uncertainty = record.get(
        "ccr_uncertainty_references",
        []
    )

    mc_uncertainty = record.get(
        "mc_uncertainty_references",
        []
    )

    if (
        pmc_uncertainty != ccr_uncertainty
        or ccr_uncertainty != mc_uncertainty
    ):
        reasons.append(
            "UNCERTAINTY_LOST"
        )

    boundaries = {
        record.get(
            "pmc_evidence_boundary_reference"
        ),
        record.get(
            "ccr_evidence_boundary_reference"
        ),
        record.get(
            "mc_evidence_boundary_reference"
        ),
    }

    if len(boundaries) != 1:
        reasons.append(
            "EVIDENCE_BOUNDARY_CHANGED"
        )

    ceilings = {
        record.get(
            "pmc_evidence_ceiling_reference"
        ),
        record.get(
            "ccr_evidence_ceiling_reference"
        ),
        record.get(
            "mc_evidence_ceiling_reference"
        ),
    }

    if len(ceilings) != 1:
        reasons.append(
            "EVIDENCE_CEILING_CHANGED"
        )

    if not record.get(
        "ccr_reference"
    ):
        reasons.append(
            "CCR_REFERENCE_MISSING"
        )

    if (
        record.get(
            "mc_input_kind"
        )
        == "RAW_PMC"
    ):
        reasons.append(
            "MC_RAW_PMC_INPUT_USED"
        )
        reasons.append(
            "CCR_BYPASSED"
        )

    if not record.get(
        "legacy_direct_interface_present"
    ):
        reasons.append(
            "HISTORICAL_INTERFACE_ARTIFACT_MISSING"
        )

    if not record.get(
        "legacy_naming_lock_present"
    ):
        reasons.append(
            "HISTORICAL_NAMING_LOCK_MISSING"
        )

    if (
        record.get(
            "interface_collision_state"
        )
        != "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION"
    ):
        reasons.append(
            "INTERFACE_COLLISION_NORMALIZED_AWAY"
        )

    if (
        record.get(
            "mc_ephemerality_collision_state"
        )
        != "MC_EPHEMERALITY_LINEAGE_COLLISION"
    ):
        reasons.append(
            "MC_EPHEMERALITY_COLLISION_LOST"
        )

    if record.get(
        "room_semantics_absorbed"
    ):
        reasons.append(
            "ROOM_SEMANTICS_ABSORBED"
        )

    if record.get(
        "pmc_authority_promoted"
    ):
        reasons.append(
            "PMC_AUTHORITY_PROMOTED"
        )

    if record.get(
        "ccr_authority_promoted"
    ):
        reasons.append(
            "CCR_AUTHORITY_PROMOTED"
        )

    if record.get(
        "mc_authority_promoted"
    ):
        reasons.append(
            "MC_AUTHORITY_PROMOTED"
        )

    if (
        record.get(
            "authority_state"
        )
        != "NONE"
    ):
        reasons.append(
            "AUTHORITY_PROMOTED"
        )

    return sorted(
        set(
            reasons
        )
    )


def expected_disposition(record):
    return (
        "VALID"
        if not evaluate_record(
            record
        )
        else "BLOCKED"
    )


def validate_record(record):
    errors = []

    if (
        record.get(
            "validation_vector"
        )
        != "PMC_CCR_MC_COMPATIBILITY"
    ):
        errors.append(
            "wrong validation vector"
        )

    expected_reasons = evaluate_record(
        record
    )

    expected = (
        "VALID"
        if not expected_reasons
        else "BLOCKED"
    )

    if (
        record.get(
            "validation_disposition"
        )
        != expected
    ):
        errors.append(
            "pipeline compatibility disposition contradicts preserved state"
        )

    if (
        sorted(
            record.get(
                "failure_reasons",
                []
            )
        )
        != expected_reasons
    ):
        errors.append(
            "pipeline compatibility failure reasons are incomplete or incorrect"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-J Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-J provenance route required"
        )

    return errors


def make_record(
    *,
    pipeline_route=None,
    room_object_id=None,
    pmc_room_object_id=None,
    ccr_room_object_id=None,
    mc_room_object_id=None,
    pmc_selected_world_id="world:a",
    ccr_selected_world_id="world:a",
    pmc_candidate_ordering=None,
    ccr_candidate_ordering=None,
    pmc_rejection_references=None,
    ccr_rejection_references=None,
    pmc_uncertainty_references=None,
    ccr_uncertainty_references=None,
    mc_uncertainty_references=None,
    pmc_evidence_boundary_reference="boundary:a",
    ccr_evidence_boundary_reference="boundary:a",
    mc_evidence_boundary_reference="boundary:a",
    pmc_evidence_ceiling_reference="ceiling:a",
    ccr_evidence_ceiling_reference="ceiling:a",
    mc_evidence_ceiling_reference="ceiling:a",
    ccr_reference="ccr:a",
    mc_input_kind="CCR",
    legacy_direct_interface_present=True,
    legacy_naming_lock_present=True,
    interface_collision_state=(
        "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION"
    ),
    mc_ephemerality_collision_state=(
        "MC_EPHEMERALITY_LINEAGE_COLLISION"
    ),
    room_semantics_absorbed=False,
    pmc_authority_promoted=False,
    ccr_authority_promoted=False,
    mc_authority_promoted=False,
    authority_state="NONE",
):
    if pipeline_route is None:
        pipeline_route = list(
            NATIVE_ROUTE
        )

    if room_object_id is None:
        room_object_id = (
            "sha512:"
            + "1" * 128
        )

    if pmc_room_object_id is None:
        pmc_room_object_id = room_object_id

    if ccr_room_object_id is None:
        ccr_room_object_id = room_object_id

    if mc_room_object_id is None:
        mc_room_object_id = room_object_id

    if pmc_candidate_ordering is None:
        pmc_candidate_ordering = [
            "world:a",
            "world:b",
            "world:c",
        ]

    if ccr_candidate_ordering is None:
        ccr_candidate_ordering = list(
            pmc_candidate_ordering
        )

    if pmc_rejection_references is None:
        pmc_rejection_references = [
            "reject:b",
            "reject:c",
        ]

    if ccr_rejection_references is None:
        ccr_rejection_references = list(
            pmc_rejection_references
        )

    if pmc_uncertainty_references is None:
        pmc_uncertainty_references = [
            "uncertainty:a"
        ]

    if ccr_uncertainty_references is None:
        ccr_uncertainty_references = list(
            pmc_uncertainty_references
        )

    if mc_uncertainty_references is None:
        mc_uncertainty_references = list(
            pmc_uncertainty_references
        )

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "PMC_CCR_MC_COMPATIBILITY",

        "pipeline_route":
            list(
                pipeline_route
            ),

        "room_object_id":
            room_object_id,

        "pmc_room_object_id":
            pmc_room_object_id,

        "ccr_room_object_id":
            ccr_room_object_id,

        "mc_room_object_id":
            mc_room_object_id,

        "pmc_selected_world_id":
            pmc_selected_world_id,

        "ccr_selected_world_id":
            ccr_selected_world_id,

        "pmc_candidate_ordering":
            list(
                pmc_candidate_ordering
            ),

        "ccr_candidate_ordering":
            list(
                ccr_candidate_ordering
            ),

        "pmc_rejection_references":
            list(
                pmc_rejection_references
            ),

        "ccr_rejection_references":
            list(
                ccr_rejection_references
            ),

        "pmc_uncertainty_references":
            list(
                pmc_uncertainty_references
            ),

        "ccr_uncertainty_references":
            list(
                ccr_uncertainty_references
            ),

        "mc_uncertainty_references":
            list(
                mc_uncertainty_references
            ),

        "pmc_evidence_boundary_reference":
            pmc_evidence_boundary_reference,

        "ccr_evidence_boundary_reference":
            ccr_evidence_boundary_reference,

        "mc_evidence_boundary_reference":
            mc_evidence_boundary_reference,

        "pmc_evidence_ceiling_reference":
            pmc_evidence_ceiling_reference,

        "ccr_evidence_ceiling_reference":
            ccr_evidence_ceiling_reference,

        "mc_evidence_ceiling_reference":
            mc_evidence_ceiling_reference,

        "ccr_reference":
            ccr_reference,

        "mc_input_kind":
            mc_input_kind,

        "mc_class_dispositions": [
            {
                "response_class":
                    "observation",
                "disposition":
                    "ADMISSIBLE",
            },
            {
                "response_class":
                    "human_process_escalation",
                "disposition":
                    "CONDITIONAL",
            },
        ],

        "legacy_direct_interface_present":
            legacy_direct_interface_present,

        "legacy_naming_lock_present":
            legacy_naming_lock_present,

        "interface_collision_state":
            interface_collision_state,

        "mc_ephemerality_collision_state":
            mc_ephemerality_collision_state,

        "room_semantics_absorbed":
            room_semantics_absorbed,

        "pmc_authority_promoted":
            pmc_authority_promoted,

        "ccr_authority_promoted":
            ccr_authority_promoted,

        "mc_authority_promoted":
            mc_authority_promoted,

        "provenance_route": [
            "room-bound-evidence:r5-b",
            "pmc:r5-b",
            "ccr:r5-c",
            "mc:r5-d",
            "validation:r6-j",
        ],

        "authority_state":
            authority_state,

        "human_gate_state":
            "ACTIVE",

        "validation_disposition":
            "",

        "failure_reasons":
            [],
    }

    reasons = evaluate_record(
        record
    )

    record[
        "failure_reasons"
    ] = reasons

    record[
        "validation_disposition"
    ] = (
        "VALID"
        if not reasons
        else "BLOCKED"
    )

    return record


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-J contract"
        ),
        (
            SCHEMA,
            "R6-J schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R5A,
            "R5-A pipeline boundary"
        ),
        (
            R5B,
            "R5-B PMC intake"
        ),
        (
            R5C,
            "R5-C PMC -> CCR"
        ),
        (
            R5D,
            "R5-D CCR -> MC"
        ),
        (
            LEGACY_INTERFACE,
            "historical PMC -> MC interface"
        ),
        (
            NAMING_LOCK,
            "PMC / CCR / MC naming lock"
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
        "R6-J = PMC / CCR / MC Compatibility.",
        "Compatibility != semantic replacement.",
        "Integration != redefinition.",
        "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate.",
        "PMC means Probabilistic Multiverse Computation only.",
        "PMC owns bounded epistemic evaluation.",
        "Room binding does not expand PMC ownership.",
        "CCR means Canonical Commitment Record.",
        "CCR records.",
        "CCR does not reinterpret.",
        "CCR construction may not reinterpret PMC truth.",
        "Commitment record != canonical promotion.",
        "Candidate commitment != action commitment.",
        "MC means Meta Collapse (Response Admissibility Layer) only.",
        "MC does not determine epistemic truth.",
        "MC does not select the PMC world.",
        "MC does not construct CCR.",
        "MC does not rewrite CCR.",
        "MC does not authorize execution.",
        "Admissibility != authority.",
        "CCR MUST remain between PMC and MC.",
        "Direct PMC -> MC routing is not valid native-v41 pipeline execution.",
        "Room context != pipeline ownership.",
        "Binding != ownership.",
        "Binding != authority.",
        "Qualification precedes analysis.",
        "Admission != resolution.",
        "PMC truth evaluation != action authority.",
        "NULL PMC outcome != pipeline error.",
        "Null analytical selection != permission to guess.",
        "MC consumes committed analytical state.",
        "MC does not rewrite it.",
        "More information needed remains a valid outcome.",
        "Pipeline traversal != object mutation.",
        "Current availability != historical admissibility.",
        "Confidence != claim authority.",
        "Commitment != claim authority.",
        "Admissibility != claim authority.",
        "Pipeline progress != epistemic resolution.",
        "Rejected != deleted.",
        "Rejected != nonexistent.",
        "Selected != only world that ever existed.",
        "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION.",
        "Collision record != silent rewrite.",
        "Preserve artifact.",
        "Preserve provenance.",
        "Prevent bypass.",
        "Historical artifact != active native route.",
        "Do not normalize collisions away.",
        "MC_EPHEMERALITY_LINEAGE_COLLISION.",
        "Receipt != MC memory.",
        "Integration receipt != MC institutional memory.",
        "No hidden winner selection.",
        "No hidden default response class.",
        "No silent fallback.",
        "Validation does not migrate ownership.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-K owns Orthogonal Transition validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-J lock: {lock}"
            )

    source_locks = {
        R5A: [
            "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate.",
            "PMC means Probabilistic Multiverse Computation only.",
            "CCR means Canonical Commitment Record.",
            "MC means Meta Collapse (Response Admissibility Layer) only.",
            "Native-v41 integration MUST NOT use the older direct-flow wording to bypass CCR.",
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION",
            "Collision record != silent rewrite.",
            "Do not normalize them away.",
        ],
        R5B: [
            "R5-B does not redefine PMC.",
            "Room binding does not expand PMC ownership.",
            "PMC may not bypass CCR.",
            "PMC may not bypass MC.",
            "Qualification precedes analysis.",
        ],
        R5C: [
            "CCR means Canonical Commitment Record.",
            "CCR construction may not reinterpret PMC truth.",
            "Direct PMC -> MC routing is not valid native-v41 pipeline execution.",
            "CCR is mandatory between PMC and MC in Ring 5.",
            "Historical artifact != active native route.",
        ],
        R5D: [
            "MC means Meta Collapse (Response Admissibility Layer) only.",
            "Native-v41 MC integration MUST receive a CCR reference.",
            "MC consumes the committed analytical state.",
            "MC does not rewrite it.",
            "MC_EPHEMERALITY_LINEAGE_COLLISION.",
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION.",
            "Native MC invocation MUST bind through CCR.",
        ],
    }

    for path, required_locks in source_locks.items():
        surface = normalized(
            path
        )

        for lock in required_locks:
            if (
                " ".join(
                    lock.split()
                )
                not in surface
            ):
                errors.append(
                    f"source boundary missing required semantic: {lock}"
                )

    r6a = normalized(
        R6A
    )

    for lock in (
        "PMC / CCR / MC Compatibility",
        "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate",
        "PMC / CCR / MC compatibility testing MUST preserve Ring 5 ownership boundaries.",
        "Validation MUST NOT normalize the historical direct PMC -> MC collision away.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-J binding: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-J schema JSON: {exc}"
        ]

    # Positive native route.
    native = make_record()

    errors.extend(
        validate_record(
            native
        )
    )

    # Null PMC result remains null.
    null_record = make_record(
        pmc_selected_world_id=None,
        ccr_selected_world_id=None,
    )

    errors.extend(
        validate_record(
            null_record
        )
    )

    # Direct bypass.
    bypass = make_record(
        pipeline_route=[
            "EVIDENCE",
            "PMC",
            "MC",
            "RAVEN",
            "HUMAN_GATE",
        ],
        mc_input_kind="RAW_PMC",
        ccr_reference=None,
    )

    if (
        "CCR_BYPASSED"
        not in bypass[
            "failure_reasons"
        ]
        or "MC_RAW_PMC_INPUT_USED"
        not in bypass[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-J failed to reject direct PMC -> MC native bypass"
        )

    # CCR changes PMC result.
    rewritten = make_record(
        ccr_selected_world_id="world:b",
    )

    if (
        "PMC_SELECTION_REINTERPRETED"
        not in rewritten[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-J failed to reject CCR reinterpretation of PMC selection"
        )

    # Collision normalized away.
    normalized_away = make_record(
        interface_collision_state=None,
    )

    if (
        "INTERFACE_COLLISION_NORMALIZED_AWAY"
        not in normalized_away[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-J failed to preserve historical direct-interface collision"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-J PMC / CCR / MC COMPATIBILITY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-J PMC / CCR / MC COMPATIBILITY: PASS"
    )
    print(
        "Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate: PRESERVED"
    )
    print(
        "PMC reserved epistemic semantics: PRESERVED"
    )
    print(
        "CCR deterministic commitment semantics: PRESERVED"
    )
    print(
        "MC response / output admissibility semantics: PRESERVED"
    )
    print(
        "Room binding -> pipeline semantic absorption: REJECTED"
    )
    print(
        "PMC selection / candidate ordering / rejection lineage: PRESERVED"
    )
    print(
        "Uncertainty / evidence boundary / evidence ceiling: PRESERVED"
    )
    print(
        "Direct PMC -> MC native bypass: REJECTED"
    )
    print(
        "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION: PRESERVED"
    )
    print(
        "Historical direct-interface artifact: PRESERVED"
    )
    print(
        "MC_EPHEMERALITY_LINEAGE_COLLISION: PRESERVED"
    )
    print(
        "PMC / CCR / MC authority promotion: REJECTED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-K Orthogonal Transition: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
