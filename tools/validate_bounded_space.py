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
    / "BOUNDED_SPACE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "geography"
    / "bounded_space.schema.json"
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


def compute_space_id(
    object_id,
    representation_binding_mode,
    zone_id,
    direct_transform_reference,
    field,
    discipline,
    question_set,
    controls,
    capabilities,
    evidence_ceiling,
    allowed_mission,
    prohibited_assumptions,
    rendering_obligations
):
    preimage = {
        "object_id":
            object_id,
        "representation_binding_mode":
            representation_binding_mode,
        "zone_id":
            zone_id,
        "direct_transform_reference":
            direct_transform_reference,
        "field":
            field,
        "discipline":
            discipline,
        "question_set":
            question_set,
        "controls":
            controls,
        "capabilities":
            capabilities,
        "evidence_ceiling":
            evidence_ceiling,
        "allowed_mission":
            allowed_mission,
        "prohibited_assumptions":
            prohibited_assumptions,
        "rendering_obligations":
            rendering_obligations,
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


def validate_binding(space):
    errors = []

    mode = space.get(
        "representation_binding_mode"
    )

    zone_id = space.get(
        "zone_id"
    )

    direct = space.get(
        "direct_transform_reference"
    )

    if mode == "ZONE":
        if not zone_id:
            errors.append(
                "ZONE-bound Space requires zone_id"
            )

        if direct is not None:
            errors.append(
                "ZONE-bound Space must not carry direct transform reference"
            )

    elif mode == "DIRECT_TRANSFORM":
        if zone_id is not None:
            errors.append(
                "DIRECT_TRANSFORM Space must not carry zone_id"
            )

        if not direct:
            errors.append(
                "DIRECT_TRANSFORM Space requires transform reference"
            )

    else:
        errors.append(
            "invalid Space representation binding mode"
        )

    return errors


def validate_space(space):
    errors = []

    errors.extend(
        validate_binding(
            space
        )
    )

    expected_id = compute_space_id(
        space.get("object_id"),
        space.get("representation_binding_mode"),
        space.get("zone_id"),
        space.get("direct_transform_reference"),
        space.get("field"),
        space.get("discipline"),
        space.get("question_set"),
        space.get("controls"),
        space.get("capabilities"),
        space.get("evidence_ceiling"),
        space.get("allowed_mission"),
        space.get("prohibited_assumptions"),
        space.get("rendering_obligations"),
    )

    if (
        space.get("space_id")
        != expected_id
    ):
        errors.append(
            "space_id does not recompute from declared mission contract"
        )

    if space.get(
        "evidence_ceiling"
    ) in (
        None,
        "",
        {},
    ):
        errors.append(
            "Space evidence ceiling is undefined"
        )

    if not space.get(
        "allowed_mission"
    ):
        errors.append(
            "Space allowed mission is undefined"
        )

    return errors


def validate():
    errors = []

    if not CONTRACT.exists():
        errors.append(
            "missing R2-E Bounded Space contract"
        )

    if not SCHEMA.exists():
        errors.append(
            "missing Bounded Space schema"
        )

    if errors:
        return errors

    try:
        schema = load_schema()
    except Exception as exc:
        return [
            f"invalid R2-E schema JSON: {exc}"
        ]

    required = set(
        schema.get(
            "required",
            []
        )
    )

    expected = {
        "object_id",
        "space_id",
        "representation_binding_mode",
        "zone_id",
        "direct_transform_reference",
        "field",
        "discipline",
        "question_set",
        "controls",
        "capabilities",
        "evidence_ceiling",
        "allowed_mission",
        "prohibited_assumptions",
        "rendering_obligations",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Bounded Space missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    modes = set(
        schema
        .get("properties", {})
        .get(
            "representation_binding_mode",
            {}
        )
        .get("enum", [])
    )

    if modes != {
        "ZONE",
        "DIRECT_TRANSFORM",
    }:
        errors.append(
            "Space binding modes are not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "source_orientation",
        "target_orientation",
        "transform_id",
        "cartography_id",
        "stick_id",
        "occupation_id",
        "active_capability_id",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R2-E improperly absorbs downstream fields: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    required_locks = [
        "Zone != Space.",
        "Persistent representation frame != active mission surface.",
        "Space identity != object identity.",
        "A Space restricts operation.",
        "It does not fracture object identity.",
        "Capability != authority.",
        "Question != authority.",
        "Mission != reachability.",
        "Space observation != canonical write.",
        "Parallel missions != parallel worlds.",
        "No full Transform semantics yet.",
        "No Orientation yet.",
        "No Cartography yet.",
        "No Stick yet.",
        "No Occupation yet.",
    ]

    for lock in required_locks:
        if lock not in contract_text:
            errors.append(
                f"missing R2-E lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    zone_id = (
        "sha512:"
        + "2" * 128
    )

    space_id = compute_space_id(
        object_id,
        "ZONE",
        zone_id,
        None,
        "security",
        "audit",
        [
            "what changed?"
        ],
        [
            "control:a"
        ],
        [
            "capability:a"
        ],
        "CEILING:ZONE-BOUND",
        "bounded analysis",
        [
            "no unsupported attribution"
        ],
        [
            "preserve provenance"
        ]
    )

    if not SHA512_RE.fullmatch(
        space_id
    ):
        errors.append(
            "space_id is not canonical SHA-512"
        )

    changed = compute_space_id(
        object_id,
        "ZONE",
        zone_id,
        None,
        "security",
        "audit",
        [
            "what changed?",
            "why?"
        ],
        [
            "control:a"
        ],
        [
            "capability:a"
        ],
        "CEILING:ZONE-BOUND",
        "bounded analysis",
        [
            "no unsupported attribution"
        ],
        [
            "preserve provenance"
        ]
    )

    if space_id == changed:
        errors.append(
            "material Space mission change did not change space_id"
        )

    if space_id == object_id:
        errors.append(
            "Space identity collapsed into object identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-E BOUNDED SPACE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-E BOUNDED SPACE: PASS"
    )
    print(
        "Space: ACTIVE BOUNDED MISSION SURFACE"
    )
    print(
        "Zone / direct transform binding: EXPLICIT"
    )
    print(
        "Object identity: PRESERVED"
    )
    print(
        "Mission / questions / controls / capabilities / ceiling: BOUNDED"
    )
    print(
        "Transform / Orientation / Cartography / Stick / Occupation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
