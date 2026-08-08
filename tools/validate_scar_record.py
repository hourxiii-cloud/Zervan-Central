#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "runtime"
    / "SCAR_RECORD.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "runtime"
    / "scar_record.schema.json"
)

R4F = (
    ROOT
    / "tools"
    / "validate_replay_envelope.py"
)

PERSISTENCE = {
    "ACTIVE",
    "HISTORICAL",
    "UNRESOLVED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_scar_record_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "scar_record_id"
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


def validate_scar(record):
    errors = []

    if (
        record.get("scar_record_id")
        != compute_scar_record_id(record)
    ):
        errors.append(
            "scar_record_id does not recompute from Scar Record"
        )

    if record.get(
        "effect_persistence"
    ) not in PERSISTENCE:
        errors.append(
            "invalid Scar effect persistence"
        )

    for field in (
        "object_id",
        "terrain_reference",
        "affected_movement_references",
        "effect_evidence_references",
        "effect_description",
        "observational_coordinate",
        "occupied_zone_reference",
        "occupied_space_reference",
        "capability_route_references",
        "evidence_boundary",
        "evidence_ceiling",
        "cartography_reference",
        "stick_reference",
        "effect_persistence",
        "provenance_route",
        "governance_reference",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Scar Record requires {field}"
            )

    movement = set(
        record.get(
            "affected_movement_references",
            []
        )
    )

    route = set(
        record.get(
            "capability_route_references",
            []
        )
    )

    if movement and route and not (
        movement & route
    ):
        errors.append(
            "Scar affected movement must remain attributable "
            "to preserved capability route"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R4-G Scar Record contract"
        ),
        (
            SCHEMA,
            "R4-G Scar Record schema"
        ),
        (
            R4F,
            "R4-F Replay Envelope validator"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    r4f = subprocess.run(
        [
            sys.executable,
            str(R4F),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if r4f.returncode != 0:
        errors.append(
            "R4-F dependency validation failed"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-G schema JSON: {exc}"
        ]

    persistence = set(
        schema
        .get("properties", {})
        .get("effect_persistence", {})
        .get("enum", [])
    )

    if persistence != PERSISTENCE:
        errors.append(
            "R4-G effect persistence vocabulary is not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "scar_replay_id",
        "scar_replay_action",
        "selected_future_route",
        "automatic_reflight",
        "new_object_id",
        "lifecycle_transition_id",
        "publication_authorization",
        "canonical_promotion",
        "confidence_score",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R4-G improperly absorbs Scar Replay, lifecycle, "
            "authority, or confidence semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    normalized = " ".join(
        CONTRACT.read_text(
            encoding="utf-8"
        ).split()
    )

    locks = [
        "A Scar is evidence that Terrain has previously affected movement.",
        "Terrain alone is not a Scar.",
        "Movement alone is not a Scar.",
        "Evidence alone is not a Scar.",
        "The relationship is the Scar.",
        "Scar != warning label.",
        "Scar != confidence score.",
        "Scar != conclusion.",
        "Scar != new Room.",
        "Implementation structure != new doctrine.",
        "Scar Record identity is not Room Object identity.",
        "Scar Record identity is not Terrain identity.",
        "Scar Record identity is not Replay Envelope identity.",
        "Historical difficulty != distinct object.",
        "Prior disturbance != distinct object.",
        "Scar != branch.",
        "Scar != Terrain.",
        "A Scar cannot be created from hypothetical movement.",
        "Prior movement MUST be attributable.",
        "Every Scar MUST contain non-empty effect evidence.",
        "The evidence determines what may be claimed.",
        "Scar existence does not raise the evidence ceiling.",
        "Effect description != attribution beyond evidence.",
        "Scar coordinate != new Origin.",
        "Scar coordinate != reconstructed approximation.",
        "Representation != truth authority.",
        "Scar MUST NOT reduce movement history to only a final finding.",
        "Scar != Restriction.",
        "Scar != Constriction.",
        "Scar != Collapse.",
        "Finding != Scar.",
        "Scar != final answer.",
        "Scar != evidence-boundary expansion.",
        "Scar != confidence promotion.",
        "Scar != certainty.",
        "Scar != truth certification.",
        "Historical effect remains attributable even if later evidence changes current understanding.",
        "Scar MUST preserve the Stick.",
        "Scar MUST NOT sever analytical continuity.",
        "Replay may expose a Scar.",
        "Replay does not manufacture a Scar.",
        "Persistence != truth authority.",
        "Persistence != lifecycle state.",
        "Unknown remains unknown.",
        "Scar is not merely metadata.",
        "Narrative concern != Scar.",
        "Past effect != guaranteed future effect.",
        "Signal != Scar.",
        "Score != Scar.",
        "Confidence != Scar.",
        "Generalization requires evidence.",
        "Scar is evidence-bearing state, not governing authority.",
        "Scar != Human Gate decision.",
        "Scar != lifecycle transition.",
        "Scar existence alone does not automatically authorize Reflight.",
        "Historical effect != current Reflight trigger.",
        "R4-H owns Scar Replay.",
        "Scar Record != publication record.",
        "No Scar Replay execution semantics yet.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in normalized
        ):
            errors.append(
                f"missing R4-G lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    scar = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "terrain_reference":
            "terrain:scar:a",
        "affected_movement_references": [
            "movement:a"
        ],
        "effect_evidence_references": [
            "evidence:movement-effect:a"
        ],
        "effect_description": [
            "terrain contact forced movement from route:a "
            "into a bounded alternate analytical route"
        ],
        "observational_coordinate": {
            "coordinate": "scar:a"
        },
        "question_contract_reference":
            "question-contract:a",
        "inquiry_envelope_reference":
            "inquiry-envelope:a",
        "occupied_zone_reference":
            "zone:a",
        "occupied_space_reference":
            "space:a",
        "transform_references": [
            "transform:a"
        ],
        "capability_route_references": [
            "movement:a",
            "route:a"
        ],
        "restriction_constriction_references": [
            "restriction:a"
        ],
        "collapse_boundary_references": [
            "collapse:a"
        ],
        "finding_references": [
            "finding:a"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "replay_envelope_reference":
            "replay:a",
        "effect_persistence":
            "HISTORICAL",
        "unresolved_implications": [
            "future recurrence remains unproven"
        ],
        "provenance_route": [
            object_id,
            "terrain:scar:a",
            "movement:a",
            "evidence:movement-effect:a",
            "cartography:a",
            "stick:a"
        ],
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "recorded_at":
            "2026-08-07T20:52:00-04:00",
    }

    scar[
        "scar_record_id"
    ] = compute_scar_record_id(
        scar
    )

    errors.extend(
        validate_scar(
            scar
        )
    )

    no_terrain = dict(
        scar
    )

    no_terrain[
        "terrain_reference"
    ] = ""

    no_terrain[
        "scar_record_id"
    ] = compute_scar_record_id(
        no_terrain
    )

    terrain_errors = validate_scar(
        no_terrain
    )

    if not any(
        "terrain_reference"
        in error
        for error in terrain_errors
    ):
        errors.append(
            "R4-G incorrectly permitted Scar without Terrain"
        )

    no_movement = dict(
        scar
    )

    no_movement[
        "affected_movement_references"
    ] = []

    no_movement[
        "scar_record_id"
    ] = compute_scar_record_id(
        no_movement
    )

    movement_errors = validate_scar(
        no_movement
    )

    if not any(
        "affected_movement_references"
        in error
        for error in movement_errors
    ):
        errors.append(
            "R4-G incorrectly permitted Scar without movement"
        )

    no_evidence = dict(
        scar
    )

    no_evidence[
        "effect_evidence_references"
    ] = []

    no_evidence[
        "scar_record_id"
    ] = compute_scar_record_id(
        no_evidence
    )

    evidence_errors = validate_scar(
        no_evidence
    )

    if not any(
        "effect_evidence_references"
        in error
        for error in evidence_errors
    ):
        errors.append(
            "R4-G incorrectly permitted Scar without effect evidence"
        )

    broken_route = dict(
        scar
    )

    broken_route[
        "capability_route_references"
    ] = [
        "route:unrelated"
    ]

    broken_route[
        "scar_record_id"
    ] = compute_scar_record_id(
        broken_route
    )

    route_errors = validate_scar(
        broken_route
    )

    if not any(
        "attributable"
        in error
        for error in route_errors
    ):
        errors.append(
            "R4-G incorrectly permitted movement detached "
            "from capability route"
        )

    changed = dict(
        scar
    )

    changed[
        "effect_description"
    ] = [
        "different attributable movement effect"
    ]

    changed[
        "scar_record_id"
    ] = compute_scar_record_id(
        changed
    )

    if (
        changed[
            "scar_record_id"
        ]
        == scar[
            "scar_record_id"
        ]
    ):
        errors.append(
            "material Scar Record change did not change identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-G SCAR RECORD: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-G SCAR RECORD: PASS"
    )
    print(
        "Terrain + prior movement + effect evidence: REQUIRED"
    )
    print(
        "Historical coordinate / representation / capability route: PRESERVED"
    )
    print(
        "Evidence boundary / ceiling / Cartography / Stick: PRESERVED"
    )
    print(
        "Warning-label / confidence-score substitution: REJECTED"
    )
    print(
        "Scar != Reflight / lifecycle / publication authority: LOCKED"
    )
    print(
        "Scar Replay execution: DEFERRED TO R4-H"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
