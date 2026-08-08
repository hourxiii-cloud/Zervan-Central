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
    / "POST_CONVERGENCE_CLOSURE_CLOSING_WITNESS.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "runtime"
    / "closing_witness.schema.json"
)

R4D = (
    ROOT
    / "tools"
    / "validate_reflight_trigger.py"
)

DISPOSITIONS = {
    "CLOSED",
    "BLOCKED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_closing_witness_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "closing_witness_id"
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


def validate_witness(record):
    errors = []

    if (
        record.get("closing_witness_id")
        != compute_closing_witness_id(record)
    ):
        errors.append(
            "closing_witness_id does not recompute from witness"
        )

    disposition = record.get(
        "closure_disposition"
    )

    if disposition not in DISPOSITIONS:
        errors.append(
            "invalid Closing Witness disposition"
        )

    for field in (
        "object_id",
        "landing_witness_reference",
        "convergence_state_reference",
        "closure_basis",
        "preserved_question",
        "representation_reference",
        "zone_reference",
        "space_reference",
        "cartography_reference",
        "stick_reference",
        "evidence_boundary",
        "evidence_ceiling",
        "preserved_lineage_reference",
        "replay_coordinates",
        "return_coordinates",
        "registry_reference",
        "governance_reference",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Closing Witness requires {field}"
            )

    obligations = record.get(
        "outstanding_analytical_obligations",
        []
    )

    blocking_reasons = record.get(
        "blocking_reasons",
        []
    )

    if (
        disposition == "CLOSED"
        and obligations
    ):
        errors.append(
            "CLOSED witness cannot retain active outstanding analytical obligations"
        )

    if (
        disposition == "CLOSED"
        and not record.get(
            "audit_witness_reference"
        )
    ):
        errors.append(
            "CLOSED witness requires Audit witness reference"
        )

    if (
        disposition == "BLOCKED"
        and not blocking_reasons
    ):
        errors.append(
            "BLOCKED witness requires blocking reasons"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R4-E Closing Witness contract"
        ),
        (
            SCHEMA,
            "R4-E Closing Witness schema"
        ),
        (
            R4D,
            "R4-D Reflight Trigger validator"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    r4d = subprocess.run(
        [
            sys.executable,
            str(R4D),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if r4d.returncode != 0:
        errors.append(
            "R4-D dependency validation failed"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-E schema JSON: {exc}"
        ]

    dispositions = set(
        schema
        .get("properties", {})
        .get("closure_disposition", {})
        .get("enum", [])
    )

    if dispositions != DISPOSITIONS:
        errors.append(
            "R4-E closure disposition vocabulary is not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "lifecycle_transition_id",
        "sealed_state_mutation",
        "reopened_state_mutation",
        "replay_envelope_id",
        "scar_record_id",
        "publication_authorization",
        "canonical_promotion",
        "reflight_execution_id",
        "rendering_contract_id",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R4-E improperly absorbs downstream or foreign semantics: "
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
        "After convergence, do not rebuild or re-explain the Room without a new analytical trigger.",
        "Importance does not authorize Reflight.",
        "Emotion does not authorize Reflight.",
        "Acknowledgment does not authorize Reflight.",
        "Celebration does not authorize Reflight.",
        "Laughter does not authorize Reflight.",
        "Repetition of a settled point does not authorize Reflight.",
        "When the message has landed: land.",
        "Preserve object and representation state.",
        "Remain naturally conversational.",
        "Do not rebuild The Room in prose.",
        "Prefer the smallest sufficient response.",
        "Small response != compressed Room.",
        "Closure preserves state.",
        "Closure does not reconstruct state.",
        "Closure does not delete state.",
        "Closure does not promote state.",
        "Closed interval != destroyed Room.",
        "CLOSED != canonical promotion.",
        "BLOCKED != analytical failure.",
        "Close the interval.",
        "Do not clone the object.",
        "Landing first.",
        "Closing Witness second.",
        "Convergence != absolute truth.",
        "Convergence != certainty.",
        "Convergence != publication approval.",
        "Closing Witness does not disable future Reflight.",
        "Closing Witness does not manufacture a Reflight Trigger.",
        "Closure now != never analyze again.",
        "Unresolved terrain != outstanding movement obligation.",
        "Closure does not convert unknown into known.",
        "Closure does not convert inaccessible into absent.",
        "Closed interval != higher evidence ceiling.",
        "Closure does not flatten Collapse into a final summary.",
        "Closure without lineage is incomplete.",
        "Closing Witness MUST preserve replay coordinates.",
        "Replay coordinates != duplicate Room.",
        "Closure != Cartography reset.",
        "Closing MUST preserve the Stick.",
        "No default substitution.",
        "Natural conversation does not require Room reconstruction.",
        "Natural conversation does not authorize Reflight.",
        "Conversation != analytical movement.",
        "No unnecessary rebuild.",
        "No unnecessary re-analysis.",
        "Audit verifies closing witnesses.",
        "Audit does not own Room truth.",
        "Audit verification != canonical promotion.",
        "Closing Witness creation alone MUST NOT silently mutate lifecycle state.",
        "Closing Witness != Registry lifecycle transition.",
        "SEALED transition remains separately attributable to Registry.",
        "REOPENED remains downstream.",
        "Closure != policy reset.",
        "Closing Witness does not imply publication authority.",
        "Closing Witness does not imply execution authority.",
        "Closing a Room interval does not publish it.",
        "Closed != published.",
        "Closing Witness != rendering contract.",
        "Closing Witness != Replay Envelope.",
        "R4-F owns Replay Envelope.",
        "No Replay semantics yet.",
        "No Scar Record semantics yet.",
        "No Scar Replay semantics yet.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in normalized
        ):
            errors.append(
                f"missing R4-E lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    witness = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "landing_witness_reference":
            "landing:a",
        "convergence_state_reference":
            "convergence:a",
        "closure_basis": [
            "current bounded analytical movement converged",
            "no active analytical obligation requires continued movement"
        ],
        "preserved_question":
            "which state remains supportable at the current evidence ceiling?",
        "representation_reference":
            "representation:a",
        "zone_reference":
            "zone:a",
        "space_reference":
            "space:a",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "unresolved_terrain_references": [
            "terrain:unresolved:a"
        ],
        "restriction_constriction_references": [
            "restriction:a"
        ],
        "collapse_boundary_references": [
            "collapse:a"
        ],
        "reflight_trigger_references": [],
        "outstanding_analytical_obligations": [],
        "preserved_lineage_reference":
            "lineage:a",
        "replay_coordinates": {
            "coordinate": "observational:a"
        },
        "return_coordinates": {
            "coordinate": "return:a"
        },
        "current_rendering_reference":
            "rendering:a",
        "closure_disposition":
            "CLOSED",
        "blocking_reasons": [],
        "audit_witness_reference":
            "audit:closing:a",
        "registry_reference":
            "registry:a",
        "governance_reference":
            "governance:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "landing:a",
            "convergence:a",
            "restriction:a",
            "collapse:a",
            "lineage:a",
            "stick:a"
        ],
        "closed_at":
            "2026-08-07T20:33:00-04:00",
    }

    witness[
        "closing_witness_id"
    ] = compute_closing_witness_id(
        witness
    )

    errors.extend(
        validate_witness(
            witness
        )
    )

    blocked = dict(
        witness
    )

    blocked[
        "closure_disposition"
    ] = "BLOCKED"

    blocked[
        "outstanding_analytical_obligations"
    ] = [
        "material contradiction requires continued bounded analysis"
    ]

    blocked[
        "blocking_reasons"
    ] = [
        "active analytical obligation remains"
    ]

    blocked[
        "audit_witness_reference"
    ] = None

    blocked[
        "closing_witness_id"
    ] = compute_closing_witness_id(
        blocked
    )

    errors.extend(
        validate_witness(
            blocked
        )
    )

    bad_closed_obligation = dict(
        witness
    )

    bad_closed_obligation[
        "outstanding_analytical_obligations"
    ] = [
        "active evidence obligation"
    ]

    bad_closed_obligation[
        "closing_witness_id"
    ] = compute_closing_witness_id(
        bad_closed_obligation
    )

    obligation_errors = validate_witness(
        bad_closed_obligation
    )

    if not any(
        "cannot retain active outstanding analytical obligations"
        in error
        for error in obligation_errors
    ):
        errors.append(
            "R4-E incorrectly permitted CLOSED state with active obligation"
        )

    bad_audit = dict(
        witness
    )

    bad_audit[
        "audit_witness_reference"
    ] = None

    bad_audit[
        "closing_witness_id"
    ] = compute_closing_witness_id(
        bad_audit
    )

    audit_errors = validate_witness(
        bad_audit
    )

    if not any(
        "requires Audit witness reference"
        in error
        for error in audit_errors
    ):
        errors.append(
            "R4-E incorrectly permitted CLOSED witness without Audit reference"
        )

    bad_blocked = dict(
        blocked
    )

    bad_blocked[
        "blocking_reasons"
    ] = []

    bad_blocked[
        "closing_witness_id"
    ] = compute_closing_witness_id(
        bad_blocked
    )

    blocked_errors = validate_witness(
        bad_blocked
    )

    if not any(
        "requires blocking reasons"
        in error
        for error in blocked_errors
    ):
        errors.append(
            "R4-E incorrectly permitted BLOCKED witness without blocking reason"
        )

    changed = dict(
        witness
    )

    changed[
        "replay_coordinates"
    ] = {
        "coordinate": "observational:b"
    }

    changed[
        "closing_witness_id"
    ] = compute_closing_witness_id(
        changed
    )

    if (
        changed[
            "closing_witness_id"
        ]
        == witness[
            "closing_witness_id"
        ]
    ):
        errors.append(
            "material Closing Witness change did not change identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-E POST-CONVERGENCE CLOSURE / CLOSING WITNESS: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-E POST-CONVERGENCE CLOSURE / CLOSING WITNESS: PASS"
    )
    print(
        "Land / preserve state / remain conversational: LOCKED"
    )
    print(
        "No rebuild / no unnecessary re-analysis: ENFORCED"
    )
    print(
        "Closing Witness / lineage / replay coordinates: BOUND"
    )
    print(
        "Audit witness / same Room / Stick continuity: PRESERVED"
    )
    print(
        "Acknowledgment / celebration / repetition -> Reflight: REJECTED"
    )
    print(
        "Lifecycle mutation / Replay / Scar semantics: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
