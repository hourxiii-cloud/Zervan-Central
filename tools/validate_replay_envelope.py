#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "runtime"
    / "REPLAY_ENVELOPE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "runtime"
    / "replay_envelope.schema.json"
)

R4E = (
    ROOT
    / "tools"
    / "validate_closing_witness.py"
)

ELIGIBILITY = {
    "ELIGIBLE",
    "BLOCKED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_replay_envelope_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "replay_envelope_id"
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


def validate_envelope(record):
    errors = []

    if (
        record.get("replay_envelope_id")
        != compute_replay_envelope_id(record)
    ):
        errors.append(
            "replay_envelope_id does not recompute from envelope"
        )

    if record.get(
        "replay_eligibility"
    ) not in ELIGIBILITY:
        errors.append(
            "invalid Replay eligibility"
        )

    for field in (
        "object_id",
        "closing_witness_reference",
        "preserved_lineage_reference",
        "question_contract_reference",
        "inquiry_envelope_reference",
        "departure_coordinate",
        "replay_observational_coordinate",
        "occupied_zone_reference",
        "occupied_space_reference",
        "evidence_used_references",
        "capability_movement_references",
        "evidence_boundary",
        "evidence_ceiling",
        "return_coordinate",
        "cartography_reference",
        "stick_reference",
        "replay_purpose",
        "replay_eligibility",
        "governance_reference",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Replay Envelope requires {field}"
            )

    if (
        record.get("replay_eligibility")
        == "BLOCKED"
        and not record.get(
            "blocking_reasons"
        )
    ):
        errors.append(
            "BLOCKED Replay Envelope requires blocking reasons"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R4-F Replay Envelope contract"
        ),
        (
            SCHEMA,
            "R4-F Replay Envelope schema"
        ),
        (
            R4E,
            "R4-E Closing Witness validator"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    r4e = subprocess.run(
        [
            sys.executable,
            str(R4E),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if r4e.returncode != 0:
        errors.append(
            "R4-E dependency validation failed"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-F schema JSON: {exc}"
        ]

    eligibility = set(
        schema
        .get("properties", {})
        .get("replay_eligibility", {})
        .get("enum", [])
    )

    if eligibility != ELIGIBILITY:
        errors.append(
            "R4-F Replay eligibility vocabulary is not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "new_object_id",
        "reconstructed_coordinate",
        "reflight_execution_id",
        "lifecycle_transition_id",
        "reopened_state_mutation",
        "scar_record_id",
        "scar_replay_id",
        "publication_authorization",
        "canonical_promotion",
        "full_payload_hydration",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R4-F improperly absorbs reconstruction, Scar, "
            "lifecycle, or authority semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    normalized = " ".join(
        CONTRACT.read_text(
            encoding="utf-8"
        ).split()
    )

    locks = [
        "Replay is not the creation of a duplicate world.",
        "Replay is the reopening of the same Room at a preserved observational coordinate.",
        "Replay preserves analytical journeys across object state and representation changes.",
        "Replay reopens.",
        "Replay does not reconstruct an approximation.",
        "No listed element may be silently substituted by a summary.",
        "Same history revisited != new world.",
        "Replay != new Room.",
        "Preserved coordinate != reconstructed coordinate.",
        "ELIGIBLE != reopened.",
        "ELIGIBLE != execution authority.",
        "BLOCKED != nonexistent historical state.",
        "Closing first.",
        "Replay Envelope second.",
        "Replay MUST NOT invent closure history.",
        "Historical question != current question.",
        "Historical scope remains historical scope.",
        "Departure coordinate != Origin.",
        "Departure coordinate != replay coordinate.",
        "No default substitution.",
        "Transform != new object.",
        "Evidence available now != evidence used then.",
        "Capability route is part of analytical history.",
        "Historical boundary remains attributable.",
        "Replay fidelity != retrospective promotion.",
        "Replay does not flatten Collapse into the eventual answer.",
        "Finding != truth authority.",
        "Rendering != Room Object.",
        "Rendering != evidence.",
        "Return coordinate != automatic rollback authority.",
        "Replay fidelity requires geometry fidelity.",
        "Replay MUST preserve the Stick.",
        "Replay MUST NOT sever analytical continuity.",
        "Purpose != evidence.",
        "Technical ability to reopen a coordinate != permission to expose its content.",
        "Replay Envelope != Human Gate decision.",
        "Replay Envelope creation does not itself transition SEALED -> REOPENED.",
        "Replay Envelope != lifecycle transition.",
        "Replay != Reflight Trigger.",
        "Replay != Reflight execution.",
        "Reflight does not justify full reconstruction.",
        "Replay does not justify full reconstruction.",
        "Payload rests.",
        "Fail closed.",
        "Do not fabricate history.",
        "Historical coordinate != alternate reality.",
        "Observation history accumulates on one object.",
        "Replay Envelope != Branch.",
        "R4-G owns Scar Record.",
        "R4-H owns Scar Replay.",
        "Replay Envelope != publication record.",
        "No Scar Record semantics yet.",
        "No Scar Replay semantics yet.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in normalized
        ):
            errors.append(
                f"missing R4-F lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    envelope = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "closing_witness_reference":
            "closing:a",
        "preserved_lineage_reference":
            "lineage:a",
        "question_contract_reference":
            "question-contract:a",
        "inquiry_envelope_reference":
            "inquiry-envelope:a",
        "departure_coordinate": {
            "coordinate": "departure:a"
        },
        "replay_observational_coordinate": {
            "coordinate": "observation:a"
        },
        "occupied_zone_reference":
            "zone:a",
        "occupied_space_reference":
            "space:a",
        "transform_references": [
            "transform:a"
        ],
        "evidence_used_references": [
            "evidence:a",
            "evidence:b"
        ],
        "capability_movement_references": [
            "movement:a",
            "movement:b"
        ],
        "evidence_boundary": {
            "scope": "historical-bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "restriction_constriction_references": [
            "restriction:a"
        ],
        "collapse_boundary_references": [
            "collapse:a"
        ],
        "finding_references": [
            "finding:a"
        ],
        "rendering_reference":
            "rendering:a",
        "return_coordinate": {
            "coordinate": "return:a"
        },
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "replay_purpose": [
            "audit reconstruction of preserved analytical journey"
        ],
        "replay_eligibility":
            "ELIGIBLE",
        "blocking_reasons": [],
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "closing:a",
            "lineage:a",
            "question-contract:a",
            "observation:a",
            "cartography:a",
            "stick:a"
        ],
        "created_at":
            "2026-08-07T20:42:00-04:00",
    }

    envelope[
        "replay_envelope_id"
    ] = compute_replay_envelope_id(
        envelope
    )

    errors.extend(
        validate_envelope(
            envelope
        )
    )

    blocked = dict(
        envelope
    )

    blocked[
        "replay_eligibility"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = [
        "preserved historical transform is unavailable"
    ]

    blocked[
        "replay_envelope_id"
    ] = compute_replay_envelope_id(
        blocked
    )

    errors.extend(
        validate_envelope(
            blocked
        )
    )

    no_coordinate = dict(
        envelope
    )

    no_coordinate[
        "replay_observational_coordinate"
    ] = {}

    no_coordinate[
        "replay_envelope_id"
    ] = compute_replay_envelope_id(
        no_coordinate
    )

    coordinate_errors = validate_envelope(
        no_coordinate
    )

    if not any(
        "replay_observational_coordinate"
        in error
        for error in coordinate_errors
    ):
        errors.append(
            "R4-F incorrectly permitted Replay without preserved coordinate"
        )

    no_question = dict(
        envelope
    )

    no_question[
        "question_contract_reference"
    ] = ""

    no_question[
        "replay_envelope_id"
    ] = compute_replay_envelope_id(
        no_question
    )

    question_errors = validate_envelope(
        no_question
    )

    if not any(
        "question_contract_reference"
        in error
        for error in question_errors
    ):
        errors.append(
            "R4-F incorrectly permitted Replay without question contract"
        )

    bad_blocked = dict(
        blocked
    )

    bad_blocked[
        "blocking_reasons"
    ] = []

    bad_blocked[
        "replay_envelope_id"
    ] = compute_replay_envelope_id(
        bad_blocked
    )

    blocked_errors = validate_envelope(
        bad_blocked
    )

    if not any(
        "requires blocking reasons"
        in error
        for error in blocked_errors
    ):
        errors.append(
            "R4-F incorrectly permitted BLOCKED Replay without reason"
        )

    changed = dict(
        envelope
    )

    changed[
        "replay_observational_coordinate"
    ] = {
        "coordinate": "observation:b"
    }

    changed[
        "replay_envelope_id"
    ] = compute_replay_envelope_id(
        changed
    )

    if (
        changed[
            "replay_envelope_id"
        ]
        == envelope[
            "replay_envelope_id"
        ]
    ):
        errors.append(
            "material Replay Envelope change did not change identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-F REPLAY ENVELOPE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-F REPLAY ENVELOPE: PASS"
    )
    print(
        "Same Room / preserved observational coordinate: LOCKED"
    )
    print(
        "Question / inquiry / Zone / Space / transform: PRESERVED"
    )
    print(
        "Evidence / movement / restrictions / collapse / findings: PRESERVED"
    )
    print(
        "Rendering / Cartography / Stick / return route: PRESERVED"
    )
    print(
        "Approximate reconstruction / duplicate world: REJECTED"
    )
    print(
        "Lifecycle mutation / Reflight execution / Scar semantics: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
