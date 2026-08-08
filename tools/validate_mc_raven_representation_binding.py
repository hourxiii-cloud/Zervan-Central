#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "MC_RAVEN_REPRESENTATION_REPORT_BINDING.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "raven_representation_binding.schema.json"
)

R5D = (
    ROOT
    / "contracts"
    / "pipeline"
    / "CCR_MC_RESPONSE_OUTPUT_ADMISSIBILITY_BINDING.md"
)

RAVEN = (
    ROOT
    / "Modules"
    / "Raven"
    / "raven_contract.md"
)

RAVEN_STATUSES = {
    "OK",
    "DEGRADED",
    "FAILED_INTEGRITY",
    "FAILED_SCHEMA",
    "FAILED_TRACEABILITY",
    "FAILED_MC_ADMISSIBILITY",
    "INSUFFICIENT_EVIDENCE",
}

MC_DISPOSITIONS = {
    "ADMISSIBLE",
    "CONDITIONAL",
    "INADMISSIBLE",
}

FINDING_CLASSES = {
    "OBSERVED",
    "INFERRED",
    "UNKNOWN",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_raven_representation_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "raven_representation_id"
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
        record.get("raven_representation_id")
        != compute_raven_representation_id(record)
    ):
        errors.append(
            "raven_representation_id does not recompute from record"
        )

    for field in (
        "mc_evaluation_id",
        "ccr_id",
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "coordinate_reference",
        "upstream_representation_reference",
        "mc_response_class_results",
        "lineage_reference",
        "provenance_route",
        "raven_status",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Raven binding requires {field}"
            )

    if (
        record.get("raven_status")
        not in RAVEN_STATUSES
    ):
        errors.append(
            "invalid Raven status"
        )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "Raven authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "Raven human_gate_state must remain ACTIVE"
        )

    if (
        record.get("unkindness_disposition")
        != "RAVEN_ASSOCIATED_FORWARD_TRANSLATION"
    ):
        errors.append(
            "The Unkindness must remain Raven-associated forward translation"
        )

    finding_ids = set()

    for finding in record.get(
        "findings",
        []
    ):
        finding_id = finding.get(
            "finding_id"
        )

        classification = finding.get(
            "classification"
        )

        if not finding_id:
            errors.append(
                "Raven finding requires finding_id"
            )
            continue

        if finding_id in finding_ids:
            errors.append(
                "Raven finding_id must be unique"
            )

        finding_ids.add(
            finding_id
        )

        if classification not in FINDING_CLASSES:
            errors.append(
                "invalid Raven finding classification"
            )

    trace_claims = {
        item.get("claim_reference")
        for item in record.get(
            "trace_map",
            []
        )
        if item.get("claim_reference")
        and item.get("source_references")
    }

    for finding in record.get(
        "findings",
        []
    ):
        finding_id = finding.get(
            "finding_id"
        )

        if (
            finding_id
            and finding.get(
                "classification"
            ) != "UNKNOWN"
            and finding_id not in trace_claims
        ):
            errors.append(
                "material Raven finding requires trace mapping"
            )

    seen_classes = set()

    for result in record.get(
        "mc_response_class_results",
        []
    ):
        response_class = result.get(
            "response_class"
        )

        disposition = result.get(
            "disposition"
        )

        if not response_class:
            errors.append(
                "Raven MC response class must be named"
            )
            continue

        if response_class in seen_classes:
            errors.append(
                "Raven may not duplicate MC response class"
            )

        seen_classes.add(
            response_class
        )

        if disposition not in MC_DISPOSITIONS:
            errors.append(
                "invalid propagated MC disposition"
            )

        if (
            disposition == "CONDITIONAL"
            and not result.get(
                "required_conditions"
            )
        ):
            errors.append(
                "Raven must preserve conditions for CONDITIONAL class"
            )

        if (
            disposition == "INADMISSIBLE"
            and not result.get(
                "inadmissibility_reasons"
            )
        ):
            errors.append(
                "Raven must preserve reasons for INADMISSIBLE class"
            )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-E contract"
        ),
        (
            SCHEMA,
            "R5-E schema"
        ),
        (
            R5D,
            "R5-D MC binding"
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
        "Raven remains interpretation / reporting only.",
        "R5-E does not redefine Raven.",
        "R5-E does not redefine MC.",
        "R5-E does not perform Human Gate approval.",
        "R5-E does not create publication authority.",
        "Representation != truth mutation.",
        "Reporting != governance.",
        "Reporting != authority.",
        "Raven is the system's voice, not its will.",
        "Raven MUST NOT bypass MC.",
        "Raven may explain MC disposition.",
        "Raven may not manufacture MC disposition.",
        "Blocked MC != permission to infer admissibility.",
        "Conditional != admissible.",
        "Conditional != authorized.",
        "Inadmissible != deleted.",
        "Reporting an inadmissible class != recommending it.",
        "Admissible != approved.",
        "Admissible != executed.",
        "Report variation != new Room.",
        "Audience variation != new Room.",
        "Format variation != new Room.",
        "Representation != access expansion.",
        "Presentation convenience != evidence admission.",
        "Strong prose != stronger evidence.",
        "Coordinate reference != Cartography ownership.",
        "Presentation transform != analytical transform.",
        "Unsupported claim -> unknown or failure.",
        "Silence is preferable to invention.",
        "Unknown != false.",
        "Inferred != observed.",
        "Trace map is mandatory for material claims.",
        "Traceability != truth certification.",
        "Human-readable != authority-bearing.",
        "OK != publication approval.",
        "DEGRADED != false.",
        "INSUFFICIENT_EVIDENCE != nonexistent evidence.",
        "No silent fallback.",
        "Semantic equivalence != byte identity.",
        "RAVEN_ASSOCIATED_FORWARD_TRANSLATION.",
        "The Unkindness is not a separate pipeline stage.",
        "Voice != authority.",
        "Brand != module.",
        "Observability != authority.",
        "Telemetry != truth.",
        "R5-H owns Report / Rendering Contract.",
        "Stage binding != final report contract.",
        "Publication-ready != published.",
        "Rendered != approved.",
        "Report generated != Human Gate approval.",
        "Raven cannot authorize publication.",
        "R5-F owns the Human Gate publication / action boundary.",
        "R5-E does not create decision authority.",
        "R5-E does not create decision options.",
        "Summary != evidence replacement.",
        "Fail closed.",
        "Do not improve unsupported meaning in presentation.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in text
        ):
            errors.append(
                f"missing R5-E lock: {lock}"
            )

    raven = normalized(
        RAVEN
    )

    raven_locks = [
        "Mutation Rights: NONE",
        "Learning Rights: NONE",
        "Authority Scope: REPORTING ONLY",
        "Never bypass MC",
        "Never introduce new facts",
        "Always distinguish observed vs inferred vs unknown",
        "Always preserve traceability from output → source",
        "Raven MUST NEVER guess through a failure.",
        "The Unkindness is Raven's reporting brand and output voice.",
        "It is not a separate module",
    ]

    for lock in raven_locks:
        if (
            " ".join(lock.split())
            not in raven
        ):
            errors.append(
                f"existing Raven semantic missing: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-E schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "new_evidence",
        "raw_telemetry",
        "pmc_world_selection",
        "ccr_generation",
        "mc_disposition_override",
        "publication_authorization",
        "execution_authorization",
        "canonical_promotion",
        "room_lifecycle_transition",
        "cartography_mutation",
        "decision_authority",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-E improperly absorbs truth/governance/action semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    record = {
        "schema_version":
            "1.0",
        "mc_evaluation_id":
            "sha512:" + "1" * 128,
        "ccr_id":
            "sha512:" + "2" * 128,
        "object_id":
            "sha512:" + "3" * 128,
        "room_revision_id":
            "revision:a",
        "room_state_root":
            "sha512:" + "4" * 128,
        "authorized_view_root":
            "sha512:" + "5" * 128,
        "evidence_boundary_reference":
            "boundary:a",
        "evidence_ceiling_reference":
            "ceiling:a",
        "coordinate_reference":
            "coordinate:a",
        "upstream_representation_reference":
            "representation:a",
        "raven_transform_references": [
            "transform:raven:a"
        ],
        "findings": [
            {
                "finding_id":
                    "finding:a",
                "classification":
                    "OBSERVED",
                "text":
                    "Observed bounded state."
            },
            {
                "finding_id":
                    "finding:b",
                "classification":
                    "UNKNOWN",
                "text":
                    "Attribution remains unknown."
            }
        ],
        "unknowns": [
            "Attribution remains unresolved."
        ],
        "mc_response_class_results": [
            {
                "response_class":
                    "observation",
                "disposition":
                    "ADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": []
            },
            {
                "response_class":
                    "technical_mitigation",
                "disposition":
                    "CONDITIONAL",
                "required_conditions": [
                    "condition:a"
                ],
                "inadmissibility_reasons": []
            },
            {
                "response_class":
                    "executive_notification",
                "disposition":
                    "INADMISSIBLE",
                "required_conditions": [],
                "inadmissibility_reasons": [
                    "reason:a"
                ]
            }
        ],
        "trace_map": [
            {
                "claim_reference":
                    "finding:a",
                "source_references": [
                    "evidence:a",
                    "ccr:a",
                    "mc:a"
                ]
            }
        ],
        "lineage_reference":
            "lineage:a",
        "provenance_route": [
            "sha512:" + "3" * 128,
            "sha512:" + "2" * 128,
            "sha512:" + "1" * 128,
            "raven:a"
        ],
        "raven_status":
            "DEGRADED",
        "unkindness_disposition":
            "RAVEN_ASSOCIATED_FORWARD_TRANSLATION",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "raven_representation_id"
    ] = compute_raven_representation_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    # Material supported finding must remain traceable.
    missing_trace = json.loads(
        json.dumps(record)
    )

    missing_trace[
        "trace_map"
    ] = []

    missing_trace[
        "raven_representation_id"
    ] = compute_raven_representation_id(
        missing_trace
    )

    if not any(
        "material Raven finding requires trace mapping"
        in error
        for error in validate_record(
            missing_trace
        )
    ):
        errors.append(
            "R5-E incorrectly permitted untraceable material finding"
        )

    # Conditional class must retain conditions.
    missing_condition = json.loads(
        json.dumps(record)
    )

    missing_condition[
        "mc_response_class_results"
    ][1][
        "required_conditions"
    ] = []

    missing_condition[
        "raven_representation_id"
    ] = compute_raven_representation_id(
        missing_condition
    )

    if not any(
        "preserve conditions"
        in error
        for error in validate_record(
            missing_condition
        )
    ):
        errors.append(
            "R5-E incorrectly erased MC conditional requirement"
        )

    # Inadmissible class must retain reason.
    missing_reason = json.loads(
        json.dumps(record)
    )

    missing_reason[
        "mc_response_class_results"
    ][2][
        "inadmissibility_reasons"
    ] = []

    missing_reason[
        "raven_representation_id"
    ] = compute_raven_representation_id(
        missing_reason
    )

    if not any(
        "preserve reasons"
        in error
        for error in validate_record(
            missing_reason
        )
    ):
        errors.append(
            "R5-E incorrectly erased MC inadmissibility reason"
        )

    # Unkindness must remain associated with Raven.
    separated_unkindness = json.loads(
        json.dumps(record)
    )

    separated_unkindness[
        "unkindness_disposition"
    ] = "SEPARATE_PIPELINE_STAGE"

    separated_unkindness[
        "raven_representation_id"
    ] = compute_raven_representation_id(
        separated_unkindness
    )

    if not any(
        "Raven-associated forward translation"
        in error
        for error in validate_record(
            separated_unkindness
        )
    ):
        errors.append(
            "R5-E incorrectly permitted The Unkindness as separate stage"
        )

    # Authority cannot move.
    promoted = json.loads(
        json.dumps(record)
    )

    promoted[
        "authority_state"
    ] = "WRITE"

    promoted[
        "raven_representation_id"
    ] = compute_raven_representation_id(
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
            "R5-E incorrectly permitted Raven authority promotion"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-E MC -> RAVEN REPRESENTATION / REPORT BINDING: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-E MC -> RAVEN REPRESENTATION / REPORT BINDING: PASS"
    )
    print(
        "MC dispositions / conditions / inadmissibility reasons: PRESERVED"
    )
    print(
        "Room / evidence boundary / claim ceiling / coordinate: PRESERVED"
    )
    print(
        "Observed / inferred / unknown distinction: BOUND"
    )
    print(
        "Material-claim trace mapping: ENFORCED"
    )
    print(
        "Raven presentation transform: ALLOWED / BOUNDED"
    )
    print(
        "The Unkindness: RAVEN-ASSOCIATED FORWARD TRANSLATION"
    )
    print(
        "Truth / governance / publication / execution authority: NOT ABSORBED"
    )
    print(
        "R5-F Raven -> Human Gate boundary: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
