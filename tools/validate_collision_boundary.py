#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys

from tools.collision_boundary import (
    CLEAN,
    COLLISION,
    UNRESOLVED_CONTEXT,
    AUTHORITY_STATE,
    HUMAN_GATE_STATE,
    analyze_collision_boundary,
    measurable_body_identity,
)

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "analysis"
    / "COLLISION_BOUNDARY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "analysis"
    / "collision_boundary.schema.json"
)


def normalized(path: Path) -> str:
    return " ".join(
        path.read_text(
            encoding="utf-8"
        ).replace("`", "").split()
    )


def validate() -> list[str]:
    errors = []

    for path in (
        CONTRACT,
        SCHEMA,
    ):
        if not path.exists():
            errors.append(
                f"missing: {path.relative_to(ROOT)}"
            )

    if errors:
        return errors

    try:
        schema = json.loads(
            SCHEMA.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        return [
            f"collision-boundary schema invalid: {exc}"
        ]

    contract = normalized(CONTRACT)

    required_markers = (
        "CLEAN",
        "COLLISION",
        "UNRESOLVED_CONTEXT",
        "UNRESOLVED_CONTEXT != CLEAN.",
        "Collision != anomaly.",
        "Collision != model error.",
        "Collision != malicious.",
        "Collision != benign.",
        "Hash != truth.",
        "Unknown remains unknown.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Collision analysis creates no authority.",
    )

    for marker in required_markers:
        if marker not in contract:
            errors.append(
                f"contract marker missing: {marker}"
            )

    properties = schema.get(
        "properties",
        {},
    )

    disposition = properties.get(
        "population_disposition",
        {},
    )

    if set(
        disposition.get(
            "enum",
            [],
        )
    ) != {
        CLEAN,
        COLLISION,
        UNRESOLVED_CONTEXT,
    }:
        errors.append(
            "schema population dispositions disagree"
        )

    if (
        properties.get(
            "authority_state",
            {},
        ).get("const")
        != "NONE"
    ):
        errors.append(
            "schema authority state must remain NONE"
        )

    if (
        properties.get(
            "human_gate_state",
            {},
        ).get("const")
        != "ACTIVE"
    ):
        errors.append(
            "schema Human Gate state must remain ACTIVE"
        )

    if AUTHORITY_STATE != "NONE":
        errors.append(
            "runtime authority state promoted"
        )

    if HUMAN_GATE_STATE != "ACTIVE":
        errors.append(
            "runtime Human Gate state changed"
        )

    return errors


def adversarial_checks() -> list[str]:
    errors = []

    surface = (
        "proto",
        "service",
        "src_port",
        "dst_port",
        "duration",
        "packets",
        "bytes",
    )

    base = {
        "member_reference": "a",
        "reviewed_label": "ARP",
        "proto": "udp",
        "service": "dns",
        "src_port": 5353,
        "dst_port": 5353,
        "duration": 0,
        "packets": 1,
        "bytes": 45,
    }

    # Target label MUST NOT enter measurable identity.
    try:
        measurable_body_identity(
            base,
            surface + ("reviewed_label",),
        )
    except ValueError:
        pass
    else:
        errors.append(
            "target label entered measurable identity"
        )

    # Row/member identity MUST NOT enter measurable identity.
    try:
        measurable_body_identity(
            base,
            surface + ("member_reference",),
        )
    except ValueError:
        pass
    else:
        errors.append(
            "member reference entered measurable identity"
        )

    # Missing measurable context MUST NOT silently become CLEAN.
    unresolved = dict(base)
    unresolved[
        "member_reference"
    ] = "unresolved"
    del unresolved["bytes"]

    result = analyze_collision_boundary(
        [unresolved],
        surface,
    )

    if (
        result.row_dispositions[0][
            "population_disposition"
        ]
        != UNRESOLVED_CONTEXT
    ):
        errors.append(
            "unresolved measurable body became CLEAN"
        )

    # Exact body with conflicting labels MUST become COLLISION.
    left = dict(base)

    right = dict(base)
    right[
        "member_reference"
    ] = "b"
    right[
        "reviewed_label"
    ] = "Thing_Speak"

    result = analyze_collision_boundary(
        [left, right],
        surface,
    )

    if result.collision_rows != 2:
        errors.append(
            "cross-label exact-body collision not detected"
        )

    if result.clean_rows != 0:
        errors.append(
            "collision member leaked into CLEAN population"
        )

    if result.supervised_member_references():
        errors.append(
            "collision member leaked into supervised denominator"
        )

    # Input ordering MUST NOT change collision identity.
    forward = analyze_collision_boundary(
        [left, right],
        surface,
    )

    reverse = analyze_collision_boundary(
        [right, left],
        surface,
    )

    if (
        forward.collision_groups[0].collision_group_id
        != reverse.collision_groups[0].collision_group_id
    ):
        errors.append(
            "collision identity depends on row order"
        )

    # Duplicate member references MUST fail closed.
    duplicate = dict(right)
    duplicate[
        "member_reference"
    ] = "a"

    try:
        analyze_collision_boundary(
            [left, duplicate],
            surface,
        )
    except ValueError:
        pass
    else:
        errors.append(
            "duplicate member reference accepted"
        )

    return errors


def main() -> int:
    errors = validate()
    errors.extend(
        adversarial_checks()
    )

    if errors:
        print(
            "AC-RTIOT-01 COLLISION BOUNDARY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "AC-RTIOT-01 COLLISION BOUNDARY: PASS"
    )
    print(
        "Population states: "
        "CLEAN / COLLISION / UNRESOLVED_CONTEXT"
    )
    print(
        "Canonical identity: SHA-512"
    )
    print(
        "Pre-split collision boundary: VERIFIED"
    )
    print(
        "Collision scoring exclusion: VERIFIED"
    )
    print(
        "Unresolved context fail-closed: VERIFIED"
    )
    print(
        "Order-independent group identity: VERIFIED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Disposition: AC_RTIOT_01_VALID"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
