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
    / "HYDRATION_REQUEST_RELEASE.md"
)

REQUEST_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "hydration_request.schema.json"
)

RELEASE_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "hydration_release_record.schema.json"
)

MISSION_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "capability_mission_request.schema.json"
)

OCCUPANCY_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "occupancy_witness.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

RELEASE_STATES = {
    "RELEASED",
    "PARTIAL",
    "BLOCKED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_request_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "hydration_request_id"
    }

    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(preimage)
        ).hexdigest()
    )


def compute_release_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "hydration_release_id"
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


def validate_request(record):
    errors = []

    if (
        record.get("hydration_request_id")
        != compute_request_id(record)
    ):
        errors.append(
            "hydration_request_id does not recompute from request"
        )

    for field in (
        "object_id",
        "active_question",
        "capability_mission_request_reference",
        "occupancy_witness_reference",
        "zone_reference",
        "space_reference",
        "orientation_reference",
        "territory_reference",
        "requested_verified_territory_references",
        "payload_scope",
        "mission_necessity_basis",
        "evidence_boundary",
        "evidence_ceiling",
        "stick_reference",
        "governance_reference",
        "authorization_reference",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Hydration Request requires {field}"
            )

    if record.get(
        "payload_scope"
    ) != "MISSION_REQUIRED":
        errors.append(
            "Hydration Request must use MISSION_REQUIRED payload scope"
        )

    basis = " ".join(
        record.get(
            "mission_necessity_basis",
            []
        )
    ).lower()

    forbidden_basis = (
        "load everything",
        "full payload",
        "for completeness",
    )

    if any(
        phrase in basis
        for phrase in forbidden_basis
    ):
        errors.append(
            "Hydration Request contains non-bounded full-payload necessity basis"
        )

    return errors


def validate_release(
    record,
    request=None,
):
    errors = []

    if (
        record.get("hydration_release_id")
        != compute_release_id(record)
    ):
        errors.append(
            "hydration_release_id does not recompute from release"
        )

    if record.get(
        "release_state"
    ) not in RELEASE_STATES:
        errors.append(
            "invalid Hydration Release state"
        )

    for field in (
        "hydration_request_reference",
        "object_id",
        "release_state",
        "release_basis",
        "evidence_boundary",
        "evidence_ceiling",
        "room_state_reference",
        "representation_state_reference",
        "stick_reference",
        "final_active_payload_scope",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Hydration Release requires {field}"
            )

    if record.get(
        "final_active_payload_scope"
    ) != "MISSION_REQUIRED":
        errors.append(
            "Hydration Release must retain MISSION_REQUIRED active payload scope"
        )

    if (
        record.get("release_state")
        == "BLOCKED"
        and not (
            record.get(
                "denied_or_blocked_references"
            )
            or record.get(
                "restriction_findings"
            )
        )
    ):
        errors.append(
            "BLOCKED Hydration Release requires blocked reference or restriction finding"
        )

    if request is not None:
        requested_territory = set(
            request.get(
                "requested_verified_territory_references",
                []
            )
        )

        requested_payload = set(
            request.get(
                "requested_payload_references",
                []
            )
        )

        restored_territory = set(
            record.get(
                "restored_verified_territory_references",
                []
            )
        )

        restored_payload = set(
            record.get(
                "restored_payload_references",
                []
            )
        )

        extra_territory = (
            restored_territory
            - requested_territory
        )

        extra_payload = (
            restored_payload
            - requested_payload
        )

        if extra_territory:
            errors.append(
                "Hydration Release restored territory outside request"
            )

        if extra_payload:
            errors.append(
                "Hydration Release restored payload outside request"
            )

        if (
            record.get("object_id")
            != request.get("object_id")
        ):
            errors.append(
                "Hydration Release object_id diverges from request"
            )

        if (
            record.get(
                "hydration_request_reference"
            )
            != request.get(
                "hydration_request_id"
            )
        ):
            errors.append(
                "Hydration Release does not bind supplied request identity"
            )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-I Hydration contract"
        ),
        (
            REQUEST_SCHEMA,
            "R3-I Hydration Request schema"
        ),
        (
            RELEASE_SCHEMA,
            "R3-I Hydration Release schema"
        ),
        (
            MISSION_SCHEMA,
            "R3-E Capability Mission Request schema"
        ),
        (
            OCCUPANCY_SCHEMA,
            "R3-D Occupancy Witness schema"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        request_schema = load(
            REQUEST_SCHEMA
        )
        release_schema = load(
            RELEASE_SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid schema JSON: {exc}"
        ]

    payload_scope = (
        request_schema
        .get("properties", {})
        .get("payload_scope", {})
        .get("const")
    )

    if payload_scope != "MISSION_REQUIRED":
        errors.append(
            "R3-I request does not fail closed to MISSION_REQUIRED scope"
        )

    final_scope = (
        release_schema
        .get("properties", {})
        .get("final_active_payload_scope", {})
        .get("const")
    )

    if final_scope != "MISSION_REQUIRED":
        errors.append(
            "R3-I release does not preserve MISSION_REQUIRED scope"
        )

    release_states = set(
        release_schema
        .get("properties", {})
        .get("release_state", {})
        .get("enum", [])
    )

    if release_states != RELEASE_STATES:
        errors.append(
            "R3-I Hydration Release state vocabulary is not locked"
        )

    request_properties = set(
        request_schema.get(
            "properties",
            {}
        )
    )

    release_properties = set(
        release_schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "full_payload",
        "load_everything",
        "lifecycle_mutation",
        "occupancy_mutation",
        "formation_mutation",
        "landing_witness_id",
        "replay_envelope_id",
        "restriction_transition_id",
        "canonical_mutation_authority",
    }

    if request_properties & forbidden:
        errors.append(
            "R3-I request absorbs prohibited or downstream semantics"
        )

    if release_properties & forbidden:
        errors.append(
            "R3-I release absorbs prohibited or downstream semantics"
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    normalized_contract_text = " ".join(
        contract_text.split()
    )

    locks = [
        "Hydration is not merely loading files.",
        "Hydration restores only verified operational territory required by the active mission and representation.",
        "Payload remains at rest except where mission-scoped access is justified.",
        "Identity travels.",
        "Payload rests.",
        "Hydrate what the question requires.",
        "Leave unnecessary payload at rest.",
        "Hydration does not convert unverified material into verified territory.",
        "Hydration does not qualify the Room.",
        "Hydration does not create reachability.",
        "Hydration does not manufacture evidence.",
        "Mission-required != potentially interesting.",
        "Available != necessary.",
        "Possible relevance != hydration justification.",
        "Hydration does not broaden representation scope.",
        "Hydration does not create another Room.",
        "Request != restored payload.",
        "There is no FULL_PAYLOAD hydration mode.",
        "There is no LOAD_EVERYTHING hydration mode.",
        "Full payload hydration without question-driven necessity is prohibited.",
        "Requested != verified by request.",
        "Hydration consumes verification.",
        "It does not create verification.",
        "Payload identity and Room identity remain distinct.",
        "Payload restoration does not imply canonical mutation.",
        "A generic desire for completeness is insufficient.",
        "Convenience != necessity.",
        "Hydration MUST NOT silently expose excluded evidence.",
        "Hydration does not raise the evidence ceiling.",
        "More accessible payload != stronger claim authority.",
        "More data != automatic analytical promotion.",
        "Restriction != absence.",
        "Technical accessibility != authorized hydration.",
        "Write capability != authority.",
        "Approval != hydration execution.",
        "Restored payload must be a subset of requested payload.",
        "Restored verified territory must be a subset of requested verified territory.",
        "Release cannot broaden request scope.",
        "At rest != absent.",
        "At rest != deleted.",
        "Release from active hydration != deletion.",
        "Release from active hydration != evidence destruction.",
        "Release from active hydration != Room closure.",
        "Hydration does not replace the Room.",
        "Payload loading does not become object identity.",
        "Hydration MUST NOT silently mutate lifecycle state.",
        "Hydration MUST NOT silently mutate Occupancy.",
        "Hydration MUST NOT silently mutate Formation.",
        "Hydration state != Room lifecycle state.",
        "Hydrated payload != occupant.",
        "Hydration Request != Occupancy Witness.",
        "Hydration Request != Capability Mission Request.",
        "Payload need follows mission.",
        "Mission does not follow payload availability.",
        "Formation Selection != hydration authority.",
        "Swarm != load everything.",
        "Expanded Analysis != full payload.",
        "Loaded content != mapped truth.",
        "Hydration MUST preserve the Stick.",
        "Signal != hydration authorization.",
        "Hydration Request != Goblin Signal event.",
        "Payload release != Landing.",
        "Hydration != replay.",
        "Hydration cannot bypass restriction.",
        "No Landing Witness semantics yet.",
        "No Replay semantics yet.",
        "No Restriction / Constriction transitions yet.",
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
                f"missing R3-I lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    request = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "active_question":
            "which verified evidence surface discriminates the current signal?",
        "capability_mission_request_reference":
            "mission:a",
        "formation_selection_reference":
            "formation:a",
        "occupancy_witness_reference":
            "occupancy:a",
        "zone_reference":
            "zone:a",
        "space_reference":
            "space:a",
        "orientation_reference":
            "orientation:a",
        "territory_reference":
            "territory:a",
        "requested_verified_territory_references": [
            "territory:verified:a"
        ],
        "requested_payload_references": [
            "payload:a",
            "payload:b"
        ],
        "payload_scope":
            "MISSION_REQUIRED",
        "mission_necessity_basis": [
            "payload:a and payload:b are required to answer the active question"
        ],
        "evidence_boundary": {
            "scope": "mission-bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "restriction_references": [
            "restriction:a"
        ],
        "stick_reference":
            "stick:a",
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "mission:a",
            "occupancy:a",
            "territory:verified:a",
            "stick:a"
        ],
        "requested_at":
            "2026-08-07T19:46:00-04:00",
    }

    request[
        "hydration_request_id"
    ] = compute_request_id(
        request
    )

    if not SHA512_RE.fullmatch(
        request[
            "hydration_request_id"
        ]
    ):
        errors.append(
            "hydration_request_id is not canonical SHA-512"
        )

    errors.extend(
        validate_request(
            request
        )
    )

    release = {
        "schema_version":
            "1.0",
        "hydration_request_reference":
            request[
                "hydration_request_id"
            ],
        "object_id":
            object_id,
        "release_state":
            "PARTIAL",
        "restored_verified_territory_references": [
            "territory:verified:a"
        ],
        "restored_payload_references": [
            "payload:a"
        ],
        "denied_or_blocked_references": [
            "payload:b"
        ],
        "retained_at_rest_references": [
            "payload:b",
            "payload:c"
        ],
        "released_from_active_payload_references": [
            "payload:prior-unneeded"
        ],
        "release_basis": [
            "payload:a is mission-required and authorized",
            "payload:b remains blocked by active restriction"
        ],
        "restriction_findings": [
            "payload:b remains restricted"
        ],
        "evidence_boundary": {
            "scope": "mission-bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "room_state_reference":
            "room-state:a",
        "representation_state_reference":
            "representation-state:a",
        "stick_reference":
            "stick:a",
        "final_active_payload_scope":
            "MISSION_REQUIRED",
        "provenance_route": [
            object_id,
            request[
                "hydration_request_id"
            ],
            "payload:a",
            "stick:a"
        ],
        "released_at":
            "2026-08-07T19:46:00-04:00",
    }

    release[
        "hydration_release_id"
    ] = compute_release_id(
        release
    )

    if not SHA512_RE.fullmatch(
        release[
            "hydration_release_id"
        ]
    ):
        errors.append(
            "hydration_release_id is not canonical SHA-512"
        )

    errors.extend(
        validate_release(
            release,
            request,
        )
    )

    if (
        request[
            "hydration_request_id"
        ]
        == object_id
    ):
        errors.append(
            "Hydration Request identity collapsed into Room Object identity"
        )

    if (
        release[
            "hydration_release_id"
        ]
        == object_id
    ):
        errors.append(
            "Hydration Release identity collapsed into Room Object identity"
        )

    if (
        release[
            "hydration_release_id"
        ]
        == request[
            "hydration_request_id"
        ]
    ):
        errors.append(
            "Hydration Release identity collapsed into Request identity"
        )

    overbroad = dict(
        release
    )

    overbroad[
        "restored_payload_references"
    ] = [
        "payload:a",
        "payload:not-requested"
    ]

    overbroad[
        "hydration_release_id"
    ] = compute_release_id(
        overbroad
    )

    overbroad_errors = validate_release(
        overbroad,
        request,
    )

    if not any(
        "outside request"
        in error
        for error in overbroad_errors
    ):
        errors.append(
            "R3-I incorrectly permitted payload restoration outside request"
        )

    full_payload = dict(
        request
    )

    full_payload[
        "payload_scope"
    ] = "FULL_PAYLOAD"

    full_payload[
        "mission_necessity_basis"
    ] = [
        "load everything for completeness"
    ]

    full_payload[
        "hydration_request_id"
    ] = compute_request_id(
        full_payload
    )

    full_errors = validate_request(
        full_payload
    )

    if not any(
        (
            "MISSION_REQUIRED"
            in error
            or "full-payload"
            in error
        )
        for error in full_errors
    ):
        errors.append(
            "R3-I incorrectly permitted full-payload hydration"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-I HYDRATION REQUEST / RELEASE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-I HYDRATION REQUEST / RELEASE: PASS"
    )
    print(
        "Mission-required verified territory only: LOCKED"
    )
    print(
        "Payload-at-rest / bounded restoration / unnecessary release: LOCKED"
    )
    print(
        "Full-payload hydration without question need: REJECTED"
    )
    print(
        "Request -> Release subset binding: ENFORCED"
    )
    print(
        "Identity / state / evidence ceiling / Stick: PRESERVED"
    )
    print(
        "Landing / Replay / Restriction-Constriction transitions: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
