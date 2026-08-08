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
    / "REFLIGHT_TRIGGER.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "runtime"
    / "reflight_trigger.schema.json"
)

R4C = (
    ROOT
    / "tools"
    / "validate_landing_witness.py"
)

TRIGGER_TYPES = {
    "NEW_EVIDENCE",
    "CONTRADICTION",
    "CHANGED_QUESTION",
    "CHANGED_EVIDENCE_CEILING",
    "SIGNAL_SPLIT",
    "SIGNAL_CONVERGENCE",
    "CHALLENGED_CONCLUSION",
    "NEWLY_REACHABLE_SURFACE",
    "MATERIALLY_DIFFERENT_RENDERING_REQUESTED",
}

ELIGIBILITY = {
    "ELIGIBLE",
    "BLOCKED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_reflight_trigger_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "reflight_trigger_id"
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


def validate_trigger(record):
    errors = []

    if (
        record.get("reflight_trigger_id")
        != compute_reflight_trigger_id(record)
    ):
        errors.append(
            "reflight_trigger_id does not recompute from trigger"
        )

    trigger_type = record.get(
        "trigger_type"
    )

    if trigger_type not in TRIGGER_TYPES:
        errors.append(
            "invalid Reflight trigger type"
        )

    if record.get(
        "reflight_eligibility"
    ) not in ELIGIBILITY:
        errors.append(
            "invalid Reflight eligibility"
        )

    for field in (
        "object_id",
        "landing_witness_reference",
        "trigger_type",
        "trigger_subject",
        "prior_question",
        "current_question",
        "prior_evidence_ceiling",
        "current_evidence_ceiling",
        "material_change_basis",
        "evidence_boundary",
        "representation_reference",
        "cartography_reference",
        "stick_reference",
        "readiness_reference",
        "reflight_eligibility",
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
                f"Reflight Trigger requires {field}"
            )

    evidence = record.get(
        "trigger_evidence_references",
        []
    )

    if (
        trigger_type
        in {
            "NEW_EVIDENCE",
            "CONTRADICTION",
        }
        and not evidence
    ):
        errors.append(
            f"{trigger_type} requires trigger evidence"
        )

    if (
        trigger_type
        == "CHANGED_QUESTION"
        and record.get("prior_question")
        == record.get("current_question")
    ):
        errors.append(
            "CHANGED_QUESTION requires materially changed question"
        )

    if (
        trigger_type
        == "CHANGED_EVIDENCE_CEILING"
        and record.get("prior_evidence_ceiling")
        == record.get("current_evidence_ceiling")
    ):
        errors.append(
            "CHANGED_EVIDENCE_CEILING requires changed ceiling"
        )

    if (
        trigger_type
        in {
            "SIGNAL_SPLIT",
            "SIGNAL_CONVERGENCE",
        }
        and (
            not record.get(
                "prior_signal_state_reference"
            )
            or not record.get(
                "current_signal_state_reference"
            )
        )
    ):
        errors.append(
            f"{trigger_type} requires prior and current signal-state references"
        )

    if (
        trigger_type
        == "CHALLENGED_CONCLUSION"
        and not record.get(
            "challenged_conclusion_reference"
        )
    ):
        errors.append(
            "CHALLENGED_CONCLUSION requires challenged conclusion reference"
        )

    if (
        trigger_type
        == "NEWLY_REACHABLE_SURFACE"
        and not record.get(
            "newly_reachable_surface_reference"
        )
    ):
        errors.append(
            "NEWLY_REACHABLE_SURFACE requires surface reference"
        )

    if (
        trigger_type
        == "MATERIALLY_DIFFERENT_RENDERING_REQUESTED"
        and not record.get(
            "requested_rendering_reference"
        )
    ):
        errors.append(
            "MATERIALLY_DIFFERENT_RENDERING_REQUESTED "
            "requires requested rendering reference"
        )

    if (
        record.get("reflight_eligibility")
        == "BLOCKED"
        and not record.get(
            "blocking_reasons"
        )
    ):
        errors.append(
            "BLOCKED Reflight Trigger requires blocking reasons"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R4-D Reflight Trigger contract"
        ),
        (
            SCHEMA,
            "R4-D Reflight Trigger schema"
        ),
        (
            R4C,
            "R4-C Landing Witness validator"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    r4c = subprocess.run(
        [
            sys.executable,
            str(R4C),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if r4c.returncode != 0:
        errors.append(
            "R4-C dependency validation failed"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-D schema JSON: {exc}"
        ]

    schema_types = set(
        schema
        .get("properties", {})
        .get("trigger_type", {})
        .get("enum", [])
    )

    if schema_types != TRIGGER_TYPES:
        errors.append(
            "R4-D source trigger vocabulary is not locked"
        )

    schema_eligibility = set(
        schema
        .get("properties", {})
        .get("reflight_eligibility", {})
        .get("enum", [])
    )

    if schema_eligibility != ELIGIBILITY:
        errors.append(
            "R4-D eligibility vocabulary is not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "reflight_execution_id",
        "movement_state",
        "new_mission_id",
        "selected_force",
        "formation_selection_id",
        "hydration_request_id",
        "closing_witness_id",
        "replay_envelope_id",
        "scar_record_id",
        "new_room_object_id",
        "canonical_promotion",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R4-D improperly absorbs execution or downstream semantics: "
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
        "Reflight requires a real trigger.",
        "New evidence is a valid trigger.",
        "Contradiction is a valid trigger.",
        "Changed question is a valid trigger.",
        "Changed evidence ceiling is a valid trigger.",
        "Signal split is a valid trigger.",
        "Signal convergence is a valid trigger.",
        "Challenged conclusion is a valid trigger.",
        "Newly reachable surface is a valid trigger.",
        "Explicitly requested materially different rendering is a valid trigger.",
        "Acknowledgment != Reflight trigger.",
        "Repetition != Reflight trigger.",
        "Celebration != Reflight trigger.",
        "Affect != Reflight trigger.",
        "Conversation continuing != Reflight trigger.",
        "Capability availability != Reflight trigger.",
        "Trigger != execution.",
        "Landing first.",
        "Trigger second.",
        "Reflight MUST NOT rebuild an approximate Room.",
        "Reflight != new Room.",
        "Repeated presentation of existing evidence is not new evidence.",
        "Contradiction != automatic conclusion reversal.",
        "Changed question does not create a new Room.",
        "Changed evidence ceiling != automatic evidence promotion.",
        "Signal split != confidence.",
        "Convergence != consensus by repetition.",
        "Convergence != truth by vote.",
        "Challenge != automatic reversal.",
        "Possible != reachable.",
        "A different format alone is insufficient unless the requested rendering requires materially different analytical traversal.",
        "No material change = no Reflight.",
        "ELIGIBLE != executed.",
        "BLOCKED != nonexistent.",
        "Trigger does not manufacture readiness.",
        "A trigger cannot silently broaden evidence access.",
        "Trigger != Cartography mutation.",
        "Reflight MUST preserve the Stick.",
        "Trigger != Restriction reversal.",
        "Trigger != Constriction reversal.",
        "Trigger != Collapse reversal.",
        "Trigger != Capability Mission Request.",
        "Trigger != force selection.",
        "Trigger != Formation Selection Record.",
        "Trigger != Hydration Request.",
        "Signal != trigger.",
        "Notification != evidence.",
        "ELIGIBLE != authorized execution.",
        "Trigger != Human Gate decision.",
        "Conversation can continue while analytical movement remains stopped.",
        "No unnecessary re-analysis.",
        "No unnecessary rebuild.",
        "Trigger != Reflight execution.",
        "R4-E owns Closing Witness / Post-Convergence Closure.",
        "Reflight != Replay.",
        "Trigger != Replay Envelope.",
        "No Closing Witness semantics yet.",
        "No Replay semantics yet.",
        "No Scar Replay semantics yet.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in normalized
        ):
            errors.append(
                f"missing R4-D lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    trigger = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "landing_witness_reference":
            "landing:a",
        "trigger_type":
            "NEW_EVIDENCE",
        "trigger_subject":
            "new provenance-bearing evidence changes supported terrain",
        "trigger_evidence_references": [
            "evidence:new:a"
        ],
        "prior_question":
            "which supported state remained at Landing?",
        "current_question":
            "does new evidence change the supported state?",
        "prior_evidence_ceiling":
            "CEILING:A",
        "current_evidence_ceiling":
            "CEILING:A",
        "prior_signal_state_reference":
            None,
        "current_signal_state_reference":
            None,
        "challenged_conclusion_reference":
            None,
        "newly_reachable_surface_reference":
            None,
        "requested_rendering_reference":
            None,
        "material_change_basis": [
            "evidence:new:a was not part of the landed analytical condition",
            "the evidence is material to the preserved question"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "representation_reference":
            "representation:a",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "readiness_reference":
            "readiness:a",
        "reflight_eligibility":
            "ELIGIBLE",
        "blocking_reasons": [],
        "governance_reference":
            "governance:a",
        "authorization_reference":
            "authorization:a",
        "human_gate_reference":
            "human-gate:a",
        "provenance_route": [
            object_id,
            "landing:a",
            "evidence:new:a",
            "cartography:a",
            "stick:a"
        ],
        "triggered_at":
            "2026-08-07T20:25:00-04:00",
    }

    trigger[
        "reflight_trigger_id"
    ] = compute_reflight_trigger_id(
        trigger
    )

    errors.extend(
        validate_trigger(
            trigger
        )
    )

    trigger_vectors = [
        (
            "CONTRADICTION",
            {
                "trigger_evidence_references": [
                    "evidence:contradiction:a"
                ]
            }
        ),
        (
            "CHANGED_QUESTION",
            {
                "prior_question":
                    "question:a",
                "current_question":
                    "materially different question:b"
            }
        ),
        (
            "CHANGED_EVIDENCE_CEILING",
            {
                "prior_evidence_ceiling":
                    "CEILING:A",
                "current_evidence_ceiling":
                    "CEILING:B"
            }
        ),
        (
            "SIGNAL_SPLIT",
            {
                "prior_signal_state_reference":
                    "signal:single:a",
                "current_signal_state_reference":
                    "signal:split:a"
            }
        ),
        (
            "SIGNAL_CONVERGENCE",
            {
                "prior_signal_state_reference":
                    "signal:split:a",
                "current_signal_state_reference":
                    "signal:converged:a"
            }
        ),
        (
            "CHALLENGED_CONCLUSION",
            {
                "challenged_conclusion_reference":
                    "conclusion:a"
            }
        ),
        (
            "NEWLY_REACHABLE_SURFACE",
            {
                "newly_reachable_surface_reference":
                    "surface:new:a"
            }
        ),
        (
            "MATERIALLY_DIFFERENT_RENDERING_REQUESTED",
            {
                "requested_rendering_reference":
                    "rendering:materially-different:a"
            }
        ),
    ]

    for trigger_type, changes in trigger_vectors:
        probe = dict(
            trigger
        )

        probe[
            "trigger_type"
        ] = trigger_type

        probe[
            "trigger_evidence_references"
        ] = []

        probe[
            "prior_signal_state_reference"
        ] = None

        probe[
            "current_signal_state_reference"
        ] = None

        probe[
            "challenged_conclusion_reference"
        ] = None

        probe[
            "newly_reachable_surface_reference"
        ] = None

        probe[
            "requested_rendering_reference"
        ] = None

        probe.update(
            changes
        )

        probe[
            "reflight_trigger_id"
        ] = compute_reflight_trigger_id(
            probe
        )

        probe_errors = validate_trigger(
            probe
        )

        if probe_errors:
            errors.append(
                f"valid source Reflight vector {trigger_type} rejected: "
                + "; ".join(probe_errors)
            )

    invalid_changed_question = dict(
        trigger
    )

    invalid_changed_question[
        "trigger_type"
    ] = "CHANGED_QUESTION"

    invalid_changed_question[
        "trigger_evidence_references"
    ] = []

    invalid_changed_question[
        "current_question"
    ] = invalid_changed_question[
        "prior_question"
    ]

    invalid_changed_question[
        "reflight_trigger_id"
    ] = compute_reflight_trigger_id(
        invalid_changed_question
    )

    invalid_errors = validate_trigger(
        invalid_changed_question
    )

    if not any(
        "materially changed question"
        in error
        for error in invalid_errors
    ):
        errors.append(
            "R4-D incorrectly permitted unchanged question as Reflight trigger"
        )

    blocked = dict(
        trigger
    )

    blocked[
        "reflight_eligibility"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = []

    blocked[
        "reflight_trigger_id"
    ] = compute_reflight_trigger_id(
        blocked
    )

    blocked_errors = validate_trigger(
        blocked
    )

    if not any(
        "requires blocking reasons"
        in error
        for error in blocked_errors
    ):
        errors.append(
            "R4-D incorrectly permitted BLOCKED trigger without reason"
        )

    changed = dict(
        trigger
    )

    changed[
        "trigger_type"
    ] = "CONTRADICTION"

    changed[
        "trigger_evidence_references"
    ] = [
        "evidence:contradiction:b"
    ]

    changed[
        "reflight_trigger_id"
    ] = compute_reflight_trigger_id(
        changed
    )

    if (
        changed[
            "reflight_trigger_id"
        ]
        == trigger[
            "reflight_trigger_id"
        ]
    ):
        errors.append(
            "material Reflight Trigger change did not change identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-D REFLIGHT TRIGGER: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-D REFLIGHT TRIGGER: PASS"
    )
    print(
        "Nine source Reflight trigger classes: LOCKED"
    )
    print(
        "Landing -> material change -> eligibility: ENFORCED"
    )
    print(
        "Acknowledgment / repetition / affect / continuation: REJECTED"
    )
    print(
        "Same Room / Cartography / Stick / readiness: PRESERVED"
    )
    print(
        "Trigger != execution / authority / force / formation: LOCKED"
    )
    print(
        "Closing Witness / Replay / Scar Replay: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
