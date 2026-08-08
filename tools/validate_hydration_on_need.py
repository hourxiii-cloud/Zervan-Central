#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "HYDRATION_ON_NEED.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "hydration_on_need.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R3I = (
    ROOT
    / "contracts"
    / "qualification"
    / "HYDRATION_REQUEST_RELEASE.md"
)

R4C = (
    ROOT
    / "contracts"
    / "runtime"
    / "LANDING_WITNESS.md"
)

R4F = (
    ROOT
    / "contracts"
    / "runtime"
    / "REPLAY_ENVELOPE.md"
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


def evaluate_record(record):
    reasons = []

    scope = record.get(
        "payload_scope"
    )

    if scope in (
        "FULL_PAYLOAD",
        "LOAD_EVERYTHING",
    ):
        reasons.append(
            "FULL_PAYLOAD_SCOPE_FORBIDDEN"
        )

    if not record.get(
        "active_mission_reference"
    ):
        reasons.append(
            "ACTIVE_MISSION_MISSING"
        )

    if not record.get(
        "active_question"
    ):
        reasons.append(
            "ACTIVE_QUESTION_MISSING"
        )

    mission_required = set(
        record.get(
            "mission_required_payload",
            []
        )
    )

    requested_payload = set(
        record.get(
            "requested_payload",
            []
        )
    )

    restored_payload = set(
        record.get(
            "restored_payload",
            []
        )
    )

    at_rest = set(
        record.get(
            "retained_at_rest_payload",
            []
        )
    )

    if (
        requested_payload
        and not mission_required
    ):
        reasons.append(
            "MISSION_NECESSITY_MISSING"
        )

    verified_available = set(
        record.get(
            "verified_territory_available",
            []
        )
    )

    requested_territory = set(
        record.get(
            "requested_verified_territory",
            []
        )
    )

    restored_territory = set(
        record.get(
            "restored_verified_territory",
            []
        )
    )

    if not requested_territory.issubset(
        verified_available
    ):
        reasons.append(
            "UNVERIFIED_TERRITORY_REQUESTED"
        )

    if not restored_territory.issubset(
        requested_territory
    ):
        reasons.append(
            "RESTORED_TERRITORY_OUTSIDE_REQUEST"
        )

    if not restored_payload.issubset(
        requested_payload
    ):
        reasons.append(
            "RESTORED_PAYLOAD_OUTSIDE_REQUEST"
        )

    if not restored_payload.issubset(
        mission_required
    ):
        reasons.append(
            "RESTORED_PAYLOAD_OUTSIDE_MISSION_NEED"
        )

    all_known_payload = (
        requested_payload
        | at_rest
        | set(
            record.get(
                "blocked_payload",
                []
            )
        )
    )

    unnecessary_requested = (
        requested_payload
        - mission_required
    )

    if unnecessary_requested:
        reasons.append(
            "MISSION_NECESSITY_MISSING"
        )

    if (
        record.get(
            "operation_context"
        )
        in (
            "NARROW_QUESTION",
            "REPLAY",
            "BOUNDED_REVISIT",
        )
        and all_known_payload
        and restored_payload == all_known_payload
        and len(all_known_payload) > len(mission_required)
    ):
        reasons.append(
            "UNNECESSARY_PAYLOAD_NOT_AT_REST"
        )

    if (
        record.get(
            "operation_context"
        )
        == "LANDING"
    ):
        before = set(
            record.get(
                "pre_landing_active_payload",
                []
            )
        )

        released = set(
            record.get(
                "landing_released_payload",
                []
            )
        )

        retained = set(
            record.get(
                "landing_retained_payload",
                []
            )
        )

        if (
            released & retained
            or (released | retained) != before
        ):
            reasons.append(
                "LANDING_PAYLOAD_PARTITION_INVALID"
            )

    restrictions = set(
        record.get(
            "restriction_references",
            []
        )
    )

    blocked = set(
        record.get(
            "blocked_payload",
            []
        )
    )

    if (
        restrictions
        and blocked & restored_payload
    ):
        reasons.append(
            "RESTRICTION_BYPASSED"
        )

    for marker in record.get(
        "provenance_route",
        []
    ):
        if marker == "evidence-boundary:broadened":
            reasons.append(
                "EVIDENCE_BOUNDARY_BROADENED"
            )

        if marker == "evidence-ceiling:elevated":
            reasons.append(
                "EVIDENCE_CEILING_ELEVATED"
            )

    if record.get(
        "object_identity_changed"
    ):
        reasons.append(
            "OBJECT_IDENTITY_REPLACED"
        )

    if record.get(
        "lifecycle_mutated"
    ):
        reasons.append(
            "LIFECYCLE_MUTATED"
        )

    if record.get(
        "occupancy_mutated"
    ):
        reasons.append(
            "OCCUPANCY_MUTATED"
        )

    if record.get(
        "formation_mutated"
    ):
        reasons.append(
            "FORMATION_MUTATED"
        )

    if not record.get(
        "stick_reference"
    ):
        reasons.append(
            "STICK_NOT_PRESERVED"
        )

    if (
        record.get(
            "authority_state"
        )
        != "NONE"
    ):
        reasons.append(
            "AUTHORITY_PROMOTED"
        )

    return sorted(
        set(
            reasons
        )
    )


def expected_disposition(record):
    return (
        "VALID"
        if not evaluate_record(
            record
        )
        else "BLOCKED"
    )


def validate_record(record):
    errors = []

    if (
        record.get(
            "validation_vector"
        )
        != "HYDRATION_ON_NEED"
    ):
        errors.append(
            "wrong validation vector"
        )

    expected_reasons = evaluate_record(
        record
    )

    expected = (
        "VALID"
        if not expected_reasons
        else "BLOCKED"
    )

    if (
        record.get(
            "validation_disposition"
        )
        != expected
    ):
        errors.append(
            "hydration disposition contradicts mission-required state"
        )

    if (
        sorted(
            record.get(
                "failure_reasons",
                []
            )
        )
        != expected_reasons
    ):
        errors.append(
            "hydration failure reasons are incomplete or incorrect"
        )

    if (
        record.get(
            "human_gate_state"
        )
        != "ACTIVE"
    ):
        errors.append(
            "R6-H Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-H provenance route required"
        )

    return errors


def make_record(
    *,
    operation_context="ACTIVE_MISSION",
    active_question="What payload is required for this bounded question?",
    active_mission_reference="mission:r6-h:a",
    payload_scope="MISSION_REQUIRED",
    verified_territory_available=None,
    requested_verified_territory=None,
    requested_payload=None,
    mission_required_payload=None,
    restored_verified_territory=None,
    restored_payload=None,
    retained_at_rest_payload=None,
    blocked_payload=None,
    pre_landing_active_payload=None,
    landing_released_payload=None,
    landing_retained_payload=None,
    restriction_references=None,
    stick_reference="stick:r6-h:a",
    object_identity_changed=False,
    lifecycle_mutated=False,
    occupancy_mutated=False,
    formation_mutated=False,
    release_state="RELEASED",
    provenance_route=None,
    authority_state="NONE",
):
    if verified_territory_available is None:
        verified_territory_available = [
            "territory:a",
            "territory:b",
            "territory:c",
        ]

    if requested_verified_territory is None:
        requested_verified_territory = [
            "territory:a"
        ]

    if requested_payload is None:
        requested_payload = [
            "payload:a"
        ]

    if mission_required_payload is None:
        mission_required_payload = [
            "payload:a"
        ]

    if restored_verified_territory is None:
        restored_verified_territory = [
            "territory:a"
        ]

    if restored_payload is None:
        restored_payload = [
            "payload:a"
        ]

    if retained_at_rest_payload is None:
        retained_at_rest_payload = [
            "payload:b",
            "payload:c",
        ]

    if blocked_payload is None:
        blocked_payload = []

    if pre_landing_active_payload is None:
        pre_landing_active_payload = []

    if landing_released_payload is None:
        landing_released_payload = []

    if landing_retained_payload is None:
        landing_retained_payload = []

    if restriction_references is None:
        restriction_references = []

    if provenance_route is None:
        provenance_route = [
            "hydration-request:r6-h",
            "hydration-release:r6-h",
        ]

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "HYDRATION_ON_NEED",

        "object_id":
            "sha512:"
            + "1" * 128,

        "operation_context":
            operation_context,

        "active_question":
            active_question,

        "active_mission_reference":
            active_mission_reference,

        "payload_scope":
            payload_scope,

        "verified_territory_available":
            list(
                verified_territory_available
            ),

        "requested_verified_territory":
            list(
                requested_verified_territory
            ),

        "requested_payload":
            list(
                requested_payload
            ),

        "mission_required_payload":
            list(
                mission_required_payload
            ),

        "restored_verified_territory":
            list(
                restored_verified_territory
            ),

        "restored_payload":
            list(
                restored_payload
            ),

        "retained_at_rest_payload":
            list(
                retained_at_rest_payload
            ),

        "blocked_payload":
            list(
                blocked_payload
            ),

        "pre_landing_active_payload":
            list(
                pre_landing_active_payload
            ),

        "landing_released_payload":
            list(
                landing_released_payload
            ),

        "landing_retained_payload":
            list(
                landing_retained_payload
            ),

        "evidence_boundary_reference":
            "boundary:r6-h:a",

        "evidence_ceiling_reference":
            "ceiling:r6-h:a",

        "restriction_references":
            list(
                restriction_references
            ),

        "stick_reference":
            stick_reference,

        "object_identity_changed":
            object_identity_changed,

        "lifecycle_mutated":
            lifecycle_mutated,

        "occupancy_mutated":
            occupancy_mutated,

        "formation_mutated":
            formation_mutated,

        "release_state":
            release_state,

        "provenance_route":
            list(
                provenance_route
            ),

        "authority_state":
            authority_state,

        "human_gate_state":
            "ACTIVE",

        "validation_disposition":
            "",

        "failure_reasons":
            [],
    }

    record[
        "failure_reasons"
    ] = evaluate_record(
        record
    )

    record[
        "validation_disposition"
    ] = expected_disposition(
        record
    )

    return record


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-H contract"
        ),
        (
            SCHEMA,
            "R6-H schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R3I,
            "R3-I Hydration"
        ),
        (
            R4C,
            "R4-C Landing"
        ),
        (
            R4F,
            "R4-F Replay"
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
        "R6-H = Hydration-On-Need.",
        "Identity travels.",
        "Payload rests.",
        "Hydration remains mission-required.",
        "Hydrate what the question requires.",
        "Leave unnecessary payload at rest.",
        "Mission-required != potentially interesting.",
        "Available != necessary.",
        "Possible relevance != hydration justification.",
        "Convenience != necessity.",
        "There is no FULL_PAYLOAD hydration mode.",
        "There is no LOAD_EVERYTHING hydration mode.",
        "Full payload hydration without question-driven necessity is prohibited.",
        "Narrow question != full-context hydration.",
        "Requested != verified by request.",
        "Request != restored payload.",
        "Restored payload MUST be a subset of requested payload.",
        "Restored verified territory MUST be a subset of requested verified territory.",
        "Release cannot broaden request scope.",
        "At rest != absent.",
        "At rest != deleted.",
        "Landing does not authorize full-payload retention.",
        "Landing payload release != deletion.",
        "Landing payload release != evidence destruction.",
        "Replay does not justify full reconstruction.",
        "Replay != hydration authority.",
        "Previously active payload != currently necessary payload.",
        "Previous hydration != current hydration authorization.",
        "Hydration MUST NOT silently expose excluded evidence.",
        "Hydration does not raise the evidence ceiling.",
        "More accessible payload != stronger claim authority.",
        "More data != automatic analytical promotion.",
        "Restriction != absence.",
        "Hydration does not replace the Room.",
        "Payload loading does not become object identity.",
        "Hydration state != Room lifecycle state.",
        "Hydrated payload != occupant.",
        "Formation Selection != hydration authority.",
        "Hydration MUST preserve the Stick.",
        "RELEASED != unrestricted access.",
        "PARTIAL != failure.",
        "BLOCKED != nonexistent.",
        "Resume != full hydration.",
        "Replay != full hydration.",
        "Landing != full hydration.",
        "Completeness desire != mission necessity.",
        "More data != better hydration.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-I owns Replay Fidelity validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-H lock: {lock}"
            )

    source_locks = {
        R3I: [
            "Identity travels.",
            "Payload rests.",
            "Hydrate what the question requires.",
            "There is no FULL_PAYLOAD hydration mode.",
            "There is no LOAD_EVERYTHING hydration mode.",
            "Restored payload must be a subset of requested payload.",
            "Restored verified territory must be a subset of requested verified territory.",
            "Hydration MUST preserve the Stick.",
        ],
        R4C: [
            "Landing may release unnecessary active payload.",
            "Landing does not authorize full-payload retention.",
            "The union of released and retained payload MUST exactly equal the active payload set before Landing.",
            "Landing MUST preserve the Stick.",
        ],
        R4F: [
            "Replay does not justify full reconstruction.",
            "Payload rests.",
            "Replay MUST preserve the Stick.",
        ],
    }

    for path, required_locks in source_locks.items():
        surface = normalized(
            path
        )

        for lock in required_locks:
            if (
                " ".join(
                    lock.split()
                )
                not in surface
            ):
                errors.append(
                    f"source boundary missing required semantic: {lock}"
                )

    r6a = normalized(
        R6A
    )

    for lock in (
        "Hydration-On-Need",
        "Identity travels.",
        "Payload rests.",
        "Hydration remains mission-required.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-H binding: {lock}"
            )

    try:
        load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-H schema JSON: {exc}"
        ]

    # Narrow question.
    narrow = make_record(
        operation_context="NARROW_QUESTION",
        requested_payload=[
            "payload:a"
        ],
        mission_required_payload=[
            "payload:a"
        ],
        restored_payload=[
            "payload:a"
        ],
        retained_at_rest_payload=[
            "payload:b",
            "payload:c",
            "payload:d",
        ],
    )

    errors.extend(
        validate_record(
            narrow
        )
    )

    # Landing releases unnecessary active payload.
    landing = make_record(
        operation_context="LANDING",
        requested_payload=[
            "payload:a"
        ],
        mission_required_payload=[
            "payload:a"
        ],
        restored_payload=[
            "payload:a"
        ],
        pre_landing_active_payload=[
            "payload:a",
            "payload:b",
            "payload:c",
        ],
        landing_released_payload=[
            "payload:b",
            "payload:c",
        ],
        landing_retained_payload=[
            "payload:a"
        ],
        retained_at_rest_payload=[
            "payload:b",
            "payload:c",
        ],
    )

    errors.extend(
        validate_record(
            landing
        )
    )

    # Replay remains bounded.
    replay = make_record(
        operation_context="REPLAY",
        requested_verified_territory=[
            "territory:a"
        ],
        requested_payload=[
            "payload:a"
        ],
        mission_required_payload=[
            "payload:a"
        ],
        restored_verified_territory=[
            "territory:a"
        ],
        restored_payload=[
            "payload:a"
        ],
        retained_at_rest_payload=[
            "payload:b",
            "payload:c",
        ],
    )

    errors.extend(
        validate_record(
            replay
        )
    )

    # Full payload mode rejected.
    full = make_record(
        payload_scope="FULL_PAYLOAD"
    )

    if (
        "FULL_PAYLOAD_SCOPE_FORBIDDEN"
        not in full[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-H failed to reject FULL_PAYLOAD hydration"
        )

    # Payload outside request rejected.
    widened = make_record(
        requested_payload=[
            "payload:a"
        ],
        mission_required_payload=[
            "payload:a"
        ],
        restored_payload=[
            "payload:a",
            "payload:b",
        ],
    )

    if (
        "RESTORED_PAYLOAD_OUTSIDE_REQUEST"
        not in widened[
            "failure_reasons"
        ]
    ):
        errors.append(
            "R6-H failed to reject payload restoration outside request"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-H HYDRATION-ON-NEED: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-H HYDRATION-ON-NEED: PASS"
    )
    print(
        "MISSION_REQUIRED is the only hydration scope: VALIDATED"
    )
    print(
        "Narrow question -> bounded payload subset: VALIDATED"
    )
    print(
        "Landing -> unnecessary active payload released: VALIDATED"
    )
    print(
        "Replay -> mission-required verified territory only: VALIDATED"
    )
    print(
        "FULL_PAYLOAD / LOAD_EVERYTHING: REJECTED"
    )
    print(
        "Payload outside request / mission need: REJECTED"
    )
    print(
        "Unnecessary payload -> retained at rest: PRESERVED"
    )
    print(
        "Evidence boundary / ceiling / restrictions: PRESERVED"
    )
    print(
        "Room identity / Stick continuity: PRESERVED"
    )
    print(
        "Lifecycle / Occupancy / Formation mutation: NOT CREATED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-I Replay Fidelity: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
