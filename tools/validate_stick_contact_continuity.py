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
    / "STICK_CONTACT_CONTINUITY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "stick_continuity_record.schema.json"
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


def compute_stick_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "stick_id"
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


def validate_stick(record):
    errors = []

    expected = compute_stick_id(
        record
    )

    if (
        record.get("stick_id")
        != expected
    ):
        errors.append(
            "stick_id does not recompute from declared continuity record"
        )

    for field in (
        "object_id",
        "origin_reference",
        "ingress_envelope_reference",
        "cartography_reference",
        "source_orientation_reference",
        "target_orientation_reference",
        "provenance_route",
        "source_coordinates",
        "target_coordinates",
        "return_coordinates",
        "continuity_reason",
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
        "continuity_state"
    )

    if state not in {
        "CONTINUOUS",
        "DEGRADED",
        "BROKEN",
    }:
        errors.append(
            "invalid Stick continuity state"
        )

    if state == "CONTINUOUS":
        if not record.get(
            "evidence_lineage_references"
        ):
            errors.append(
                "CONTINUOUS Stick requires evidence lineage"
            )

    return errors


def validate():
    errors = []

    if not CONTRACT.exists():
        errors.append(
            "missing R2-I Stick / Contact Continuity contract"
        )

    if not SCHEMA.exists():
        errors.append(
            "missing Stick Continuity Record schema"
        )

    if errors:
        return errors

    try:
        schema = load_schema()
    except Exception as exc:
        return [
            f"invalid R2-I schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "stick_id",
        "object_id",
        "origin_reference",
        "ingress_envelope_reference",
        "cartography_reference",
        "source_orientation_reference",
        "target_orientation_reference",
        "transform_reference",
        "space_reference",
        "evidence_lineage_references",
        "provenance_route",
        "observation_references",
        "restriction_references",
        "source_coordinates",
        "target_coordinates",
        "return_coordinates",
        "continuity_state",
        "continuity_reason",
        "recorded_at",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Stick Continuity Record missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    states = set(
        schema
        .get("properties", {})
        .get("continuity_state", {})
        .get("enum", [])
    )

    if states != {
        "CONTINUOUS",
        "DEGRADED",
        "BROKEN",
    }:
        errors.append(
            "Stick continuity states are not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "passageway_id",
        "passage_state",
        "passage_authorization",
        "occupation_id",
        "occupant_id",
        "capability_position",
        "movement_execution",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R2-I improperly absorbs downstream semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    locks = [
        "Freedom of movement requires continuity of contact.",
        "Freedom of perspective requires continuity of object identity.",
        "Stick identity is not object identity.",
        "Cartography != Stick.",
        "Transform != Stick.",
        "Coordinate change != continuity loss.",
        "Restriction != absence.",
        "DEGRADED does not silently become CONTINUOUS.",
        "BROKEN fails closed.",
        "Stick does not move anything.",
        "Stick != Passageway.",
        "Stick continuity != occupation.",
        "No Passageway semantics yet.",
        "No Occupation semantics yet.",
    ]

    for lock in locks:
        if lock not in contract_text:
            errors.append(
                f"missing R2-I lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    probe = {
        "schema_version": "1.0",
        "object_id": object_id,
        "origin_reference": "origin:a",
        "ingress_envelope_reference": "ingress:a",
        "cartography_reference": "cartography:a",
        "source_orientation_reference": "orientation:a",
        "target_orientation_reference": "orientation:b",
        "transform_reference": "transform:a",
        "space_reference": "space:a",
        "evidence_lineage_references": [
            "evidence:a"
        ],
        "provenance_route": [
            object_id,
            "origin:a",
        ],
        "observation_references": [
            "observation:a"
        ],
        "restriction_references": [
            "restriction:a"
        ],
        "source_coordinates": {
            "position": "a"
        },
        "target_coordinates": {
            "position": "b"
        },
        "return_coordinates": {
            "position": "return-a"
        },
        "continuity_state": "CONTINUOUS",
        "continuity_reason": "all required bindings resolve",
        "recorded_at": "2026-08-07T18:55:00-04:00",
    }

    probe[
        "stick_id"
    ] = compute_stick_id(
        probe
    )

    if not SHA512_RE.fullmatch(
        probe["stick_id"]
    ):
        errors.append(
            "stick_id is not canonical SHA-512"
        )

    changed = dict(
        probe
    )

    changed[
        "target_orientation_reference"
    ] = "orientation:c"

    changed[
        "stick_id"
    ] = compute_stick_id(
        changed
    )

    if (
        probe["stick_id"]
        == changed["stick_id"]
    ):
        errors.append(
            "material continuity change did not change stick_id"
        )

    if (
        probe["stick_id"]
        == object_id
    ):
        errors.append(
            "Stick identity collapsed into object identity"
        )

    errors.extend(
        validate_stick(
            probe
        )
    )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-I STICK / CONTACT CONTINUITY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-I STICK / CONTACT CONTINUITY: PASS"
    )
    print(
        "Movement / perspective continuity: BOUND"
    )
    print(
        "Object / Origin / Ingress / Cartography: PRESERVED"
    )
    print(
        "Transform / evidence lineage / provenance / coordinates: PRESERVED"
    )
    print(
        "CONTINUOUS / DEGRADED / BROKEN: LOCKED"
    )
    print(
        "Passageway / Occupation semantics: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
