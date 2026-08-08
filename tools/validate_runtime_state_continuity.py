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
    / "RUNTIME_STATE_CONTINUITY_CROSS_OPERATION_INTEGRITY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "runtime"
    / "runtime_state_continuity_record.schema.json"
)

R4H = (
    ROOT
    / "tools"
    / "validate_scar_replay.py"
)

OPERATIONS = [
    "R4-A",
    "R4-B",
    "R4-C",
    "R4-D",
    "R4-E",
    "R4-F",
    "R4-G",
    "R4-H",
]

STATUS = {
    "VALID",
    "BLOCKED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_continuity_record_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "continuity_record_id"
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


def validate_record(record):
    errors = []

    if (
        record.get("continuity_record_id")
        != compute_continuity_record_id(record)
    ):
        errors.append(
            "continuity_record_id does not recompute from record"
        )

    if record.get(
        "continuity_status"
    ) not in STATUS:
        errors.append(
            "invalid continuity status"
        )

    for field in (
        "object_id",
        "operation_chain",
        "room_state_reference",
        "representation_state_reference",
        "execution_state_reference",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "cartography_reference",
        "stick_reference",
        "lineage_reference",
        "provenance_route",
        "continuity_status",
        "governance_reference",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Runtime-State Continuity Record requires {field}"
            )

    if (
        record.get("continuity_status")
        == "BLOCKED"
        and not record.get(
            "blocking_reasons"
        )
    ):
        errors.append(
            "BLOCKED continuity record requires blocking reasons"
        )

    room_state = record.get(
        "room_state_reference"
    )

    representation_state = record.get(
        "representation_state_reference"
    )

    execution_state = record.get(
        "execution_state_reference"
    )

    state_refs = [
        room_state,
        representation_state,
        execution_state,
    ]

    if (
        all(state_refs)
        and len(set(state_refs)) != 3
    ):
        errors.append(
            "Room, representation, and execution state references "
            "must remain distinct"
        )

    chain = record.get(
        "operation_chain",
        []
    )

    operations = [
        item.get("operation")
        for item in chain
        if isinstance(item, dict)
    ]

    if len(operations) != len(set(operations)):
        errors.append(
            "runtime operation chain contains duplicate operation identifier"
        )

    indexes = []

    for operation in operations:
        if operation not in OPERATIONS:
            errors.append(
                f"unknown runtime operation {operation}"
            )
            continue

        indexes.append(
            OPERATIONS.index(operation)
        )

    if indexes != sorted(indexes):
        errors.append(
            "runtime operations are out of canonical order"
        )

    object_id = record.get(
        "object_id"
    )

    for item in chain:
        if not isinstance(item, dict):
            errors.append(
                "runtime operation binding must be an object"
            )
            continue

        if item.get(
            "object_id"
        ) != object_id:
            errors.append(
                "runtime operation object identity mismatch"
            )

        for field in (
            "artifact_reference",
            "evidence_boundary_reference",
            "evidence_ceiling_reference",
            "lineage_reference",
            "provenance_reference",
        ):
            if item.get(field) in (
                None,
                "",
            ):
                errors.append(
                    f"runtime operation binding requires {field}"
                )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R4-I continuity contract"
        ),
        (
            SCHEMA,
            "R4-I continuity schema"
        ),
        (
            R4H,
            "R4-H Scar Replay validator"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    r4h = subprocess.run(
        [
            sys.executable,
            str(R4H),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if r4h.returncode != 0:
        errors.append(
            "R4-H dependency validation failed"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-I schema JSON: {exc}"
        ]

    schema_ops = set(
        schema
        ["properties"]
        ["operation_chain"]
        ["items"]
        ["properties"]
        ["operation"]
        ["enum"]
    )

    if schema_ops != set(OPERATIONS):
        errors.append(
            "R4-I operation vocabulary does not match R4-A through R4-H"
        )

    schema_status = set(
        schema
        ["properties"]
        ["continuity_status"]
        ["enum"]
    )

    if schema_status != STATUS:
        errors.append(
            "R4-I continuity status vocabulary is not locked"
        )

    forbidden = {
        "new_object_id",
        "new_origin_id",
        "lifecycle_transition_id",
        "reflight_execution_id",
        "publication_authorization",
        "canonical_promotion",
        "ownership_transfer",
        "full_payload_hydration",
    }

    leaked = (
        set(
            schema.get(
                "properties",
                {}
            )
        )
        & forbidden
    )

    if leaked:
        errors.append(
            "R4-I improperly absorbs object creation, lifecycle, "
            "execution, publication, or ownership semantics: "
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
        "Operation PASS != chain PASS.",
        "Implementation structure != new doctrine.",
        "Runtime change != object replacement.",
        "Room state != representation state.",
        "Room state != execution state.",
        "Representation state != execution state.",
        "A transition in one domain does not silently mutate another domain.",
        "Operations MUST NOT appear out of canonical order.",
        "Ordering != mandatory execution of every operation.",
        "one chain = one Room Object.",
        "Object mismatch = continuity failure.",
        "Runtime operation != genesis.",
        "Representation change != Room replacement.",
        "No silent default substitution.",
        "Approximate reconstruction is not continuity.",
        "Stick break = continuity failure.",
        "No runtime operation may silently broaden historical evidence access.",
        "Boundary change != retroactive evidence use.",
        "Runtime continuity != retrospective promotion.",
        "Landing does not undo narrowing.",
        "Closure does not undo narrowing.",
        "Replay does not erase narrowing.",
        "Collapse history survives Landing, Closure, Replay, Scar, and Scar Replay.",
        "Landing stops movement without ending occupation.",
        "Trigger != execution.",
        "Closure does not destroy Replay capability.",
        "Replay reconstructing an approximation = continuity failure.",
        "Scar does not replace the underlying history.",
        "Challenge does not delete history.",
        "Ignore-with-evidence does not delete history.",
        "Continue does not bypass Reflight Trigger.",
        "Branch does not manufacture distinct-object identity.",
        "No Compression Out applies to provenance history.",
        "A chain that cannot identify its historical route is not continuous.",
        "Runtime operations do not accumulate authority merely through sequence.",
        "Technical success != governing authority.",
        "Composition != ownership collapse.",
        "State-domain conflation is a constitutional runtime defect.",
        "VALID != analytical truth.",
        "VALID != canonical promotion.",
        "BLOCKED != nonexistent Room.",
        "Do not guess the missing link.",
        "Do not reconstruct an approximate link.",
        "Do not silently repair history.",
        "Surface the break.",
        "R4-J owns aggregate Ring 4 closure.",
        "R4-I PASS is necessary but not sufficient for Ring 4 aggregate closure.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in normalized
        ):
            errors.append(
                f"missing R4-I lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    chain = []

    for operation in OPERATIONS:
        chain.append(
            {
                "operation":
                    operation,
                "artifact_reference":
                    f"artifact:{operation.lower()}",
                "object_id":
                    object_id,
                "input_coordinate_reference":
                    f"coordinate:{operation.lower()}:in",
                "output_coordinate_reference":
                    f"coordinate:{operation.lower()}:out",
                "evidence_boundary_reference":
                    "boundary:a",
                "evidence_ceiling_reference":
                    "ceiling:a",
                "lineage_reference":
                    "lineage:a",
                "provenance_reference":
                    f"provenance:{operation.lower()}",
            }
        )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "operation_chain":
            chain,
        "room_state_reference":
            "room-state:a",
        "representation_state_reference":
            "representation-state:a",
        "execution_state_reference":
            "execution-state:a",
        "evidence_boundary_reference":
            "boundary:a",
        "evidence_ceiling_reference":
            "ceiling:a",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "lineage_reference":
            "lineage:a",
        "provenance_route": [
            object_id,
            "lineage:a",
            "cartography:a",
            "stick:a"
        ],
        "continuity_status":
            "VALID",
        "blocking_reasons": [],
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "validated_at":
            "2026-08-07T21:02:00-04:00",
    }

    record[
        "continuity_record_id"
    ] = compute_continuity_record_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    # --------------------------------------------------------
    # Object identity fracture must fail.
    # --------------------------------------------------------

    fractured = json.loads(
        json.dumps(record)
    )

    fractured[
        "operation_chain"
    ][4][
        "object_id"
    ] = (
        "sha512:"
        + "2" * 128
    )

    fractured[
        "continuity_record_id"
    ] = compute_continuity_record_id(
        fractured
    )

    fractured_errors = validate_record(
        fractured
    )

    if not any(
        "object identity mismatch"
        in error
        for error in fractured_errors
    ):
        errors.append(
            "R4-I incorrectly permitted cross-operation object identity fracture"
        )

    # --------------------------------------------------------
    # Out-of-order operation must fail.
    # --------------------------------------------------------

    out_of_order = json.loads(
        json.dumps(record)
    )

    out_of_order[
        "operation_chain"
    ][2], out_of_order[
        "operation_chain"
    ][3] = (
        out_of_order[
            "operation_chain"
        ][3],
        out_of_order[
            "operation_chain"
        ][2],
    )

    out_of_order[
        "continuity_record_id"
    ] = compute_continuity_record_id(
        out_of_order
    )

    order_errors = validate_record(
        out_of_order
    )

    if not any(
        "out of canonical order"
        in error
        for error in order_errors
    ):
        errors.append(
            "R4-I incorrectly permitted out-of-order runtime chain"
        )

    # --------------------------------------------------------
    # Duplicate operation must fail.
    # --------------------------------------------------------

    duplicate = json.loads(
        json.dumps(record)
    )

    duplicate[
        "operation_chain"
    ][7][
        "operation"
    ] = "R4-G"

    duplicate[
        "continuity_record_id"
    ] = compute_continuity_record_id(
        duplicate
    )

    duplicate_errors = validate_record(
        duplicate
    )

    if not any(
        "duplicate operation identifier"
        in error
        for error in duplicate_errors
    ):
        errors.append(
            "R4-I incorrectly permitted duplicate runtime operation"
        )

    # --------------------------------------------------------
    # State-domain conflation must fail.
    # --------------------------------------------------------

    conflated = dict(
        record
    )

    conflated[
        "execution_state_reference"
    ] = conflated[
        "room_state_reference"
    ]

    conflated[
        "continuity_record_id"
    ] = compute_continuity_record_id(
        conflated
    )

    conflation_errors = validate_record(
        conflated
    )

    if not any(
        "must remain distinct"
        in error
        for error in conflation_errors
    ):
        errors.append(
            "R4-I incorrectly permitted state-domain conflation"
        )

    # --------------------------------------------------------
    # Ordered subsequence is valid.
    # --------------------------------------------------------

    subsequence = json.loads(
        json.dumps(record)
    )

    subsequence[
        "operation_chain"
    ] = [
        subsequence[
            "operation_chain"
        ][0],
        subsequence[
            "operation_chain"
        ][2],
        subsequence[
            "operation_chain"
        ][5],
        subsequence[
            "operation_chain"
        ][7],
    ]

    subsequence[
        "continuity_record_id"
    ] = compute_continuity_record_id(
        subsequence
    )

    subsequence_errors = validate_record(
        subsequence
    )

    if subsequence_errors:
        errors.append(
            "R4-I rejected valid ordered runtime subsequence: "
            + "; ".join(
                subsequence_errors
            )
        )

    # --------------------------------------------------------
    # BLOCKED requires reason.
    # --------------------------------------------------------

    blocked = dict(
        record
    )

    blocked[
        "continuity_status"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = []

    blocked[
        "continuity_record_id"
    ] = compute_continuity_record_id(
        blocked
    )

    blocked_errors = validate_record(
        blocked
    )

    if not any(
        "requires blocking reasons"
        in error
        for error in blocked_errors
    ):
        errors.append(
            "R4-I incorrectly permitted BLOCKED continuity without reason"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-I RUNTIME-STATE CONTINUITY / "
            "CROSS-OPERATION INTEGRITY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-I RUNTIME-STATE CONTINUITY / "
        "CROSS-OPERATION INTEGRITY: PASS"
    )
    print(
        "R4-A -> R4-H ordered continuity: LOCKED"
    )
    print(
        "Canonical Room identity across operations: PRESERVED"
    )
    print(
        "Room / representation / execution state separation: ENFORCED"
    )
    print(
        "Evidence boundary / ceiling / lineage / provenance: PRESERVED"
    )
    print(
        "Cartography / coordinates / Stick continuity: PRESERVED"
    )
    print(
        "Object drift / state conflation / approximate repair: REJECTED"
    )
    print(
        "R4-J aggregate closure: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
