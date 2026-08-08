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
    / "SCAR_REPLAY.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "runtime"
    / "scar_replay.schema.json"
)

R4G = (
    ROOT
    / "tools"
    / "validate_scar_record.py"
)

ACTIONS = {
    "REPLAY",
    "SUMMARIZE",
    "CONTINUE",
    "BRANCH",
    "CHALLENGE",
    "IGNORE_WITH_EVIDENCE",
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


def compute_scar_replay_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "scar_replay_id"
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


def validate_scar_replay(record):
    errors = []

    if (
        record.get("scar_replay_id")
        != compute_scar_replay_id(record)
    ):
        errors.append(
            "scar_replay_id does not recompute from Scar Replay Record"
        )

    action = record.get(
        "requested_action"
    )

    if action not in ACTIONS:
        errors.append(
            "invalid Scar Replay action"
        )

    eligibility = record.get(
        "action_eligibility"
    )

    if eligibility not in ELIGIBILITY:
        errors.append(
            "invalid Scar Replay eligibility"
        )

    for field in (
        "object_id",
        "scar_record_reference",
        "observer_reference",
        "requested_action",
        "action_basis",
        "historical_observational_coordinate",
        "historical_question_contract_reference",
        "historical_zone_reference",
        "historical_space_reference",
        "prior_movement_references",
        "scar_effect_evidence_references",
        "recorded_effect_references",
        "evidence_boundary",
        "evidence_ceiling",
        "cartography_reference",
        "stick_reference",
        "action_eligibility",
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
                f"Scar Replay requires {field}"
            )

    if (
        action == "REPLAY"
        and not record.get(
            "replay_envelope_reference"
        )
    ):
        errors.append(
            "REPLAY requires Replay Envelope reference"
        )

    if (
        action == "SUMMARIZE"
        and not record.get(
            "replay_envelope_reference"
        )
    ):
        errors.append(
            "SUMMARIZE requires Replay Envelope provenance"
        )

    if (
        action == "CONTINUE"
        and not record.get(
            "reflight_trigger_reference"
        )
    ):
        errors.append(
            "CONTINUE requires Reflight Trigger reference"
        )

    if (
        action == "BRANCH"
        and not record.get(
            "branch_control_reference"
        )
    ):
        errors.append(
            "BRANCH requires branch-control reference"
        )

    if (
        action == "CHALLENGE"
        and not record.get(
            "challenge_evidence_references"
        )
    ):
        errors.append(
            "CHALLENGE requires challenge evidence"
        )

    if (
        action == "IGNORE_WITH_EVIDENCE"
        and not record.get(
            "ignore_evidence_references"
        )
    ):
        errors.append(
            "IGNORE_WITH_EVIDENCE requires ignore evidence"
        )

    if (
        eligibility == "BLOCKED"
        and not record.get(
            "blocking_reasons"
        )
    ):
        errors.append(
            "BLOCKED Scar Replay requires blocking reasons"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R4-H Scar Replay contract"
        ),
        (
            SCHEMA,
            "R4-H Scar Replay schema"
        ),
        (
            R4G,
            "R4-G Scar Record validator"
        ),
    ):
        if not path.exists():
            errors.append(
                f"missing {label}"
            )

    if errors:
        return errors

    r4g = subprocess.run(
        [
            sys.executable,
            str(R4G),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if r4g.returncode != 0:
        errors.append(
            "R4-G dependency validation failed"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R4-H schema JSON: {exc}"
        ]

    schema_actions = set(
        schema
        .get("properties", {})
        .get("requested_action", {})
        .get("enum", [])
    )

    if schema_actions != ACTIONS:
        errors.append(
            "R4-H six-action source vocabulary is not locked"
        )

    schema_eligibility = set(
        schema
        .get("properties", {})
        .get("action_eligibility", {})
        .get("enum", [])
    )

    if schema_eligibility != ELIGIBILITY:
        errors.append(
            "R4-H action eligibility vocabulary is not locked"
        )

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "new_object_id",
        "branch_object_id",
        "lifecycle_transition_id",
        "publication_authorization",
        "canonical_promotion",
        "full_payload_hydration",
        "scar_deleted",
        "historical_state_replaced",
    }

    leaked = properties & forbidden

    if leaked:
        errors.append(
            "R4-H improperly absorbs object creation, deletion, "
            "lifecycle, publication, or hydration semantics: "
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
        "A Scar is evidence that Terrain has previously affected movement.",
        "Scar Replay allows a future observer to replay, summarize, continue, branch, challenge, or ignore with evidence without creating a new world merely to revisit the old one.",
        "These six action classes are native-v41 Scar Replay actions.",
        "Action type != authority.",
        "Action type != execution.",
        "Scar Replay MUST preserve the Scar Record.",
        "Scar Replay MUST NOT replace it.",
        "Revisit != new world.",
        "Historical observation != new object.",
        "Scar Replay != new Room.",
        "Observer change does not change Room identity.",
        "Preserved coordinate != reconstructed coordinate.",
        "Historical question != present question.",
        "Current perspective MUST NOT overwrite prior perspective.",
        "Scar Replay MUST NOT reduce the journey to only a warning or conclusion.",
        "Historical effect != current conclusion.",
        "REPLAY requires a Replay Envelope reference.",
        "Replay != Reflight.",
        "Summary != replacement.",
        "Summary != deletion.",
        "Summary != new canonical state.",
        "No Compression Out.",
        "CONTINUE requires a valid attributable Reflight Trigger reference.",
        "Scar existence alone is insufficient.",
        "CONTINUE != automatic Reflight.",
        "Reflight Trigger first.",
        "Continuation second.",
        "Scar Replay does not itself mint branch identity.",
        "BRANCH requires an attributable branch-control reference.",
        "Scar Replay BRANCH != new world.",
        "Perspective alone != branch.",
        "CHALLENGE requires non-empty challenge evidence.",
        "Challenge does not erase the original Scar.",
        "IGNORE_WITH_EVIDENCE requires non-empty ignore evidence.",
        "Ignoring the Scar does not delete it.",
        "Ignoring the Scar does not make it nonexistent.",
        "Ignore != erase.",
        "Ignore != absent.",
        "Ignore requires evidence.",
        "ELIGIBLE != execution.",
        "ELIGIBLE != authority.",
        "BLOCKED != nonexistent Scar.",
        "Historical record remains attributable.",
        "Current interpretation may differ.",
        "History != current interpretation.",
        "Scar Replay MUST NOT reconstruct an approximation.",
        "Historical geometry remains attributable.",
        "Scar Replay MUST preserve the Stick.",
        "Scar Replay MUST NOT sever analytical continuity.",
        "Current access != historical evidence use.",
        "Scar Replay != retrospective promotion.",
        "REPLAY != CONTINUE.",
        "SUMMARIZE != CONTINUE.",
        "CHALLENGE != automatic CONTINUE.",
        "IGNORE_WITH_EVIDENCE != automatic CONTINUE.",
        "Distinct object still requires affirmative evidence.",
        "Identity travels.",
        "Payload rests.",
        "Scar Replay != full reconstruction.",
        "Historical access != governing authority.",
        "ELIGIBLE != authorized execution.",
        "Scar Replay Record != Human Gate decision.",
        "Scar Replay != lifecycle transition.",
        "SUMMARIZE is not publication.",
        "CHALLENGE is not publication.",
        "IGNORE_WITH_EVIDENCE is not publication.",
        "Scar Replay Record != publication record.",
        "No Scar Replay action deletes the original Scar.",
        "Historical evidence remains auditable.",
        "Do not clone reality.",
        "R4-I owns Runtime-State Continuity / Cross-Operation Integrity.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in normalized
        ):
            errors.append(
                f"missing R4-H lock: {lock}"
            )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    base = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "scar_record_reference":
            "scar:a",
        "replay_envelope_reference":
            "replay:a",
        "observer_reference":
            "observer:future:a",
        "requested_action":
            "REPLAY",
        "action_basis": [
            "future observer requires attributable historical Scar context"
        ],
        "historical_observational_coordinate": {
            "coordinate": "scar:a"
        },
        "historical_question_contract_reference":
            "question-contract:a",
        "historical_zone_reference":
            "zone:a",
        "historical_space_reference":
            "space:a",
        "historical_transform_references": [
            "transform:a"
        ],
        "prior_movement_references": [
            "movement:a"
        ],
        "scar_effect_evidence_references": [
            "evidence:scar:a"
        ],
        "recorded_effect_references": [
            "effect:a"
        ],
        "evidence_boundary": {
            "scope": "historical-bounded"
        },
        "evidence_ceiling":
            "CEILING:A",
        "cartography_reference":
            "cartography:a",
        "stick_reference":
            "stick:a",
        "reflight_trigger_reference":
            None,
        "branch_control_reference":
            None,
        "challenge_evidence_references": [],
        "ignore_evidence_references": [],
        "action_eligibility":
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
            "scar:a",
            "replay:a",
            "movement:a",
            "evidence:scar:a",
            "cartography:a",
            "stick:a"
        ],
        "requested_at":
            "2026-08-07T20:55:00-04:00",
    }

    base[
        "scar_replay_id"
    ] = compute_scar_replay_id(
        base
    )

    errors.extend(
        validate_scar_replay(
            base
        )
    )

    vectors = [
        (
            "SUMMARIZE",
            {
                "replay_envelope_reference":
                    "replay:a"
            }
        ),
        (
            "CONTINUE",
            {
                "reflight_trigger_reference":
                    "reflight:a"
            }
        ),
        (
            "BRANCH",
            {
                "branch_control_reference":
                    "branch-control:a"
            }
        ),
        (
            "CHALLENGE",
            {
                "challenge_evidence_references": [
                    "evidence:challenge:a"
                ]
            }
        ),
        (
            "IGNORE_WITH_EVIDENCE",
            {
                "ignore_evidence_references": [
                    "evidence:ignore:a"
                ]
            }
        ),
    ]

    for action, changes in vectors:
        probe = dict(
            base
        )

        probe[
            "requested_action"
        ] = action

        probe[
            "reflight_trigger_reference"
        ] = None

        probe[
            "branch_control_reference"
        ] = None

        probe[
            "challenge_evidence_references"
        ] = []

        probe[
            "ignore_evidence_references"
        ] = []

        probe.update(
            changes
        )

        probe[
            "scar_replay_id"
        ] = compute_scar_replay_id(
            probe
        )

        probe_errors = validate_scar_replay(
            probe
        )

        if probe_errors:
            errors.append(
                f"valid Scar Replay action {action} rejected: "
                + "; ".join(
                    probe_errors
                )
            )

    no_continue_trigger = dict(
        base
    )

    no_continue_trigger[
        "requested_action"
    ] = "CONTINUE"

    no_continue_trigger[
        "reflight_trigger_reference"
    ] = None

    no_continue_trigger[
        "scar_replay_id"
    ] = compute_scar_replay_id(
        no_continue_trigger
    )

    continue_errors = validate_scar_replay(
        no_continue_trigger
    )

    if not any(
        "CONTINUE requires Reflight Trigger"
        in error
        for error in continue_errors
    ):
        errors.append(
            "R4-H incorrectly permitted CONTINUE without Reflight Trigger"
        )

    no_branch_control = dict(
        base
    )

    no_branch_control[
        "requested_action"
    ] = "BRANCH"

    no_branch_control[
        "branch_control_reference"
    ] = None

    no_branch_control[
        "scar_replay_id"
    ] = compute_scar_replay_id(
        no_branch_control
    )

    branch_errors = validate_scar_replay(
        no_branch_control
    )

    if not any(
        "BRANCH requires branch-control"
        in error
        for error in branch_errors
    ):
        errors.append(
            "R4-H incorrectly permitted BRANCH without branch control"
        )

    no_challenge_evidence = dict(
        base
    )

    no_challenge_evidence[
        "requested_action"
    ] = "CHALLENGE"

    no_challenge_evidence[
        "challenge_evidence_references"
    ] = []

    no_challenge_evidence[
        "scar_replay_id"
    ] = compute_scar_replay_id(
        no_challenge_evidence
    )

    challenge_errors = validate_scar_replay(
        no_challenge_evidence
    )

    if not any(
        "CHALLENGE requires challenge evidence"
        in error
        for error in challenge_errors
    ):
        errors.append(
            "R4-H incorrectly permitted CHALLENGE without evidence"
        )

    no_ignore_evidence = dict(
        base
    )

    no_ignore_evidence[
        "requested_action"
    ] = "IGNORE_WITH_EVIDENCE"

    no_ignore_evidence[
        "ignore_evidence_references"
    ] = []

    no_ignore_evidence[
        "scar_replay_id"
    ] = compute_scar_replay_id(
        no_ignore_evidence
    )

    ignore_errors = validate_scar_replay(
        no_ignore_evidence
    )

    if not any(
        "IGNORE_WITH_EVIDENCE requires ignore evidence"
        in error
        for error in ignore_errors
    ):
        errors.append(
            "R4-H incorrectly permitted evidence-free Ignore"
        )

    blocked = dict(
        base
    )

    blocked[
        "action_eligibility"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = []

    blocked[
        "scar_replay_id"
    ] = compute_scar_replay_id(
        blocked
    )

    blocked_errors = validate_scar_replay(
        blocked
    )

    if not any(
        "requires blocking reasons"
        in error
        for error in blocked_errors
    ):
        errors.append(
            "R4-H incorrectly permitted BLOCKED action without reason"
        )

    changed = dict(
        base
    )

    changed[
        "observer_reference"
    ] = "observer:future:b"

    changed[
        "scar_replay_id"
    ] = compute_scar_replay_id(
        changed
    )

    if (
        changed[
            "scar_replay_id"
        ]
        == base[
            "scar_replay_id"
        ]
    ):
        errors.append(
            "material Scar Replay change did not change identity"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R4-H SCAR REPLAY: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R4-H SCAR REPLAY: PASS"
    )
    print(
        "Replay / summarize / continue / branch / challenge / ignore: LOCKED"
    )
    print(
        "Future observer / same Room / preserved coordinate: LOCKED"
    )
    print(
        "Continue -> Reflight Trigger / Branch -> branch control: ENFORCED"
    )
    print(
        "Challenge / Ignore-with-evidence: EVIDENCE REQUIRED"
    )
    print(
        "Scar history / Cartography / Stick / provenance: PRESERVED"
    )
    print(
        "Clone / erase / approximate reconstruction / silent authority: REJECTED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
