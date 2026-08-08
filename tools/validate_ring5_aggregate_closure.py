#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "RING5_EXISTING_PIPELINE_INTEGRATION_AGGREGATE_CLOSURE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "ring5_aggregate_closure.schema.json"
)

RUNNER = (
    ROOT
    / "tools"
    / "validate_ring5.py"
)

SUBRING_CONTRACTS = [
    (
        "R5-A",
        ROOT
        / "contracts"
        / "pipeline"
        / "PIPELINE_INTEGRATION_BOUNDARY_EXISTING_SEMANTICS_LOCK.md"
    ),
    (
        "R5-B",
        ROOT
        / "contracts"
        / "pipeline"
        / "ROOM_BOUND_EVIDENCE_PMC_INTAKE_BINDING.md"
    ),
    (
        "R5-C",
        ROOT
        / "contracts"
        / "pipeline"
        / "PMC_CCR_CANDIDATE_COMMITMENT_LINEAGE.md"
    ),
    (
        "R5-D",
        ROOT
        / "contracts"
        / "pipeline"
        / "CCR_MC_RESPONSE_OUTPUT_ADMISSIBILITY_BINDING.md"
    ),
    (
        "R5-E",
        ROOT
        / "contracts"
        / "pipeline"
        / "MC_RAVEN_REPRESENTATION_REPORT_BINDING.md"
    ),
    (
        "R5-F",
        ROOT
        / "contracts"
        / "pipeline"
        / "RAVEN_HUMAN_GATE_PUBLICATION_ACTION_BOUNDARY.md"
    ),
    (
        "R5-G",
        ROOT
        / "contracts"
        / "pipeline"
        / "DECISION_OPTION_LINEAGE.md"
    ),
    (
        "R5-H",
        ROOT
        / "contracts"
        / "pipeline"
        / "REPORT_RENDERING_CONTRACT.md"
    ),
    (
        "R5-I",
        ROOT
        / "contracts"
        / "pipeline"
        / "PIPELINE_CROSS_STAGE_INTEGRITY_NO_RESPONSIBILITY_ABSORPTION.md"
    ),
]

COMPLETED_SUBRINGS = [
    "R5-A",
    "R5-B",
    "R5-C",
    "R5-D",
    "R5-E",
    "R5-F",
    "R5-G",
    "R5-H",
    "R5-I",
]

DEPENDENCY_RINGS = [
    "R1",
    "R2",
    "R3",
    "R4",
]

PIPELINE_ROUTE = [
    "ROOM_BOUND_EVIDENCE",
    "PMC_INTAKE",
    "PMC",
    "CCR",
    "MC",
    "RAVEN",
    "HUMAN_GATE",
]

COLLISION_STATES = [
    "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION",
    "MC_EPHEMERALITY_LINEAGE_COLLISION",
]


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_ring5_closure_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "ring5_closure_id"
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
    record = {
        "schema_version":
            "1.0",

        "native_version":
            "vTemporal.41.0",

        "implementation_identity":
            "v41 Complete",

        "ring":
            "R5-J",

        "completed_subrings":
            list(
                COMPLETED_SUBRINGS
            ),

        "dependency_rings":
            list(
                DEPENDENCY_RINGS
            ),

        "pipeline_route":
            list(
                PIPELINE_ROUTE
            ),

        "collision_states":
            list(
                COLLISION_STATES
            ),

        "ownership_separation_state":
            "PRESERVED",

        "authority_separation_state":
            "PRESERVED",

        "no_compression_out_state":
            "PRESERVED",

        "closure_disposition":
            "VALIDATED_CANDIDATE",

        "promotion_state":
            "CANDIDATE",

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",

        "blocking_reasons":
            [],

        "lineage_reference":
            "ring5:lineage:vTemporal.41.0",

        "provenance_route": [
            "R1",
            "R2",
            "R3",
            "R4",
            "R5-A",
            "R5-B",
            "R5-C",
            "R5-D",
            "R5-E",
            "R5-F",
            "R5-G",
            "R5-H",
            "R5-I",
            "R5-J",
        ],
    }

    record[
        "ring5_closure_id"
    ] = compute_ring5_closure_id(
        record
    )

    return record


def validate_record(record):
    errors = []

    if (
        record.get("ring5_closure_id")
        != compute_ring5_closure_id(record)
    ):
        errors.append(
            "ring5_closure_id does not recompute from record"
        )

    if (
        record.get("native_version")
        != "vTemporal.41.0"
    ):
        errors.append(
            "native version must remain vTemporal.41.0"
        )

    if (
        record.get("implementation_identity")
        != "v41 Complete"
    ):
        errors.append(
            "implementation identity must remain v41 Complete"
        )

    if (
        record.get("ring")
        != "R5-J"
    ):
        errors.append(
            "closure record ring must remain R5-J"
        )

    if (
        record.get("completed_subrings")
        != COMPLETED_SUBRINGS
    ):
        errors.append(
            "completed Ring 5 subring order is incomplete or changed"
        )

    if (
        record.get("dependency_rings")
        != DEPENDENCY_RINGS
    ):
        errors.append(
            "Ring 5 dependency ring set is incomplete or changed"
        )

    if (
        record.get("pipeline_route")
        != PIPELINE_ROUTE
    ):
        errors.append(
            "Ring 5 native pipeline route is incomplete or changed"
        )

    if (
        record.get("collision_states")
        != COLLISION_STATES
    ):
        errors.append(
            "Ring 5 collision set is incomplete or changed"
        )

    if (
        record.get("ownership_separation_state")
        != "PRESERVED"
    ):
        errors.append(
            "Ring 5 ownership separation must remain PRESERVED"
        )

    if (
        record.get("authority_separation_state")
        != "PRESERVED"
    ):
        errors.append(
            "Ring 5 authority separation must remain PRESERVED"
        )

    if (
        record.get("no_compression_out_state")
        != "PRESERVED"
    ):
        errors.append(
            "Ring 5 No Compression Out state must remain PRESERVED"
        )

    disposition = record.get(
        "closure_disposition"
    )

    if disposition not in {
        "VALIDATED_CANDIDATE",
        "BLOCKED",
    }:
        errors.append(
            "invalid Ring 5 closure disposition"
        )

    if (
        disposition == "BLOCKED"
        and not record.get(
            "blocking_reasons"
        )
    ):
        errors.append(
            "BLOCKED Ring 5 closure requires blocking reasons"
        )

    if (
        record.get("promotion_state")
        != "CANDIDATE"
    ):
        errors.append(
            "Ring 5 promotion_state must remain CANDIDATE"
        )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "Ring 5 authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "Ring 5 Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "lineage_reference"
    ):
        errors.append(
            "Ring 5 closure requires lineage_reference"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "Ring 5 closure requires provenance_route"
        )

    return errors


def validate_subring_surface():
    errors = []

    for ring, path in SUBRING_CONTRACTS:
        if not path.exists():
            errors.append(
                f"missing completed subring contract {ring}"
            )

    if errors:
        return errors

    surfaces = {
        ring: normalized(path)
        for ring, path in SUBRING_CONTRACTS
    }

    expected = {
        "R5-A": [
            "Integration != redefinition.",
            "Binding != ownership.",
            "Binding != authority.",
        ],
        "R5-B": [
            "Qualification precedes analysis.",
            "Coordinate reference != Cartography ownership.",
        ],
        "R5-C": [
            "PMC selects or denies.",
            "CCR records.",
        ],
        "R5-D": [
            "Native-v41 MC integration MUST receive a CCR reference.",
            "Receipt != MC memory.",
        ],
        "R5-E": [
            "Raven may not manufacture MC disposition.",
            "Raven cannot authorize publication.",
        ],
        "R5-F": [
            "Human Gate decision != execution.",
            "No default approval exists.",
        ],
        "R5-G": [
            "Decision option != decision.",
            "Decision option != approval.",
            "Decision option != execution.",
        ],
        "R5-H": [
            "Report != truth authority.",
            "Report != publication authority.",
            "Report != certification.",
        ],
        "R5-I": [
            "No stage may silently absorb another stage's responsibility.",
            "No Compression Out applies end-to-end.",
            "R5-J owns Ring 5 Aggregate Closure.",
        ],
    }

    for ring, locks in expected.items():
        surface = surfaces[
            ring
        ]

        for lock in locks:
            if (
                " ".join(
                    lock.split()
                )
                not in surface
            ):
                errors.append(
                    f"{ring} missing aggregate closure lock: {lock}"
                )

    return errors


def validate_runner_surface():
    errors = []

    if not RUNNER.exists():
        return [
            "missing Ring 5 aggregate runner"
        ]

    text = RUNNER.read_text(
        encoding="utf-8"
    )

    positions = []

    for ring in (
        "R5-A",
        "R5-B",
        "R5-C",
        "R5-D",
        "R5-E",
        "R5-F",
        "R5-G",
        "R5-H",
        "R5-I",
        "R5-J",
    ):
        marker = f'"{ring}"'

        position = text.find(
            marker
        )

        if position < 0:
            errors.append(
                f"Ring 5 aggregate runner missing {ring}"
            )
        else:
            positions.append(
                (
                    ring,
                    position,
                )
            )

    if len(positions) == 10:
        ordered = [
            ring
            for ring, _ in sorted(
                positions,
                key=lambda item: item[1]
            )
        ]

        expected = [
            "R5-A",
            "R5-B",
            "R5-C",
            "R5-D",
            "R5-E",
            "R5-F",
            "R5-G",
            "R5-H",
            "R5-I",
            "R5-J",
        ]

        if ordered != expected:
            errors.append(
                "Ring 5 aggregate runner subring order is invalid"
            )

    for dependency in (
        "1",
        "2",
        "3",
        "4",
    ):
        if (
            f"ring_number in ("
            not in text
            and f"validate_ring{dependency}.py"
            not in text
        ):
            errors.append(
                f"Ring 5 runner dependency surface does not expose Ring {dependency}"
            )

    if (
        "regenerate_version_references.py"
        not in text
    ):
        errors.append(
            "Ring 5 runner lost version-reference synchronization preflight"
        )

    if (
        'print("RING 5 RESULT: PASS")'
        not in text
    ):
        errors.append(
            "Ring 5 runner lost aggregate PASS receipt"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-J contract"
        ),
        (
            SCHEMA,
            "R5-J schema"
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
        "R5-J adds no new analytical primitive.",
        "R5-J adds no new pipeline stage.",
        "R5-J does not redefine any completed Ring 5 function.",
        "Closure != promotion.",
        "Validation != authority.",
        "Ring completion != canonical promotion.",
        "R5-J does not reopen Rings 1 through 4.",
        "Inner contradiction requires explicit reopen.",
        "Outer implementation defect requires outer repair.",
        "Validator defect requires validator repair.",
        "R5-A: COMPLETE.",
        "R5-B: COMPLETE.",
        "R5-C: COMPLETE.",
        "R5-D: COMPLETE.",
        "R5-E: COMPLETE.",
        "R5-F: COMPLETE.",
        "R5-G: COMPLETE.",
        "R5-H: COMPLETE.",
        "R5-I: COMPLETE.",
        "Pipeline shortcut != optimization.",
        "Transport != ownership.",
        "Convenience != ownership.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Human Gate approval != execution.",
        "Human authorization != autonomous Zervan authority.",
        "Stage transition != new Room.",
        "Evidence availability != evidence admission.",
        "Confidence != higher claim ceiling.",
        "Presentation quality != stronger evidence.",
        "Human approval != stronger evidence.",
        "Unknown remains unknown.",
        "Rejected != deleted.",
        "Unavailable != nonexistent.",
        "Conditional != admissible.",
        "Blocked != false.",
        "More information needed remains valid.",
        "No Compression Out applies.",
        "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION.",
        "MC_EPHEMERALITY_LINEAGE_COLLISION.",
        "Collision suppression is invalid.",
        "Surface collisions.",
        "Do not normalize them away.",
        "Report != truth authority.",
        "Report != publication authority.",
        "Report != certification.",
        "Rendered != published.",
        "No decision is inferred from silence.",
        "No default approval exists.",
        "Prior approval != standing approval.",
        "Option != decision.",
        "Option != authority.",
        "Option != approval.",
        "Option != execution.",
        "No hidden winner.",
        "Report identity != Room identity.",
        "Report identity != truth.",
        "Report validation != authority.",
        "Render success != authority.",
        "R5-J is closure only.",
        "Closure receipt != new system primitive.",
        "Receipt != truth.",
        "Receipt != authority.",
        "Receipt != promotion.",
        "VALIDATED_CANDIDATE != canonical.",
        "VALIDATED_CANDIDATE != promoted.",
        "VALIDATED_CANDIDATE != authority.",
        "VALIDATED_CANDIDATE != publication.",
        "Ring 5 closure does not promote Git main.",
        "Promotion remains Human-Gate-governed.",
        "Validation success != promotion.",
        "Commit success != promotion.",
        "Push success != promotion.",
        "Repository presence != promotion.",
        "Any required failure makes Ring 5 fail closed.",
        "No partial aggregate PASS.",
        "Ring 5 — Existing Pipeline Integration: COMPLETE.",
        "Closure state: VALIDATED_CANDIDATE.",
        "Native version: vTemporal.41.0.",
        "Implementation identity: v41 Complete.",
        "Promotion state: CANDIDATE.",
        "Authority: NONE.",
        "Human Gate: ACTIVE.",
        "This is a candidate implementation closure.",
        "It is not canonical promotion.",
        "Fail closed.",
        "Do not promote during closure.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R5-J lock: {lock}"
            )

    errors.extend(
        validate_subring_surface()
    )

    errors.extend(
        validate_runner_surface()
    )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-J schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "new_pipeline_stage",
        "new_analytical_primitive",
        "execution_authorization",
        "publication_execution",
        "canonical_promotion",
        "room_lifecycle_transition",
        "cartography_mutation",
        "evidence_boundary_override",
        "evidence_ceiling_override",
        "autonomous_authority",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-J improperly introduces closure-time responsibility: "
            + ", ".join(
                sorted(
                    leaked
                )
            )
        )

    record = make_valid_record()

    errors.extend(
        validate_record(
            record
        )
    )

    # --------------------------------------------------------
    # Missing subring
    # --------------------------------------------------------

    missing_subring = json.loads(
        json.dumps(
            record
        )
    )

    missing_subring[
        "completed_subrings"
    ].remove(
        "R5-I"
    )

    missing_subring[
        "ring5_closure_id"
    ] = compute_ring5_closure_id(
        missing_subring
    )

    if not any(
        "subring order is incomplete or changed"
        in error
        for error in validate_record(
            missing_subring
        )
    ):
        errors.append(
            "R5-J incorrectly permitted incomplete subring closure"
        )

    # --------------------------------------------------------
    # Route drift
    # --------------------------------------------------------

    route_drift = json.loads(
        json.dumps(
            record
        )
    )

    route_drift[
        "pipeline_route"
    ] = [
        "ROOM_BOUND_EVIDENCE",
        "PMC_INTAKE",
        "PMC",
        "MC",
        "RAVEN",
        "HUMAN_GATE",
    ]

    route_drift[
        "ring5_closure_id"
    ] = compute_ring5_closure_id(
        route_drift
    )

    if not any(
        "pipeline route is incomplete or changed"
        in error
        for error in validate_record(
            route_drift
        )
    ):
        errors.append(
            "R5-J incorrectly permitted aggregate CCR bypass"
        )

    # --------------------------------------------------------
    # Collision suppression
    # --------------------------------------------------------

    collision_suppression = json.loads(
        json.dumps(
            record
        )
    )

    collision_suppression[
        "collision_states"
    ] = [
        "INTERFACE_COLLISION_REQUIRING_CCR_PRESERVATION"
    ]

    collision_suppression[
        "ring5_closure_id"
    ] = compute_ring5_closure_id(
        collision_suppression
    )

    if not any(
        "collision set is incomplete or changed"
        in error
        for error in validate_record(
            collision_suppression
        )
    ):
        errors.append(
            "R5-J incorrectly permitted collision suppression"
        )

    # --------------------------------------------------------
    # Promotion
    # --------------------------------------------------------

    promoted = json.loads(
        json.dumps(
            record
        )
    )

    promoted[
        "promotion_state"
    ] = "CANONICAL"

    promoted[
        "ring5_closure_id"
    ] = compute_ring5_closure_id(
        promoted
    )

    if not any(
        "promotion_state must remain CANDIDATE"
        in error
        for error in validate_record(
            promoted
        )
    ):
        errors.append(
            "R5-J incorrectly permitted closure-time promotion"
        )

    # --------------------------------------------------------
    # Authority promotion
    # --------------------------------------------------------

    autonomous = json.loads(
        json.dumps(
            record
        )
    )

    autonomous[
        "authority_state"
    ] = "AUTONOMOUS"

    autonomous[
        "ring5_closure_id"
    ] = compute_ring5_closure_id(
        autonomous
    )

    if not any(
        "authority_state must remain NONE"
        in error
        for error in validate_record(
            autonomous
        )
    ):
        errors.append(
            "R5-J incorrectly permitted autonomous authority"
        )

    # --------------------------------------------------------
    # Human Gate removal
    # --------------------------------------------------------

    no_gate = json.loads(
        json.dumps(
            record
        )
    )

    no_gate[
        "human_gate_state"
    ] = "DISABLED"

    no_gate[
        "ring5_closure_id"
    ] = compute_ring5_closure_id(
        no_gate
    )

    if not any(
        "Human Gate state must remain ACTIVE"
        in error
        for error in validate_record(
            no_gate
        )
    ):
        errors.append(
            "R5-J incorrectly permitted Human Gate removal"
        )

    # --------------------------------------------------------
    # BLOCKED must explain itself
    # --------------------------------------------------------

    blocked = json.loads(
        json.dumps(
            record
        )
    )

    blocked[
        "closure_disposition"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = []

    blocked[
        "ring5_closure_id"
    ] = compute_ring5_closure_id(
        blocked
    )

    if not any(
        "BLOCKED Ring 5 closure requires blocking reasons"
        in error
        for error in validate_record(
            blocked
        )
    ):
        errors.append(
            "R5-J incorrectly permitted unexplained BLOCKED closure"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-J RING 5 EXISTING PIPELINE INTEGRATION "
            "AGGREGATE CLOSURE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-J RING 5 EXISTING PIPELINE INTEGRATION "
        "AGGREGATE CLOSURE: PASS"
    )
    print(
        "R5-A -> R5-I implementation surface: COMPLETE"
    )
    print(
        "Room-Bound Evidence -> PMC -> CCR -> MC -> Raven -> Human Gate: LOCKED"
    )
    print(
        "Decision Option / Report lineage: BOUND"
    )
    print(
        "Ownership / authority separation: PRESERVED"
    )
    print(
        "Known Ring 5 collisions: SURFACED"
    )
    print(
        "No Compression Out / lineage / provenance: PRESERVED"
    )
    print(
        "Closure disposition: VALIDATED_CANDIDATE"
    )
    print(
        "Promotion state: CANDIDATE"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "Canonical promotion: NOT PERFORMED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
