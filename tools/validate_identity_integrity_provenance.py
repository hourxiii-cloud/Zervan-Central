#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTENT_ID_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)


def sha512_identity(data: bytes) -> str:
    return "sha512:" + hashlib.sha512(data).hexdigest()


def verify_content_identity(
    data: bytes,
    identity: str
) -> bool:
    return sha512_identity(data) == identity


def validate_schema_contract():
    errors = []

    schema_path = (
        ROOT
        / "schemas"
        / "identity"
        / "ingress_envelope.schema.json"
    )

    contract_path = (
        ROOT
        / "contracts"
        / "identity"
        / "IDENTITY_INTEGRITY_PROVENANCE.md"
    )

    if not schema_path.exists():
        errors.append("missing ingress envelope schema")

    if not contract_path.exists():
        errors.append("missing R1-C identity contract")

    if errors:
        return errors

    try:
        schema = json.loads(
            schema_path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        return [f"invalid ingress schema JSON: {exc}"]

    required = set(schema.get("required", []))

    expected = {
        "schema_version",
        "source_identity",
        "content_identity",
        "storage",
        "schema_identity",
        "serialization_identity",
        "provenance",
        "admission_boundary",
        "custody",
        "time",
        "controls",
        "evidence_restrictions",
        "authorization_posture",
    }

    missing = expected - required

    if missing:
        errors.append(
            "ingress schema missing required fields: "
            + ", ".join(sorted(missing))
        )

    content_identity = (
        schema
        .get("properties", {})
        .get("content_identity", {})
    )

    algorithm = (
        content_identity
        .get("properties", {})
        .get("algorithm", {})
        .get("const")
    )

    if algorithm != "sha512":
        errors.append(
            "canonical content identity algorithm "
            "must be sha512"
        )

    pattern = (
        content_identity
        .get("properties", {})
        .get("value", {})
        .get("pattern")
    )

    if pattern != "^sha512:[0-9a-f]{128}$":
        errors.append(
            "canonical SHA-512 identity format "
            "is not locked"
        )

    availability = (
        schema
        .get("properties", {})
        .get("storage", {})
        .get("properties", {})
        .get("availability", {})
        .get("enum", [])
    )

    required_availability = {
        "KNOWN_AVAILABLE",
        "KNOWN_RESTRICTED",
        "KNOWN_UNAVAILABLE",
        "UNRESOLVED",
        "ABSENT",
    }

    for state in required_availability:
        if state not in availability:
            errors.append(
                f"missing evidence availability state: "
                f"{state}"
            )

    attestation = (
        schema
        .get("properties", {})
        .get("attestation", {})
        .get("properties", {})
        .get("status", {})
        .get("enum", [])
    )

    required_attestation = {
        "VERIFIED",
        "FAILED",
        "ABSENT",
        "UNRESOLVED",
    }

    for state in required_attestation:
        if state not in attestation:
            errors.append(
                f"missing attestation state: {state}"
            )

    return errors


def main():
    errors = validate_schema_contract()

    if errors:
        print(
            "R1-C IDENTITY / INTEGRITY / "
            "PROVENANCE: FAIL"
        )

        for error in errors:
            print(f" - {error}")

        return 1

    probe = b"zervan-r1-c-integrity-probe"
    identity = sha512_identity(probe)

    if not CONTENT_ID_RE.fullmatch(identity):
        print(
            "R1-C IDENTITY / INTEGRITY / "
            "PROVENANCE: FAIL"
        )
        print(
            " - generated SHA-512 identity "
            "format invalid"
        )
        return 1

    if not verify_content_identity(
        probe,
        identity
    ):
        print(
            "R1-C IDENTITY / INTEGRITY / "
            "PROVENANCE: FAIL"
        )
        print(" - SHA-512 verification failed")
        return 1

    if verify_content_identity(
        probe + b"-changed",
        identity
    ):
        print(
            "R1-C IDENTITY / INTEGRITY / "
            "PROVENANCE: FAIL"
        )
        print(
            " - changed payload incorrectly "
            "retained identity"
        )
        return 1

    print(
        "R1-C IDENTITY / INTEGRITY / "
        "PROVENANCE: PASS"
    )
    print(
        "Canonical content identity: SHA-512"
    )
    print(
        "Integrity boundary: byte sameness, "
        "not truth"
    )
    print(
        "Attestation boundary: assertion, "
        "not correctness"
    )
    print(
        "Provenance requirement: traversable "
        "toward origin"
    )
    print(
        "Restricted evidence existence: preserved"
    )
    print(
        "Integration boundary: external "
        "adaptation does not redefine identity"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
