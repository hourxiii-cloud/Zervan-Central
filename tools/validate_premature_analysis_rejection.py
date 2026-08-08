#!/usr/bin/env python3

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "validation"
    / "PREMATURE_ANALYSIS_REJECTION.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "validation"
    / "premature_analysis_rejection.schema.json"
)

R6A = (
    ROOT
    / "contracts"
    / "validation"
    / "VALIDATION_AUDIT_BOUNDARY_VECTOR_REGISTRY.md"
)

R3A = (
    ROOT
    / "contracts"
    / "qualification"
    / "QUALIFICATION_REQUEST_MISSION_FITNESS.md"
)

R3B = (
    ROOT
    / "contracts"
    / "qualification"
    / "QUALIFICATION_RECORD_DISPOSITION.md"
)

R3C = (
    ROOT
    / "contracts"
    / "qualification"
    / "ROOM_LIFECYCLE_READINESS.md"
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


def expected_rejection_reasons(record):
    reasons = []

    if (
        record.get("request_state")
        != "READY"
    ):
        reasons.append(
            "REQUEST_NOT_READY"
        )

    if (
        record.get("qualification_disposition")
        != "QUALIFIED"
    ):
        reasons.append(
            "ROOM_NOT_QUALIFIED"
        )

    if (
        record.get("room_lifecycle_state")
        != "READY"
    ):
        reasons.append(
            "ROOM_NOT_READY"
        )

    if record.get(
        "readiness_blockers"
    ):
        reasons.append(
            "READINESS_BLOCKER_PRESENT"
        )

    if not record.get(
        "analytical_capability_available"
    ):
        reasons.append(
            "CAPABILITY_UNAVAILABLE"
        )

    if not record.get(
        "analytical_admission_requested"
    ):
        reasons.append(
            "ANALYSIS_NOT_REQUESTED"
        )

    if not record.get(
        "evidence_boundary_reference"
    ):
        reasons.append(
            "EVIDENCE_BOUNDARY_UNRESOLVED"
        )

    if not record.get(
        "evidence_ceiling_reference"
    ):
        reasons.append(
            "EVIDENCE_CEILING_UNRESOLVED"
        )

    return reasons


def expected_gate_result(record):
    return (
        "ALLOWED"
        if not expected_rejection_reasons(
            record
        )
        else "REJECTED"
    )


def validate_record(record):
    errors = []

    if (
        record.get("validation_vector")
        != "PREMATURE_ANALYSIS_REJECTION"
    ):
        errors.append(
            "wrong validation vector"
        )

    expected_reasons = (
        expected_rejection_reasons(
            record
        )
    )

    expected_result = (
        "ALLOWED"
        if not expected_reasons
        else "REJECTED"
    )

    if (
        record.get("gate_result")
        != expected_result
    ):
        errors.append(
            "analytical admission gate result contradicts qualification/readiness state"
        )

    if (
        set(
            record.get(
                "rejection_reasons",
                []
            )
        )
        != set(expected_reasons)
    ):
        errors.append(
            "analytical admission rejection reasons are incomplete or incorrect"
        )

    if (
        record.get("gate_result")
        == "ALLOWED"
        and record.get(
            "rejection_reasons"
        )
    ):
        errors.append(
            "ALLOWED analytical admission may not retain rejection reasons"
        )

    if (
        record.get("gate_result")
        == "REJECTED"
        and not record.get(
            "rejection_reasons"
        )
    ):
        errors.append(
            "REJECTED analytical admission requires rejection reasons"
        )

    if (
        record.get("analytical_occupancy_state")
        != "NOT_ENTERED"
    ):
        errors.append(
            "R6-C gate validation may not establish analytical occupation"
        )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "R6-C authority state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "R6-C Human Gate state must remain ACTIVE"
        )

    if not record.get(
        "provenance_route"
    ):
        errors.append(
            "R6-C validation requires provenance route"
        )

    return errors


def make_record(
    *,
    request_state="READY",
    qualification_disposition="QUALIFIED",
    room_lifecycle_state="READY",
    readiness_blockers=None,
    evidence_boundary_reference="boundary:a",
    evidence_ceiling_reference="ceiling:a",
    analytical_capability_available=True,
    analytical_admission_requested=True,
    hydration_state="NOT_REQUESTED",
):
    if readiness_blockers is None:
        readiness_blockers = []

    record = {
        "schema_version":
            "1.0",

        "validation_vector":
            "PREMATURE_ANALYSIS_REJECTION",

        "object_id":
            "sha512:"
            + "1" * 128,

        "qualification_request_reference":
            "qualification-request:a",

        "qualification_record_reference":
            (
                "qualification-record:a"
                if qualification_disposition is not None
                else None
            ),

        "request_state":
            request_state,

        "qualification_disposition":
            qualification_disposition,

        "room_lifecycle_state":
            room_lifecycle_state,

        "readiness_blockers":
            list(
                readiness_blockers
            ),

        "evidence_boundary_reference":
            evidence_boundary_reference,

        "evidence_ceiling_reference":
            evidence_ceiling_reference,

        "analytical_capability_available":
            analytical_capability_available,

        "analytical_admission_requested":
            analytical_admission_requested,

        "hydration_state":
            hydration_state,

        "analytical_occupancy_state":
            "NOT_ENTERED",

        "gate_result":
            "",

        "rejection_reasons":
            [],

        "provenance_route": [
            "qualification-request:a",
            "qualification-record:a",
            "lifecycle:a",
            "r6-c:a",
        ],

        "authority_state":
            "NONE",

        "human_gate_state":
            "ACTIVE",
    }

    record[
        "rejection_reasons"
    ] = expected_rejection_reasons(
        record
    )

    record[
        "gate_result"
    ] = expected_gate_result(
        record
    )

    return record


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R6-C contract"
        ),
        (
            SCHEMA,
            "R6-C schema"
        ),
        (
            R6A,
            "R6-A registry"
        ),
        (
            R3A,
            "R3-A Qualification Request"
        ),
        (
            R3B,
            "R3-B Qualification Record"
        ),
        (
            R3C,
            "R3-C Lifecycle Readiness"
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
        "R6-C = Premature-Analysis Rejection.",
        "Capability availability != qualification.",
        "Qualification precedes analysis.",
        "Available engine != permitted analysis.",
        "Request READY != Room READY.",
        "Request READY != QUALIFIED.",
        "Request READY != analytical permission.",
        "PROVISIONAL MUST NOT permit analytical admission.",
        "REJECTED MUST NOT permit analytical admission.",
        "DEGRADED MUST NOT permit analytical admission.",
        "QUALIFIED != READY.",
        "QUALIFIED alone is not sufficient for READY.",
        "READY != ACTIVE.",
        "READY != occupied.",
        "Availability != presence.",
        "Blocked != absent.",
        "Unresolved != passed.",
        "Can compute != may analyze.",
        "Hydration != qualification.",
        "Hydration != readiness.",
        "Payload availability != analytical permission.",
        "Compute power != evidence authority.",
        "Model availability != higher claim ceiling.",
        "Unknown remains unknown.",
        "Unresolved != permission.",
        "No default READY exists.",
        "Silence != readiness.",
        "Previous readiness != current readiness.",
        "Rejected admission means the analytical pipeline has not begun.",
        "Rejection != partial execution.",
        "ALLOWED != analytical occupation.",
        "ALLOWED != ACTIVE.",
        "ALLOWED != execution completed.",
        "Gate result != lifecycle mutation.",
        "Gate result != qualification disposition.",
        "Gate result != authority.",
        "Rejection reasons accumulate.",
        "Permission != presence.",
        "Permission != execution.",
        "Released payload != qualification success.",
        "Released payload != READY.",
        "The validator observes the boundary.",
        "It does not own the boundary.",
        "Validation observation != state ownership.",
        "Classification != repair.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "R6-D owns Proportional-Force Routing validation.",
    ]

    for lock in locks:
        if (
            " ".join(
                lock.split()
            )
            not in text
        ):
            errors.append(
                f"missing R6-C lock: {lock}"
            )

    source_locks = {
        R3A: [
            "Qualification precedes analysis.",
            "Request READY != Room READY.",
            "Request READY != QUALIFIED.",
            "Unresolved != passed.",
        ],
        R3B: [
            "Qualification occupation != analytical occupation.",
            "QUALIFIED != READY.",
            "No analytical occupation yet.",
        ],
        R3C: [
            "Qualification precedes analysis.",
            "QUALIFIED is necessary for READY.",
            "QUALIFIED alone is not sufficient for READY.",
            "READY != occupied.",
            "Availability != presence.",
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
        "Premature-Analysis Rejection",
        "Capability availability != qualification.",
        "Qualification precedes analysis.",
    ):
        if (
            " ".join(
                lock.split()
            )
            not in r6a
        ):
            errors.append(
                f"R6-A registry missing R6-C binding: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R6-C schema JSON: {exc}"
        ]

    forbidden = {
        "pmc_output",
        "ccr_id",
        "mc_evaluation",
        "raven_report",
        "active_transition",
        "occupancy_witness",
        "execution_authorization",
        "canonical_promotion",
        "evidence_boundary_override",
        "evidence_ceiling_override",
    }

    leaked = (
        set(
            schema.get(
                "properties",
                {}
            )
        )
        & forbidden
    )

    if leaked:
        errors.append(
            "R6-C improperly absorbs downstream semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    # Positive control.
    positive = make_record()

    errors.extend(
        validate_record(
            positive
        )
    )

    if (
        positive[
            "gate_result"
        ]
        != "ALLOWED"
    ):
        errors.append(
            "R6-C positive READY control did not allow admission"
        )

    # QUALIFIED but not READY.
    qualified_not_ready = make_record(
        room_lifecycle_state="QUALIFIED"
    )

    if (
        qualified_not_ready[
            "gate_result"
        ]
        != "REJECTED"
        or "ROOM_NOT_READY"
        not in qualified_not_ready[
            "rejection_reasons"
        ]
    ):
        errors.append(
            "R6-C failed to reject QUALIFIED-but-not-READY Room"
        )

    # PROVISIONAL with capability available.
    provisional = make_record(
        qualification_disposition="PROVISIONAL",
        room_lifecycle_state="PROVISIONAL"
    )

    if (
        provisional[
            "gate_result"
        ]
        != "REJECTED"
    ):
        errors.append(
            "R6-C failed to reject PROVISIONAL Room with available capability"
        )

    # Hydration released but Room not READY.
    hydrated = make_record(
        room_lifecycle_state="QUALIFIED",
        hydration_state="RELEASED"
    )

    if (
        hydrated[
            "gate_result"
        ]
        != "REJECTED"
    ):
        errors.append(
            "R6-C incorrectly allowed hydration to substitute for READY"
        )

    # Readiness blocker.
    blocked = make_record(
        readiness_blockers=[
            "provenance unresolved"
        ]
    )

    if (
        blocked[
            "gate_result"
        ]
        != "REJECTED"
        or "READINESS_BLOCKER_PRESENT"
        not in blocked[
            "rejection_reasons"
        ]
    ):
        errors.append(
            "R6-C failed to reject unresolved readiness blocker"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R6-C PREMATURE-ANALYSIS REJECTION: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R6-C PREMATURE-ANALYSIS REJECTION: PASS"
    )
    print(
        "Request READY / Room QUALIFIED / Room READY: SEPARATED"
    )
    print(
        "Available analytical capability -> premature analysis: REJECTED"
    )
    print(
        "QUALIFIED without READY -> analysis: REJECTED"
    )
    print(
        "PROVISIONAL / REJECTED / DEGRADED -> analysis: REJECTED"
    )
    print(
        "Readiness blockers -> analysis: REJECTED"
    )
    print(
        "Hydration RELEASED -> qualification/readiness substitution: REJECTED"
    )
    print(
        "READY positive control -> downstream admission: ALLOWED"
    )
    print(
        "Gate validation -> analytical occupation / ACTIVE: NOT PERFORMED"
    )
    print(
        "Evidence boundary / ceiling: PRESERVED"
    )
    print(
        "Authority: NONE"
    )
    print(
        "Human Gate: ACTIVE"
    )
    print(
        "R6-D Proportional-Force Routing: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
