#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "ORTHOGONAL_TRANSITION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "orthogonal_transition.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R6G = (
    ROOT
    / "contracts"
    / "validation"
    / "DISTINCT_OBJECT_VALIDATION.md"
)

R2J = (
    ROOT
    / "contracts"
    / "geography"
    / "PASSAGEWAY_DISTINCT_OBJECT_CONTACT.md"
)

R2I = (
    ROOT
    / "contracts"
    / "geography"
    / "STICK_CONTACT_CONTINUITY.md"
)

R3D = (
    ROOT
    / "contracts"
    / "qualification"
    / "OCCUPANCY_WITNESS_PRESENCE.md"
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


def expected_occupancy_events(
    source_object_id,
    target_object_id,
):
    return [
        {
            "object_id":
                source_object_id,
            "event":
                "EXITED",
        },
        {
            "object_id":
                target_object_id,
            "event":
                "ENTERED",
        },
        {
            "object_id":
                target_object_id,
            "event":
                "PRESENT",
        },
        {
            "object_id":
                target_object_id,
            "event":
                "EXITED",
        },
        {
            "object_id":
                source_object_id,
            "event":
                "ENTERED",
        },
    ]


def evaluate_record(record):
    reasons = []

    source = record.get(
        "source_object_id"
    )

    target = record.get(
        "target_object_id"
    )

    returned = record.get(
        "returned_object_id"
    )

    if source == target:
        reasons.append(
            "SOURCE_TARGET_IDENTITY_COLLISION"
        )

    if returned != source:
        reasons.append(
            "RETURNED_SOURCE_IDENTITY_CHANGED"
        )

    if not record.get(
        "source_genesis_reference"
    ):
        reasons.append(
            "SOURCE_GENESIS_MISSING"
        )

    if not record.get(
        "target_genesis_reference"
    ):
        reasons.append(
            "TARGET_GENESIS_MISSING"
        )

    if not record.get(
        "source_origin_reference"
    ):
        reasons.append(
            "SOURCE_ORIGIN_MISSING"
        )

    if not record.get(
        "target_origin_reference"
    ):
        reasons.append(
            "TARGET_ORIGIN_MISSING"
        )

    if not record.get(
        "source_cartography_reference"
    ):
        reasons.append(
            "SOURCE_CARTOGRAPHY_MISSING"
        )

    if not record.get(
        "target_cartography_reference"
    ):
        reasons.append(
            "TARGET_CARTOGRAPHY_MISSING"
        )

    if not record.get(
        "source_stick_reference"
    ):
        reasons.append(
            "SOURCE_STICK_MISSING"
        )

    if not record.get(
        "target_stick_reference"
    ):
        reasons.append(
            "TARGET_STICK_MISSING"
        )

    if (
        record.get(
            "outbound_passageway_state"
        )
        != "ESTABLISHED"
    ):
        reasons.append(
            "OUTBOUND_PASSAGEWAY_NOT_ESTABLISHED"
        )

    if (
        record.get(
            "return_passageway_state"
        )
        != "ESTABLISHED"
    ):
        reasons.append(
            "RETURN_PASSAGEWAY_NOT_ESTABLISHED"
        )

    if not record.get(
        "outbound_direction_authorized"
    ):
        reasons.append(
            "OUTBOUND_DIRECTION_UNAUTHORIZED"
        )

    if not record.get(
        "return_direction_authorized"
    ):
        reasons.append(
            "RETURN_DIRECTION_UNAUTHORIZED"
        )

    actual_events = record.get(
        "occupancy_events",
        []
    )

    expected_events = expected_occupancy_events(
        source,
        target,
    )

    if actual_events != expected_events:
        reasons.append(
            "OCCUPANCY_EVENT_ORDER_INVALID"
        )

        valid_bindings = (
            len(actual_events) == 5
            and all(
                event.get(
                    "object_id"
                )
                in (
                    source,
                    target,
                )
                for event in actual_events
            )
        )

        if not valid_bindings:
            reasons.append(
                "OCCUPANCY_OBJECT_BINDING_INVALID"
            )
    else:
        for index, event in enumerate(
            actual_events
        ):
            expected_object = (
                source
                if index in (
                    0,
                    4,
                )
                else target
            )

            if (
                event.get(
                    "object_id"
                )
                != expected_object
            ):
                reasons.append(
                    "OCCUPANCY_OBJECT_BINDING_INVALID"
                )

    if (
        record.get(
            "source_return_coordinate"
        )
        != record.get(
            "returned_source_coordinate"
        )
    ):
        reasons.append(
            "SOURCE_RETURN_COORDINATE_CHANGED"
        )

    if (
        record.get(
            "source_evidence_boundary_reference"
        )
        != record.get(
            "returned_source_evidence_boundary_reference"
        )
    ):
        reasons.append(
            "SOURCE_EVIDENCE_BOUNDARY_CONTAMINATED"
        )

    if (
        record.get(
            "source_evidence_ceiling_reference"
        )
        != record.get(
            "returned_source_evidence_ceiling_reference"
        )
    ):
        reasons.append(
            "SOURCE_EVIDENCE_CEILING_CONTAMINATED"
        )

    if record.get(
        "unauthorized_cross_object_transfers"
    ):
        reasons.append(
            "UNAUTHORIZED_CROSS_OBJECT_TRANSFER"
        )

    if record.get(
        "source_contamination_detected"
    ):
        reasons.append(
            "SOURCE_CONTAMINATION_DETECTED"
        )

    if record.get(
        "target_contamination_detected"
    ):
        reasons.append(
            "TARGET_CONTAMINATION_DETECTED"
        )

    if record.get(
        "merge_created"
    ):
        reasons.append(
            "MERGE_INVENTED"
        )

    if record.get(
        "synthesized_object_created"
    ):
        reasons.append(
            "SYNTHESIZED_OBJECT_INVENTED"
        )

    if record.get(
        "reconstruction_used"
    ):
        reasons.append(
            "RECONSTRUCTION_USED"
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
        != "ORTHOGONAL_TRANSITION"
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
            "orthogonal-transition disposition contradicts transition state"
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
            "orthogonal-transition failure reasons are incomplete or incorrect"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-K Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-K provenance route required"
        )

    return errors


def make_record(
    *,
    source_object_id=None,
    target_object_id=None,
    returned_object_id=None,
    source_genesis_reference="genesis:a",
    target_genesis_reference="genesis:b",
    source_origin_reference="origin:a",
    target_origin_reference="origin:b",
    source_cartography_reference="cartography:a",
    target_cartography_reference="cartography:b",
    source_stick_reference="stick:a",
    target_stick_reference="stick:b",
    source_evidence_boundary_reference="boundary:a",
    target_evidence_boundary_reference="boundary:b",
    returned_source_evidence_boundary_reference="boundary:a",
    source_evidence_ceiling_reference="ceiling:a",
    target_evidence_ceiling_reference="ceiling:b",
    returned_source_evidence_ceiling_reference="ceiling:a",
    outbound_passageway_state="ESTABLISHED",
    return_passageway_state="ESTABLISHED",
    outbound_direction_authorized=True,
    return_direction_authorized=True,
    occupancy_events=None,
    source_return_coordinate="coord:a:return",
    returned_source_coordinate="coord:a:return",
    unauthorized_cross_object_transfers=None,
    source_contamination_detected=False,
    target_contamination_detected=False,
    merge_created=False,
    synthesized_object_created=False,
    reconstruction_used=False,
    authority_state="NONE",
):
    if source_object_id is None:
        source_object_id = (
            "sha512:"
            + "1" * 128
        )

    if target_object_id is None:
        target_object_id = (
            "sha512:"
            + "2" * 128
        )

    if returned_object_id is None:
        returned_object_id = (
            source_object_id
        )

    if occupancy_events is None:
        occupancy_events = (
            expected_occupancy_events(
                source_object_id,
                target_object_id,
            )
        )

    if unauthorized_cross_object_transfers is None:
        unauthorized_cross_object_transfers = []

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "ORTHOGONAL_TRANSITION",

        "source_object_id":
            source_object_id,

        "target_object_id":
            target_object_id,

        "returned_object_id":
            returned_object_id,

        "source_genesis_reference":
            source_genesis_reference,

        "target_genesis_reference":
            target_genesis_reference,

        "source_origin_reference":
            source_origin_reference,

        "target_origin_reference":
            target_origin_reference,

        "source_cartography_reference":
            source_cartography_reference,

        "target_cartography_reference":
            target_cartography_reference,

        "source_stick_reference":
            source_stick_reference,

        "target_stick_reference":
            target_stick_reference,

        "source_evidence_boundary_reference":
            source_evidence_boundary_reference,

        "target_evidence_boundary_reference":
            target_evidence_boundary_reference,

        "returned_source_evidence_boundary_reference":
            returned_source_evidence_boundary_reference,

        "source_evidence_ceiling_reference":
            source_evidence_ceiling_reference,

        "target_evidence_ceiling_reference":
            target_evidence_ceiling_reference,

        "returned_source_evidence_ceiling_reference":
            returned_source_evidence_ceiling_reference,

        "outbound_passageway_state":
            outbound_passageway_state,

        "return_passageway_state":
            return_passageway_state,

        "outbound_direction_authorized":
            outbound_direction_authorized,

        "return_direction_authorized":
            return_direction_authorized,

        "occupancy_events":
            list(
                occupancy_events
            ),

        "source_return_coordinate":
            source_return_coordinate,

        "returned_source_coordinate":
            returned_source_coordinate,

        "shared_provenance": [
            "provenance:shared:a",
        ],

        "source_non_shared_provenance": [
            "provenance:source-only:a",
        ],

        "target_non_shared_provenance": [
            "provenance:target-only:b",
        ],

        "unauthorized_cross_object_transfers":
            list(
                unauthorized_cross_object_transfers
            ),

        "source_contamination_detected":
            source_contamination_detected,

        "target_contamination_detected":
            target_contamination_detected,

        "merge_created":
            merge_created,

        "synthesized_object_created":
            synthesized_object_created,

        "reconstruction_used":
            reconstruction_used,

        "provenance_route": [
            "room:a",
            "occupancy:a:exited",
            "passageway:a-b",
            "room:b",
            "occupancy:b:entered",
            "occupancy:b:present",
            "occupancy:b:exited",
            "passageway:b-a",
            "room:a:return",
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
            "R6-K contract"
        ),
        (
            SCHEMA,
            "R6-K schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R6G,
            "R6-G Distinct Object"
        ),
        (
            R2J,
            "R2-J Passageway"
        ),
        (
            R2I,
            "R2-I Stick"
        ),
        (
            R3D,
            "R3-D Occupancy"
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
        "R6-K = Orthogonal Transition.",
        "Leave one Room.",
        "Occupy a genuinely different Room.",
        "Preserve distinct identity.",
        "Return to the first Room.",
        "Verify absence of contamination.",
        "Orthogonal transition != perspective rotation.",
        "Different Room != different view of same Room.",
        "Return != reconstruction.",
        "source_object_id != target_object_id.",
        "Different perspective does not satisfy orthogonal movement.",
        "Different Zone does not satisfy orthogonal movement.",
        "Different Space does not satisfy orthogonal movement.",
        "Branch does not satisfy orthogonal movement by itself.",
        "Passageway established != Passageway traversed.",
        "A -> B does not silently authorize B -> A.",
        "EXITED does not destroy Room A.",
        "Leave != destroy.",
        "Entry into B MUST NOT reuse Room A identity.",
        "Presence does not merge the Rooms.",
        "History accumulates.",
        "The returning Room A object_id MUST equal the pre-transition Room A object_id.",
        "Return != replacement object.",
        "Return != new Genesis.",
        "Room A preserves its Stick.",
        "Room B preserves its Stick.",
        "Stick != Passageway.",
        "Connected maps != merged reality.",
        "Contact != contamination permission.",
        "Shared provenance != contamination.",
        "Cross-object access != inherited admissibility.",
        "Cross-object movement != claim-authority transfer.",
        "Passageway provenance MUST NOT overwrite object provenance.",
        "Relationship != identity.",
        "Contact != identity collapse.",
        "Orthogonal transition is not Merge.",
        "Passageway != Merge.",
        "Traversal != synthesis.",
        "Same Room returned to != similar Room recreated.",
        "Occupancy Witness identity != Room Object identity.",
        "Passageway availability does not authorize movement.",
        "Technical ability to traverse != authorization to traverse.",
        "Approval != execution.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-L owns RBT-001 validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-K lock: {lock}"
            )

    source_locks = {
        R2J: [
            "Only DISTINCT_OBJECT may support ESTABLISHED Passageway contact.",
            "Passageway established != Passageway traversed.",
            "A -> B does not silently authorize B -> A.",
            "Contamination controls are explicit.",
            "Return route is explicit.",
            "Cartography remains independent.",
            "Stick continuity remains independent.",
            "Cross-object contact != identity collapse.",
            "Cross-object contact != Merge.",
            "Passageway != Merge.",
            "Passageway availability != movement authorization.",
        ],
        R3D: [
            "Occupation establishes presence.",
            "ENTERED records establishment of bounded presence.",
            "PRESENT records continued bounded presence at the declared coordinates.",
            "EXITED records termination of that bounded presence.",
            "Every Occupancy Witness resolves to one canonical object_id.",
            "Presence does not expand evidence access.",
            "Presence does not raise the evidence ceiling.",
            "Return coordinates preserve the route back.",
        ],
        R2I: [
            "Freedom of movement requires continuity of contact.",
            "Stick binds object identity.",
            "Stick binds Origin.",
            "Stick binds Cartography.",
            "Stick binds provenance.",
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
        "Orthogonal Transition",
        "leave one Room;",
        "occupy a genuinely different Room;",
        "preserve distinct identity;",
        "return to the first Room;",
        "verify absence of contamination.",
        "Orthogonal transition != perspective rotation.",
        "Different Room != different view of same Room.",
        "Return != reconstruction.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-K binding: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-K schema JSON: {exc}"
        ]

    # Positive A -> B -> A.
    valid = make_record()

    errors.extend(
        validate_record(
            valid
        )
    )

    # Same-object pseudo-transition.
    same_object = make_record(
        target_object_id=(
            "sha512:"
            + "1" * 128
        )
    )

    if (
        "SOURCE_TARGET_IDENTITY_COLLISION"
        not in same_object[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-K failed to reject same-object pseudo-transition"
        )

    # Return reconstruction.
    reconstructed = make_record(
        returned_object_id=(
            "sha512:"
            + "3" * 128
        ),
        reconstruction_used=True,
    )

    if (
        "RETURNED_SOURCE_IDENTITY_CHANGED"
        not in reconstructed[
            "failure_reasons"
        ]
        or "RECONSTRUCTION_USED"
        not in reconstructed[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-K failed to reject reconstructed source return"
        )

    # Unauthorized transfer.
    contaminated = make_record(
        unauthorized_cross_object_transfers=[
            "target-only-evidence -> source",
        ],
        source_contamination_detected=True,
    )

    if (
        "UNAUTHORIZED_CROSS_OBJECT_TRANSFER"
        not in contaminated[
            "failure_reasons"
        ]
        or "SOURCE_CONTAMINATION_DETECTED"
        not in contaminated[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-K failed to reject cross-object contamination"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-K ORTHOGONAL TRANSITION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-K ORTHOGONAL TRANSITION: PASS"
    )
    print(
        "Room A EXITED -> Room B ENTERED / PRESENT: VALIDATED"
    )
    print(
        "Room B EXITED -> original Room A ENTERED: VALIDATED"
    )
    print(
        "Room A / Room B distinct identity: PRESERVED"
    )
    print(
        "Independent Genesis / Origin / Cartography / Stick: PRESERVED"
    )
    print(
        "Outbound and return Passageway directionality: VALIDATED"
    )
    print(
        "Same-object perspective shift -> orthogonal transition: REJECTED"
    )
    print(
        "Return as reconstructed replacement Room: REJECTED"
    )
    print(
        "Source evidence boundary / ceiling on return: PRESERVED"
    )
    print(
        "Unauthorized cross-object transfer / contamination: REJECTED"
    )
    print(
        "Merge / synthesized-object creation: REJECTED"
    )
    print(
        "Return coordinate: PRESERVED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-L RBT-001: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
