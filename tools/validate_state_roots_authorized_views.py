#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

STATE_SCHEMA = (
    ROOT / "schemas/state/state_record.schema.json"
)

VIEW_SCHEMA = (
    ROOT / "schemas/state/authorized_view.schema.json"
)

POINTER_SCHEMA = (
    ROOT / "schemas/state/state_pointer.schema.json"
)

CONTRACT = (
    ROOT / "contracts/state/STATE_ROOTS_AUTHORIZED_VIEWS.md"
)


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def sha512_root(value):
    return (
        "sha512:"
        + hashlib.sha512(canonical_bytes(value)).hexdigest()
    )


def state_preimage(
    manifest_reference,
    state_sequence,
    state_payload
):
    return {
        "manifest_reference": manifest_reference,
        "state_sequence": state_sequence,
        "state_payload": state_payload,
    }


def compute_state_root(
    manifest_reference,
    state_sequence,
    state_payload
):
    return sha512_root(
        state_preimage(
            manifest_reference,
            state_sequence,
            state_payload
        )
    )


def view_preimage(
    source_state_root,
    authorization_reference,
    view_scope,
    projection,
    restrictions
):
    return {
        "source_state_root": source_state_root,
        "authorization_reference": authorization_reference,
        "view_scope": view_scope,
        "projection": projection,
        "restrictions": restrictions,
    }


def compute_authorized_view_root(
    source_state_root,
    authorization_reference,
    view_scope,
    projection,
    restrictions
):
    return sha512_root(
        view_preimage(
            source_state_root,
            authorization_reference,
            view_scope,
            projection,
            restrictions
        )
    )


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate():
    errors = []

    for path, label in [
        (CONTRACT, "R1-E state contract"),
        (STATE_SCHEMA, "state record schema"),
        (VIEW_SCHEMA, "authorized view schema"),
        (POINTER_SCHEMA, "state pointer schema"),
    ]:
        if not path.exists():
            errors.append(f"missing {label}")

    if errors:
        return errors

    try:
        state = load(STATE_SCHEMA)
        view = load(VIEW_SCHEMA)
        pointer = load(POINTER_SCHEMA)
    except Exception as exc:
        return [f"invalid R1-E schema JSON: {exc}"]

    state_required = set(state.get("required", []))

    for field in {
        "manifest_reference",
        "state_sequence",
        "state_payload",
        "provenance_route",
        "state_root",
    }:
        if field not in state_required:
            errors.append(
                f"state record missing required field: {field}"
            )

    view_required = set(view.get("required", []))

    for field in {
        "source_state_root",
        "authorization_reference",
        "view_scope",
        "projection",
        "restrictions",
        "authorized_view_root",
    }:
        if field not in view_required:
            errors.append(
                f"authorized view missing required field: {field}"
            )

    pointer_required = set(pointer.get("required", []))

    for field in {
        "active_manifest_reference",
        "active_state_root",
        "state_sequence",
        "prior_state_root",
        "mutation_reason",
        "authorization_reference",
        "provenance_route",
    }:
        if field not in pointer_required:
            errors.append(
                f"state pointer missing required field: {field}"
            )

    forbidden = {
        "branch_id",
        "merge_id",
        "room_id",
        "object_id",
    }

    for name, schema in [
        ("State Record", state),
        ("Authorized View", view),
        ("State Pointer", pointer),
    ]:
        props = set(schema.get("properties", {}))
        leaked = props & forbidden

        if leaked:
            errors.append(
                f"{name} improperly defines R1-F/object fields: "
                + ", ".join(sorted(leaked))
            )

    pointer_props = set(
        pointer.get("properties", {})
    )

    if "state_payload" in pointer_props:
        errors.append(
            "State Pointer must not contain canonical state payload"
        )

    contract_text = CONTRACT.read_text(encoding="utf-8")

    required_locks = [
        "Definition is not state.",
        "State is not projection.",
        "Projection is not execution.",
        "State root != object identity.",
        "Authorized View Root != State Root.",
        "R1-F remains blocked.",
    ]

    for lock in required_locks:
        if lock not in contract_text:
            errors.append(
                f"missing R1-E separation lock: {lock}"
            )

    probe_root = compute_state_root(
        "manifest:probe",
        1,
        {"signal": "stable"}
    )

    if not SHA512_RE.fullmatch(probe_root):
        errors.append(
            "computed State Root is not canonical SHA-512 form"
        )

    view_root = compute_authorized_view_root(
        probe_root,
        "auth:probe",
        {"fields": ["signal"]},
        {"signal": "stable"},
        []
    )

    if not SHA512_RE.fullmatch(view_root):
        errors.append(
            "computed Authorized View Root is invalid"
        )

    if view_root == probe_root:
        errors.append(
            "Authorized View Root collapsed into State Root"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print("R1-E STATE ROOTS / AUTHORIZED VIEWS: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print("R1-E STATE ROOTS / AUTHORIZED VIEWS: PASS")
    print("State Root: deterministic SHA-512 state identity")
    print("Authorized View Root: deterministic projection identity")
    print("Manifest Pointer / State Pointer: SEPARATE")
    print("Canonical state / projection: SEPARATE")
    print("Canonical state / execution state: SEPARATE")
    print("Branch / merge semantics: DEFERRED TO R1-F")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
