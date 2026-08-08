#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "CCR_MC_RESPONSE_OUTPUT_ADMISSIBILITY_BINDING.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "mc_response_output_admissibility.schema.json"
)

R5C = (
    ROOT
    / "contracts"
    / "pipeline"
    / "PMC_CCR_CANDIDATE_COMMITMENT_LINEAGE.md"
)

MC = (
    ROOT
    / "Doctrine"
    / "MC.md"
)

NAMING = (
    ROOT
    / "Doctrine"
    / "PMC_MC_NAMING_LOCK.md"
)

CLASS_DISPOSITIONS = {
    "ADMISSIBLE",
    "CONDITIONAL",
    "INADMISSIBLE",
}

EVALUATION_DISPOSITIONS = {
    "EVALUATED",
    "BLOCKED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_mc_evaluation_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "mc_evaluation_id"
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
        record.get("mc_evaluation_id")
        != compute_mc_evaluation_id(record)
    ):
        errors.append(
            "mc_evaluation_id does not recompute from record"
        )

    for field in (
        "ccr_id",
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "coordinate_reference",
        "representation_reference",
        "response_class_results",
        "lineage_reference",
        "provenance_route",
        "evaluation_disposition",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"MC binding requires {field}"
            )

    if (
        record.get("evaluation_disposition")
        not in EVALUATION_DISPOSITIONS
    ):
        errors.append(
            "invalid MC evaluation disposition"
        )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "MC authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "MC human_gate_state must remain ACTIVE"
        )

    if (
        record.get("ephemerality_collision_state")
        != "MC_EPHEMERALITY_LINEAGE_COLLISION"
    ):
        errors.append(
            "MC ephemerality collision must remain explicit"
        )

    if (
        record.get("interface_collision_state")
        != "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION"
    ):
        errors.append(
            "PMC->MC interface collision must preserve CCR"
        )

    if (
        record.get("evaluation_disposition")
        == "BLOCKED"
        and not record.get("blocking_reasons")
    ):
        errors.append(
            "BLOCKED MC evaluation requires blocking reasons"
        )

    seen_classes = set()

    for result in record.get(
        "response_class_results",
        []
    ):
        response_class = result.get(
            "response_class"
        )

        disposition = result.get(
            "disposition"
        )

        if not response_class:
            errors.append(
                "MC response class must be named"
            )
            continue

        if response_class in seen_classes:
            errors.append(
                "MC response class may appear only once"
            )

        seen_classes.add(
            response_class
        )

        if disposition not in CLASS_DISPOSITIONS:
            errors.append(
                "invalid MC response-class disposition"
            )

        conditions = result.get(
            "required_conditions",
            []
        )

        reasons = result.get(
            "inadmissibility_reasons",
            []
        )

        if (
            disposition == "CONDITIONAL"
            and not conditions
        ):
            errors.append(
                "CONDITIONAL response class requires conditions"
            )

        if (
            disposition == "INADMISSIBLE"
            and not reasons
        ):
            errors.append(
                "INADMISSIBLE response class requires reasons"
            )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-D contract"
        ),
        (
            SCHEMA,
            "R5-D schema"
        ),
        (
            R5C,
            "R5-C CCR contract"
        ),
        (
            MC,
            "MC doctrine"
        ),
        (
            NAMING,
            "PMC/CCR/MC naming lock"
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
        "MC means Meta Collapse (Response Admissibility Layer) only.",
        "R5-D does not reinterpret CCR.",
        "R5-D does not authorize execution.",
        "Admissibility != authority.",
        "Direct PMC -> MC routing remains invalid for native-v41 pipeline execution.",
        "Native-v41 MC integration MUST receive a CCR reference.",
        "MC consumes the committed analytical state.",
        "MC does not rewrite it.",
        "Null analytical selection != permission to guess.",
        "Blocked upstream != nonexistent upstream.",
        "MC MUST NOT access raw telemetry through R5-D.",
        "MC MUST NOT introduce new facts.",
        "No hidden default response class.",
        "ADMISSIBLE != execute.",
        "CONDITIONAL != execute.",
        "INADMISSIBLE != analytical falsehood.",
        "A conditional result with no condition is invalid.",
        "Inadmissible != deleted.",
        "MC response gating != uncertainty resolution.",
        "Admissible response != broader evidence.",
        "Admissible response != higher claim ceiling.",
        "MC does not own Room identity.",
        "MC does not own Registry state.",
        "MC does not own Cartography.",
        "Coordinate reference != Cartography ownership.",
        "Governance gating does not create evidence.",
        "MC MUST preserve conditional and blocked states.",
        "More information needed remains a valid outcome.",
        "Capability != permission.",
        "Urgency != authority.",
        "MC computational working state is ephemeral.",
        "Receipt != MC memory.",
        "Receipt != retained MC internal computation.",
        "Receipt != analytical truth.",
        "Receipt != authority.",
        "MC_EPHEMERALITY_LINEAGE_COLLISION.",
        "Integration receipt != MC institutional memory.",
        "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION.",
        "Native MC invocation MUST bind through CCR.",
        "Historical artifact != active native route.",
        "No random class disposition.",
        "No hidden default.",
        "No silent fallback.",
        "EVALUATED != all classes admissible.",
        "BLOCKED != CCR false.",
        "MC determines admissibility only.",
        "MC does not execute.",
        "MC does not publish.",
        "MC does not promote canon.",
        "MC does not mutate Room state.",
        "Admissibility != approval.",
        "Approval != execution.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Raven may render admissibility.",
        "Raven may not manufacture admissibility.",
        "R5-D does not perform Raven rendering.",
        "Admissibility receipt != summary substitution.",
        "Fail closed.",
        "Do not repair CCR inside MC.",
        "R5-E owns MC -> Raven Representation / Report Contract Binding.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in text
        ):
            errors.append(
                f"missing R5-D lock: {lock}"
            )

    naming = normalized(
        NAMING
    )

    naming_locks = [
        "MC means Meta Collapse (Response Admissibility Layer) only.",
        "MC may not create truth, alter PMC output, or generate CCR content.",
        "MC determines only what response/output classes are admissible, conditional, or inadmissible.",
        "Human Gate alone controls whether an admissible action is taken.",
    ]

    for lock in naming_locks:
        if (
            " ".join(lock.split())
            not in naming
        ):
            errors.append(
                f"existing MC naming semantic missing: {lock}"
            )

    mc = normalized(
        MC
    )

    mc_locks = [
        "MC does not analyze raw data.",
        "MC may not influence, reinterpret, or feedback into PMC.",
        "Access raw telemetry",
        "Introduce new facts",
        "Resolve ambiguity by assumption",
        "MC defines what is allowed, not what is executed.",
        "MC retains no state.",
        "MC outputs are destroyed",
    ]

    for lock in mc_locks:
        if (
            " ".join(lock.split())
            not in mc
        ):
            errors.append(
                f"existing MC semantic missing: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-D schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "raw_telemetry",
        "selected_world_id_override",
        "pmc_candidate_ordering_override",
        "new_evidence",
        "incident_declaration",
        "actor_attribution",
        "execution_authorization",
        "publication_authorization",
        "canonical_promotion",
        "room_lifecycle_transition",
        "mc_internal_working_state",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-D improperly absorbs truth/action/Room/MC-memory semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    ccr_id = (
        "sha512:"
        + "2" * 128
    )

    state_root = (
        "sha512:"
        + "3" * 128
    )

    view_root = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "ccr_id":
            ccr_id,
        "object_id":
            object_id,
        "room_revision_id":
            "revision:a",
        "room_state_root":
            state_root,
        "authorized_view_root":
            view_root,
        "evidence_boundary_reference":
            "boundary:a",
        "evidence_ceiling_reference":
            "ceiling:a",
        "coordinate_reference":
            "coordinate:a",
        "representation_reference":
            "representation:a",
        "governance_constraint_references": [
            "governance:a"
        ],
        "propagated_uncertainty_references": [
            "uncertainty:a"
        ],
        "response_class_results": [
            {
                "response_class":
                    "observation",
                "disposition":
                    "ADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": []
            },
            {
                "response_class":
                    "technical_mitigation",
                "disposition":
                    "CONDITIONAL",
                "required_conditions": [
                    "condition:a"
                ],
                "inadmissibility_reasons": []
            },
            {
                "response_class":
                    "human_process_escalation",
                "disposition":
                    "INADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": [
                    "reason:a"
                ]
            }
        ],
        "lineage_reference":
            "lineage:a",
        "provenance_route": [
            object_id,
            ccr_id,
            "mc:a"
        ],
        "evaluation_disposition":
            "EVALUATED",
        "blocking_reasons": [],
        "ephemerality_collision_state":
            "MC_EPHEMERALITY_LINEAGE_COLLISION",
        "interface_collision_state":
            "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "mc_evaluation_id"
    ] = compute_mc_evaluation_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    conditional_without_condition = json.loads(
        json.dumps(record)
    )

    conditional_without_condition[
        "response_class_results"
    ][1][
        "required_conditions"
    ] = []

    conditional_without_condition[
        "mc_evaluation_id"
    ] = compute_mc_evaluation_id(
        conditional_without_condition
    )

    if not any(
        "CONDITIONAL response class requires conditions"
        in error
        for error in validate_record(
            conditional_without_condition
        )
    ):
        errors.append(
            "R5-D incorrectly permitted conditionless CONDITIONAL result"
        )

    inadmissible_without_reason = json.loads(
        json.dumps(record)
    )

    inadmissible_without_reason[
        "response_class_results"
    ][2][
        "inadmissibility_reasons"
    ] = []

    inadmissible_without_reason[
        "mc_evaluation_id"
    ] = compute_mc_evaluation_id(
        inadmissible_without_reason
    )

    if not any(
        "INADMISSIBLE response class requires reasons"
        in error
        for error in validate_record(
            inadmissible_without_reason
        )
    ):
        errors.append(
            "R5-D incorrectly permitted unexplained INADMISSIBLE result"
        )

    duplicate_class = json.loads(
        json.dumps(record)
    )

    duplicate_class[
        "response_class_results"
    ].append(
        {
            "response_class":
                "observation",
            "disposition":
                "ADMISSIBLE",
            "required_conditions": [],
            "inadmissibility_reasons": []
        }
    )

    duplicate_class[
        "mc_evaluation_id"
    ] = compute_mc_evaluation_id(
        duplicate_class
    )

    if not any(
        "may appear only once"
        in error
        for error in validate_record(
            duplicate_class
        )
    ):
        errors.append(
            "R5-D incorrectly permitted multiple dispositions for one class"
        )

    blocked = json.loads(
        json.dumps(record)
    )

    blocked[
        "evaluation_disposition"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = []

    blocked[
        "mc_evaluation_id"
    ] = compute_mc_evaluation_id(
        blocked
    )

    if not any(
        "BLOCKED MC evaluation requires blocking reasons"
        in error
        for error in validate_record(
            blocked
        )
    ):
        errors.append(
            "R5-D incorrectly permitted unexplained BLOCKED evaluation"
        )

    promoted = json.loads(
        json.dumps(record)
    )

    promoted[
        "authority_state"
    ] = "WRITE"

    promoted[
        "mc_evaluation_id"
    ] = compute_mc_evaluation_id(
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
            "R5-D incorrectly permitted authority promotion"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-D CCR -> MC RESPONSE / OUTPUT ADMISSIBILITY BINDING: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-D CCR -> MC RESPONSE / OUTPUT ADMISSIBILITY BINDING: PASS"
    )
    print(
        "CCR identity / Room / evidence boundary / claim ceiling: PRESERVED"
    )
    print(
        "ADMISSIBLE / CONDITIONAL / INADMISSIBLE classification: ENFORCED"
    )
    print(
        "Conditional requirements / inadmissibility reasons: ATTRIBUTABLE"
    )
    print(
        "Direct PMC->MC bypass / raw telemetry / truth rewrite: REJECTED"
    )
    print(
        "MC computational ephemerality: PRESERVED"
    )
    print(
        "MC admissibility lineage receipt: ESTABLISHED"
    )
    print(
        "Action / publication / canonical authority: NOT ABSORBED"
    )
    print(
        "R5-E MC -> Raven binding: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
