#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "geography"
    / "ORIENTATION_COORDINATES.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "orientation_record.schema.json"
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


def compute_orientation_id(
    object_id,
    origin_reference,
    zone_id,
    territory_reference,
    space_id,
    representation_transform_reference,
    perspective_or_discipline,
    time_constraint,
    evidence_constraints,
    active_question,
    active_mission,
    evidence_boundary,
    evidence_ceiling,
    current_coordinates,
    return_coordinates,
    resolution_state,
    provenance_route
):
    preimage = {
        "object_id":
            object_id,
        "origin_reference":
            origin_reference,
        "zone_id":
            zone_id,
        "territory_reference":
            territory_reference,
        "space_id":
            space_id,
        "representation_transform_reference":
            representation_transform_reference,
        "perspective_or_discipline":
            perspective_or_discipline,
        "time_constraint":
            time_constraint,
        "evidence_constraints":
            evidence_constraints,
        "active_question":
            active_question,
        "active_mission":
            active_mission,
        "evidence_boundary":
            evidence_boundary,
        "evidence_ceiling":
            evidence_ceiling,
        "current_coordinates":
            current_coordinates,
        "return_coordinates":
            return_coordinates,
        "resolution_state":
            resolution_state,
        "provenance_route":
            provenance_route,
    }

    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(preimage)
        ).hexdigest()
    )


def load_schema():
    return json.loads(
        SCHEMA.read_text(
            encoding="utf-8"
        )
    )


def validate_orientation(record):
    errors = []

    expected = compute_orientation_id(
        record.get("object_id"),
        record.get("origin_reference"),
        record.get("zone_id"),
        record.get("territory_reference"),
        record.get("space_id"),
        record.get("representation_transform_reference"),
        record.get("perspective_or_discipline"),
        record.get("time_constraint"),
        record.get("evidence_constraints"),
        record.get("active_question"),
        record.get("active_mission"),
        record.get("evidence_boundary"),
        record.get("evidence_ceiling"),
        record.get("current_coordinates"),
        record.get("return_coordinates"),
        record.get("resolution_state"),
        record.get("provenance_route"),
    )

    if record.get("orientation_id") != expected:
        errors.append(
            "orientation_id does not recompute from declared orientation"
        )

    for field in (
        "origin_reference",
        "territory_reference",
        "evidence_boundary",
        "evidence_ceiling",
        "current_coordinates",
        "return_coordinates",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"{field} is undefined"
            )

    state = record.get(
        "resolution_state"
    )

    if state not in {
        "RESOLVED",
        "PROVISIONAL",
        "UNRESOLVED",
    }:
        errors.append(
            "invalid Orientation resolution state"
        )

    if state == "RESOLVED":
        if record.get(
            "active_mission"
        ) in (
            None,
            "",
        ):
            errors.append(
                "RESOLVED Orientation requires active mission"
            )

        if record.get(
            "active_question"
        ) in (
            None,
            "",
        ):
            errors.append(
                "RESOLVED Orientation requires active question"
            )

    return errors


def validate():
    errors = []

    if not CONTRACT.exists():
        errors.append(
            "missing R2-G Orientation / Coordinates contract"
        )

    if not SCHEMA.exists():
        errors.append(
            "missing Orientation Record schema"
        )

    if errors:
        return errors

    try:
        schema = load_schema()
    except Exception as exc:
        return [
            f"invalid R2-G schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "orientation_id",
        "object_id",
        "origin_reference",
        "zone_id",
        "territory_reference",
        "space_id",
        "representation_transform_reference",
        "perspective_or_discipline",
        "time_constraint",
        "evidence_constraints",
        "active_question",
        "active_mission",
        "evidence_boundary",
        "evidence_ceiling",
        "current_coordinates",
        "return_coordinates",
        "resolution_state",
        "provenance_route",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Orientation Record missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    states = set(
        schema
        .get("properties", {})
        .get("resolution_state", {})
        .get("enum", [])
    )

    if states != {
        "RESOLVED",
        "PROVISIONAL",
        "UNRESOLVED",
    }:
        errors.append(
            "Orientation resolution states are not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "cartography_id",
        "stick_id",
        "passageway_id",
        "occupation_id",
        "capability_position",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R2-G improperly absorbs downstream fields: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    locks = [
        "Where am I?",
        "Orient first.",
        "Reason second.",
        "Orientation identity is not object identity.",
        "Coordinate change != object change.",
        "UNRESOLVED MUST NOT silently become RESOLVED.",
        "Historical coordinate != duplicate reality.",
        "Same analytical world != same mind.",
        "Orientation != Cartography.",
        "Coordinates != map.",
        "Coordinates != Stick.",
        "Orientation != Passageway.",
        "Oriented != occupied.",
        "No Cartography yet.",
        "No Stick yet.",
        "No Passageway yet.",
        "No Occupation yet.",
    ]

    for lock in locks:
        if lock not in contract_text:
            errors.append(
                f"missing R2-G lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    orientation_id = compute_orientation_id(
        object_id,
        "origin:a",
        "sha512:" + "2" * 128,
        "territory:a",
        "sha512:" + "3" * 128,
        "transform:a",
        "Audit",
        {
            "start": "2026-08-01",
            "end": "2026-08-07",
        },
        [
            "restricted:evidence-b"
        ],
        "what changed?",
        "bounded analysis",
        {
            "included": ["evidence:a"],
            "excluded": ["evidence:b"],
        },
        "CEILING:A",
        {
            "representation": "audit",
            "position": "current",
        },
        {
            "representation": "origin",
            "position": "return",
        },
        "RESOLVED",
        [
            object_id,
            "origin:a",
        ],
    )

    if not SHA512_RE.fullmatch(
        orientation_id
    ):
        errors.append(
            "orientation_id is not canonical SHA-512"
        )

    changed = compute_orientation_id(
        object_id,
        "origin:a",
        "sha512:" + "2" * 128,
        "territory:a",
        "sha512:" + "3" * 128,
        "transform:a",
        "Security",
        {
            "start": "2026-08-01",
            "end": "2026-08-07",
        },
        [
            "restricted:evidence-b"
        ],
        "what changed?",
        "bounded analysis",
        {
            "included": ["evidence:a"],
            "excluded": ["evidence:b"],
        },
        "CEILING:A",
        {
            "representation": "security",
            "position": "current",
        },
        {
            "representation": "origin",
            "position": "return",
        },
        "RESOLVED",
        [
            object_id,
            "origin:a",
        ],
    )

    if orientation_id == changed:
        errors.append(
            "material Orientation change did not change orientation_id"
        )

    if orientation_id == object_id:
        errors.append(
            "Orientation identity collapsed into object identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-G ORIENTATION / COORDINATES: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-G ORIENTATION / COORDINATES: PASS"
    )
    print(
        "Where am I?: RESOLVABLE"
    )
    print(
        "Orient first / reason second: LOCKED"
    )
    print(
        "Object / Origin / Zone / Territory / Space / Transform: REFERENCED"
    )
    print(
        "Evidence boundary / ceiling / current / return coordinates: EXPLICIT"
    )
    print(
        "Cartography / Stick / Passageway / Occupation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
