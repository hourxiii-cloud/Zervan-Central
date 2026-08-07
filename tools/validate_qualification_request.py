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
    / "QUALIFICATION_REQUEST_MISSION_FITNESS.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "qualification_request.schema.json"
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


def compute_qualification_request_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "qualification_request_id"
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


def validate_request(record):
    errors = []

    expected = compute_qualification_request_id(
        record
    )

    if (
        record.get("qualification_request_id")
        != expected
    ):
        errors.append(
            "qualification_request_id does not recompute from request"
        )

    state = record.get(
        "request_state"
    )

    if state not in {
        "DRAFT",
        "READY",
        "BLOCKED",
    }:
        errors.append(
            "invalid Qualification Request state"
        )

    if state == "READY":
        required_ready = (
            "object_id",
            "provisional_room_reference",
            "origin_reference",
            "ingress_reference",
            "orientation_reference",
            "territory_reference",
            "qualification_mission",
            "active_question",
            "entry_constraints",
            "evidence_obligations",
            "evidence_boundary",
            "evidence_ceiling",
            "prohibited_assumptions",
            "human_gate_conditions",
            "qualification_requirements",
            "provenance_route",
        )

        for field in required_ready:
            if record.get(field) in (
                None,
                "",
                {},
                [],
            ):
                errors.append(
                    f"READY Qualification Request requires {field}"
                )

    included = set(
        record.get(
            "included_evidence",
            []
        )
    )

    excluded = set(
        record.get(
            "excluded_evidence",
            []
        )
    )

    overlap = included & excluded

    if overlap:
        errors.append(
            "evidence cannot be both included and excluded: "
            + ", ".join(
                sorted(overlap)
            )
        )

    return errors


def validate():
    errors = []

    if not CONTRACT.exists():
        errors.append(
            "missing R3-A Qualification Request contract"
        )

    if not SCHEMA.exists():
        errors.append(
            "missing Qualification Request schema"
        )

    if errors:
        return errors

    try:
        schema = load_schema()
    except Exception as exc:
        return [
            f"invalid R3-A schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "qualification_request_id",
        "object_id",
        "provisional_room_reference",
        "origin_reference",
        "ingress_reference",
        "zone_id",
        "space_id",
        "orientation_reference",
        "territory_reference",
        "qualification_mission",
        "active_question",
        "entry_constraints",
        "evidence_obligations",
        "included_evidence",
        "excluded_evidence",
        "evidence_boundary",
        "evidence_ceiling",
        "prohibited_assumptions",
        "human_gate_conditions",
        "qualification_requirements",
        "request_state",
        "provenance_route",
        "requested_at",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Qualification Request missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    states = set(
        schema
        .get("properties", {})
        .get("request_state", {})
        .get("enum", [])
    )

    if states != {
        "DRAFT",
        "READY",
        "BLOCKED",
    }:
        errors.append(
            "Qualification Request states are not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "qualification_disposition",
        "qualification_record_id",
        "qualification_lead",
        "participating_capabilities",
        "formation_id",
        "formation_type",
        "occupancy_witness_id",
        "capability_mission_id",
        "cartography_changes",
        "distinct_object_result",
        "recommended_formation",
        "replay_route",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R3-A improperly absorbs downstream qualification semantics: "
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
        "Qualification precedes analysis.",
        "The Qualification Request declares what must be qualified.",
        "The Qualification Request does not claim qualification success.",
        "Qualification does not prove every fact inside the Room.",
        "Qualification does not authorize publication.",
        "Qualification does not authorize execution.",
        "Mission declared != mission fit.",
        "Requested != fit.",
        "Requested != QUALIFIED.",
        "Request READY != Room READY.",
        "Request READY != QUALIFIED.",
        "Provisional reference != object identity.",
        "Excluded != absent.",
        "Restriction != absence.",
        "Assumption != evidence.",
        "Unresolved != passed.",
        "Sufficient != complete.",
        "Approval != execution.",
        "Entry permission != presence.",
        "Request != formation selection.",
        "Request != capability assignment.",
        "Request != Record.",
        "Write capability != authority.",
        "No qualification disposition yet.",
        "No analytical occupation yet.",
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
                f"missing R3-A lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    probe = {
        "schema_version": "1.0",
        "object_id": object_id,
        "provisional_room_reference":
            "room:provisional:a",
        "origin_reference":
            "origin:a",
        "ingress_reference":
            "ingress:a",
        "zone_id":
            "sha512:" + "2" * 128,
        "space_id":
            "sha512:" + "3" * 128,
        "orientation_reference":
            "orientation:a",
        "territory_reference":
            "territory:a",
        "qualification_mission":
            "establish mission fitness",
        "active_question":
            "is the Room sufficiently established for this mission?",
        "entry_constraints": [
            "qualification-only access"
        ],
        "evidence_obligations": [
            "preserve provenance",
            "evaluate boundary",
        ],
        "included_evidence": [
            "evidence:a"
        ],
        "excluded_evidence": [
            "evidence:b"
        ],
        "evidence_boundary": {
            "included": [
                "evidence:a"
            ],
            "excluded": [
                "evidence:b"
            ],
        },
        "evidence_ceiling":
            "CEILING:QUALIFICATION",
        "prohibited_assumptions": [
            "do not infer missing evidence"
        ],
        "human_gate_conditions": [
            "preserve Human Gate requirements"
        ],
        "qualification_requirements": [
            "object_identity",
            "boundary",
            "provenance",
            "geometry",
            "mission_fitness",
            "uncertainty",
            "restrictions",
            "reachable_surfaces",
        ],
        "request_state":
            "READY",
        "provenance_route": [
            object_id,
            "origin:a",
            "ingress:a",
        ],
        "requested_at":
            "2026-08-07T19:08:00-04:00",
    }

    probe[
        "qualification_request_id"
    ] = compute_qualification_request_id(
        probe
    )

    if not SHA512_RE.fullmatch(
        probe[
            "qualification_request_id"
        ]
    ):
        errors.append(
            "qualification_request_id is not canonical SHA-512"
        )

    request_errors = validate_request(
        probe
    )

    if request_errors:
        errors.extend(
            request_errors
        )

    changed = dict(
        probe
    )

    changed[
        "active_question"
    ] = (
        "what additional evidence is required "
        "for mission fitness?"
    )

    changed[
        "qualification_request_id"
    ] = compute_qualification_request_id(
        changed
    )

    if (
        probe["qualification_request_id"]
        == changed["qualification_request_id"]
    ):
        errors.append(
            "material request change did not change request identity"
        )

    if (
        probe["qualification_request_id"]
        == object_id
    ):
        errors.append(
            "Qualification Request identity collapsed into object identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-A QUALIFICATION REQUEST / MISSION FITNESS: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-A QUALIFICATION REQUEST / MISSION FITNESS: PASS"
    )
    print(
        "Qualification precedes analysis: LOCKED"
    )
    print(
        "Mission / question / representation / evidence boundary: DECLARED"
    )
    print(
        "Entry / evidence / Human Gate conditions: PRESERVED"
    )
    print(
        "Mission fitness: REQUESTED, NOT PRESUMED"
    )
    print(
        "Disposition / formation / occupation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
