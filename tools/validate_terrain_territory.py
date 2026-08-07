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
    / "TERRAIN_TERRITORY.md"
)

TERRAIN_SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "terrain_record.schema.json"
)

TERRITORY_SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "territory_record.schema.json"
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


def sha512_identity(value):
    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(value)
        ).hexdigest()
    )


def compute_terrain_record_id(
    object_id,
    representation_reference,
    observation_reference,
    features,
    accessibility_state,
    observed_at
):
    return sha512_identity({
        "object_id":
            object_id,
        "representation_reference":
            representation_reference,
        "observation_reference":
            observation_reference,
        "features":
            features,
        "accessibility_state":
            accessibility_state,
        "observed_at":
            observed_at,
    })


def compute_territory_record_id(
    object_id,
    reachable_terrain_references,
    validated_relationship_references,
    reachable_surface_references,
    unresolved_reachability_references,
    excluded_unreachable_references,
    derived_at
):
    return sha512_identity({
        "object_id":
            object_id,
        "reachable_terrain_references":
            reachable_terrain_references,
        "validated_relationship_references":
            validated_relationship_references,
        "reachable_surface_references":
            reachable_surface_references,
        "unresolved_reachability_references":
            unresolved_reachability_references,
        "excluded_unreachable_references":
            excluded_unreachable_references,
        "derived_at":
            derived_at,
    })


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def validate_reachability(
    reachability_state
):
    return reachability_state in {
        "REACHABLE",
        "UNREACHABLE",
        "UNRESOLVED",
    }


def enters_active_territory(
    reachability_state
):
    return (
        reachability_state
        == "REACHABLE"
    )


def validate():
    errors = []

    for path, label in [
        (
            CONTRACT,
            "R2-C Terrain / Territory contract"
        ),
        (
            TERRAIN_SCHEMA,
            "Terrain Record schema"
        ),
        (
            TERRITORY_SCHEMA,
            "Territory Record schema"
        ),
    ]:
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        terrain = load(
            TERRAIN_SCHEMA
        )

        territory = load(
            TERRITORY_SCHEMA
        )

    except Exception as exc:
        return [
            f"invalid R2-C schema JSON: {exc}"
        ]

    terrain_required = set(
        terrain.get(
            "required",
            []
        )
    )

    for field in {
        "terrain_record_id",
        "object_id",
        "representation_reference",
        "observation_reference",
        "features",
        "accessibility_state",
        "provenance_route",
        "observed_at",
    }:
        if field not in terrain_required:
            errors.append(
                "Terrain Record missing "
                f"required field: {field}"
            )

    territory_required = set(
        territory.get(
            "required",
            []
        )
    )

    for field in {
        "territory_record_id",
        "object_id",
        "reachable_terrain_references",
        "validated_relationship_references",
        "reachable_surface_references",
        "unresolved_reachability_references",
        "excluded_unreachable_references",
        "provenance_route",
        "derived_at",
    }:
        if field not in territory_required:
            errors.append(
                "Territory Record missing "
                f"required field: {field}"
            )

    terrain_features = set(
        terrain
        .get("properties", {})
        .get("features", {})
        .get("properties", {})
    )

    required_features = {
        "source_structure",
        "fields",
        "records",
        "relationships",
        "density",
        "absence",
        "fractures",
        "signal_concentrations",
        "boundaries",
        "gradients",
        "discontinuities",
        "reachable_surfaces",
        "unreachable_surfaces",
        "stable_regions",
        "uncertainty_frontiers",
        "deformation_regions",
    }

    missing_features = (
        required_features
        - terrain_features
    )

    if missing_features:
        errors.append(
            "Terrain feature vocabulary incomplete: "
            + ", ".join(
                sorted(missing_features)
            )
        )

    accessibility_states = set(
        terrain
        .get("properties", {})
        .get("accessibility_state", {})
        .get("enum", [])
    )

    if accessibility_states != {
        "OBSERVED",
        "RESTRICTED",
        "UNAVAILABLE",
        "UNRESOLVED",
    }:
        errors.append(
            "Terrain accessibility states are not locked"
        )

    # Do not pull later geography primitives forward.
    forbidden = {
        "zone_id",
        "space_id",
        "transform_id",
        "orientation_id",
        "cartography_id",
        "occupation_id",
        "passageway_id",
    }

    for name, schema in [
        (
            "Terrain",
            terrain
        ),
        (
            "Territory",
            territory
        ),
    ]:
        properties = set(
            schema.get(
                "properties",
                {}
            )
        )

        leaked = (
            properties
            & forbidden
        )

        if leaked:
            errors.append(
                f"{name} improperly defines downstream fields: "
                + ", ".join(
                    sorted(leaked)
                )
            )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    required_locks = [
        "Terrain != Territory.",
        "Terrain is not a conclusion.",
        "Possible != reachable.",
        "Known != reachable.",
        "Only REACHABLE material belongs to active Territory.",
        "Terrain identity is not object identity.",
        "Territory identity is not object identity.",
        "Terrain != Cartography.",
        "Territory != Cartography.",
        "Reachable != occupied.",
        "No Zone semantics yet.",
        "No Space semantics yet.",
        "No Cartography yet.",
        "No Occupation yet.",
    ]

    for lock in required_locks:
        if lock not in contract_text:
            errors.append(
                f"missing R2-C lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    terrain_id = compute_terrain_record_id(
        object_id,
        "representation:probe",
        "observation:probe",
        {
            "records": [
                "record:a"
            ],
            "fractures": [
                "fracture:a"
            ],
        },
        "OBSERVED",
        "2026-08-07T18:30:00-04:00"
    )

    if not SHA512_RE.fullmatch(
        terrain_id
    ):
        errors.append(
            "Terrain Record identity is not canonical SHA-512"
        )

    territory_id = compute_territory_record_id(
        object_id,
        [
            terrain_id
        ],
        [
            "relationship:a"
        ],
        [
            "surface:a"
        ],
        [
            "surface:unknown"
        ],
        [
            "surface:blocked"
        ],
        "2026-08-07T18:31:00-04:00"
    )

    if not SHA512_RE.fullmatch(
        territory_id
    ):
        errors.append(
            "Territory Record identity is not canonical SHA-512"
        )

    if terrain_id == territory_id:
        errors.append(
            "Terrain identity collapsed into Territory identity"
        )

    if not enters_active_territory(
        "REACHABLE"
    ):
        errors.append(
            "REACHABLE material cannot enter Territory"
        )

    if enters_active_territory(
        "UNRESOLVED"
    ):
        errors.append(
            "UNRESOLVED material entered active Territory"
        )

    if enters_active_territory(
        "UNREACHABLE"
    ):
        errors.append(
            "UNREACHABLE material entered active Territory"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-C TERRAIN / TERRITORY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-C TERRAIN / TERRITORY: PASS"
    )
    print(
        "Terrain: ENCOUNTERED INFORMATIONAL STRUCTURE"
    )
    print(
        "Territory: NAVIGABLY REACHABLE GEOGRAPHY"
    )
    print(
        "Representation-sensitive Terrain: SAME OBJECT"
    )
    print(
        "UNRESOLVED / UNREACHABLE: OUTSIDE ACTIVE TERRITORY"
    )
    print(
        "Zone / Space / Transform / Cartography / Occupation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
