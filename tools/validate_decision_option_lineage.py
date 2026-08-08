#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "DECISION_OPTION_LINEAGE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "decision_option_lineage.schema.json"
)

R5F = (
    ROOT
    / "contracts"
    / "pipeline"
    / "RAVEN_HUMAN_GATE_PUBLICATION_ACTION_BOUNDARY.md"
)

OPTION_STATUSES = {
    "AVAILABLE",
    "CONDITIONAL",
    "UNAVAILABLE",
    "BLOCKED",
}

MC_DISPOSITIONS = {
    "ADMISSIBLE",
    "CONDITIONAL",
    "INADMISSIBLE",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_decision_option_id(record):
    preimage = {
        k: v
        for k, v in record.items()
        if k != "decision_option_id"
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
        record.get("decision_option_id")
        != compute_decision_option_id(record)
    ):
        errors.append(
            "decision_option_id does not recompute from record"
        )

    for field in (
        "option_label",
        "option_description",
        "option_status",
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "coordinate_reference",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "pmc_intake_binding_id",
        "pmc_run_id",
        "ccr_id",
        "mc_evaluation_id",
        "mc_response_class",
        "mc_disposition",
        "raven_representation_id",
        "lineage_reference",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Decision option requires {field}"
            )

    status = record.get(
        "option_status"
    )

    disposition = record.get(
        "mc_disposition"
    )

    if status not in OPTION_STATUSES:
        errors.append(
            "invalid decision option status"
        )

    if disposition not in MC_DISPOSITIONS:
        errors.append(
            "invalid MC disposition"
        )

    if (
        status == "AVAILABLE"
        and disposition != "ADMISSIBLE"
    ):
        errors.append(
            "AVAILABLE requires MC ADMISSIBLE"
        )

    if (
        status == "CONDITIONAL"
        and disposition != "CONDITIONAL"
    ):
        errors.append(
            "CONDITIONAL option requires MC CONDITIONAL"
        )

    if (
        status == "CONDITIONAL"
        and not record.get(
            "required_conditions"
        )
    ):
        errors.append(
            "CONDITIONAL option requires conditions"
        )

    if (
        status == "UNAVAILABLE"
        and disposition != "INADMISSIBLE"
    ):
        errors.append(
            "UNAVAILABLE requires MC INADMISSIBLE"
        )

    if (
        status == "UNAVAILABLE"
        and not record.get(
            "inadmissibility_reasons"
        )
    ):
        errors.append(
            "UNAVAILABLE option requires inadmissibility reasons"
        )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "Decision option authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "Decision option Human Gate state must remain ACTIVE"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-G contract"
        ),
        (
            SCHEMA,
            "R5-G schema"
        ),
        (
            R5F,
            "R5-F Human Gate contract"
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
        "Decision option != decision.",
        "Decision option != authority.",
        "Decision option != approval.",
        "Decision option != execution.",
        "Decision options are downstream analytical / reporting artifacts.",
        "They do not become a new truth-producing pipeline stage.",
        "Option lineage MUST NOT begin at Raven alone.",
        "Decision option lineage is end-to-end lineage.",
        "An option does not create a new Room.",
        "Alternative course != alternate Room.",
        "Decision option generation != access expansion.",
        "Possible action != permission to invent supporting evidence.",
        "Decision utility != higher claim ceiling.",
        "An option MUST NOT be presented as available when its MC disposition is INADMISSIBLE.",
        "Admissible option != approved option.",
        "Presentation ordering != decision ranking.",
        "Option description != directive.",
        "AVAILABLE != approved.",
        "CONDITIONAL != approved.",
        "UNAVAILABLE != nonexistent.",
        "BLOCKED != false analysis.",
        "First option != recommended option.",
        "Last option != rejected option.",
        "No hidden default winner.",
        "Recommendation != decision.",
        "Recommendation != approval.",
        "Recommendation != execution.",
        "Approval of one option MUST NOT silently approve another option.",
        "Changed option != previously approved option.",
        "Decision option does not own Cartography.",
        "Coordinate reference != Cartography ownership.",
        "Actionability != certainty.",
        "A conditional option without conditions is invalid.",
        "Condition != decoration.",
        "Unavailable != deleted.",
        "Unavailable != recommended.",
        "Null != denied.",
        "Null != approved.",
        "Decision option != decision authority.",
        "Decision option != Human Gate approval.",
        "Decision option != publication authority.",
        "Decision option != canonical promotion.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Reference != erasure.",
        "Fail closed.",
        "Do not manufacture a preferred decision.",
        "R5-H owns Report / Rendering Contract.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in text
        ):
            errors.append(
                f"missing R5-G lock: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-G schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "execution_authorization",
        "publication_authorization",
        "canonical_promotion",
        "decision_authority",
        "evidence_boundary_override",
        "evidence_ceiling_override",
        "room_lifecycle_transition",
        "preferred_option",
        "automatic_selection",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-G improperly absorbs decision/action authority: "
            + ", ".join(
                sorted(leaked)
            )
        )

    record = {
        "schema_version":
            "1.0",
        "option_label":
            "Continue observation",
        "option_description":
            "Continue bounded observation under the current evidence state.",
        "option_status":
            "AVAILABLE",
        "object_id":
            "sha512:" + "1" * 128,
        "room_revision_id":
            "revision:a",
        "room_state_root":
            "sha512:" + "2" * 128,
        "authorized_view_root":
            "sha512:" + "3" * 128,
        "coordinate_reference":
            "coordinate:a",
        "evidence_boundary_reference":
            "boundary:a",
        "evidence_ceiling_reference":
            "ceiling:a",
        "pmc_intake_binding_id":
            "sha512:" + "4" * 128,
        "pmc_run_id":
            "pmc-run:a",
        "ccr_id":
            "sha512:" + "5" * 128,
        "mc_evaluation_id":
            "sha512:" + "6" * 128,
        "mc_response_class":
            "observation",
        "mc_disposition":
            "ADMISSIBLE",
        "required_conditions": [],
        "inadmissibility_reasons": [],
        "raven_representation_id":
            "sha512:" + "7" * 128,
        "human_gate_decision_reference":
            None,
        "uncertainty_references": [
            "uncertainty:a"
        ],
        "lineage_reference":
            "lineage:a",
        "provenance_route": [
            "room:a",
            "pmc-intake:a",
            "pmc:a",
            "ccr:a",
            "mc:a",
            "raven:a",
            "option:a"
        ],
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "decision_option_id"
    ] = compute_decision_option_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    bad_available = json.loads(
        json.dumps(record)
    )

    bad_available[
        "mc_disposition"
    ] = "INADMISSIBLE"

    bad_available[
        "decision_option_id"
    ] = compute_decision_option_id(
        bad_available
    )

    if not any(
        "AVAILABLE requires MC ADMISSIBLE"
        in error
        for error in validate_record(
            bad_available
        )
    ):
        errors.append(
            "R5-G incorrectly exposed MC-inadmissible option as AVAILABLE"
        )

    conditional = json.loads(
        json.dumps(record)
    )

    conditional[
        "option_status"
    ] = "CONDITIONAL"

    conditional[
        "mc_disposition"
    ] = "CONDITIONAL"

    conditional[
        "required_conditions"
    ] = []

    conditional[
        "decision_option_id"
    ] = compute_decision_option_id(
        conditional
    )

    if not any(
        "CONDITIONAL option requires conditions"
        in error
        for error in validate_record(
            conditional
        )
    ):
        errors.append(
            "R5-G incorrectly permitted conditionless conditional option"
        )

    unavailable = json.loads(
        json.dumps(record)
    )

    unavailable[
        "option_status"
    ] = "UNAVAILABLE"

    unavailable[
        "mc_disposition"
    ] = "INADMISSIBLE"

    unavailable[
        "inadmissibility_reasons"
    ] = []

    unavailable[
        "decision_option_id"
    ] = compute_decision_option_id(
        unavailable
    )

    if not any(
        "UNAVAILABLE option requires inadmissibility reasons"
        in error
        for error in validate_record(
            unavailable
        )
    ):
        errors.append(
            "R5-G incorrectly erased unavailable-option reason"
        )

    promoted = json.loads(
        json.dumps(record)
    )

    promoted[
        "authority_state"
    ] = "WRITE"

    promoted[
        "decision_option_id"
    ] = compute_decision_option_id(
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
            "R5-G incorrectly permitted decision-option authority promotion"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-G DECISION OPTION LINEAGE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-G DECISION OPTION LINEAGE: PASS"
    )
    print(
        "Room -> PMC -> CCR -> MC -> Raven option lineage: BOUND"
    )
    print(
        "AVAILABLE / CONDITIONAL / UNAVAILABLE / BLOCKED: ENFORCED"
    )
    print(
        "MC disposition / conditions / inadmissibility reasons: PRESERVED"
    )
    print(
        "Evidence boundary / claim ceiling / uncertainty: PRESERVED"
    )
    print(
        "Option ranking / preferred winner / automatic selection: NOT CREATED"
    )
    print(
        "Decision / approval / execution authority: NOT ABSORBED"
    )
    print(
        "R5-H Report / Rendering Contract: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
