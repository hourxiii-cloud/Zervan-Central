#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "RAVEN_HUMAN_GATE_PUBLICATION_ACTION_BOUNDARY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "human_gate_transition_decision.schema.json"
)

R5E = (
    ROOT
    / "contracts"
    / "pipeline"
    / "MC_RAVEN_REPRESENTATION_REPORT_BINDING.md"
)

HUMAN_GATE = (
    ROOT
    / "governance"
    / "human_gate_authority_boundary.md"
)

RAVEN = (
    ROOT
    / "Modules"
    / "Raven"
    / "raven_contract.md"
)

TRANSITION_CLASSES = {
    "PUBLICATION",
    "EXTERNAL_DEPLOYMENT",
    "PRODUCTION_EXECUTION",
    "SYSTEM_POPULATION",
    "PACKAGE_PROMOTION",
    "COMPLIANCE_CLAIM",
    "LEGAL_FINDING",
    "CERTIFICATION_CLAIM",
    "OPERATIONAL_AUTHORITY",
    "DISCIPLINARY_OR_HR_ACTION",
    "AUTHORITY_BEARING_AUTOMATION",
    "IRREVERSIBLE_EXTERNAL_CHANGE",
}

DECISION_STATES = {
    "PENDING",
    "APPROVED",
    "DENIED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_human_gate_decision_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "human_gate_decision_id"
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


def validate_record(record):
    errors = []

    if (
        record.get("human_gate_decision_id")
        != compute_human_gate_decision_id(record)
    ):
        errors.append(
            "human_gate_decision_id does not recompute from record"
        )

    for field in (
        "raven_representation_id",
        "mc_evaluation_id",
        "ccr_id",
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "coordinate_reference",
        "transition_class",
        "transition_target",
        "requested_scope",
        "mc_admissibility_references",
        "lineage_reference",
        "provenance_route",
        "decision_state",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Human Gate decision requires {field}"
            )

    if (
        record.get("transition_class")
        not in TRANSITION_CLASSES
    ):
        errors.append(
            "unknown Human Gate transition class"
        )

    decision_state = record.get(
        "decision_state"
    )

    if decision_state not in DECISION_STATES:
        errors.append(
            "invalid Human Gate decision state"
        )

    if (
        decision_state in {
            "APPROVED",
            "DENIED",
        }
        and not record.get(
            "human_decision_reference"
        )
    ):
        errors.append(
            f"{decision_state} requires human_decision_reference"
        )

    if (
        decision_state in {
            "APPROVED",
            "DENIED",
        }
        and not record.get(
            "decision_time_reference"
        )
    ):
        errors.append(
            f"{decision_state} requires decision_time_reference"
        )

    if (
        decision_state == "DENIED"
        and not record.get(
            "decision_reasons"
        )
    ):
        errors.append(
            "DENIED requires decision reasons"
        )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "Zervan authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "Human Gate state must remain ACTIVE"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-F contract"
        ),
        (
            SCHEMA,
            "R5-F schema"
        ),
        (
            R5E,
            "R5-E Raven binding"
        ),
        (
            HUMAN_GATE,
            "Human Gate boundary"
        ),
        (
            RAVEN,
            "Raven contract"
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
        "Raven may prepare representation.",
        "Raven may prepare a publication-ready report.",
        "Raven does not authorize authority-bearing movement.",
        "Human Gate controls authority-bearing movement.",
        "Human Gate decision != execution.",
        "R5-F owns Raven Representation -> Human Gate Transition Decision.",
        "R5-F does not execute an approved transition.",
        "R5-G owns Decision Option Lineage.",
        "Explicit human approval is required for authority-bearing movement.",
        "Raven output != Human Gate decision.",
        "Publication-ready != approved.",
        "One Human Gate approval applies only to the explicitly requested transition.",
        "Approval for one transition MUST NOT silently authorize another.",
        "PENDING means no authority-bearing movement is authorized.",
        "No decision state may be inferred from silence.",
        "No default approval exists.",
        "Approval scope != general authority.",
        "Human approval governs movement.",
        "Human approval does not manufacture evidence.",
        "Approval != execution.",
        "Permission != movement.",
        "Decision record != external side effect.",
        "DENIED != false analysis.",
        "DENIED != erased report.",
        "PENDING != implied approval.",
        "PENDING != timeout approval.",
        "Human Gate approval does not silently rewrite MC classification.",
        "Approval != MC reinterpretation.",
        "Human decision != evidence admission.",
        "Human approval != higher claim ceiling.",
        "Human Gate decision does not create a new Room.",
        "Decision reference != Registry transition.",
        "Publication-ready != published.",
        "Approval of one report version does not silently approve another version.",
        "Human Gate approval != persistent autonomous authority.",
        "Validation != promotion.",
        "Repository presence != authority.",
        "Gate approval != evidentiary proof.",
        "Authority to issue a claim != truth of the claim.",
        "Decision identity != truth.",
        "Decision identity != execution.",
        "Receipt != authority.",
        "Hash != truth.",
        "Write access != Human Gate approval.",
        "Commit author != Human Gate authority.",
        "Human authorization != system authority.",
        "Prior approval != standing approval.",
        "Fail closed.",
        "No default approval.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in text
        ):
            errors.append(
                f"missing R5-F lock: {lock}"
            )

    gate = normalized(
        HUMAN_GATE
    )

    gate_locks = [
        "Human Gate preserves the boundary between analysis and authority-bearing action.",
        "Zervan does not authorize action by itself.",
        "Authority-bearing movement requires explicit human approval.",
        "Human authorization permits authority-bearing action.",
        "Prepared movement is not execution.",
        "Local validation is not authority.",
        "Human Gate controls authority.",
    ]

    for lock in gate_locks:
        if (
            " ".join(lock.split())
            not in gate
        ):
            errors.append(
                f"existing Human Gate semantic missing: {lock}"
            )

    raven = normalized(
        RAVEN
    )

    raven_locks = [
        "Authority Scope: REPORTING ONLY",
        "Generate actions that execute automatically",
        "Raven is the system's voice — not its will.",
    ]

    for lock in raven_locks:
        if (
            " ".join(lock.split())
            not in raven
        ):
            errors.append(
                f"existing Raven authority semantic missing: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-F schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "execution_result",
        "publication_result",
        "external_side_effect",
        "room_lifecycle_transition",
        "evidence_boundary_override",
        "evidence_ceiling_override",
        "mc_disposition_override",
        "canonical_truth",
        "system_authority",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-F improperly absorbs execution/truth/Room semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    record = {
        "schema_version":
            "1.0",
        "raven_representation_id":
            "sha512:" + "1" * 128,
        "mc_evaluation_id":
            "sha512:" + "2" * 128,
        "ccr_id":
            "sha512:" + "3" * 128,
        "object_id":
            "sha512:" + "4" * 128,
        "room_revision_id":
            "revision:a",
        "room_state_root":
            "sha512:" + "5" * 128,
        "authorized_view_root":
            "sha512:" + "6" * 128,
        "evidence_boundary_reference":
            "boundary:a",
        "evidence_ceiling_reference":
            "ceiling:a",
        "coordinate_reference":
            "coordinate:a",
        "transition_class":
            "PUBLICATION",
        "transition_target":
            "report:a",
        "requested_scope":
            "publish exact Raven representation report:a",
        "mc_admissibility_references": [
            "mc-class:publication:a"
        ],
        "governance_constraint_references": [
            "governance:a"
        ],
        "human_decision_reference":
            None,
        "decision_state":
            "PENDING",
        "decision_reasons": [],
        "lineage_reference":
            "lineage:a",
        "provenance_route": [
            "sha512:" + "4" * 128,
            "sha512:" + "3" * 128,
            "sha512:" + "2" * 128,
            "sha512:" + "1" * 128,
            "human-gate-request:a"
        ],
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "decision_time_reference":
            None,
    }

    record[
        "human_gate_decision_id"
    ] = compute_human_gate_decision_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    approved_without_human = json.loads(
        json.dumps(record)
    )

    approved_without_human[
        "decision_state"
    ] = "APPROVED"

    approved_without_human[
        "human_gate_decision_id"
    ] = compute_human_gate_decision_id(
        approved_without_human
    )

    if not any(
        "APPROVED requires human_decision_reference"
        in error
        for error in validate_record(
            approved_without_human
        )
    ):
        errors.append(
            "R5-F incorrectly permitted approval without human attribution"
        )

    approved = json.loads(
        json.dumps(record)
    )

    approved[
        "decision_state"
    ] = "APPROVED"

    approved[
        "human_decision_reference"
    ] = "human-decision:a"

    approved[
        "decision_time_reference"
    ] = "decision-time:a"

    approved[
        "human_gate_decision_id"
    ] = compute_human_gate_decision_id(
        approved
    )

    approved_errors = validate_record(
        approved
    )

    if approved_errors:
        errors.append(
            "R5-F rejected valid attributed approval: "
            + "; ".join(
                approved_errors
            )
        )

    denied_without_reason = json.loads(
        json.dumps(approved)
    )

    denied_without_reason[
        "decision_state"
    ] = "DENIED"

    denied_without_reason[
        "decision_reasons"
    ] = []

    denied_without_reason[
        "human_gate_decision_id"
    ] = compute_human_gate_decision_id(
        denied_without_reason
    )

    if not any(
        "DENIED requires decision reasons"
        in error
        for error in validate_record(
            denied_without_reason
        )
    ):
        errors.append(
            "R5-F incorrectly permitted unexplained denial"
        )

    unknown_transition = json.loads(
        json.dumps(record)
    )

    unknown_transition[
        "transition_class"
    ] = "DO_WHATEVER"

    unknown_transition[
        "human_gate_decision_id"
    ] = compute_human_gate_decision_id(
        unknown_transition
    )

    if not any(
        "unknown Human Gate transition class"
        in error
        for error in validate_record(
            unknown_transition
        )
    ):
        errors.append(
            "R5-F incorrectly defaulted unknown transition class"
        )

    promoted = json.loads(
        json.dumps(record)
    )

    promoted[
        "authority_state"
    ] = "AUTONOMOUS"

    promoted[
        "human_gate_decision_id"
    ] = compute_human_gate_decision_id(
        promoted
    )

    if not any(
        "Zervan authority_state must remain NONE"
        in error
        for error in validate_record(
            promoted
        )
    ):
        errors.append(
            "R5-F incorrectly promoted Zervan system authority"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-F RAVEN -> HUMAN GATE PUBLICATION / ACTION BOUNDARY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-F RAVEN -> HUMAN GATE PUBLICATION / ACTION BOUNDARY: PASS"
    )
    print(
        "Raven representation / MC / CCR / Room lineage: BOUND"
    )
    print(
        "PENDING / APPROVED / DENIED Human Gate decision: ENFORCED"
    )
    print(
        "Exact transition class / target / scope binding: REQUIRED"
    )
    print(
        "Evidence boundary / claim ceiling / Room state: PRESERVED"
    )
    print(
        "Approval reuse / silent default / self-authorization: REJECTED"
    )
    print(
        "Human Gate approval -> execution equivalence: REJECTED"
    )
    print(
        "Zervan autonomous authority: NONE"
    )
    print(
        "R5-G Decision Option Lineage: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
