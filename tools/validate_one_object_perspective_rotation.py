#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "ONE_OBJECT_PERSPECTIVE_ROTATION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "one_object_perspective_rotation.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

INNER_VALIDATORS = [
    (
        "Canonical Room Object",
        "tools/validate_canonical_room_object_identity.py",
    ),
    (
        "Bounded Zone",
        "tools/validate_bounded_zone.py",
    ),
    (
        "Bounded Space",
        "tools/validate_bounded_space.py",
    ),
    (
        "Representation Transform",
        "tools/validate_representation_transform.py",
    ),
    (
        "Orientation / Coordinates",
        "tools/validate_orientation_coordinates.py",
    ),
    (
        "Cartography",
        "tools/validate_cartography.py",
    ),
    (
        "Stick / Contact Continuity",
        "tools/validate_stick_contact_continuity.py",
    ),
]


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def normalized(path):
    text = path.read_text(
        encoding="utf-8"
    )

    for token in (
        "**",
        "__",
        "`",
    ):
        text = text.replace(
            token,
            ""
        )

    return " ".join(
        text.split()
    )


def make_valid_record():
    object_id = (
        "sha512:"
        + "1" * 128
    )

    state_root = (
        "sha512:"
        + "2" * 128
    )

    provenance = [
        "provenance:origin:a",
        "provenance:evidence:a",
    ]

    exclusions = [
        "excluded:evidence:x",
        "excluded:claim:y",
    ]

    disagreement = [
        "disagreement:hypothesis:a-vs-b",
    ]

    perspectives = []

    for index, label in enumerate(
        (
            "ME",
            "YOU",
            "US_WE",
        ),
        start=1,
    ):
        perspectives.append(
            {
                "perspective_id":
                    f"perspective:{index}",

                "object_id":
                    object_id,

                "room_revision_id":
                    "revision:rotation:a",

                "room_state_root":
                    state_root,

                # Views MAY differ where separately governed.
                "authorized_view_root":
                    (
                        "sha512:"
                        + str(index + 2) * 128
                    ),

                "zone_reference":
                    f"zone:{label}",

                "space_reference":
                    f"space:{label}:active",

                "representation_transform_reference":
                    f"transform:{index}",

                "orientation_reference":
                    f"orientation:{index}",

                "coordinate_reference":
                    f"coordinate:{index}",

                "evidence_boundary_reference":
                    "boundary:rotation:a",

                "evidence_ceiling_reference":
                    "ceiling:rotation:a",

                "provenance_anchors":
                    list(provenance),

                "exclusion_references":
                    list(exclusions),

                "disagreement_references":
                    list(disagreement),
            }
        )

    transitions = []

    for source, destination in zip(
        perspectives,
        perspectives[1:],
    ):
        transitions.append(
            {
                "source_perspective_id":
                    source[
                        "perspective_id"
                    ],

                "destination_perspective_id":
                    destination[
                        "perspective_id"
                    ],

                "source_object_id":
                    source[
                        "object_id"
                    ],

                "destination_object_id":
                    destination[
                        "object_id"
                    ],

                "continuity_state":
                    "PRESERVED",
            }
        )

    return {
        "schema_version":
            "1.0",

        "validation_vector":
            "ONE_OBJECT_PERSPECTIVE_ROTATION",

        "object_id":
            object_id,

        "room_revision_id":
            "revision:rotation:a",

        "room_state_root":
            state_root,

        "evidence_boundary_reference":
            "boundary:rotation:a",

        "evidence_ceiling_reference":
            "ceiling:rotation:a",

        "provenance_anchors":
            provenance,

        "exclusion_references":
            exclusions,

        "disagreement_references":
            disagreement,

        "perspectives":
            perspectives,

        "stick_transitions":
            transitions,

        "branch_references":
            [],

        "passageway_references":
            [],

        "validation_disposition":
            "VALID",

        "failure_reasons":
            [],

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",
    }


def validate_record(record):
    errors = []

    if (
        record.get(
            "validation_vector"
        )
        != "ONE_OBJECT_PERSPECTIVE_ROTATION"
    ):
        errors.append(
            "wrong validation vector"
        )

    perspectives = record.get(
        "perspectives",
        []
    )

    if len(perspectives) < 3:
        errors.append(
            "one-object perspective rotation requires at least three perspectives"
        )

    expected_object = record.get(
        "object_id"
    )

    expected_revision = record.get(
        "room_revision_id"
    )

    expected_state = record.get(
        "room_state_root"
    )

    expected_boundary = record.get(
        "evidence_boundary_reference"
    )

    expected_ceiling = record.get(
        "evidence_ceiling_reference"
    )

    expected_provenance = set(
        record.get(
            "provenance_anchors",
            []
        )
    )

    expected_exclusions = set(
        record.get(
            "exclusion_references",
            []
        )
    )

    expected_disagreement = set(
        record.get(
            "disagreement_references",
            []
        )
    )

    perspective_ids = []

    for perspective in perspectives:
        pid = perspective.get(
            "perspective_id"
        )

        if not pid:
            errors.append(
                "perspective requires perspective_id"
            )
        else:
            perspective_ids.append(
                pid
            )

        if (
            perspective.get(
                "object_id"
            )
            != expected_object
        ):
            errors.append(
                "perspective rotation changed canonical object identity"
            )

        if (
            perspective.get(
                "room_revision_id"
            )
            != expected_revision
        ):
            errors.append(
                "pure perspective rotation changed Room revision"
            )

        if (
            perspective.get(
                "room_state_root"
            )
            != expected_state
        ):
            errors.append(
                "pure perspective rotation changed Room state root"
            )

        if (
            perspective.get(
                "evidence_boundary_reference"
            )
            != expected_boundary
        ):
            errors.append(
                "perspective rotation changed evidence boundary"
            )

        if (
            perspective.get(
                "evidence_ceiling_reference"
            )
            != expected_ceiling
        ):
            errors.append(
                "perspective rotation changed evidence ceiling"
            )

        if not perspective.get(
            "authorized_view_root"
        ):
            errors.append(
                "perspective requires Authorized View reference"
            )

        for field in (
            "zone_reference",
            "space_reference",
            "representation_transform_reference",
            "orientation_reference",
            "coordinate_reference",
        ):
            if not perspective.get(
                field
            ):
                errors.append(
                    f"perspective requires {field}"
                )

        if not expected_provenance.issubset(
            set(
                perspective.get(
                    "provenance_anchors",
                    []
                )
            )
        ):
            errors.append(
                "perspective rotation lost provenance"
            )

        if not expected_exclusions.issubset(
            set(
                perspective.get(
                    "exclusion_references",
                    []
                )
            )
        ):
            errors.append(
                "perspective rotation lost governing exclusions"
            )

        if not expected_disagreement.issubset(
            set(
                perspective.get(
                    "disagreement_references",
                    []
                )
            )
        ):
            errors.append(
                "perspective rotation erased disagreement"
            )

    if (
        len(perspective_ids)
        != len(
            set(
                perspective_ids
            )
        )
    ):
        errors.append(
            "perspective_id must be unique"
        )

    transitions = record.get(
        "stick_transitions",
        []
    )

    required_transition_count = max(
        0,
        len(perspectives) - 1
    )

    if (
        len(transitions)
        != required_transition_count
    ):
        errors.append(
            "perspective rotation requires exactly one Stick transition per adjacent move"
        )
    else:
        for index, transition in enumerate(
            transitions
        ):
            source = perspectives[
                index
            ]

            destination = perspectives[
                index + 1
            ]

            if (
                transition.get(
                    "source_perspective_id"
                )
                != source.get(
                    "perspective_id"
                )
                or transition.get(
                    "destination_perspective_id"
                )
                != destination.get(
                    "perspective_id"
                )
            ):
                errors.append(
                    "Stick transition ordering does not match perspective rotation"
                )

            if (
                transition.get(
                    "source_object_id"
                )
                != expected_object
                or transition.get(
                    "destination_object_id"
                )
                != expected_object
            ):
                errors.append(
                    "Stick transition does not preserve object identity"
                )

            if (
                transition.get(
                    "continuity_state"
                )
                != "PRESERVED"
            ):
                errors.append(
                    "Stick continuity is not PRESERVED"
                )

    if record.get(
        "branch_references"
    ):
        errors.append(
            "pure perspective rotation may not create branch semantics"
        )

    if record.get(
        "passageway_references"
    ):
        errors.append(
            "pure perspective rotation may not create Passageway semantics"
        )

    disposition = record.get(
        "validation_disposition"
    )

    if disposition not in {
        "VALID",
        "BLOCKED",
    }:
        errors.append(
            "invalid perspective-rotation validation disposition"
        )

    if (
        disposition == "BLOCKED"
        and not record.get(
            "failure_reasons"
        )
    ):
        errors.append(
            "BLOCKED perspective rotation requires failure reasons"
        )

    if (
        record.get(
            "authority_state"
        )
        != "NONE"
    ):
        errors.append(
            "R6-B authority state must remain NONE"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-B Human Gate state must remain ACTIVE"
        )

    return errors


def validate_inner_surfaces():
    errors = []

    for name, relative_path in INNER_VALIDATORS:
        path = ROOT / relative_path

        if not path.exists():
            errors.append(
                f"missing inner validator: {relative_path}"
            )
            continue

        result = subprocess.run(
            [
                sys.executable,
                str(path),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            errors.append(
                f"inner surface failed: {name}"
            )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-B contract"
        ),
        (
            SCHEMA,
            "R6-B schema"
        ),
        (
            R6A,
            "R6-A boundary contract"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    text = normalized(
        CONTRACT
    )

    locks = [
        "R6-B = One-Object Perspective Rotation.",
        "Turn one Room through multiple Zones and Spaces.",
        "Preserve identity.",
        "Preserve provenance.",
        "Preserve exclusions.",
        "Preserve evidence ceilings.",
        "Preserve disagreement.",
        "Turn the object.",
        "Do not clone the world.",
        "Perspective rotation is representation movement on one object.",
        "Different Zone != different Room.",
        "Different Space != different Room.",
        "Different orientation != different Room.",
        "Different rendering != different Room.",
        "ONE ROOM OBJECT.",
        "MANY DECLARED REPRESENTATIONS.",
        "ZERO SILENT CLONES.",
        "Perspective and Authorized View are not identical concepts.",
        "Perspective rotation itself does not grant broader access.",
        "Representation != authorization.",
        "Rotation != access expansion.",
        "Different view != different provenance history.",
        "Excluded != nonexistent.",
        "Excluded != admitted from another angle.",
        "Closer view != stronger evidence.",
        "More legible view != stronger evidence.",
        "Different angle != higher claim ceiling.",
        "Perspective convergence != evidence convergence.",
        "Representation agreement != analytical truth.",
        "Disagreement is preserved until evidence resolves it.",
        "Zone change != branch.",
        "A Space restricts operation.",
        "It does not fracture object identity.",
        "Transform != object mutation.",
        "Transform != evidence mutation.",
        "Transform != claim-ceiling promotion.",
        "Transform != branch.",
        "Orientation precedes reasoning.",
        "Coordinate change != identity change.",
        "Coordinate change != truth change.",
        "Perspective does not own Cartography.",
        "Representation does not own Cartography.",
        "Movement continuity != reconstruction.",
        "Perspective != branch.",
        "Perspective transition != inter-Room passage.",
        "State mutation != perspective rotation.",
        "VALID != analytical truth.",
        "VALID != promotion.",
        "VALID != authority.",
        "Fail closed.",
        "Do not repair the vector by cloning the Room.",
        "Perspective rotation MUST be established before orthogonal Room transition is treated as validated.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-C owns the next extended Validation and Audit vector.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-B lock: {lock}"
            )

    r6a = normalized(
        R6A
    )

    r6a_locks = [
        "PERSPECTIVE_ROTATION",
        "One-Object Perspective Rotation",
        "Turn the object.",
        "Do not clone the world.",
    ]

    for lock in r6a_locks:
        if lock not in r6a:
            errors.append(
                f"R6-A registry missing required R6-B vector binding: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-B schema JSON: {exc}"
        ]

    forbidden = {
        "branch_id",
        "new_room_id",
        "passageway_id",
        "genesis_manifest",
        "lifecycle_transition",
        "evidence_admission",
        "claim_ceiling_override",
        "execution_authorization",
        "canonical_promotion",
    }

    top_properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    leaked = (
        top_properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R6-B improperly absorbs non-rotation semantics: "
            + ", ".join(
                sorted(
                    leaked
                )
            )
        )

    errors.extend(
        validate_record(
            make_valid_record()
        )
    )

    # Compose live inner validators.
    errors.extend(
        validate_inner_surfaces()
    )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-B ONE-OBJECT PERSPECTIVE ROTATION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-B ONE-OBJECT PERSPECTIVE ROTATION: PASS"
    )
    print(
        "Canonical Room Object identity: PRESERVED"
    )
    print(
        "Multiple Zones / Spaces / transforms / orientations: EXERCISED"
    )
    print(
        "Provenance / exclusions / evidence ceiling: PRESERVED"
    )
    print(
        "Material disagreement: PRESERVED"
    )
    print(
        "Stick / contact continuity: PRESERVED"
    )
    print(
        "Branch / Passageway / distinct-object promotion: NOT INVOKED"
    )
    print(
        "Perspective -> access expansion: REJECTED"
    )
    print(
        "Perspective -> stronger claim: REJECTED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-C next extended validation vector: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
