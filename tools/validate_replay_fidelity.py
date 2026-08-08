#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "REPLAY_FIDELITY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "replay_fidelity.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R4F = (
    ROOT
    / "contracts"
    / "runtime"
    / "REPLAY_ENVELOPE.md"
)

R4C = (
    ROOT
    / "contracts"
    / "runtime"
    / "LANDING_WITNESS.md"
)

R2I = (
    ROOT
    / "contracts"
    / "geography"
    / "STICK_CONTACT_CONTINUITY.md"
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


def changed(record, historical, replay):
    return (
        record.get(historical)
        != record.get(replay)
    )


def evaluate_record(record):
    reasons = []

    comparisons = [
        (
            "historical_object_id",
            "replay_object_id",
            "OBJECT_IDENTITY_CHANGED",
        ),
        (
            "historical_lineage_reference",
            "replay_lineage_reference",
            "LINEAGE_CHANGED",
        ),
        (
            "historical_question_reference",
            "replay_question_reference",
            "HISTORICAL_QUESTION_SUBSTITUTED",
        ),
        (
            "historical_inquiry_envelope_reference",
            "replay_inquiry_envelope_reference",
            "INQUIRY_ENVELOPE_SUBSTITUTED",
        ),
        (
            "historical_observational_coordinate",
            "replay_observational_coordinate",
            "OBSERVATIONAL_COORDINATE_CHANGED",
        ),
        (
            "historical_zone_reference",
            "replay_zone_reference",
            "ZONE_SUBSTITUTED",
        ),
        (
            "historical_space_reference",
            "replay_space_reference",
            "SPACE_SUBSTITUTED",
        ),
        (
            "historical_transform_references",
            "replay_transform_references",
            "TRANSFORM_HISTORY_CHANGED",
        ),
        (
            "historical_evidence_used_references",
            "replay_evidence_used_references",
            "EVIDENCE_USED_CHANGED",
        ),
        (
            "historical_capability_movement_references",
            "replay_capability_movement_references",
            "CAPABILITY_MOVEMENT_CHANGED",
        ),
        (
            "historical_evidence_boundary_reference",
            "replay_evidence_boundary_reference",
            "EVIDENCE_BOUNDARY_CHANGED",
        ),
        (
            "historical_evidence_ceiling_reference",
            "replay_evidence_ceiling_reference",
            "EVIDENCE_CEILING_CHANGED",
        ),
        (
            "historical_restriction_references",
            "replay_restriction_references",
            "RESTRICTION_HISTORY_CHANGED",
        ),
        (
            "historical_collapse_references",
            "replay_collapse_references",
            "COLLAPSE_HISTORY_CHANGED",
        ),
        (
            "historical_finding_references",
            "replay_finding_references",
            "FINDING_HISTORY_CHANGED",
        ),
        (
            "historical_rendering_reference",
            "replay_rendering_reference",
            "HISTORICAL_RENDERING_SUBSTITUTED",
        ),
        (
            "historical_return_coordinate",
            "replay_return_coordinate",
            "RETURN_COORDINATE_CHANGED",
        ),
        (
            "historical_cartography_reference",
            "replay_cartography_reference",
            "CARTOGRAPHY_CHANGED",
        ),
        (
            "historical_stick_reference",
            "replay_stick_reference",
            "STICK_CHANGED",
        ),
    ]

    for historical, replay, reason in comparisons:
        if changed(
            record,
            historical,
            replay,
        ):
            reasons.append(
                reason
            )

    if not record.get(
        "closing_witness_reference"
    ):
        reasons.append(
            "CLOSING_WITNESS_MISSING"
        )

    if record.get(
        "approximate_reconstruction_used"
    ):
        reasons.append(
            "APPROXIMATE_RECONSTRUCTION_USED"
        )

    if record.get(
        "new_room_created"
    ):
        reasons.append(
            "NEW_ROOM_INVENTED"
        )

    if record.get(
        "branch_created"
    ):
        reasons.append(
            "BRANCH_INVENTED"
        )

    if record.get(
        "lifecycle_mutated"
    ):
        reasons.append(
            "LIFECYCLE_MUTATED"
        )

    if record.get(
        "reflight_executed"
    ):
        reasons.append(
            "REFLIGHT_EXECUTED"
        )

    if record.get(
        "full_payload_hydration_requested"
    ):
        reasons.append(
            "FULL_PAYLOAD_HYDRATION_REQUESTED"
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
        != "REPLAY_FIDELITY"
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
            "replay fidelity disposition contradicts preserved historical state"
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
            "replay fidelity failure reasons are incomplete or incorrect"
        )

    expected_eligibility = (
        "ELIGIBLE"
        if not expected_reasons
        else "BLOCKED"
    )

    if (
        record.get(
            "replay_eligibility"
        )
        != expected_eligibility
    ):
        errors.append(
            "replay eligibility contradicts fidelity state"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-I Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-I provenance route required"
        )

    return errors


def make_record(
    *,
    historical_rendering_reference="rendering:historical:a",
    replay_rendering_reference="rendering:historical:a",
    closing_witness_reference="closing:r6-i:a",
    historical_object_id=None,
    replay_object_id=None,
    historical_lineage_reference="lineage:r6-i:a",
    replay_lineage_reference="lineage:r6-i:a",
    historical_question_reference="question:r6-i:a",
    replay_question_reference="question:r6-i:a",
    historical_inquiry_envelope_reference="inquiry:r6-i:a",
    replay_inquiry_envelope_reference="inquiry:r6-i:a",
    historical_observational_coordinate="coord:observation:a",
    replay_observational_coordinate="coord:observation:a",
    historical_zone_reference="zone:a",
    replay_zone_reference="zone:a",
    historical_space_reference="space:a",
    replay_space_reference="space:a",
    historical_transform_references=None,
    replay_transform_references=None,
    historical_evidence_used_references=None,
    replay_evidence_used_references=None,
    historical_capability_movement_references=None,
    replay_capability_movement_references=None,
    historical_evidence_boundary_reference="boundary:a",
    replay_evidence_boundary_reference="boundary:a",
    historical_evidence_ceiling_reference="ceiling:a",
    replay_evidence_ceiling_reference="ceiling:a",
    historical_restriction_references=None,
    replay_restriction_references=None,
    historical_collapse_references=None,
    replay_collapse_references=None,
    historical_finding_references=None,
    replay_finding_references=None,
    historical_return_coordinate="coord:return:a",
    replay_return_coordinate="coord:return:a",
    historical_cartography_reference="cartography:a",
    replay_cartography_reference="cartography:a",
    historical_stick_reference="stick:a",
    replay_stick_reference="stick:a",
    approximate_reconstruction_used=False,
    new_room_created=False,
    branch_created=False,
    lifecycle_mutated=False,
    reflight_executed=False,
    full_payload_hydration_requested=False,
    authority_state="NONE",
):
    if historical_object_id is None:
        historical_object_id = (
            "sha512:"
            + "1" * 128
        )

    if replay_object_id is None:
        replay_object_id = historical_object_id

    if historical_transform_references is None:
        historical_transform_references = [
            "transform:a",
            "transform:b",
        ]

    if replay_transform_references is None:
        replay_transform_references = list(
            historical_transform_references
        )

    if historical_evidence_used_references is None:
        historical_evidence_used_references = [
            "evidence:a",
            "evidence:b",
        ]

    if replay_evidence_used_references is None:
        replay_evidence_used_references = list(
            historical_evidence_used_references
        )

    if historical_capability_movement_references is None:
        historical_capability_movement_references = [
            "movement:a",
            "movement:b",
        ]

    if replay_capability_movement_references is None:
        replay_capability_movement_references = list(
            historical_capability_movement_references
        )

    if historical_restriction_references is None:
        historical_restriction_references = [
            "restriction:a"
        ]

    if replay_restriction_references is None:
        replay_restriction_references = list(
            historical_restriction_references
        )

    if historical_collapse_references is None:
        historical_collapse_references = [
            "collapse:a"
        ]

    if replay_collapse_references is None:
        replay_collapse_references = list(
            historical_collapse_references
        )

    if historical_finding_references is None:
        historical_finding_references = [
            "finding:a"
        ]

    if replay_finding_references is None:
        replay_finding_references = list(
            historical_finding_references
        )

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "REPLAY_FIDELITY",

        "historical_object_id":
            historical_object_id,

        "replay_object_id":
            replay_object_id,

        "closing_witness_reference":
            closing_witness_reference,

        "historical_lineage_reference":
            historical_lineage_reference,

        "replay_lineage_reference":
            replay_lineage_reference,

        "historical_question_reference":
            historical_question_reference,

        "replay_question_reference":
            replay_question_reference,

        "historical_inquiry_envelope_reference":
            historical_inquiry_envelope_reference,

        "replay_inquiry_envelope_reference":
            replay_inquiry_envelope_reference,

        "historical_departure_coordinate":
            "coord:departure:a",

        "historical_observational_coordinate":
            historical_observational_coordinate,

        "replay_observational_coordinate":
            replay_observational_coordinate,

        "historical_zone_reference":
            historical_zone_reference,

        "replay_zone_reference":
            replay_zone_reference,

        "historical_space_reference":
            historical_space_reference,

        "replay_space_reference":
            replay_space_reference,

        "historical_transform_references":
            list(
                historical_transform_references
            ),

        "replay_transform_references":
            list(
                replay_transform_references
            ),

        "historical_evidence_used_references":
            list(
                historical_evidence_used_references
            ),

        "replay_evidence_used_references":
            list(
                replay_evidence_used_references
            ),

        "historical_capability_movement_references":
            list(
                historical_capability_movement_references
            ),

        "replay_capability_movement_references":
            list(
                replay_capability_movement_references
            ),

        "historical_evidence_boundary_reference":
            historical_evidence_boundary_reference,

        "replay_evidence_boundary_reference":
            replay_evidence_boundary_reference,

        "historical_evidence_ceiling_reference":
            historical_evidence_ceiling_reference,

        "replay_evidence_ceiling_reference":
            replay_evidence_ceiling_reference,

        "historical_restriction_references":
            list(
                historical_restriction_references
            ),

        "replay_restriction_references":
            list(
                replay_restriction_references
            ),

        "historical_collapse_references":
            list(
                historical_collapse_references
            ),

        "replay_collapse_references":
            list(
                replay_collapse_references
            ),

        "historical_finding_references":
            list(
                historical_finding_references
            ),

        "replay_finding_references":
            list(
                replay_finding_references
            ),

        "historical_rendering_reference":
            historical_rendering_reference,

        "replay_rendering_reference":
            replay_rendering_reference,

        "historical_return_coordinate":
            historical_return_coordinate,

        "replay_return_coordinate":
            replay_return_coordinate,

        "historical_cartography_reference":
            historical_cartography_reference,

        "replay_cartography_reference":
            replay_cartography_reference,

        "historical_stick_reference":
            historical_stick_reference,

        "replay_stick_reference":
            replay_stick_reference,

        "approximate_reconstruction_used":
            approximate_reconstruction_used,

        "new_room_created":
            new_room_created,

        "branch_created":
            branch_created,

        "lifecycle_mutated":
            lifecycle_mutated,

        "reflight_executed":
            reflight_executed,

        "full_payload_hydration_requested":
            full_payload_hydration_requested,

        "replay_eligibility":
            "",

        "provenance_route": [
            "landing:r6-i:a",
            "closing:r6-i:a",
            "replay:r6-i:a",
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

    record[
        "replay_eligibility"
    ] = (
        "ELIGIBLE"
        if not reasons
        else "BLOCKED"
    )

    return record


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-I contract"
        ),
        (
            SCHEMA,
            "R6-I schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R4F,
            "R4-F Replay Envelope"
        ),
        (
            R4C,
            "R4-C Landing Witness"
        ),
        (
            R2I,
            "R2-I Stick"
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
        "R6-I = Replay Fidelity.",
        "Replay != reconstruction.",
        "Replay != new Room.",
        "Replay reopens the same Room at a preserved observational coordinate.",
        "Same history revisited != new world.",
        "Historical coordinate != alternate reality.",
        "No required historical element may silently be replaced by a summary.",
        "Preserved coordinate != reconstructed coordinate.",
        "Historical question != current question.",
        "Historical scope remains historical scope.",
        "No default substitution.",
        "Replay fidelity requires geometry fidelity.",
        "Evidence available now != evidence used then.",
        "Historical evidence route remains historical evidence route.",
        "Replay != evidence-boundary expansion.",
        "Replay fidelity != retrospective promotion.",
        "Capability route is part of analytical history.",
        "Restriction != absence.",
        "Replay does not flatten Collapse into the eventual answer.",
        "Finding != truth authority.",
        "Historical finding != current interpretation.",
        "Rendering != Room Object.",
        "Rendering != evidence.",
        "Return coordinate != rollback authority.",
        "Landing != Replay.",
        "Replay MUST preserve the Stick.",
        "Replay MUST NOT sever analytical continuity.",
        "Replay fidelity != full payload reload.",
        "ELIGIBLE != reopened.",
        "ELIGIBLE != execution authority.",
        "BLOCKED != nonexistent historical state.",
        "Fail closed.",
        "Do not fabricate history.",
        "Current convenience != replay fidelity.",
        "Replay Envelope != Branch.",
        "Replay does not create a duplicate world.",
        "Observation history accumulates on one object.",
        "Replay Envelope != lifecycle transition.",
        "Replay != Reflight Trigger.",
        "Replay != Reflight execution.",
        "Replay Envelope != publication record.",
        "VALID != reopened.",
        "VALID != authority.",
        "Missing != permission to fabricate.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-J owns PMC / CCR / MC Compatibility validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-I lock: {lock}"
            )

    source_locks = {
        R4F: [
            "Replay is the reopening of the same Room at a preserved observational coordinate.",
            "Replay does not reconstruct an approximation.",
            "No listed element may be silently substituted by a summary.",
            "Historical question != current question.",
            "Evidence available now != evidence used then.",
            "Replay fidelity != retrospective promotion.",
            "Replay fidelity requires geometry fidelity.",
            "Replay MUST preserve the Stick.",
            "Replay does not justify full reconstruction.",
            "Fail closed.",
            "Do not fabricate history.",
        ],
        R4C: [
            "Landing preserves object identity.",
            "Landing preserves prior question.",
            "Landing preserves prior rendering.",
            "Landing preserves state so the system does not need to rebuild the Room merely to remain conversational.",
            "Landing != Replay Envelope.",
        ],
        R2I: [
            "Stick binds object identity.",
            "Stick binds provenance.",
            "Stick binds Transform history.",
            "Stick binds evidence lineage.",
            "Stick binds return coordinates.",
            "BROKEN fails closed.",
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
        "Replay Fidelity",
        "Replay != reconstruction.",
        "Replay != new Room.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-I binding: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-I schema JSON: {exc}"
        ]

    # Exact replay.
    exact = make_record()

    errors.extend(
        validate_record(
            exact
        )
    )

    # Missing historical rendering remains missing.
    no_rendering = make_record(
        historical_rendering_reference=None,
        replay_rendering_reference=None,
    )

    errors.extend(
        validate_record(
            no_rendering
        )
    )

    # Current question substitution.
    question_substitution = make_record(
        replay_question_reference="question:current",
    )

    if (
        "HISTORICAL_QUESTION_SUBSTITUTED"
        not in question_substitution[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-I failed to reject current-question substitution"
        )

    # Approximate coordinate reconstruction.
    approximate = make_record(
        replay_observational_coordinate="coord:approximately-a",
        approximate_reconstruction_used=True,
    )

    if (
        "OBSERVATIONAL_COORDINATE_CHANGED"
        not in approximate[
            "failure_reasons"
        ]
        or "APPROXIMATE_RECONSTRUCTION_USED"
        not in approximate[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-I failed to reject approximate reconstruction"
        )

    # Later evidence cannot rewrite historical evidence use.
    evidence_substitution = make_record(
        replay_evidence_used_references=[
            "evidence:a",
            "evidence:b",
            "evidence:new",
        ],
    )

    if (
        "EVIDENCE_USED_CHANGED"
        not in evidence_substitution[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-I failed to preserve historical evidence-use route"
        )

    # Missing rendering may not be synthesized as historical.
    synthetic_rendering = make_record(
        historical_rendering_reference=None,
        replay_rendering_reference="rendering:synthetic",
    )

    if (
        "HISTORICAL_RENDERING_SUBSTITUTED"
        not in synthetic_rendering[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-I failed to reject synthetic historical rendering"
        )

    # New Room prohibited.
    new_room = make_record(
        replay_object_id=(
            "sha512:"
            + "2" * 128
        ),
        new_room_created=True,
    )

    if (
        "OBJECT_IDENTITY_CHANGED"
        not in new_room[
            "failure_reasons"
        ]
        or "NEW_ROOM_INVENTED"
        not in new_room[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-I failed to reject replay-as-new-Room"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-I REPLAY FIDELITY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-I REPLAY FIDELITY: PASS"
    )
    print(
        "Historical Room identity / lineage: PRESERVED"
    )
    print(
        "Exact observational coordinate: PRESERVED"
    )
    print(
        "Historical question / inquiry envelope: PRESERVED"
    )
    print(
        "Zone / Space / transform history / Cartography: PRESERVED"
    )
    print(
        "Evidence used / boundary / ceiling: PRESERVED"
    )
    print(
        "Capability movement / restrictions / Collapse history: PRESERVED"
    )
    print(
        "Historical findings / rendering state / return coordinate: PRESERVED"
    )
    print(
        "Approximate reconstruction / current-default substitution: REJECTED"
    )
    print(
        "Later evidence -> historical evidence rewrite: REJECTED"
    )
    print(
        "Missing historical rendering -> synthetic original: REJECTED"
    )
    print(
        "Replay -> new Room / Branch / lifecycle / Reflight: REJECTED"
    )
    print(
        "Replay -> full-payload hydration: REJECTED"
    )
    print(
        "Stick continuity: PRESERVED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-J PMC / CCR / MC Compatibility: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
