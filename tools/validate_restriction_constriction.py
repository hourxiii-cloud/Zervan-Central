#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "runtime"
    / "RESTRICTION_CONSTRICTION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "runtime"
    / "restriction_constriction_record.schema.json"
)

RING3 = (
    ROOT
    / "tools"
    / "validate_ring3.py"
)

SHA512_RE = re.compile(
    r"^sha512:[0-9a-f]{128}$"
)

OPERATIONS = {
    "RESTRICTION",
    "CONSTRICTION",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_record_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "restriction_constriction_id"
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
        record.get(
            "restriction_constriction_id"
        )
        != compute_record_id(record)
    ):
        errors.append(
            "restriction_constriction_id does not recompute from record"
        )

    operation = record.get(
        "operation_type"
    )

    if operation not in OPERATIONS:
        errors.append(
            "invalid Restriction / Constriction operation type"
        )

    for field in (
        "object_id",
        "active_question",
        "mission_reference",
        "representation_reference",
        "evidence_references",
        "pre_supported_states",
        "post_supported_states",
        "operation_basis",
        "evidence_boundary",
        "evidence_ceiling",
        "provenance_anchors",
        "representation_history_references",
        "cartography_reference",
        "stick_reference",
        "return_state_reference",
        "governance_reference",
        "authorization_reference",
        "provenance_route",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Restriction / Constriction Record requires {field}"
            )

    pre = set(
        record.get(
            "pre_supported_states",
            []
        )
    )

    post = set(
        record.get(
            "post_supported_states",
            []
        )
    )

    removed = set(
        record.get(
            "removed_from_support_states",
            []
        )
    )

    if not post.issubset(
        pre
    ):
        errors.append(
            "post-supported states must be a subset of pre-supported states"
        )

    if not removed.issubset(
        pre
    ):
        errors.append(
            "removed-from-support states must originate in pre-supported states"
        )

    overlap = (
        post
        & removed
    )

    if overlap:
        errors.append(
            "state cannot be both post-supported and removed from support"
        )

    expected_removed = (
        pre
        - post
    )

    if removed != expected_removed:
        errors.append(
            "removed-from-support states must exactly equal pre minus post"
        )

    if len(
        post
    ) >= len(
        pre
    ):
        errors.append(
            "Restriction / Constriction must reduce the supported-state set"
        )

    if (
        operation == "CONSTRICTION"
        and not record.get(
            "further_evidence_references"
        )
    ):
        errors.append(
            "CONSTRICTION requires further evidence"
        )

    if (
        operation == "CONSTRICTION"
        and not record.get(
            "prior_operation_reference"
        )
    ):
        errors.append(
            "CONSTRICTION requires prior operation reference"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R4-A Restriction / Constriction contract"
        ),
        (
            SCHEMA,
            "R4-A Restriction / Constriction schema"
        ),
        (
            RING3,
            "Ring 3 aggregate validator"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    ring3 = subprocess.run(
        [
            sys.executable,
            str(RING3),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if ring3.returncode != 0:
        errors.append(
            "Ring 3 dependency validation failed"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-A schema JSON: {exc}"
        ]

    operations = set(
        schema
        .get("properties", {})
        .get("operation_type", {})
        .get("enum", [])
    )

    if operations != OPERATIONS:
        errors.append(
            "R4-A operation vocabulary is not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "collapse_boundary_id",
        "landing_witness_id",
        "reflight_trigger_id",
        "closing_witness_id",
        "replay_envelope_id",
        "scar_record_id",
        "lifecycle_transition_id",
        "formation_selection_id",
        "occupancy_mutation",
        "canonical_promotion",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R4-A improperly absorbs downstream or foreign semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    contract_text = CONTRACT.read_text(
        encoding="utf-8"
    )

    normalized = " ".join(
        contract_text.split()
    )

    locks = [
        "One Room Object.",
        "Multiple Evidence-Compatible States.",
        "Evidence.",
        "Restriction.",
        "Fewer Supported States.",
        "Further Evidence.",
        "Constriction.",
        "Most Correct Supported State.",
        "Every valid analytical operation shall reduce uncertainty without reducing provenance.",
        "Restriction is not deletion.",
        "Perspective is not authority.",
        "Supported-state change != object-identity change.",
        "Operation type != lifecycle state.",
        "Removed from current support != deleted.",
        "Removed from current support != impossible forever.",
        "Most correct supported != absolute truth.",
        "Most correct supported != decision authority.",
        "Post-operation supported states MUST be a subset of pre-operation supported states.",
        "Restriction / Constriction narrows current support.",
        "Historical support != current support.",
        "Evidence drives narrowing.",
        "Preference does not.",
        "Perspective does not.",
        "Convenience does not.",
        "Narrative neatness does not.",
        "Constriction without further evidence is prohibited.",
        "Repeated assertion != further evidence.",
        "Agreement != further evidence.",
        "Mission is not evidence.",
        "Question is not evidence.",
        "Excluded != absent.",
        "Restricted != nonexistent.",
        "Narrower state count does not raise claim authority.",
        "State-count reduction != confidence promotion.",
        "State-count reduction != publication authority.",
        "No provenance loss for analytical convenience.",
        "Representation does not create truth authority.",
        "State reduction != Cartographic deletion.",
        "Reduction MUST NOT sever analytical continuity.",
        "Reconstructibility != mutation authority.",
        "Evidence narrowing cannot override policy.",
        "Technical capability != authority.",
        "Write capability != authority.",
        "Runtime-state operation != lifecycle transition.",
        "State narrowing != presence.",
        "Restriction != Formation Selection.",
        "Constriction != Formation Selection.",
        "Hydration != Restriction.",
        "Hydration != Constriction.",
        "Notification != evidence.",
        "Restriction != Collapse.",
        "Constriction != Collapse.",
        "R4-B owns Collapse Boundary.",
        "Narrowing != compression out.",
        "No Collapse semantics yet.",
        "No Landing semantics yet.",
        "No Reflight semantics yet.",
        "No Closing Witness semantics yet.",
        "No Replay semantics yet.",
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
                f"missing R4-A lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    restriction = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "operation_type":
            "RESTRICTION",
        "active_question":
            "which evidence-compatible states remain supported?",
        "mission_reference":
            "mission:a",
        "representation_reference":
            "representation:a",
        "prior_operation_reference":
            None,
        "evidence_references": [
            "evidence:a"
        ],
        "further_evidence_references": [],
        "pre_supported_states": [
            "STATE_A",
            "STATE_B",
            "STATE_C"
        ],
        "post_supported_states": [
            "STATE_A",
            "STATE_B"
        ],
        "removed_from_support_states": [
            "STATE_C"
        ],
        "unresolved_states": [
            "STATE_A",
            "STATE_B"
        ],
        "operation_basis": [
            "evidence:a no longer supports STATE_C"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "provenance_anchors": [
            "provenance:a"
        ],
        "representation_history_references": [
            "representation:a"
        ],
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "return_state_reference":
            "supported-state-set:pre:a",
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "mission:a",
            "evidence:a",
            "representation:a",
            "stick:a"
        ],
        "operated_at":
            "2026-08-07T20:00:00-04:00",
    }

    restriction[
        "restriction_constriction_id"
    ] = compute_record_id(
        restriction
    )

    if not SHA512_RE.fullmatch(
        restriction[
            "restriction_constriction_id"
        ]
    ):
        errors.append(
            "restriction_constriction_id is not canonical SHA-512"
        )

    errors.extend(
        validate_record(
            restriction
        )
    )

    constriction = dict(
        restriction
    )

    constriction[
        "operation_type"
    ] = "CONSTRICTION"

    constriction[
        "prior_operation_reference"
    ] = restriction[
        "restriction_constriction_id"
    ]

    constriction[
        "evidence_references"
    ] = [
        "evidence:a",
        "evidence:b"
    ]

    constriction[
        "further_evidence_references"
    ] = [
        "evidence:b"
    ]

    constriction[
        "pre_supported_states"
    ] = [
        "STATE_A",
        "STATE_B"
    ]

    constriction[
        "post_supported_states"
    ] = [
        "STATE_A"
    ]

    constriction[
        "removed_from_support_states"
    ] = [
        "STATE_B"
    ]

    constriction[
        "unresolved_states"
    ] = []

    constriction[
        "operation_basis"
    ] = [
        "further evidence:b no longer supports STATE_B"
    ]

    constriction[
        "return_state_reference"
    ] = restriction[
        "restriction_constriction_id"
    ]

    constriction[
        "provenance_route"
    ] = [
        object_id,
        restriction[
            "restriction_constriction_id"
        ],
        "evidence:b",
        "stick:a"
    ]

    constriction[
        "restriction_constriction_id"
    ] = compute_record_id(
        constriction
    )

    errors.extend(
        validate_record(
            constriction
        )
    )

    invalid_new_state = dict(
        restriction
    )

    invalid_new_state[
        "post_supported_states"
    ] = [
        "STATE_A",
        "STATE_NEW"
    ]

    invalid_new_state[
        "removed_from_support_states"
    ] = [
        "STATE_B",
        "STATE_C"
    ]

    invalid_new_state[
        "restriction_constriction_id"
    ] = compute_record_id(
        invalid_new_state
    )

    invalid_errors = validate_record(
        invalid_new_state
    )

    if not any(
        "subset of pre-supported"
        in error
        for error in invalid_errors
    ):
        errors.append(
            "R4-A incorrectly permitted invention of newly supported state"
        )

    no_further_evidence = dict(
        constriction
    )

    no_further_evidence[
        "further_evidence_references"
    ] = []

    no_further_evidence[
        "restriction_constriction_id"
    ] = compute_record_id(
        no_further_evidence
    )

    no_further_errors = validate_record(
        no_further_evidence
    )

    if not any(
        "requires further evidence"
        in error
        for error in no_further_errors
    ):
        errors.append(
            "R4-A incorrectly permitted Constriction without further evidence"
        )

    changed = dict(
        restriction
    )

    changed[
        "post_supported_states"
    ] = [
            "STATE_A"
    ]

    changed[
        "removed_from_support_states"
    ] = [
        "STATE_B",
        "STATE_C"
    ]

    changed[
        "restriction_constriction_id"
    ] = compute_record_id(
        changed
    )

    if (
        changed[
            "restriction_constriction_id"
        ]
        == restriction[
            "restriction_constriction_id"
        ]
    ):
        errors.append(
            "material supported-state change did not change record identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-A RESTRICTION / CONSTRICTION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-A RESTRICTION / CONSTRICTION: PASS"
    )
    print(
        "One Room / supported-state narrowing: LOCKED"
    )
    print(
        "Restriction -> fewer supported states: ENFORCED"
    )
    print(
        "Further evidence -> Constriction: ENFORCED"
    )
    print(
        "Provenance / representation history / Stick: PRESERVED"
    )
    print(
        "Deletion / state invention / confidence promotion: REJECTED"
    )
    print(
        "Collapse / Landing / Reflight / Replay: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
