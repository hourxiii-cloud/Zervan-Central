#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "object"
    / "CANONICAL_ROOM_OBJECT_IDENTITY_SINGULARITY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "object"
    / "canonical_room_object.schema.json"
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


def compute_object_id(
    genesis_manifest_reference,
    origin_content_identity,
    object_nonce
):
    preimage = {
        "genesis_manifest_reference":
            genesis_manifest_reference,
        "origin_content_identity":
            origin_content_identity,
        "object_nonce":
            object_nonce,
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


def validate():
    errors = []

    if not CONTRACT.exists():
        errors.append(
            "missing R2-A object identity contract"
        )

    if not SCHEMA.exists():
        errors.append(
            "missing Canonical Room Object schema"
        )

    if errors:
        return errors

    try:
        schema = load_schema()
    except Exception as exc:
        return [
            f"invalid R2-A schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "object_id",
        "genesis_manifest_reference",
        "origin_content_identity",
        "object_nonce",
        "provenance_origin_reference",
        "establishment_status",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Canonical Room Object missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    object_pattern = (
        schema
        .get("properties", {})
        .get("object_id", {})
        .get("pattern")
    )

    if object_pattern != "^sha512:[0-9a-f]{128}$":
        errors.append(
            "object_id format is not SHA-512 locked"
        )

    establishment_states = set(
        schema
        .get("properties", {})
        .get("establishment_status", {})
        .get("enum", [])
    )

    if establishment_states != {
        "PROPOSED",
        "ESTABLISHED",
        "REJECTED",
    }:
        errors.append(
            "object establishment states are not locked"
        )

    # R2-A MUST NOT absorb downstream geography/state identities.
    forbidden_fields = {
        "state_root",
        "authorized_view_root",
        "branch_id",
        "merge_id",
        "terrain",
        "territory",
        "zone_id",
        "space_id",
        "transform_id",
        "cartography",
        "passageway_id",
    }

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    leaked = (
        properties
        & forbidden_fields
    )

    if leaked:
        errors.append(
            "R2-A schema improperly absorbs downstream fields: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    required_locks = [
        "THE ROOM IS ONE ANALYTICAL OBJECT.",
        "Object identity != originating content identity.",
        "Manifest identity != object identity.",
        "State Root != object identity.",
        "Authorized View Root != object identity.",
        "Branch identity != object identity.",
        "Merge identity != object identity.",
        "Computable != established.",
        "TURN THE OBJECT.",
        "DO NOT CLONE THE WORLD.",
    ]

    for lock in required_locks:
        if lock not in contract_text:
            errors.append(
                f"missing R2-A singularity lock: {lock}"
            )

    origin = (
        "sha512:"
        + "1" * 128
    )

    first = compute_object_id(
        "manifest:genesis-a",
        origin,
        "object-1"
    )

    second = compute_object_id(
        "manifest:genesis-a",
        origin,
        "object-1"
    )

    if first != second:
        errors.append(
            "object identity is not deterministic"
        )

    if not SHA512_RE.fullmatch(first):
        errors.append(
            "computed object identity is not canonical SHA-512 form"
        )

    separated = compute_object_id(
        "manifest:genesis-a",
        origin,
        "object-2"
    )

    if first == separated:
        errors.append(
            "object nonce failed to separate independent objects"
        )

    changed_genesis = compute_object_id(
        "manifest:genesis-b",
        origin,
        "object-1"
    )

    if first == changed_genesis:
        errors.append(
            "Genesis lineage is not bound into object identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-A CANONICAL ROOM OBJECT IDENTITY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-A CANONICAL ROOM OBJECT IDENTITY: PASS"
    )
    print(
        "Object singularity: ONE OBJECT"
    )
    print(
        "Object identity: deterministic SHA-512 establishment identity"
    )
    print(
        "Revision / state / view / branch / merge: DO NOT REPLACE OBJECT ID"
    )
    print(
        "Distinct object: independent Genesis + affirmative evidence"
    )
    print(
        "Downstream geography: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
