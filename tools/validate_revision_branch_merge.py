#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT / "contracts/lineage/REVISION_BRANCH_MERGE.md"
)

BRANCH_SCHEMA = (
    ROOT / "schemas/lineage/branch_record.schema.json"
)

MERGE_SCHEMA = (
    ROOT / "schemas/lineage/merge_record.schema.json"
)

DISTINCT_SCHEMA = (
    ROOT / "schemas/lineage/distinct_object_record.schema.json"
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


def compute_branch_id(
    parent_manifest_reference,
    parent_state_root,
    branch_reason,
    branch_nonce
):
    return sha512_identity({
        "parent_manifest_reference":
            parent_manifest_reference,
        "parent_state_root":
            parent_state_root,
        "branch_reason":
            branch_reason,
        "branch_nonce":
            branch_nonce,
    })


def compute_merge_id(
    left_lineage_reference,
    right_lineage_reference,
    left_state_root,
    right_state_root,
    merge_rationale,
    merge_nonce
):
    return sha512_identity({
        "left_lineage_reference":
            left_lineage_reference,
        "right_lineage_reference":
            right_lineage_reference,
        "left_state_root":
            left_state_root,
        "right_state_root":
            right_state_root,
        "merge_rationale":
            merge_rationale,
        "merge_nonce":
            merge_nonce,
    })


def load(path):
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def validate():
    errors = []

    for path, label in [
        (CONTRACT, "R1-F lineage contract"),
        (BRANCH_SCHEMA, "Branch schema"),
        (MERGE_SCHEMA, "Merge schema"),
        (DISTINCT_SCHEMA, "Distinct Object schema"),
    ]:
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        branch = load(BRANCH_SCHEMA)
        merge = load(MERGE_SCHEMA)
        distinct = load(DISTINCT_SCHEMA)
    except Exception as exc:
        return [
            f"invalid R1-F schema JSON: {exc}"
        ]

    branch_required = set(
        branch.get("required", [])
    )

    for field in {
        "parent_manifest_reference",
        "parent_state_root",
        "branch_id",
        "branch_reason",
        "branch_nonce",
        "authorization_reference",
        "provenance_route",
    }:
        if field not in branch_required:
            errors.append(
                f"Branch record missing required field: {field}"
            )

    merge_required = set(
        merge.get("required", [])
    )

    for field in {
        "left_lineage_reference",
        "right_lineage_reference",
        "left_manifest_reference",
        "right_manifest_reference",
        "left_state_root",
        "right_state_root",
        "merge_id",
        "merge_rationale",
        "merge_nonce",
        "conflicts",
        "unresolved_differences",
        "authorization_reference",
        "provenance_route",
    }:
        if field not in merge_required:
            errors.append(
                f"Merge record missing required field: {field}"
            )

    distinct_required = set(
        distinct.get("required", [])
    )

    for field in {
        "evidence_of_distinctness",
        "relationship_to_source",
        "shared_provenance",
        "non_shared_provenance",
        "independent_boundary",
        "origin_route",
        "object_geometry",
        "passageway_conditions",
        "contamination_controls",
        "return_route",
        "determination",
    }:
        if field not in distinct_required:
            errors.append(
                f"Distinct Object record missing required field: {field}"
            )

    determination_enum = (
        distinct
        .get("properties", {})
        .get("determination", {})
        .get("enum", [])
    )

    if set(determination_enum) != {
        "SAME_OBJECT",
        "DISTINCT_OBJECT",
        "UNRESOLVED",
    }:
        errors.append(
            "Distinct Object determination states are not locked"
        )

    branch_properties = set(
        branch.get("properties", {})
    )

    forbidden_branch_fields = {
        "room_id",
        "object_id",
        "new_object_id",
        "genesis_id",
    }

    leaked = (
        branch_properties
        & forbidden_branch_fields
    )

    if leaked:
        errors.append(
            "Branch schema improperly creates object identity fields: "
            + ", ".join(sorted(leaked))
        )

    merge_properties = set(
        merge.get("properties", {})
    )

    required_parent_fields = {
        "left_lineage_reference",
        "right_lineage_reference",
        "left_manifest_reference",
        "right_manifest_reference",
        "left_state_root",
        "right_state_root",
    }

    missing_parent_fields = (
        required_parent_fields
        - merge_properties
    )

    if missing_parent_fields:
        errors.append(
            "Merge schema cannot preserve all parents: "
            + ", ".join(sorted(missing_parent_fields))
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    required_locks = [
        "Branch != new Room.",
        "Perspective != branch.",
        "Authorized View != branch.",
        "Historical state != branch.",
        "Distinct object != branch.",
        "Same-object merge != new object.",
        "Cross-object contact != identity collapse.",
        "Replay != duplicate world.",
        "No silent merge.",
        "No parent overwrite.",
        "No perspective cloning.",
    ]

    for lock in required_locks:
        if lock not in contract_text:
            errors.append(
                f"missing R1-F lock: {lock}"
            )

    root = (
        "sha512:"
        + "0" * 128
    )

    branch_id = compute_branch_id(
        "manifest:probe",
        root,
        "alternate evidence path",
        "branch-nonce"
    )

    if not SHA512_RE.fullmatch(
        branch_id
    ):
        errors.append(
            "Branch identity is not canonical SHA-512 form"
        )

    merge_id = compute_merge_id(
        branch_id,
        "lineage:right",
        root,
        root,
        "reconcile compatible paths",
        "merge-nonce"
    )

    if not SHA512_RE.fullmatch(
        merge_id
    ):
        errors.append(
            "Merge identity is not canonical SHA-512 form"
        )

    if merge_id == branch_id:
        errors.append(
            "Merge identity collapsed into Branch identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R1-F REVISION / BRANCH / MERGE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R1-F REVISION / BRANCH / MERGE: PASS"
    )
    print(
        "Revision: SAME OBJECT"
    )
    print(
        "Branch: SAME OBJECT BY DEFAULT"
    )
    print(
        "Perspective / Authorized View: NOT BRANCH"
    )
    print(
        "Distinct Object: AFFIRMATIVE EVIDENCE REQUIRED"
    )
    print(
        "Same-object Merge: SAME OBJECT"
    )
    print(
        "Merge parent overwrite: FORBIDDEN"
    )
    print(
        "Silent identity collapse: FORBIDDEN"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
