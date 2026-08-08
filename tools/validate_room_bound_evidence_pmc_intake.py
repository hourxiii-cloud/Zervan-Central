#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "ROOM_BOUND_EVIDENCE_PMC_INTAKE_BINDING.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "room_bound_evidence_pmc_intake.schema.json"
)

R5A = (
    ROOT
    / "contracts"
    / "pipeline"
    / "PIPELINE_INTEGRATION_BOUNDARY_EXISTING_SEMANTICS_LOCK.md"
)

PMC = (
    ROOT
    / "Doctrine"
    / "PMC.md"
)

EVIDENCE_CLASSES = {
    "STRUCTURAL",
    "INTERPRETIVE",
}

DISPOSITIONS = {
    "ADMISSIBLE",
    "BLOCKED",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_intake_binding_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "intake_binding_id"
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
        record.get("intake_binding_id")
        != compute_intake_binding_id(record)
    ):
        errors.append(
            "intake_binding_id does not recompute from record"
        )

    if record.get(
        "intake_disposition"
    ) not in DISPOSITIONS:
        errors.append(
            "invalid PMC intake disposition"
        )

    classes = set(
        record.get(
            "evidence_classes",
            []
        )
    )

    if not classes:
        errors.append(
            "PMC intake requires evidence_classes"
        )

    if not classes.issubset(
        EVIDENCE_CLASSES
    ):
        errors.append(
            "invalid PMC evidence class"
        )

    for field in (
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "evidence_references",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "coordinate_reference",
        "representation_reference",
        "lineage_reference",
        "qualification_reference",
        "deterministic_parameter_references",
        "provenance_route",
        "intake_disposition",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"PMC intake requires {field}"
            )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "PMC intake authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "PMC intake human_gate_state must remain ACTIVE"
        )

    if (
        record.get("intake_disposition")
        == "BLOCKED"
        and not record.get(
            "blocking_reasons"
        )
    ):
        errors.append(
            "BLOCKED PMC intake requires blocking reasons"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-B contract"
        ),
        (
            SCHEMA,
            "R5-B schema"
        ),
        (
            R5A,
            "R5-A boundary"
        ),
        (
            PMC,
            "PMC doctrine"
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
        "R5-B binds qualified Room-context evidence to PMC intake.",
        "R5-B does not redefine PMC.",
        "R5-B does not perform PMC collapse.",
        "Binding != analysis.",
        "Binding != truth.",
        "Binding != authority.",
        "PMC receives bounded evidence context.",
        "PMC does not become the owner of that context.",
        "Similar evidence != same Room.",
        "Current Room state != historical intake state.",
        "Authorized View Root constrains visibility.",
        "Restricted != nonexistent.",
        "Unavailable to PMC != nonexistent in the Room.",
        "Evidence MUST NOT be silently replaced by narrative summary.",
        "Identity travels.",
        "Payload rests.",
        "PMC intake != full-payload hydration authority.",
        "Hash != truth.",
        "Signature != correctness.",
        "Integrity != semantic correctness.",
        "Interpretive evidence MUST remain advisory.",
        "Interpretation is not authority.",
        "Unpinned material is not valid native-v41 PMC intake.",
        "Pinned != true.",
        "Pinned != authoritative.",
        "PMC MUST NOT silently broaden the evidence boundary.",
        "Evidence ceiling != confidence score.",
        "Confidence does not override claim ceiling.",
        "Coordinate != truth.",
        "Coordinate != authority.",
        "Coordinate reference != Cartography ownership.",
        "Representation MUST NOT alter Room identity.",
        "Perspective != evidence.",
        "Perspective != authority.",
        "Unknown remains unknown.",
        "Admission != resolution.",
        "Qualification precedes analysis.",
        "Qualification != analytical truth.",
        "Qualification != PMC selection.",
        "No hidden defaults.",
        "No silent substitution.",
        "PMC may not authorize action.",
        "PMC may not bypass CCR.",
        "PMC may not bypass MC.",
        "Room binding does not expand PMC ownership.",
        "ADMISSIBLE != true.",
        "ADMISSIBLE != PMC-selected.",
        "ADMISSIBLE != action-authorized.",
        "BLOCKED != evidence nonexistent.",
        "Fail closed.",
        "Do not fabricate missing intake state.",
        "Binding != ownership.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Reference != compression out.",
        "Envelope != summary substitution.",
        "R5-C owns PMC -> CCR Candidate Commitment Lineage.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in text
        ):
            errors.append(
                f"missing R5-B lock: {lock}"
            )

    pmc = normalized(
        PMC
    )

    pmc_locks = [
        "PMC is not a decision engine.",
        "Interpretation is not authority.",
        "Inputs are pinned",
        "Parameters are deterministic and recorded.",
        "candidate denial",
        "no silent fallback",
        "PMC may not",
        "bypass MC",
    ]

    for lock in pmc_locks:
        if (
            " ".join(lock.split())
            not in pmc
        ):
            errors.append(
                f"existing PMC semantic missing: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-B schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "candidate_worlds",
        "selected_world_id",
        "pmc_collapse_result",
        "ccr_record",
        "mc_admissibility",
        "publication_authorization",
        "execution_authorization",
        "canonical_promotion",
        "room_lifecycle_transition",
        "full_payload",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-B improperly absorbs PMC/downstream/Room semantics: "
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
        "evidence_references": [
            "evidence:a",
            "evidence:b"
        ],
        "evidence_integrity_references": [
            "sha512:evidence:a",
            "sha512:evidence:b"
        ],
        "evidence_classes": [
            "STRUCTURAL",
            "INTERPRETIVE"
        ],
        "evidence_boundary_reference":
            "boundary:a",
        "evidence_ceiling_reference":
            "claim-ceiling:a",
        "coordinate_reference":
            "coordinate:a",
        "representation_reference":
            "representation:a",
        "transform_references": [
            "transform:a"
        ],
        "lineage_reference":
            "lineage:a",
        "unresolved_state_references": [
            "unknown:a"
        ],
        "qualification_reference":
            "qualification:a",
        "deterministic_parameter_references": [
            "parameters:a"
        ],
        "provenance_route": [
            object_id,
            "revision:a",
            state_root,
            view_root,
            "evidence:a",
            "boundary:a",
            "coordinate:a",
            "qualification:a"
        ],
        "intake_disposition":
            "ADMISSIBLE",
        "blocking_reasons": [],
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "created_at":
            "2026-08-07T22:31:00-04:00",
    }

    record[
        "intake_binding_id"
    ] = compute_intake_binding_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    missing_boundary = dict(
        record
    )

    missing_boundary[
        "evidence_boundary_reference"
    ] = ""

    missing_boundary[
        "intake_binding_id"
    ] = compute_intake_binding_id(
        missing_boundary
    )

    if not any(
        "evidence_boundary_reference"
        in error
        for error in validate_record(
            missing_boundary
        )
    ):
        errors.append(
            "R5-B incorrectly permitted intake without evidence boundary"
        )

    missing_view = dict(
        record
    )

    missing_view[
        "authorized_view_root"
    ] = ""

    missing_view[
        "intake_binding_id"
    ] = compute_intake_binding_id(
        missing_view
    )

    if not any(
        "authorized_view_root"
        in error
        for error in validate_record(
            missing_view
        )
    ):
        errors.append(
            "R5-B incorrectly permitted intake without Authorized View Root"
        )

    blocked = dict(
        record
    )

    blocked[
        "intake_disposition"
    ] = "BLOCKED"

    blocked[
        "blocking_reasons"
    ] = []

    blocked[
        "intake_binding_id"
    ] = compute_intake_binding_id(
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
            "R5-B incorrectly permitted BLOCKED intake without reason"
        )

    promoted = dict(
        record
    )

    promoted[
        "authority_state"
    ] = "WRITE"

    promoted[
        "intake_binding_id"
    ] = compute_intake_binding_id(
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
            "R5-B incorrectly permitted authority promotion"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-B ROOM-BOUND EVIDENCE -> PMC INTAKE BINDING: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-B ROOM-BOUND EVIDENCE -> PMC INTAKE BINDING: PASS"
    )
    print(
        "Room identity / revision / state / Authorized View: BOUND"
    )
    print(
        "Evidence references / classes / integrity / provenance: PRESERVED"
    )
    print(
        "Boundary / claim ceiling / coordinate / transform: PRESERVED"
    )
    print(
        "Qualification / unknowns / deterministic replay context: BOUND"
    )
    print(
        "PMC ownership / collapse / action authority: NOT ABSORBED"
    )
    print(
        "R5-C PMC -> CCR binding: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
