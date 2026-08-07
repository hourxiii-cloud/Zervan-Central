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
    / "OCCUPANCY_WITNESS_PRESENCE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "occupancy_witness.schema.json"
)

LIFECYCLE_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "room_lifecycle_transition.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

OCCUPANCY_EVENTS = {
    "ENTERED",
    "PRESENT",
    "EXITED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_occupancy_witness_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "occupancy_witness_id"
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


def validate_witness(record):
    errors = []

    expected = compute_occupancy_witness_id(
        record
    )

    if (
        record.get("occupancy_witness_id")
        != expected
    ):
        errors.append(
            "occupancy_witness_id does not recompute from witness"
        )

    if record.get(
        "occupancy_event"
    ) not in OCCUPANCY_EVENTS:
        errors.append(
            "invalid occupancy witness event"
        )

    for field in (
        "object_id",
        "occupant_capability",
        "lifecycle_readiness_reference",
        "qualification_record_reference",
        "occupied_zone_id",
        "occupied_space_id",
        "orientation_reference",
        "cartography_reference",
        "stick_reference",
        "entry_authorization_reference",
        "governance_constraint_reference",
        "evidence_boundary",
        "evidence_ceiling",
        "current_coordinates",
        "return_coordinates",
        "occupancy_basis",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Occupancy Witness requires {field}"
            )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-D Occupancy Witness contract"
        ),
        (
            SCHEMA,
            "R3-D Occupancy Witness schema"
        ),
        (
            LIFECYCLE_SCHEMA,
            "R3-C lifecycle schema"
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
        lifecycle_schema = load(
            LIFECYCLE_SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid schema JSON: {exc}"
        ]

    events = set(
        schema
        .get("properties", {})
        .get("occupancy_event", {})
        .get("enum", [])
    )

    if events != OCCUPANCY_EVENTS:
        errors.append(
            "Occupancy Witness event vocabulary is not locked"
        )

    lifecycle_states = set(
        lifecycle_schema
        .get("properties", {})
        .get("target_state", {})
        .get("enum", [])
    )

    if "READY" not in lifecycle_states:
        errors.append(
            "R3-D cannot resolve READY lifecycle substrate"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "capability_mission_id",
        "mission_request_id",
        "movement_state",
        "movement_vector",
        "formation_selection_id",
        "selected_formation",
        "goblin_signal_event_id",
        "active_lifecycle_transition_id",
        "landing_witness_id",
        "hydration_request_id",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R3-D improperly absorbs downstream semantics: "
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
        "Information is occupied before it is interpreted.",
        "Capabilities occupy the same Room Object through permitted Zones and Spaces.",
        "They do not create private copies of informational reality.",
        "Occupation establishes presence.",
        "Representation establishes position.",
        "Mission establishes movement.",
        "Evidence establishes escalation.",
        "Capability != truth owner.",
        "Capability != Room identity.",
        "Occupancy Witness identity is not Room Object identity.",
        "Occupancy Witness identity is not capability identity.",
        "READY != occupied.",
        "Occupancy Witness establishes presence.",
        "QUALIFIED != occupied.",
        "Qualification Record != Occupancy Witness.",
        "Occupant perspective != new Room.",
        "Observer != object.",
        "Zone != occupant.",
        "Space != occupant.",
        "Cartography != occupation.",
        "Mapped position != presence unless witnessed.",
        "Presence MUST NOT sever continuity.",
        "Technical ability to enter != authorization to enter.",
        "Entry authorization != truth authority.",
        "Approval != presence.",
        "Presence does not expand evidence access.",
        "Presence does not raise the evidence ceiling.",
        "Occupation != evidence promotion.",
        "Presence != interpretation.",
        "Presence != finding.",
        "Presence != conclusion.",
        "Occupancy Witness != Capability Mission Request.",
        "Presence != mission.",
        "Occupancy Witness != Formation Selection Record.",
        "Multiple occupants != formation by default.",
        "Occupancy Witness != lifecycle mutation.",
        "Presence != ACTIVE transition.",
        "Occupancy Witness != Goblin Signal event.",
        "Witness != propagation.",
        "EXITED is not Landing.",
        "Landing != exit.",
        "Write capability != authority.",
        "Occupant != authority.",
        "No capability mission yet.",
        "No movement execution yet.",
        "No formation selection yet.",
        "No Goblin Signal propagation yet.",
        "No ACTIVE lifecycle transition yet.",
        "No Landing semantics yet.",
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
                f"missing R3-D lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    probe = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "occupant_capability":
            "Goblin:qualification-lead",
        "occupancy_event":
            "ENTERED",
        "lifecycle_readiness_reference":
            "lifecycle:ready:a",
        "qualification_record_reference":
            "qualification:record:a",
        "occupied_zone_id":
            "sha512:" + "2" * 128,
        "occupied_space_id":
            "sha512:" + "3" * 128,
        "orientation_reference":
            "orientation:a",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "entry_authorization_reference":
            "authorization:entry:a",
        "governance_constraint_reference":
            "governance:entry:a",
        "human_gate_reference":
            "human-gate:a",
        "evidence_boundary": {
            "included": [
                "evidence:a"
            ]
        },
        "evidence_ceiling":
            "CEILING:A",
        "current_coordinates": {
            "zone": "a",
            "space": "a",
        },
        "return_coordinates": {
            "position": "ready-origin"
        },
        "occupancy_basis": [
            "Room lifecycle READY",
            "entry authorization resolved",
            "bounded Zone and Space resolved",
        ],
        "provenance_route": [
            object_id,
            "qualification:record:a",
            "lifecycle:ready:a",
            "authorization:entry:a",
        ],
        "witnessed_at":
            "2026-08-07T19:25:00-04:00",
    }

    probe[
        "occupancy_witness_id"
    ] = compute_occupancy_witness_id(
        probe
    )

    if not SHA512_RE.fullmatch(
        probe[
            "occupancy_witness_id"
        ]
    ):
        errors.append(
            "occupancy_witness_id is not canonical SHA-512"
        )

    errors.extend(
        validate_witness(
            probe
        )
    )

    if (
        probe["occupancy_witness_id"]
        == object_id
    ):
        errors.append(
            "Occupancy Witness identity collapsed into object identity"
        )

    changed = dict(
        probe
    )

    changed[
        "occupancy_event"
    ] = "PRESENT"

    changed[
        "occupancy_witness_id"
    ] = compute_occupancy_witness_id(
        changed
    )

    if (
        changed["occupancy_witness_id"]
        == probe["occupancy_witness_id"]
    ):
        errors.append(
            "material occupancy event change did not change witness identity"
        )

    missing_authorization = dict(
        probe
    )

    missing_authorization[
        "entry_authorization_reference"
    ] = None

    missing_authorization[
        "occupancy_witness_id"
    ] = compute_occupancy_witness_id(
        missing_authorization
    )

    missing_errors = validate_witness(
        missing_authorization
    )

    if not any(
        "entry_authorization_reference"
        in error
        for error in missing_errors
    ):
        errors.append(
            "Occupancy Witness incorrectly permitted unresolved entry authorization"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-D OCCUPANCY WITNESS / PRESENCE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-D OCCUPANCY WITNESS / PRESENCE: PASS"
    )
    print(
        "Occupation before interpretation: LOCKED"
    )
    print(
        "ENTERED / PRESENT / EXITED witness events: LOCKED"
    )
    print(
        "Same Room / bounded Zone / Space / coordinates: PRESERVED"
    )
    print(
        "Entry authorization / continuity / evidence ceiling: BOUND"
    )
    print(
        "Mission / movement / formation / ACTIVE transition: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
