#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT / "contracts" / "runtime" / "LANDING_WITNESS.md"
)

SCHEMA = (
    ROOT / "schemas" / "runtime" / "landing_witness.schema.json"
)

R4B = (
    ROOT / "tools" / "validate_collapse_boundary.py"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_landing_witness_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "landing_witness_id"
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

    if (
        record.get("landing_witness_id")
        != compute_landing_witness_id(record)
    ):
        errors.append(
            "landing_witness_id does not recompute from witness"
        )

    for field in (
        "object_id",
        "occupant_capability",
        "occupancy_witness_reference",
        "mission_reference",
        "zone_reference",
        "space_reference",
        "orientation_reference",
        "cartography_reference",
        "stick_reference",
        "prior_question",
        "readiness_reference",
        "current_coordinates",
        "return_coordinates",
        "landing_basis",
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
                f"Landing Witness requires {field}"
            )

    before = set(
        record.get(
            "active_payload_before_landing",
            []
        )
    )

    released = set(
        record.get(
            "payload_released_at_landing",
            []
        )
    )

    retained = set(
        record.get(
            "active_payload_retained_after_landing",
            []
        )
    )

    if released & retained:
        errors.append(
            "payload cannot be both released and retained at Landing"
        )

    if not released.issubset(before):
        errors.append(
            "released payload must originate in pre-Landing active payload"
        )

    if not retained.issubset(before):
        errors.append(
            "retained payload must originate in pre-Landing active payload"
        )

    if (released | retained) != before:
        errors.append(
            "released plus retained payload must exactly partition "
            "pre-Landing active payload"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R4-C Landing Witness contract"
        ),
        (
            SCHEMA,
            "R4-C Landing Witness schema"
        ),
        (
            R4B,
            "R4-B Collapse Boundary validator"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    r4b = subprocess.run(
        [
            sys.executable,
            str(R4B),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if r4b.returncode != 0:
        errors.append(
            "R4-B dependency validation failed"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-C schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "reflight_trigger_id",
        "closing_witness_id",
        "replay_envelope_id",
        "scar_record_id",
        "occupancy_exit",
        "new_room_object_id",
        "lifecycle_transition_id",
        "mission_completion",
        "canonical_promotion",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R4-C improperly absorbs downstream or foreign semantics: "
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
        "Capabilities may cease movement without ceasing occupation.",
        "Landing preserves object identity.",
        "Landing preserves orientation.",
        "Landing preserves representation position.",
        "Landing preserves Cartography.",
        "Landing preserves provenance.",
        "Landing preserves prior question.",
        "Landing preserves prior rendering.",
        "Landing preserves unresolved terrain.",
        "Landing preserves readiness.",
        "Landing may release unnecessary active payload.",
        "Landing is not exit.",
        "Landing is not closure.",
        "Landing is not replay.",
        "Movement state != occupancy state.",
        "Stopped movement != exited Room.",
        "Landing MUST preserve a valid Occupancy Witness reference.",
        "Landing cannot manufacture presence.",
        "Landing cannot terminate presence.",
        "Landing != Occupancy EXITED.",
        "The Room remains the Room.",
        "Stopped movement != lost orientation.",
        "Landing does not reset representation to a default.",
        "No default substitution.",
        "Landing != Cartography reset.",
        "Landing MUST NOT reduce provenance.",
        "Question preservation != reflight.",
        "Rendering preservation != rendering execution.",
        "Unresolved != failed Landing.",
        "Landing does not erase uncertainty.",
        "Readiness != movement.",
        "Readiness != automatic reflight.",
        "Readiness != execution authority.",
        "Release from active hydration != deletion.",
        "Released payload != absent.",
        "Released payload != destroyed evidence.",
        "Landing does not authorize full-payload retention.",
        "The union of released and retained payload MUST exactly equal the active payload set before Landing.",
        "Landing != Restriction.",
        "Landing != Constriction.",
        "Landing != Collapse.",
        "Landing coordinate != new origin.",
        "Landing MUST preserve the Stick.",
        "Landing MUST NOT sever analytical continuity.",
        "Stopping movement != policy reset.",
        "Landing Witness != reflight authorization.",
        "Landing Witness != lifecycle transition.",
        "Mission completion != Landing.",
        "Landing != Capability Return.",
        "One occupant Landing != whole formation Landing.",
        "Landing does not select formation.",
        "Notification != Landing.",
        "Landing first.",
        "Notify second.",
        "Landing != Reflight.",
        "R4-D owns Reflight Trigger.",
        "Landing preserves state so the system does not need to rebuild the Room merely to remain conversational.",
        "Landing != Replay Envelope.",
        "No Reflight Trigger semantics yet.",
        "No Closing Witness semantics yet.",
        "No Replay semantics yet.",
        "No Scar Replay semantics yet.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in normalized
        ):
            errors.append(
                f"missing R4-C lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    witness = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "occupant_capability":
            "Goblin:a",
        "occupancy_witness_reference":
            "occupancy:a",
        "mission_reference":
            "mission:a",
        "formation_reference":
            "formation:a",
        "zone_reference":
            "zone:a",
        "space_reference":
            "space:a",
        "orientation_reference":
            "orientation:a",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "prior_question":
            "which state remains supportable?",
        "prior_rendering_reference":
            "rendering:a",
        "unresolved_terrain_references": [
            "terrain:unresolved:a"
        ],
        "readiness_reference":
            "readiness:a",
        "restriction_constriction_references": [
            "restriction:a"
        ],
        "collapse_boundary_references": [
            "collapse:a"
        ],
        "active_payload_before_landing": [
            "payload:a",
            "payload:b",
            "payload:c"
        ],
        "payload_released_at_landing": [
            "payload:b",
            "payload:c"
        ],
        "active_payload_retained_after_landing": [
            "payload:a"
        ],
        "current_coordinates": {
            "position": "landed:a"
        },
        "return_coordinates": {
            "position": "prior-route:a"
        },
        "landing_basis": [
            "current analytical movement has converged",
            "preserve readiness without continued movement"
        ],
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "occupancy:a",
            "mission:a",
            "collapse:a",
            "cartography:a",
            "stick:a"
        ],
        "landed_at":
            "2026-08-07T20:19:00-04:00",
    }

    witness[
        "landing_witness_id"
    ] = compute_landing_witness_id(
        witness
    )

    if not SHA512_RE.fullmatch(
        witness[
            "landing_witness_id"
        ]
    ):
        errors.append(
            "landing_witness_id is not canonical SHA-512"
        )

    errors.extend(
        validate_witness(
            witness
        )
    )

    overlap = dict(
        witness
    )

    overlap[
        "payload_released_at_landing"
    ] = [
        "payload:a",
        "payload:b",
        "payload:c"
    ]

    overlap[
        "active_payload_retained_after_landing"
    ] = [
        "payload:a"
    ]

    overlap[
        "landing_witness_id"
    ] = compute_landing_witness_id(
        overlap
    )

    overlap_errors = validate_witness(
        overlap
    )

    if not any(
        "both released and retained"
        in error
        for error in overlap_errors
    ):
        errors.append(
            "R4-C incorrectly permitted overlapping payload disposition"
        )

    lost = dict(
        witness
    )

    lost[
        "payload_released_at_landing"
    ] = [
        "payload:b"
    ]

    lost[
        "active_payload_retained_after_landing"
    ] = [
        "payload:a"
    ]

    lost[
        "landing_witness_id"
    ] = compute_landing_witness_id(
        lost
    )

    lost_errors = validate_witness(
        lost
    )

    if not any(
        "exactly partition"
        in error
        for error in lost_errors
    ):
        errors.append(
            "R4-C incorrectly permitted silent loss of active payload history"
        )

    invented = dict(
        witness
    )

    invented[
        "active_payload_retained_after_landing"
    ] = [
        "payload:a",
        "payload:not-active"
    ]

    invented[
        "landing_witness_id"
    ] = compute_landing_witness_id(
        invented
    )

    invented_errors = validate_witness(
        invented
    )

    if not any(
        "retained payload must originate"
        in error
        for error in invented_errors
    ):
        errors.append(
            "R4-C incorrectly permitted invented retained payload"
        )

    changed = dict(
        witness
    )

    changed[
        "current_coordinates"
    ] = {
        "position": "landed:b"
    }

    changed[
        "landing_witness_id"
    ] = compute_landing_witness_id(
        changed
    )

    if (
        changed[
            "landing_witness_id"
        ]
        == witness[
            "landing_witness_id"
        ]
    ):
        errors.append(
            "material Landing Witness change did not change identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-C LANDING WITNESS: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-C LANDING WITNESS: PASS"
    )
    print(
        "Movement stopped / occupation preserved: LOCKED"
    )
    print(
        "Identity / orientation / representation / Cartography: PRESERVED"
    )
    print(
        "Question / rendering / unresolved terrain / readiness: PRESERVED"
    )
    print(
        "Active payload release / retain partition: ENFORCED"
    )
    print(
        "Stick / provenance / return coordinates: PRESERVED"
    )
    print(
        "Reflight / Closing Witness / Replay: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
