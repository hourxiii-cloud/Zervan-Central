#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "qualification"
    / "ROOM_LIFECYCLE_READINESS.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "room_lifecycle_transition.schema.json"
)

QUALIFICATION_SCHEMA = (
    ROOT
    / "schemas"
    / "qualification"
    / "qualification_record.schema.json"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

SOURCE_STATES = {
    "DETECTED",
    "PROVISIONAL",
    "QUALIFYING",
    "QUALIFIED",
    "READY",
    "ACTIVE",
    "LANDED",
    "DEGRADED",
    "SEALED",
    "REOPENED",
    "REJECTED",
    "SUPERSEDED",
}

R3C_TRANSITIONS = {
    ("DETECTED", "PROVISIONAL"),
    ("PROVISIONAL", "QUALIFYING"),
    ("QUALIFYING", "QUALIFIED"),
    ("QUALIFYING", "PROVISIONAL"),
    ("QUALIFYING", "REJECTED"),
    ("QUALIFYING", "DEGRADED"),
    ("QUALIFIED", "READY"),
}

DISPOSITION_TARGETS = {
    "QUALIFIED": "QUALIFIED",
    "PROVISIONAL": "PROVISIONAL",
    "REJECTED": "REJECTED",
    "DEGRADED": "DEGRADED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_lifecycle_transition_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "lifecycle_transition_id"
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


def validate_transition(record):
    errors = []

    expected = compute_lifecycle_transition_id(
        record
    )

    if (
        record.get("lifecycle_transition_id")
        != expected
    ):
        errors.append(
            "lifecycle_transition_id does not recompute from transition"
        )

    source = record.get(
        "source_state"
    )

    target = record.get(
        "target_state"
    )

    disposition = record.get(
        "qualification_disposition"
    )

    if source not in SOURCE_STATES:
        errors.append(
            "invalid source lifecycle state"
        )

    if target not in SOURCE_STATES:
        errors.append(
            "invalid target lifecycle state"
        )

    if (
        source,
        target,
    ) not in R3C_TRANSITIONS:
        errors.append(
            f"transition {source} -> {target} is outside R3-C transition surface"
        )

    for field in (
        "object_id",
        "transition_basis",
        "registry_reference",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"lifecycle transition requires {field}"
            )

    if source == "QUALIFYING":
        if not record.get(
            "qualification_record_reference"
        ):
            errors.append(
                "QUALIFYING disposition transition requires "
                "qualification_record_reference"
            )

        expected_target = DISPOSITION_TARGETS.get(
            disposition
        )

        if expected_target != target:
            errors.append(
                "qualification disposition does not support target lifecycle state"
            )

    if (
        source == "QUALIFIED"
        and target == "READY"
    ):
        if disposition != "QUALIFIED":
            errors.append(
                "READY requires QUALIFIED disposition"
            )

        for field in (
            "qualification_record_reference",
            "declared_mission",
            "evidence_ceiling",
            "readiness_requirements",
            "audit_reference",
        ):
            if record.get(field) in (
                None,
                "",
                {},
                [],
            ):
                errors.append(
                    f"READY transition requires {field}"
                )

        if record.get(
            "unresolved_readiness_blockers"
        ):
            errors.append(
                "READY transition cannot retain unresolved readiness blockers"
            )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R3-C lifecycle contract"
        ),
        (
            SCHEMA,
            "R3-C lifecycle schema"
        ),
        (
            QUALIFICATION_SCHEMA,
            "R3-B Qualification Record schema"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    try:
        schema = load(
            SCHEMA
        )
        qualification_schema = load(
            QUALIFICATION_SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid schema JSON: {exc}"
        ]

    source_states = set(
        schema
        .get("properties", {})
        .get("source_state", {})
        .get("enum", [])
    )

    target_states = set(
        schema
        .get("properties", {})
        .get("target_state", {})
        .get("enum", [])
    )

    if source_states != SOURCE_STATES:
        errors.append(
            "source lifecycle vocabulary diverges from source-defined behavior"
        )

    if target_states != SOURCE_STATES:
        errors.append(
            "target lifecycle vocabulary diverges from source-defined behavior"
        )

    r3c_dispositions = set(
        item
        for item in (
            schema
            .get("properties", {})
            .get("qualification_disposition", {})
            .get("enum", [])
        )
        if item is not None
    )

    r3b_dispositions = set(
        qualification_schema
        .get("properties", {})
        .get("qualification_disposition", {})
        .get("enum", [])
    )

    if r3c_dispositions != r3b_dispositions:
        errors.append(
            "R3-C qualification dispositions diverge from R3-B"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "occupancy_witness_id",
        "occupant_id",
        "selected_formation",
        "formation_selection_id",
        "capability_mission_id",
        "landing_witness_id",
        "reflight_trigger_id",
        "closing_witness_id",
        "replay_envelope_id",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R3-C improperly absorbs downstream semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    normalized_contract_text = " ".join(
        contract_text.split()
    )

    locks = [
        "Qualification precedes analysis.",
        "Lifecycle state does not own truth.",
        "Lifecycle transition MUST be attributable.",
        "History accumulates.",
        "Registry defines and resolves Room lifecycle state.",
        "Audit verifies transition integrity.",
        "Disposition != lifecycle mutation.",
        "DETECTED != PROVISIONAL.",
        "Signal existence != qualified Room.",
        "PROVISIONAL != QUALIFIED.",
        "PROVISIONAL != READY.",
        "QUALIFYING != QUALIFIED.",
        "Work in progress != qualification success.",
        "Only QUALIFIED disposition may support lifecycle QUALIFIED.",
        "QUALIFIED != READY.",
        "QUALIFIED != ACTIVE.",
        "PROVISIONAL disposition != qualification success.",
        "Rejected != erased.",
        "DEGRADED != nonexistent.",
        "DEGRADED != READY.",
        "READY means available for formation selection and analytical occupation.",
        "READY != ACTIVE.",
        "READY != occupied.",
        "Availability != presence.",
        "QUALIFIED is necessary for READY.",
        "QUALIFIED alone is not sufficient for READY.",
        "Blocked != absent.",
        "Write capability != authority.",
        "Approval != execution.",
        "READY != formation selected.",
        "Lifecycle transition != formation selection.",
        "Lifecycle transition != Occupancy Witness.",
        "READY != publication authority.",
        "No ACTIVE transition yet.",
        "No LANDED transition yet.",
        "No SEALED transition yet.",
        "No REOPENED transition yet.",
        "No SUPERSEDED transition yet.",
    ]

    for lock in locks:
        normalized_lock = " ".join(
            lock.split()
        )

        if (
            normalized_lock
            not in normalized_contract_text
        ):
            errors.append(
                f"missing R3-C lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    qualified = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "source_state":
            "QUALIFYING",
        "target_state":
            "QUALIFIED",
        "qualification_request_reference":
            "request:a",
        "qualification_record_reference":
            "record:a",
        "qualification_disposition":
            "QUALIFIED",
        "declared_mission":
            "bounded analytical mission",
        "evidence_ceiling":
            "CEILING:A",
        "readiness_requirements":
            [],
        "unresolved_readiness_blockers":
            [],
        "transition_basis": [
            "Qualification Record disposition is QUALIFIED"
        ],
        "registry_reference":
            "registry:a",
        "audit_reference":
            "audit:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "request:a",
            "record:a",
        ],
        "transitioned_at":
            "2026-08-07T19:22:00-04:00",
    }

    qualified[
        "lifecycle_transition_id"
    ] = compute_lifecycle_transition_id(
        qualified
    )

    errors.extend(
        validate_transition(
            qualified
        )
    )

    ready = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "source_state":
            "QUALIFIED",
        "target_state":
            "READY",
        "qualification_request_reference":
            "request:a",
        "qualification_record_reference":
            "record:a",
        "qualification_disposition":
            "QUALIFIED",
        "declared_mission":
            "bounded analytical mission",
        "evidence_ceiling":
            "CEILING:A",
        "readiness_requirements": [
            "qualification integrity verified",
            "representation references resolvable",
            "provenance route resolvable",
        ],
        "unresolved_readiness_blockers":
            [],
        "transition_basis": [
            "qualified Room is available for formation selection "
            "and analytical occupation"
        ],
        "registry_reference":
            "registry:a",
        "audit_reference":
            "audit:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "record:a",
            "registry:a",
        ],
        "transitioned_at":
            "2026-08-07T19:22:00-04:00",
    }

    ready[
        "lifecycle_transition_id"
    ] = compute_lifecycle_transition_id(
        ready
    )

    errors.extend(
        validate_transition(
            ready
        )
    )

    if not SHA512_RE.fullmatch(
        ready[
            "lifecycle_transition_id"
        ]
    ):
        errors.append(
            "lifecycle_transition_id is not canonical SHA-512"
        )

    if (
        ready["lifecycle_transition_id"]
        == object_id
    ):
        errors.append(
            "Lifecycle transition identity collapsed into object identity"
        )

    blocked = dict(
        ready
    )

    blocked[
        "unresolved_readiness_blockers"
    ] = [
        "Audit transition integrity unresolved"
    ]

    blocked[
        "lifecycle_transition_id"
    ] = compute_lifecycle_transition_id(
        blocked
    )

    blocked_errors = validate_transition(
        blocked
    )

    if not any(
        "unresolved readiness blockers"
        in error
        for error in blocked_errors
    ):
        errors.append(
            "READY incorrectly permitted unresolved readiness blockers"
        )

    wrong_disposition = dict(
        qualified
    )

    wrong_disposition[
        "qualification_disposition"
    ] = "PROVISIONAL"

    wrong_disposition[
        "lifecycle_transition_id"
    ] = compute_lifecycle_transition_id(
        wrong_disposition
    )

    wrong_errors = validate_transition(
        wrong_disposition
    )

    if not any(
        "does not support target lifecycle state"
        in error
        for error in wrong_errors
    ):
        errors.append(
            "PROVISIONAL disposition incorrectly permitted QUALIFIED state"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R3-C ROOM LIFECYCLE / READINESS: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R3-C ROOM LIFECYCLE / READINESS: PASS"
    )
    print(
        "DETECTED / PROVISIONAL / QUALIFYING / QUALIFIED / READY: BOUND"
    )
    print(
        "Qualification disposition -> lifecycle transition: ENFORCED"
    )
    print(
        "READY blockers: FAIL-CLOSED"
    )
    print(
        "Registry ownership / Audit integrity: PRESERVED"
    )
    print(
        "ACTIVE / Landing / Replay / Supersession execution: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
