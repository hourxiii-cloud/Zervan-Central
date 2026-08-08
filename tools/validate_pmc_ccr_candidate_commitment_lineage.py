#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "PMC_CCR_CANDIDATE_COMMITMENT_LINEAGE.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "canonical_commitment_record.schema.json"
)

R5B = (
    ROOT
    / "contracts"
    / "pipeline"
    / "ROOM_BOUND_EVIDENCE_PMC_INTAKE_BINDING.md"
)

NAMING = (
    ROOT
    / "Doctrine"
    / "PMC_MC_NAMING_LOCK.md"
)

LEGACY_INTERFACE = (
    ROOT
    / "Doctrine"
    / "PMC_MC_INTERFACE.md"
)

DISPOSITIONS = {
    "CANDIDATE_RECORDED",
    "NULL_RECORDED",
    "BLOCKED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_ccr_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "ccr_id"
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
        record.get("ccr_id")
        != compute_ccr_id(record)
    ):
        errors.append(
            "ccr_id does not recompute from record"
        )

    disposition = record.get(
        "commitment_disposition"
    )

    if disposition not in DISPOSITIONS:
        errors.append(
            "invalid CCR commitment disposition"
        )

    for field in (
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "pmc_intake_binding_id",
        "pmc_run_id",
        "pmc_output_reference",
        "evidence_references",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "coordinate_reference",
        "representation_reference",
        "invariants_checked_references",
        "replay_reference",
        "lineage_reference",
        "provenance_route",
        "commitment_disposition",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"CCR requires {field}"
            )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "CCR authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "CCR human_gate_state must remain ACTIVE"
        )

    selected = record.get(
        "selected_world_id"
    )

    ordering = record.get(
        "candidate_ordering",
        []
    )

    if (
        selected is not None
        and selected not in ordering
    ):
        errors.append(
            "selected_world_id must appear in candidate_ordering"
        )

    if (
        disposition == "CANDIDATE_RECORDED"
        and selected is None
    ):
        errors.append(
            "CANDIDATE_RECORDED requires selected_world_id"
        )

    if (
        disposition == "NULL_RECORDED"
        and selected is not None
    ):
        errors.append(
            "NULL_RECORDED requires selected_world_id to remain null"
        )

    if (
        disposition == "BLOCKED"
        and not record.get(
            "blocking_reasons"
        )
    ):
        errors.append(
            "BLOCKED CCR requires blocking reasons"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-C contract"
        ),
        (
            SCHEMA,
            "R5-C schema"
        ),
        (
            R5B,
            "R5-B binding"
        ),
        (
            NAMING,
            "PMC/CCR/MC naming lock"
        ),
        (
            LEGACY_INTERFACE,
            "legacy PMC->MC interface"
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
        "CCR means Canonical Commitment Record.",
        "R5-C does not redefine PMC.",
        "R5-C does not redefine MC.",
        "R5-C does not authorize action.",
        "R5-C preserves PMC analytical state without reinterpreting it.",
        "Commitment record != canonical promotion.",
        "Candidate commitment != action commitment.",
        "Direct PMC -> MC routing is not valid native-v41 pipeline execution.",
        "CCR != canonical promotion.",
        "CCR != Human Gate approval.",
        "CCR != Registry state mutation.",
        "CCR may record PMC output.",
        "CCR may not reinterpret PMC output.",
        "CCR construction may not reinterpret PMC truth.",
        "NULL PMC outcome != pipeline error.",
        "CCR does not manufacture success.",
        "CCR does not own Room identity.",
        "PMC -> CCR handoff MUST NOT silently change Room Object identity.",
        "CCR may reference state.",
        "CCR does not own state.",
        "CCR MUST NOT replace evidence lineage with a summary-only representation.",
        "Coordinate reference != Cartography ownership.",
        "CCR MUST NOT silently substitute another perspective.",
        "CCR MUST NOT admit new evidence.",
        "CCR MUST NOT raise claim authority.",
        "High confidence != higher claim ceiling.",
        "CCR commitment != certainty.",
        "Uncertainty MUST NOT disappear merely because a CCR exists.",
        "Commitment record != uncertainty elimination.",
        "Rejected != deleted.",
        "Rejected != nonexistent.",
        "Selected != only world that ever existed.",
        "No Compression Out applies to rejected-world lineage.",
        "Equivalent PMC outputs and equivalent Room-bound lineage MUST produce the same CCR identity.",
        "No hidden defaults.",
        "No hidden heuristic winner selection.",
        "CANDIDATE_RECORDED != canonical promotion.",
        "NULL_RECORDED != failure.",
        "BLOCKED != PMC truth reversal.",
        "CCR does not select the world.",
        "PMC selects or denies.",
        "CCR records.",
        "PMC ordering remains PMC ordering.",
        "If the source PMC state cannot be reconstructed, CCR is BLOCKED.",
        "Receipt != truth.",
        "Hash != truth.",
        "MC receives CCR.",
        "CCR is mandatory between PMC and MC in Ring 5.",
        "R5-C does not perform MC admissibility.",
        "Historical artifact != active native route.",
        "CCR creates no action authority.",
        "CCR creates no publication authority.",
        "CCR creates no certification authority.",
        "CCR creates no canonical promotion authority.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Write capability != authority.",
        "Deterministic record != authority.",
        "CCR is not permission to flatten PMC history into the selected world alone.",
        "Fail closed.",
        "Do not reinterpret PMC output to repair the record.",
        "R5-D owns CCR -> MC Response / Output Admissibility Binding.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in text
        ):
            errors.append(
                f"missing R5-C lock: {lock}"
            )

    naming = normalized(
        NAMING
    )

    naming_locks = [
        "CCR means Canonical Commitment Record",
        "CCR construction may not reinterpret PMC truth.",
        "Evidence",
        "PMC:",
        "CCR:",
        "MC:",
    ]

    for lock in naming_locks:
        if (
            " ".join(lock.split())
            not in naming
        ):
            errors.append(
                f"existing CCR naming semantic missing: {lock}"
            )

    legacy = normalized(
        LEGACY_INTERFACE
    )

    if (
        "PMC → MC is the only permitted flow."
        not in legacy
    ):
        errors.append(
            "expected legacy PMC->MC collision is not attributable"
        )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-C schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "mc_admissibility",
        "admissible_response_classes",
        "raven_report",
        "human_gate_decision",
        "execution_authorization",
        "publication_authorization",
        "canonical_promotion",
        "room_lifecycle_transition",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-C improperly absorbs MC/downstream/Room semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    object_id = (
        "sha512:"
        + "1" * 128
    )

    state_root = (
        "sha512:"
        + "2" * 128
    )

    view_root = (
        "sha512:"
        + "3" * 128
    )

    intake_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "room_revision_id":
            "revision:a",
        "room_state_root":
            state_root,
        "authorized_view_root":
            view_root,
        "pmc_intake_binding_id":
            intake_id,
        "pmc_run_id":
            "pmc-run:a",
        "pmc_output_reference":
            "pmc-output:a",
        "selected_world_id":
            "world:a",
        "candidate_ordering": [
            "world:a",
            "world:b",
            "world:c"
        ],
        "rejection_references": [
            "rejection:world:b",
            "rejection:world:c"
        ],
        "evidence_references": [
            "evidence:a",
            "evidence:b"
        ],
        "evidence_boundary_reference":
            "boundary:a",
        "evidence_ceiling_reference":
            "ceiling:a",
        "coordinate_reference":
            "coordinate:a",
        "representation_reference":
            "representation:a",
        "transform_references": [
            "transform:a"
        ],
        "uncertainty_references": [
            "uncertainty:a"
        ],
        "unresolved_state_references": [
            "unknown:a"
        ],
        "invariants_checked_references": [
            "invariant:zsd",
            "invariant:zea",
            "invariant:zee",
            "invariant:oraborus"
        ],
        "replay_reference":
            "pmc-replay:a",
        "lineage_reference":
            "lineage:a",
        "provenance_route": [
            object_id,
            intake_id,
            "pmc-run:a",
            "pmc-output:a",
            "world:a",
            "lineage:a"
        ],
        "commitment_disposition":
            "CANDIDATE_RECORDED",
        "blocking_reasons": [],
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "ccr_id"
    ] = compute_ccr_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    # Selected world must be in PMC ordering.
    missing_selected = dict(
        record
    )

    missing_selected[
        "selected_world_id"
    ] = "world:not-in-ordering"

    missing_selected[
        "ccr_id"
    ] = compute_ccr_id(
        missing_selected
    )

    if not any(
        "selected_world_id must appear"
        in error
        for error in validate_record(
            missing_selected
        )
    ):
        errors.append(
            "R5-C incorrectly permitted CCR selected-world substitution"
        )

    # Null result is valid and must stay null.
    null_record = dict(
        record
    )

    null_record[
        "selected_world_id"
    ] = None

    null_record[
        "commitment_disposition"
    ] = "NULL_RECORDED"

    null_record[
        "ccr_id"
    ] = compute_ccr_id(
        null_record
    )

    null_errors = validate_record(
        null_record
    )

    if null_errors:
        errors.append(
            "R5-C rejected valid NULL PMC commitment: "
            + "; ".join(
                null_errors
            )
        )

    # Candidate disposition cannot hide null selection.
    fake_candidate = dict(
        null_record
    )

    fake_candidate[
        "commitment_disposition"
    ] = "CANDIDATE_RECORDED"

    fake_candidate[
        "ccr_id"
    ] = compute_ccr_id(
        fake_candidate
    )

    if not any(
        "requires selected_world_id"
        in error
        for error in validate_record(
            fake_candidate
        )
    ):
        errors.append(
            "R5-C incorrectly manufactured candidate from NULL PMC result"
        )

    # BLOCKED requires reason.
    blocked = dict(
        record
    )

    blocked[
        "commitment_disposition"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = []

    blocked[
        "ccr_id"
    ] = compute_ccr_id(
        blocked
    )

    if not any(
        "requires blocking reasons"
        in error
        for error in validate_record(
            blocked
        )
    ):
        errors.append(
            "R5-C incorrectly permitted BLOCKED CCR without reason"
        )

    # Authority cannot be promoted.
    promoted = dict(
        record
    )

    promoted[
        "authority_state"
    ] = "WRITE"

    promoted[
        "ccr_id"
    ] = compute_ccr_id(
        promoted
    )

    if not any(
        "authority_state must remain NONE"
        in error
        for error in validate_record(
            promoted
        )
    ):
        errors.append(
            "R5-C incorrectly permitted authority promotion"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-C PMC -> CCR CANDIDATE COMMITMENT LINEAGE: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-C PMC -> CCR CANDIDATE COMMITMENT LINEAGE: PASS"
    )
    print(
        "PMC output / Room identity / evidence lineage: BOUND"
    )
    print(
        "Selected / rejected / uncertainty / replay state: PRESERVED"
    )
    print(
        "NULL PMC outcome preservation: ENFORCED"
    )
    print(
        "CCR truth reinterpretation / direct PMC->MC bypass: REJECTED"
    )
    print(
        "Authority / promotion / MC admissibility: NOT ABSORBED"
    )
    print(
        "R5-D CCR -> MC binding: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
