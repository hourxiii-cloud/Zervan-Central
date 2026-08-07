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
    / "PASSAGEWAY_DISTINCT_OBJECT_CONTACT.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "passageway_record.schema.json"
)

DISTINCT_SCHEMA = (
    ROOT
    / "schemas"
    / "lineage"
    / "distinct_object_record.schema.json"
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


def compute_passageway_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "passageway_id"
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


def validate_passageway(record):
    errors = []

    expected = compute_passageway_id(
        record
    )

    if record.get("passageway_id") != expected:
        errors.append(
            "passageway_id does not recompute from declared Passageway"
        )

    state = record.get("passageway_state")
    result = record.get("distinct_object_result")

    if state not in {
        "PROPOSED",
        "ESTABLISHED",
        "BLOCKED",
    }:
        errors.append(
            "invalid Passageway state"
        )

    if result not in {
        "SAME_OBJECT",
        "DISTINCT_OBJECT",
        "UNRESOLVED",
    }:
        errors.append(
            "invalid distinct-object result"
        )

    if state == "ESTABLISHED":
        if result != "DISTINCT_OBJECT":
            errors.append(
                "ESTABLISHED Passageway requires DISTINCT_OBJECT"
            )

        if (
            record.get("source_object_id")
            == record.get("target_object_id")
        ):
            errors.append(
                "ESTABLISHED Passageway requires distinct object identities"
            )

        for field in (
            "distinct_object_determination_reference",
            "relationship_to_source",
            "source_origin_reference",
            "target_origin_reference",
            "source_cartography_reference",
            "target_cartography_reference",
            "source_stick_reference",
            "target_stick_reference",
            "evidence_of_distinctness_references",
            "passageway_conditions",
            "contamination_controls",
            "return_route",
            "authorization_reference",
            "provenance_route",
        ):
            if record.get(field) in (
                None,
                "",
                [],
                {},
            ):
                errors.append(
                    f"ESTABLISHED Passageway requires {field}"
                )

    if (
        result == "SAME_OBJECT"
        and state == "ESTABLISHED"
    ):
        errors.append(
            "SAME_OBJECT cannot establish cross-object Passageway"
        )

    if (
        result == "UNRESOLVED"
        and state == "ESTABLISHED"
    ):
        errors.append(
            "UNRESOLVED cannot establish cross-object Passageway"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R2-J Passageway contract"
        ),
        (
            SCHEMA,
            "R2-J Passageway schema"
        ),
        (
            DISTINCT_SCHEMA,
            "R1-F Distinct Object schema"
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
        distinct_schema = load(
            DISTINCT_SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "passageway_id",
        "source_object_id",
        "target_object_id",
        "distinct_object_determination_reference",
        "distinct_object_result",
        "relationship_to_source",
        "source_origin_reference",
        "target_origin_reference",
        "source_cartography_reference",
        "target_cartography_reference",
        "source_stick_reference",
        "target_stick_reference",
        "shared_provenance",
        "non_shared_provenance",
        "evidence_of_distinctness_references",
        "passageway_conditions",
        "contamination_controls",
        "return_route",
        "authorization_reference",
        "human_gate_reference",
        "passageway_state",
        "provenance_route",
        "recorded_at",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Passageway Record missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    passageway_results = set(
        schema
        .get("properties", {})
        .get("distinct_object_result", {})
        .get("enum", [])
    )

    r1f_results = set(
        distinct_schema
        .get("properties", {})
        .get("determination", {})
        .get("enum", [])
    )

    if passageway_results != r1f_results:
        errors.append(
            "R2-J distinct-object vocabulary diverges from R1-F"
        )

    if passageway_results != {
        "SAME_OBJECT",
        "DISTINCT_OBJECT",
        "UNRESOLVED",
    }:
        errors.append(
            "R1-F distinct-object states are not preserved"
        )

    states = set(
        schema
        .get("properties", {})
        .get("passageway_state", {})
        .get("enum", [])
    )

    if states != {
        "PROPOSED",
        "ESTABLISHED",
        "BLOCKED",
    }:
        errors.append(
            "Passageway states are not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "occupation_id",
        "occupant_id",
        "capability_position",
        "movement_execution",
        "traversal_record",
        "merge_id",
        "new_object_id",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R2-J improperly absorbs downstream or foreign semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    locks = [
        "Contact != identity collapse.",
        "Related does not mean identical.",
        "Different perspective does not mean distinct object.",
        "Only `DISTINCT_OBJECT` can support an ESTABLISHED Passageway.",
        "Same object != Passageway.",
        "Unknown remains unknown.",
        "Passageway identity is not Room identity.",
        "Shared provenance does not collapse object identity.",
        "Passageway convenience is not evidence of distinctness.",
        "Cartography remains independent.",
        "Stick != Passageway.",
        "Cross-object contact != Merge.",
        "Passageway != Merge.",
        "Passageway != Genesis.",
        "Passageway established != Passageway traversed.",
        "Passageway availability != movement authorization.",
        "Contact != presence.",
        "RING 2 OPERATIONAL GEOGRAPHY: COMPLETE WHEN R2-A THROUGH R2-J PASS.",
    ]

    for lock in locks:
        if lock not in contract_text:
            errors.append(
                f"missing R2-J lock: {lock}"
            )

    source = (
        "sha512:"
        + "1" * 128
    )

    target = (
        "sha512:"
        + "2" * 128
    )

    probe = {
        "schema_version": "1.0",
        "source_object_id": source,
        "target_object_id": target,
        "distinct_object_determination_reference":
            "distinct-object:test-a",
        "distinct_object_result":
            "DISTINCT_OBJECT",
        "relationship_to_source":
            "validated adjoining analytical object",
        "source_origin_reference":
            "origin:source",
        "target_origin_reference":
            "origin:target",
        "source_cartography_reference":
            "cartography:source",
        "target_cartography_reference":
            "cartography:target",
        "source_stick_reference":
            "stick:source",
        "target_stick_reference":
            "stick:target",
        "shared_provenance": [
            "provenance:shared"
        ],
        "non_shared_provenance": [
            "provenance:source-only",
            "provenance:target-only",
        ],
        "evidence_of_distinctness_references": [
            "evidence:distinct-a"
        ],
        "passageway_conditions": [
            "contact under declared evidence boundary"
        ],
        "contamination_controls": [
            "preserve independent state",
            "preserve independent provenance",
        ],
        "return_route": [
            "object:source",
            "cartography:source",
            "orientation:source",
        ],
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "passageway_state":
            "ESTABLISHED",
        "provenance_route": [
            source,
            "origin:source",
            "distinct-object:test-a",
            target,
            "origin:target",
        ],
        "recorded_at":
            "2026-08-07T18:58:00-04:00",
    }

    probe[
        "passageway_id"
    ] = compute_passageway_id(
        probe
    )

    if not SHA512_RE.fullmatch(
        probe["passageway_id"]
    ):
        errors.append(
            "passageway_id is not canonical SHA-512"
        )

    errors.extend(
        validate_passageway(
            probe
        )
    )

    same_object = dict(
        probe
    )

    same_object[
        "target_object_id"
    ] = source

    same_object[
        "distinct_object_result"
    ] = "SAME_OBJECT"

    same_object[
        "passageway_id"
    ] = compute_passageway_id(
        same_object
    )

    same_errors = validate_passageway(
        same_object
    )

    if not any(
        "requires DISTINCT_OBJECT"
        in error
        or "distinct object identities"
        in error
        or "SAME_OBJECT"
        in error
        for error in same_errors
    ):
        errors.append(
            "SAME_OBJECT incorrectly permitted ESTABLISHED Passageway"
        )

    unresolved = dict(
        probe
    )

    unresolved[
        "distinct_object_result"
    ] = "UNRESOLVED"

    unresolved[
        "passageway_id"
    ] = compute_passageway_id(
        unresolved
    )

    unresolved_errors = validate_passageway(
        unresolved
    )

    if not any(
        "requires DISTINCT_OBJECT"
        in error
        or "UNRESOLVED"
        in error
        for error in unresolved_errors
    ):
        errors.append(
            "UNRESOLVED incorrectly permitted ESTABLISHED Passageway"
        )

    if (
        probe["passageway_id"]
        in {
            source,
            target,
        }
    ):
        errors.append(
            "Passageway identity collapsed into object identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-J PASSAGEWAYS / DISTINCT-OBJECT CONTACT: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-J PASSAGEWAYS / DISTINCT-OBJECT CONTACT: PASS"
    )
    print(
        "R1-F distinct-object determination: CONSUMED"
    )
    print(
        "Independent object identities / origins / geometry: PRESERVED"
    )
    print(
        "Passageway conditions / contamination controls / return route: BOUND"
    )
    print(
        "Cross-object contact: NO IDENTITY COLLAPSE"
    )
    print(
        "Occupation / traversal / movement execution: DEFERRED"
    )
    print(
        "RING 2 OPERATIONAL GEOGRAPHY: COMPLETE"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
