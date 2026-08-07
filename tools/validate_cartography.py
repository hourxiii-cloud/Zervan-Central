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
    / "CARTOGRAPHY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "cartography_record.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

DOWNSTREAM_REFERENCE_FIELDS = {
    "capability_position_references",
    "collapse_boundary_references",
    "passageway_references",
    "propagation_vector_references",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_cartography_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "cartography_id"
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


def validate_cartography(record):
    errors = []

    expected = compute_cartography_id(
        record
    )

    if (
        record.get("cartography_id")
        != expected
    ):
        errors.append(
            "cartography_id does not recompute from declared Cartography"
        )

    if not record.get(
        "object_id"
    ):
        errors.append(
            "Cartography object_id is undefined"
        )

    for field in (
        "object_topology",
        "room_geometry",
        "provenance_anchors",
        "invariant_anchors",
        "return_routes",
    ):
        if record.get(field) in (
            None,
            {},
            [],
        ):
            errors.append(
                f"{field} is undefined or empty"
            )

    return errors


def validate():
    errors = []

    if not CONTRACT.exists():
        errors.append(
            "missing R2-H Cartography contract"
        )

    if not SCHEMA.exists():
        errors.append(
            "missing Cartography Record schema"
        )

    if errors:
        return errors

    try:
        schema = load_schema()
    except Exception as exc:
        return [
            f"invalid R2-H schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "cartography_id",
        "object_id",
        "object_topology",
        "room_geometry",
        "zone_references",
        "transform_references",
        "space_references",
        "orientation_references",
        "terrain_references",
        "territory_references",
        "provenance_anchors",
        "evidence_boundaries",
        "evidence_ceilings",
        "stable_regions",
        "uncertainty_frontiers",
        "deformation_regions",
        "invariant_anchors",
        "return_routes",
        "perspective_overlays",
        "evolution_references",
        "capability_position_references",
        "collapse_boundary_references",
        "passageway_references",
        "propagation_vector_references",
        "recorded_at",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Cartography Record missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    # Downstream objects may be referenced here because the source explicitly
    # requires Cartography to preserve them. Their semantics must not leak in.
    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden_semantic_fields = {
        "stick_id",
        "occupation_id",
        "occupant_id",
        "passageway_state",
        "passage_authorization",
        "collapse_operation",
        "propagation_execution",
    }

    leaked = (
        properties
        & forbidden_semantic_fields
    )

    if leaked:
        errors.append(
            "R2-H improperly defines downstream semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    if not DOWNSTREAM_REFERENCE_FIELDS.issubset(
        properties
    ):
        errors.append(
            "Cartography does not preserve all source-required "
            "downstream reference classes"
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    normalized_contract_text = " ".join(
        contract_text.split()
    )

    locks = [
        "Analysis produces understanding.",
        "Cartography preserves understanding as navigable geometry without cloning the object.",
        "Cartography identity != object identity.",
        "Map != Room Object.",
        "Zone difference != separate map of reality.",
        "Parallel missions != parallel worlds.",
        "Map presence != reachability.",
        "Displayed != reachable.",
        "Unknown remains unknown.",
        "Evolution != overwrite.",
        "Renderer != geometry.",
        "Vocabulary != topology.",
        "Opaque downstream reference != downstream semantics.",
        "Cartography != Stick.",
        "Mapped position != occupied position.",
        "No Stick yet.",
        "No Passageway semantics yet.",
        "No Occupation semantics yet.",
    ]

    for lock in locks:
        normalized_lock = " ".join(
            lock.split()
        )

        if normalized_lock not in normalized_contract_text:
            errors.append(
                f"missing R2-H lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    probe = {
        "schema_version": "1.0",
        "object_id": object_id,
        "object_topology": {
            "nodes": ["room"],
            "edges": [],
        },
        "room_geometry": {
            "coordinate_system": "analytical",
        },
        "zone_references": [
            "zone:a"
        ],
        "transform_references": [
            "transform:a"
        ],
        "space_references": [
            "space:a"
        ],
        "orientation_references": [
            "orientation:a"
        ],
        "terrain_references": [
            "terrain:a"
        ],
        "territory_references": [
            "territory:a"
        ],
        "provenance_anchors": [
            "provenance:a"
        ],
        "evidence_boundaries": [
            {
                "reference": "boundary:a"
            }
        ],
        "evidence_ceilings": [
            "CEILING:A"
        ],
        "stable_regions": [
            {
                "reference": "stable:a"
            }
        ],
        "uncertainty_frontiers": [
            {
                "reference": "uncertain:a"
            }
        ],
        "deformation_regions": [
            {
                "reference": "deformation:a"
            }
        ],
        "invariant_anchors": [
            object_id,
            "origin:a",
        ],
        "return_routes": [
            {
                "reference": "return:a"
            }
        ],
        "perspective_overlays": [
            {
                "reference": "overlay:a"
            }
        ],
        "evolution_references": [
            "cartography:prior"
        ],
        "capability_position_references": [],
        "collapse_boundary_references": [],
        "passageway_references": [],
        "propagation_vector_references": [],
        "recorded_at":
            "2026-08-07T18:51:00-04:00",
    }

    probe[
        "cartography_id"
    ] = compute_cartography_id(
        probe
    )

    if not SHA512_RE.fullmatch(
        probe["cartography_id"]
    ):
        errors.append(
            "cartography_id is not canonical SHA-512"
        )

    changed = dict(
        probe
    )

    changed[
        "room_geometry"
    ] = {
        "coordinate_system":
            "analytical",
        "new_supported_region":
            "region:b",
    }

    changed[
        "cartography_id"
    ] = compute_cartography_id(
        changed
    )

    if (
        probe["cartography_id"]
        == changed["cartography_id"]
    ):
        errors.append(
            "material Cartography change did not change cartography_id"
        )

    if (
        probe["cartography_id"]
        == object_id
    ):
        errors.append(
            "Cartography identity collapsed into object identity"
        )

    if validate_cartography(
        probe
    ):
        errors.extend(
            validate_cartography(
                probe
            )
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-H ANALYTICAL CARTOGRAPHY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-H ANALYTICAL CARTOGRAPHY: PASS"
    )
    print(
        "Understanding -> navigable geometry: PRESERVED"
    )
    print(
        "One object / same Cartography / bounded overlays: LOCKED"
    )
    print(
        "Topology / geometry / transforms / missions / orientation: PRESERVED"
    )
    print(
        "Evidence / uncertainty / deformation / return routes: PRESERVED"
    )
    print(
        "Stick / Passageway / Occupation semantics: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
