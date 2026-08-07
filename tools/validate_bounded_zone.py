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
    / "BOUNDED_ZONE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "bounded_zone.schema.json"
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


def compute_zone_id(
    object_id,
    transform_type,
    perspective_owner_or_discipline,
    included_evidence,
    excluded_evidence,
    time_frame,
    evidence_ceiling,
    prohibited_assumptions,
    provenance_route,
    return_coordinates
):
    preimage = {
        "object_id":
            object_id,
        "transform_type":
            transform_type,
        "perspective_owner_or_discipline":
            perspective_owner_or_discipline,
        "included_evidence":
            included_evidence,
        "excluded_evidence":
            excluded_evidence,
        "time_frame":
            time_frame,
        "evidence_ceiling":
            evidence_ceiling,
        "prohibited_assumptions":
            prohibited_assumptions,
        "provenance_route":
            provenance_route,
        "return_coordinates":
            return_coordinates,
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


def validate_zone(zone):
    errors = []

    expected_id = compute_zone_id(
        zone.get("object_id"),
        zone.get("transform_type"),
        zone.get("perspective_owner_or_discipline"),
        zone.get("included_evidence"),
        zone.get("excluded_evidence"),
        zone.get("time_frame"),
        zone.get("evidence_ceiling"),
        zone.get("prohibited_assumptions"),
        zone.get("provenance_route"),
        zone.get("return_coordinates"),
    )

    if zone.get("zone_id") != expected_id:
        errors.append(
            "zone_id does not recompute from declared Zone frame"
        )

    included = set(
        zone.get(
            "included_evidence",
            []
        )
    )

    excluded = set(
        zone.get(
            "excluded_evidence",
            []
        )
    )

    overlap = included & excluded

    if overlap:
        errors.append(
            "evidence cannot be simultaneously included and excluded: "
            + ", ".join(
                sorted(overlap)
            )
        )

    if not zone.get(
        "provenance_route"
    ):
        errors.append(
            "Zone provenance route is empty"
        )

    if zone.get(
        "evidence_ceiling"
    ) in (
        None,
        "",
        {},
    ):
        errors.append(
            "Zone evidence ceiling is undefined"
        )

    if zone.get(
        "time_frame"
    ) in (
        None,
        "",
        {},
    ):
        errors.append(
            "Zone time frame is undefined"
        )

    if zone.get(
        "return_coordinates"
    ) in (
        None,
        "",
        {},
    ):
        errors.append(
            "Zone return coordinates are undefined"
        )

    return errors


def validate():
    errors = []

    if not CONTRACT.exists():
        errors.append(
            "missing R2-D Bounded Zone contract"
        )

    if not SCHEMA.exists():
        errors.append(
            "missing Bounded Zone schema"
        )

    if errors:
        return errors

    try:
        schema = load_schema()
    except Exception as exc:
        return [
            f"invalid R2-D schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "object_id",
        "zone_id",
        "transform_type",
        "perspective_owner_or_discipline",
        "included_evidence",
        "excluded_evidence",
        "time_frame",
        "evidence_ceiling",
        "prohibited_assumptions",
        "provenance_route",
        "return_coordinates",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Bounded Zone missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "space_id",
        "mission",
        "question",
        "transform_id",
        "source_orientation",
        "target_orientation",
        "cartography_id",
        "stick_id",
        "occupation_id",
        "capability_id",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R2-D improperly absorbs downstream fields: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    required_locks = [
        "Reality is established once.",
        "Representation may turn many times.",
        "Zone identity != object identity.",
        "Excluded != absent.",
        "Zone observation does not authorize canonical mutation.",
        "Zone != Space.",
        "Persistent frame != active mission.",
        "Representation cannot manufacture reachability.",
        "No Space semantics yet.",
        "No full Transform semantics yet.",
        "No Orientation semantics yet.",
        "No Cartography yet.",
        "No Stick yet.",
        "No Occupation yet.",
    ]

    for lock in required_locks:
        if lock not in contract_text:
            errors.append(
                f"missing R2-D lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    zone_id = compute_zone_id(
        object_id,
        "PERSPECTIVE",
        "Audit",
        [
            "evidence:a",
            "evidence:b",
        ],
        [
            "evidence:c",
        ],
        {
            "start": "2026-08-01",
            "end": "2026-08-07",
        },
        "CEILING:DECLARED",
        [
            "no attribution without evidence",
        ],
        [
            object_id,
            "origin:probe",
        ],
        {
            "reference":
                "return:probe",
        }
    )

    if not SHA512_RE.fullmatch(
        zone_id
    ):
        errors.append(
            "zone_id is not canonical SHA-512"
        )

    same_zone_id = compute_zone_id(
        object_id,
        "PERSPECTIVE",
        "Audit",
        [
            "evidence:a",
            "evidence:b",
        ],
        [
            "evidence:c",
        ],
        {
            "end": "2026-08-07",
            "start": "2026-08-01",
        },
        "CEILING:DECLARED",
        [
            "no attribution without evidence",
        ],
        [
            object_id,
            "origin:probe",
        ],
        {
            "reference":
                "return:probe",
        }
    )

    if zone_id != same_zone_id:
        errors.append(
            "Zone identity is not deterministic under canonical JSON"
        )

    changed_zone_id = compute_zone_id(
        object_id,
        "PERSPECTIVE",
        "Security",
        [
            "evidence:a",
            "evidence:b",
        ],
        [
            "evidence:c",
        ],
        {
            "start": "2026-08-01",
            "end": "2026-08-07",
        },
        "CEILING:DECLARED",
        [
            "no attribution without evidence",
        ],
        [
            object_id,
            "origin:probe",
        ],
        {
            "reference":
                "return:probe",
        }
    )

    if zone_id == changed_zone_id:
        errors.append(
            "material Zone-frame change did not change zone_id"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-D BOUNDED ZONE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-D BOUNDED ZONE: PASS"
    )
    print(
        "Zone: PERSISTENT DECLARED REPRESENTATION FRAME"
    )
    print(
        "Object identity: PRESERVED"
    )
    print(
        "Evidence inclusion / exclusion / ceiling: EXPLICIT"
    )
    print(
        "Prohibited assumptions / provenance / return coordinates: EXPLICIT"
    )
    print(
        "Space / Transform / Orientation / Cartography / Stick / Occupation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
