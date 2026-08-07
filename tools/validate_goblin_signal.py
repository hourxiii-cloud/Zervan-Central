#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "qualification"
    / "GOBLIN_SIGNAL_ROOM_EVENT_PROPAGATION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "goblin_signal_event.schema.json"
)

QUALIFICATION_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "qualification_record.schema.json"
)

OCCUPANCY_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "occupancy_witness.schema.json"
)

RETURN_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "capability_return.schema.json"
)

FORMATION_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "formation_selection_record.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

EVENT_CLASSES = {
    "ROOM_EVENT",
    "DISTURBANCE",
    "QUALIFICATION_CHANGE",
    "OCCUPANCY_CHANGE",
    "BRANCH_OR_ADJOINING_OBJECT_SIGNAL",
    "CAPABILITY_RETURN_NOTIFICATION",
}

SCOPES = {
    "LOCAL",
    "ROOM",
    "FORMATION",
    "FAMILY",
    "CONTROL_PLANE",
}

DELIVERY_STATES = {
    "EMITTED",
    "DELIVERED",
    "PARTIAL",
    "BLOCKED",
}

QUALIFICATION_SUBTYPES = {
    "QUALIFIED",
    "REJECTED",
    "INSTABILITY",
    "BRANCH_AVAILABLE",
    "FURTHER_RECONNAISSANCE_NEEDED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_event_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "goblin_signal_event_id"
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


def validate_event(record):
    errors = []

    expected = compute_event_id(
        record
    )

    if (
        record.get("goblin_signal_event_id")
        != expected
    ):
        errors.append(
            "goblin_signal_event_id does not recompute from event"
        )

    if record.get(
        "event_class"
    ) not in EVENT_CLASSES:
        errors.append(
            "invalid Goblin Signal event class"
        )

    if record.get(
        "propagation_scope"
    ) not in SCOPES:
        errors.append(
            "invalid Goblin Signal propagation scope"
        )

    if record.get(
        "delivery_state"
    ) not in DELIVERY_STATES:
        errors.append(
            "invalid Goblin Signal delivery state"
        )

    for field in (
        "object_id",
        "event_class",
        "event_subtype",
        "source_record_type",
        "source_record_reference",
        "source_component",
        "event_subject",
        "stick_reference",
        "evidence_boundary",
        "evidence_ceiling",
        "propagation_scope",
        "intended_recipients",
        "sequence_coordinate",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Goblin Signal Event requires {field}"
            )

    if (
        record.get("event_class")
        == "QUALIFICATION_CHANGE"
        and record.get("event_subtype")
        not in QUALIFICATION_SUBTYPES
    ):
        errors.append(
            "invalid qualification-change subtype"
        )

    if (
        record.get("event_class")
        == "OCCUPANCY_CHANGE"
        and record.get("source_record_type")
        != "OCCUPANCY_WITNESS"
    ):
        errors.append(
            "OCCUPANCY_CHANGE must bind an Occupancy Witness"
        )

    if (
        record.get("event_class")
        == "CAPABILITY_RETURN_NOTIFICATION"
        and record.get("source_record_type")
        != "CAPABILITY_RETURN"
    ):
        errors.append(
            "CAPABILITY_RETURN_NOTIFICATION must bind a Capability Return"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-H Goblin Signal contract"
        ),
        (
            SCHEMA,
            "R3-H Goblin Signal schema"
        ),
        (
            QUALIFICATION_SCHEMA,
            "R3-B Qualification Record schema"
        ),
        (
            OCCUPANCY_SCHEMA,
            "R3-D Occupancy Witness schema"
        ),
        (
            RETURN_SCHEMA,
            "R3-E Capability Return schema"
        ),
        (
            FORMATION_SCHEMA,
            "R3-G Formation Selection schema"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid schema JSON: {exc}"
        ]

    classes = set(
        schema
        .get("properties", {})
        .get("event_class", {})
        .get("enum", [])
    )

    scopes = set(
        schema
        .get("properties", {})
        .get("propagation_scope", {})
        .get("enum", [])
    )

    delivery_states = set(
        schema
        .get("properties", {})
        .get("delivery_state", {})
        .get("enum", [])
    )

    if classes != EVENT_CLASSES:
        errors.append(
            "R3-H event-class vocabulary is not source-locked"
        )

    if scopes != SCOPES:
        errors.append(
            "R3-H propagation-scope vocabulary is not locked"
        )

    if delivery_states != DELIVERY_STATES:
        errors.append(
            "R3-H delivery-state vocabulary is not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "lifecycle_mutation",
        "qualification_disposition",
        "occupancy_event_mutation",
        "formation_type_selection",
        "branch_creation",
        "distinct_object_determination",
        "hydration_request_id",
        "payload_release",
        "publication_authorization",
        "execution_authorization",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R3-H improperly absorbs source-owner/downstream semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    normalized_contract_text = " ".join(
        contract_text.split()
    )

    locks = [
        "Goblin Signal communicates.",
        "Communication != ownership.",
        "Goblin Signal announces what occurred.",
        "Goblin Signal does not decide that it occurred.",
        "Propagation != source-state mutation.",
        "Signal != truth.",
        "Signal cannot outrun Registry state.",
        "Announcement != qualification decision.",
        "Room event != Room Object.",
        "Disturbance != finding.",
        "Disturbance != automatic escalation.",
        "Qualification Change Event != Qualification Record.",
        "Qualification Change Event != Registry transition.",
        "Goblin Signal does not create presence.",
        "Goblin Signal does not terminate presence.",
        "Occupancy Witness establishes presence state.",
        "Branch signal != branch creation.",
        "Adjoining-object signal != new Room.",
        "Notification != Capability Return.",
        "Notification does not rewrite bounded findings.",
        "Goblin Signal MUST NOT synthesize a source record when one is required.",
        "No fake source.",
        "Goblin Signal remains communicator.",
        "Source ownership != communication ownership.",
        "Propagation does not broaden access.",
        "Propagation does not raise claim ceiling.",
        "Scope != authority.",
        "Broadcast capability != permission to broadcast.",
        "Partial delivery MUST NOT be represented as full propagation.",
        "Blocked communication does not erase the source event.",
        "Source event persists independently of delivery success.",
        "Event ordering matters.",
        "Communicator != authority.",
        "Signal may trigger consideration.",
        "Signal does not perform the governed action.",
        "Repeated notification != independent evidence.",
        "Event count != confidence.",
        "Consensus-by-broadcast is prohibited.",
        "Transport failure != analytical erasure.",
        "Return first.",
        "Notify second.",
        "Presence first.",
        "Selection first.",
        "Signal != hydration request.",
        "Signal != payload release.",
        "Signal != lifecycle transition.",
        "Event propagation != publication.",
        "Event propagation != decision authority.",
        "No Hydration semantics yet.",
        "No ACTIVE lifecycle transition execution yet.",
    ]

    for lock in locks:
        normalized_lock = " ".join(
            lock.split()
        )

        if (
            normalized_lock
            not in normalized_contract_text
        ):
            errors.append(
                f"missing R3-H lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    qualification_event = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "event_class":
            "QUALIFICATION_CHANGE",
        "event_subtype":
            "QUALIFIED",
        "source_record_type":
            "LIFECYCLE_TRANSITION",
        "source_record_reference":
            "lifecycle:qualified:a",
        "source_component":
            "Registry",
        "event_subject":
            "Room qualification finalized as QUALIFIED",
        "prior_state_reference":
            "lifecycle:qualifying:a",
        "resulting_state_reference":
            "lifecycle:qualified:a",
        "zone_references": [
            "zone:a"
        ],
        "space_references": [
            "space:a"
        ],
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "evidence_boundary": {
            "scope": "qualification"
        },
        "evidence_ceiling":
            "CEILING:A",
        "propagation_scope":
            "ROOM",
        "intended_recipients": [
            "TOC",
            "Governance",
            "Audit"
        ],
        "delivery_state":
            "EMITTED",
        "sequence_coordinate":
            1001,
        "provenance_route": [
            object_id,
            "lifecycle:qualified:a",
            "stick:a"
        ],
        "emitted_at":
            "2026-08-07T19:42:00-04:00",
    }

    qualification_event[
        "goblin_signal_event_id"
    ] = compute_event_id(
        qualification_event
    )

    if not SHA512_RE.fullmatch(
        qualification_event[
            "goblin_signal_event_id"
        ]
    ):
        errors.append(
            "goblin_signal_event_id is not canonical SHA-512"
        )

    errors.extend(
        validate_event(
            qualification_event
        )
    )

    occupancy_event = dict(
        qualification_event
    )

    occupancy_event[
        "event_class"
    ] = "OCCUPANCY_CHANGE"

    occupancy_event[
        "event_subtype"
    ] = "ENTERED"

    occupancy_event[
        "source_record_type"
    ] = "OCCUPANCY_WITNESS"

    occupancy_event[
        "source_record_reference"
    ] = "occupancy:a"

    occupancy_event[
        "source_component"
    ] = "Registry"

    occupancy_event[
        "event_subject"
    ] = "Capability entered bounded Room representation"

    occupancy_event[
        "prior_state_reference"
    ] = None

    occupancy_event[
        "resulting_state_reference"
    ] = "occupancy:a"

    occupancy_event[
        "sequence_coordinate"
    ] = 1002

    occupancy_event[
        "goblin_signal_event_id"
    ] = compute_event_id(
        occupancy_event
    )

    errors.extend(
        validate_event(
            occupancy_event
        )
    )

    return_event = dict(
        qualification_event
    )

    return_event[
        "event_class"
    ] = "CAPABILITY_RETURN_NOTIFICATION"

    return_event[
        "event_subtype"
    ] = "CAPABILITY_RETURNED"

    return_event[
        "source_record_type"
    ] = "CAPABILITY_RETURN"

    return_event[
        "source_record_reference"
    ] = "capability:return:a"

    return_event[
        "source_component"
    ] = "Goblin:a"

    return_event[
        "event_subject"
    ] = "Bounded capability return available"

    return_event[
        "prior_state_reference"
    ] = None

    return_event[
        "resulting_state_reference"
    ] = None

    return_event[
        "sequence_coordinate"
    ] = 1003

    return_event[
        "goblin_signal_event_id"
    ] = compute_event_id(
        return_event
    )

    errors.extend(
        validate_event(
            return_event
        )
    )

    bad_occupancy = dict(
        occupancy_event
    )

    bad_occupancy[
        "source_record_type"
    ] = "GOBLIN_SIGNAL_EVENT"

    bad_occupancy[
        "goblin_signal_event_id"
    ] = compute_event_id(
        bad_occupancy
    )

    bad_errors = validate_event(
        bad_occupancy
    )

    if not any(
        "must bind an Occupancy Witness"
        in error
        for error in bad_errors
    ):
        errors.append(
            "R3-H incorrectly permitted occupancy announcement "
            "without Occupancy Witness source"
        )

    changed = dict(
        qualification_event
    )

    changed[
        "event_subtype"
    ] = "INSTABILITY"

    changed[
        "event_subject"
    ] = "Qualification instability detected"

    changed[
        "goblin_signal_event_id"
    ] = compute_event_id(
        changed
    )

    if (
        changed[
            "goblin_signal_event_id"
        ]
        == qualification_event[
            "goblin_signal_event_id"
        ]
    ):
        errors.append(
            "material event change did not change Goblin Signal identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-H GOBLIN SIGNAL / ROOM EVENT PROPAGATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-H GOBLIN SIGNAL / ROOM EVENT PROPAGATION: PASS"
    )
    print(
        "Room / disturbance / qualification / occupancy / branch / return events: LOCKED"
    )
    print(
        "Source record before propagation: ENFORCED"
    )
    print(
        "Communication != ownership / mutation: LOCKED"
    )
    print(
        "Scope / recipients / delivery / sequence / provenance: PRESERVED"
    )
    print(
        "Hydration / ACTIVE execution / publication: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
