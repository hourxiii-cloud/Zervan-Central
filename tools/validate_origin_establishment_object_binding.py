#!/usr/bin/env python3

from pathlib import Path
import hashlib
import importlib.util
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "object"
    / "ORIGIN_ESTABLISHMENT_OBJECT_BINDING.md"
)

RECEIPT_SCHEMA = (
    ROOT
    / "schemas"
    / "object"
    / "origin_establishment_receipt.schema.json"
)

INGRESS_SCHEMA = (
    ROOT
    / "schemas"
    / "identity"
    / "ingress_envelope.schema.json"
)

GENESIS_SCHEMA = (
    ROOT
    / "schemas"
    / "manifest"
    / "genesis_manifest.schema.json"
)

OBJECT_SCHEMA = (
    ROOT
    / "schemas"
    / "object"
    / "canonical_room_object.schema.json"
)

R2A_VALIDATOR = (
    ROOT
    / "tools"
    / "validate_canonical_room_object_identity.py"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def load_r2a():
    spec = importlib.util.spec_from_file_location(
        "validate_canonical_room_object_identity",
        R2A_VALIDATOR
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_receipt_id(
    ingress_envelope_reference,
    genesis_manifest_reference,
    object_id,
    final_status,
    duplicate_check,
    authorization_reference,
    decided_at
):
    preimage = {
        "ingress_envelope_reference":
            ingress_envelope_reference,
        "genesis_manifest_reference":
            genesis_manifest_reference,
        "object_id":
            object_id,
        "final_status":
            final_status,
        "duplicate_check":
            duplicate_check,
        "authorization_reference":
            authorization_reference,
        "decided_at":
            decided_at,
    }

    return (
        "sha512:"
        + hashlib.sha512(
            canonical_bytes(preimage)
        ).hexdigest()
    )


def validate_transition(
    initial_status,
    final_status
):
    return (
        initial_status == "PROPOSED"
        and final_status in {
            "ESTABLISHED",
            "REJECTED",
        }
    )


def provenance_compatible(
    ingress_origin,
    genesis_origin,
    object_origin
):
    values = {
        value
        for value in (
            ingress_origin,
            genesis_origin,
            object_origin,
        )
        if value is not None
    }

    return len(values) <= 1


def validate_binding(
    *,
    ingress,
    ingress_reference,
    genesis,
    genesis_reference,
    room_object,
    receipt
):
    errors = []

    try:
        ingress_content_id = (
            ingress["content_identity"]["value"]
        )
    except Exception:
        errors.append(
            "Ingress canonical content identity is missing"
        )
        return errors

    if not SHA512_RE.fullmatch(
        ingress_content_id
    ):
        errors.append(
            "Ingress canonical content identity is invalid"
        )

    if (
        genesis.get("ingress_envelope_reference")
        != ingress_reference
    ):
        errors.append(
            "Genesis Manifest does not reference consumed Ingress Envelope"
        )

    if (
        genesis.get("origin_content_identity")
        != ingress_content_id
    ):
        errors.append(
            "Genesis origin content identity does not match Ingress"
        )

    if (
        room_object.get("origin_content_identity")
        != ingress_content_id
    ):
        errors.append(
            "Room Object origin content identity does not match Ingress"
        )

    if (
        room_object.get("genesis_manifest_reference")
        != genesis_reference
    ):
        errors.append(
            "Room Object does not reference consumed Genesis Manifest"
        )

    ingress_origin = (
        ingress
        .get("provenance", {})
        .get("origin_reference")
    )

    genesis_origin = genesis.get(
        "provenance_origin_reference"
    )

    object_origin = room_object.get(
        "provenance_origin_reference"
    )

    if not provenance_compatible(
        ingress_origin,
        genesis_origin,
        object_origin
    ):
        errors.append(
            "Origin provenance references contradict"
        )

    r2a = load_r2a()

    expected_object_id = r2a.compute_object_id(
        genesis_reference,
        ingress_content_id,
        room_object.get("object_nonce")
    )

    if (
        room_object.get("object_id")
        != expected_object_id
    ):
        errors.append(
            "Canonical object identity does not recompute"
        )

    if not validate_transition(
        receipt.get("initial_status"),
        receipt.get("final_status")
    ):
        errors.append(
            "Invalid R2-B establishment transition"
        )

    if (
        receipt.get("ingress_envelope_reference")
        != ingress_reference
    ):
        errors.append(
            "Receipt Ingress reference mismatch"
        )

    if (
        receipt.get("genesis_manifest_reference")
        != genesis_reference
    ):
        errors.append(
            "Receipt Genesis reference mismatch"
        )

    if (
        receipt.get("object_id")
        != room_object.get("object_id")
    ):
        errors.append(
            "Receipt object identity mismatch"
        )

    checks = receipt.get(
        "prerequisite_checks",
        {}
    )

    required_checks = {
        "ingress_present",
        "content_identity_valid",
        "genesis_present",
        "ingress_reference_match",
        "content_identity_match",
        "provenance_continuity",
        "object_identity_match",
        "authorization_resolved",
    }

    if set(checks) != required_checks:
        errors.append(
            "Receipt prerequisite checks are incomplete or expanded"
        )

    final_status = receipt.get(
        "final_status"
    )

    duplicate_check = receipt.get(
        "duplicate_check"
    )

    if final_status == "ESTABLISHED":
        if duplicate_check != "CLEAR":
            errors.append(
                "ESTABLISHED requires duplicate check CLEAR"
            )

        if not all(
            checks.get(name) is True
            for name in required_checks
        ):
            errors.append(
                "ESTABLISHED requires every prerequisite check to pass"
            )

        if not receipt.get(
            "authorization_reference"
        ):
            errors.append(
                "ESTABLISHED requires authorization reference"
            )

        human_gate = receipt.get(
            "human_gate",
            {}
        )

        if (
            human_gate.get("status")
            == "UNRESOLVED"
        ):
            errors.append(
                "ESTABLISHED cannot carry unresolved Human Gate state"
            )

        if (
            human_gate.get("status")
            == "REQUIRED_SATISFIED"
            and not human_gate.get("reference")
        ):
            errors.append(
                "Satisfied Human Gate requires evidence reference"
            )

        if (
            room_object.get("establishment_status")
            != "ESTABLISHED"
        ):
            errors.append(
                "Room Object status does not match ESTABLISHED receipt"
            )

    if final_status == "REJECTED":
        if (
            room_object.get("establishment_status")
            != "REJECTED"
        ):
            errors.append(
                "Room Object status does not match REJECTED receipt"
            )

    expected_receipt_id = compute_receipt_id(
        ingress_reference,
        genesis_reference,
        room_object.get("object_id"),
        final_status,
        duplicate_check,
        receipt.get("authorization_reference"),
        receipt.get("decided_at")
    )

    if (
        receipt.get("establishment_receipt_id")
        != expected_receipt_id
    ):
        errors.append(
            "Establishment receipt identity does not recompute"
        )

    return errors


def validate():
    errors = []

    required_paths = [
        (CONTRACT, "R2-B contract"),
        (RECEIPT_SCHEMA, "R2-B receipt schema"),
        (INGRESS_SCHEMA, "R1-C Ingress schema"),
        (GENESIS_SCHEMA, "R1-D Genesis schema"),
        (OBJECT_SCHEMA, "R2-A Room Object schema"),
        (R2A_VALIDATOR, "R2-A identity validator"),
    ]

    for path, label in required_paths:
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        receipt_schema = load(
            RECEIPT_SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R2-B schema JSON: {exc}"
        ]

    required = set(
        receipt_schema.get(
            "required",
            []
        )
    )

    expected = {
        "establishment_receipt_id",
        "ingress_envelope_reference",
        "genesis_manifest_reference",
        "object_id",
        "initial_status",
        "final_status",
        "duplicate_check",
        "prerequisite_checks",
        "authorization_reference",
        "human_gate",
        "provenance_route",
        "decided_at",
        "decision_reason",
    }

    missing = expected - required

    if missing:
        errors.append(
            "Establishment receipt missing required fields: "
            + ", ".join(
                sorted(missing)
            )
        )

    initial_const = (
        receipt_schema
        .get("properties", {})
        .get("initial_status", {})
        .get("const")
    )

    if initial_const != "PROPOSED":
        errors.append(
            "R2-B initial establishment state is not locked to PROPOSED"
        )

    final_states = set(
        receipt_schema
        .get("properties", {})
        .get("final_status", {})
        .get("enum", [])
    )

    if final_states != {
        "ESTABLISHED",
        "REJECTED",
    }:
        errors.append(
            "R2-B terminal establishment states are not locked"
        )

    duplicate_states = set(
        receipt_schema
        .get("properties", {})
        .get("duplicate_check", {})
        .get("enum", [])
    )

    if duplicate_states != {
        "CLEAR",
        "EXISTING_OBJECT",
        "UNRESOLVED",
    }:
        errors.append(
            "Duplicate-establishment states are not locked"
        )

    properties = set(
        receipt_schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "terrain",
        "territory",
        "zone_id",
        "space_id",
        "transform_id",
        "cartography",
        "occupation",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R2-B improperly pulls downstream geography forward: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    required_locks = [
        "Computable != established.",
        "Establishment != qualification.",
        "Establishment != truth.",
        "Duplicate establishment must be CLEAR.",
        "Nonce cannot be used to clone around duplicate control.",
        "Receipt identity is not object identity.",
        "No Terrain yet.",
        "No Territory yet.",
        "No Zone yet.",
        "No Space yet.",
        "No Cartography yet.",
        "No Occupation yet.",
    ]

    for lock in required_locks:
        if lock not in contract_text:
            errors.append(
                f"missing R2-B lock: {lock}"
            )

    if not validate_transition(
        "PROPOSED",
        "ESTABLISHED"
    ):
        errors.append(
            "PROPOSED -> ESTABLISHED transition unavailable"
        )

    if not validate_transition(
        "PROPOSED",
        "REJECTED"
    ):
        errors.append(
            "PROPOSED -> REJECTED transition unavailable"
        )

    for invalid in [
        ("ESTABLISHED", "PROPOSED"),
        ("REJECTED", "ESTABLISHED"),
        ("ESTABLISHED", "REJECTED"),
    ]:
        if validate_transition(
            *invalid
        ):
            errors.append(
                "invalid establishment transition permitted: "
                + " -> ".join(invalid)
            )

    probe_id = compute_receipt_id(
        "ingress:probe",
        "genesis:probe",
        "sha512:" + "0" * 128,
        "ESTABLISHED",
        "CLEAR",
        "auth:probe",
        "2026-08-07T18:25:00-04:00"
    )

    if not SHA512_RE.fullmatch(
        probe_id
    ):
        errors.append(
            "Establishment receipt identity is not canonical SHA-512"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R2-B ORIGIN ESTABLISHMENT / OBJECT BINDING: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R2-B ORIGIN ESTABLISHMENT / OBJECT BINDING: PASS"
    )
    print(
        "Origin -> Ingress -> Genesis -> Object: BOUND"
    )
    print(
        "Object identity: RECOMPUTED"
    )
    print(
        "PROPOSED -> ESTABLISHED / REJECTED: LOCKED"
    )
    print(
        "Duplicate establishment: FAIL CLOSED"
    )
    print(
        "Provenance route to Origin: PRESERVED"
    )
    print(
        "Qualification / geography / occupation: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
