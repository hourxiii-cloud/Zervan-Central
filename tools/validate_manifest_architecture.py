#!/usr/bin/env python3

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

SCHEMAS = {
    "GENESIS": (
        ROOT
        / "schemas"
        / "manifest"
        / "genesis_manifest.schema.json"
    ),
    "REVISION": (
        ROOT
        / "schemas"
        / "manifest"
        / "revision_manifest.schema.json"
    ),
    "POINTER": (
        ROOT
        / "schemas"
        / "manifest"
        / "manifest_pointer.schema.json"
    ),
}

CONTRACT = (
    ROOT
    / "contracts"
    / "manifest"
    / "MANIFEST_ARCHITECTURE.md"
)

DOCTRINE_MANIFEST = (
    ROOT
    / "DoctrineOps"
    / "DOCTRINE_MANIFEST.md"
)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate():
    errors = []

    if not CONTRACT.exists():
        errors.append("missing R1-D manifest architecture contract")

    if not DOCTRINE_MANIFEST.exists():
        errors.append("missing DoctrineOps doctrine manifest")

    for name, path in SCHEMAS.items():
        if not path.exists():
            errors.append(
                f"missing {name.lower()} manifest schema"
            )

    if errors:
        return errors

    try:
        genesis = load_json(SCHEMAS["GENESIS"])
        revision = load_json(SCHEMAS["REVISION"])
        pointer = load_json(SCHEMAS["POINTER"])
    except Exception as exc:
        return [f"invalid manifest schema JSON: {exc}"]

    if (
        genesis
        .get("properties", {})
        .get("manifest_type", {})
        .get("const")
        != "GENESIS"
    ):
        errors.append("Genesis manifest_type is not locked")

    if (
        revision
        .get("properties", {})
        .get("manifest_type", {})
        .get("const")
        != "REVISION"
    ):
        errors.append("Revision manifest_type is not locked")

    genesis_required = set(genesis.get("required", []))
    revision_required = set(revision.get("required", []))
    pointer_required = set(pointer.get("required", []))

    for field in {
        "origin_content_identity",
        "ingress_envelope_reference",
        "provenance_origin_reference",
        "establishment_boundary",
        "definition",
    }:
        if field not in genesis_required:
            errors.append(
                f"Genesis missing required field: {field}"
            )

    for field in {
        "genesis_manifest_reference",
        "predecessor_manifest_reference",
        "revision_sequence",
        "revision_reason",
        "definition_change",
        "provenance_route",
    }:
        if field not in revision_required:
            errors.append(
                f"Revision missing required field: {field}"
            )

    for field in {
        "genesis_manifest_reference",
        "active_manifest_reference",
        "revision_sequence",
        "mutation_reason",
        "authorization_reference",
        "prior_pointer_reference",
    }:
        if field not in pointer_required:
            errors.append(
                f"Pointer missing required field: {field}"
            )

    genesis_props = genesis.get("properties", {})
    origin_pattern = (
        genesis_props
        .get("origin_content_identity", {})
        .get("pattern")
    )

    if origin_pattern != "^sha512:[0-9a-f]{128}$":
        errors.append(
            "Genesis origin content identity is not SHA-512 locked"
        )

    forbidden_state_fields = {
        "state_root",
        "authorized_view_root",
        "occupancy_state",
        "operation_state",
        "branch_id",
        "merge_id",
    }

    for schema_name, schema in (
        ("Genesis", genesis),
        ("Revision", revision),
        ("Pointer", pointer),
    ):
        props = set(schema.get("properties", {}))
        forbidden = props & forbidden_state_fields

        if forbidden:
            errors.append(
                f"{schema_name} improperly defines downstream fields: "
                + ", ".join(sorted(forbidden))
            )

    if (
        "definition" in pointer.get("properties", {})
        or "definition_change" in pointer.get("properties", {})
    ):
        errors.append(
            "Manifest Pointer must not carry full definition payload"
        )

    contract_text = CONTRACT.read_text(encoding="utf-8")

    required_locks = [
        "Manifest content identity != analytical-object identity.",
        "Definition != state.",
        "Definition != projection.",
        "Revision is not automatically branch.",
    ]

    for lock in required_locks:
        if lock not in contract_text:
            errors.append(
                f"missing manifest separation lock: {lock}"
            )

    doctrine_text = DOCTRINE_MANIFEST.read_text(
        encoding="utf-8"
    )

    if (
        "resolves **existence and required presence**, "
        "not interpretation"
        not in doctrine_text
    ):
        errors.append(
            "Doctrine Manifest existence/interpretation boundary "
            "not found"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print("R1-D MANIFEST ARCHITECTURE: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print("R1-D MANIFEST ARCHITECTURE: PASS")
    print(
        "Doctrine Manifest: system/doctrine existence control"
    )
    print(
        "Genesis Manifest: immutable establishment record"
    )
    print(
        "Revision Manifest: immutable definition-change record"
    )
    print(
        "Manifest Pointer: mutable current-definition locator"
    )
    print(
        "State roots / authorized views: deferred to R1-E"
    )
    print(
        "Branch / merge semantics: deferred to R1-F"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
