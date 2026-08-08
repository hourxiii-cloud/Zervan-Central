#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = (
    ROOT
    / "contracts"
    / "pipeline"
    / "REPORT_RENDERING_CONTRACT.md"
)

SCHEMA = (
    ROOT
    / "schemas"
    / "pipeline"
    / "report_rendering_record.schema.json"
)

R5E = (
    ROOT
    / "contracts"
    / "pipeline"
    / "MC_RAVEN_REPRESENTATION_REPORT_BINDING.md"
)

R5F = (
    ROOT
    / "contracts"
    / "pipeline"
    / "RAVEN_HUMAN_GATE_PUBLICATION_ACTION_BOUNDARY.md"
)

R5G = (
    ROOT
    / "contracts"
    / "pipeline"
    / "DECISION_OPTION_LINEAGE.md"
)

RAVEN = (
    ROOT
    / "Modules"
    / "Raven"
    / "raven_contract.md"
)

REPORT_STATUSES = {
    "OK",
    "DEGRADED",
    "FAILED_TRACEABILITY",
    "INSUFFICIENT_EVIDENCE",
    "BLOCKED",
}

PUBLICATION_STATES = {
    "DRAFT",
    "RENDERED",
    "PUBLICATION_READY",
    "PUBLICATION_APPROVED",
}

REPORT_CLASSES = {
    "HUMAN_READABLE",
    "STRUCTURED",
    "EXECUTIVE",
    "TECHNICAL",
    "AUDIT",
    "GOVERNANCE",
    "DECISION_SUPPORT",
}


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def compute_report_id(record):
    preimage = {
        key: value
        for key, value in record.items()
        if key != "report_id"
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
        record.get("report_id")
        != compute_report_id(record)
    ):
        errors.append(
            "report_id does not recompute from record"
        )

    for field in (
        "report_class",
        "rendering_profile",
        "raven_representation_id",
        "object_id",
        "room_revision_id",
        "room_state_root",
        "authorized_view_root",
        "evidence_boundary_reference",
        "evidence_ceiling_reference",
        "coordinate_reference",
        "lineage_reference",
        "provenance_route",
        "report_status",
        "publication_state",
    ):
        if record.get(field) in (
            None,
            "",
            {},
            [],
        ):
            errors.append(
                f"Report rendering requires {field}"
            )

    if (
        record.get("report_class")
        not in REPORT_CLASSES
    ):
        errors.append(
            "invalid report class"
        )

    if (
        record.get("report_status")
        not in REPORT_STATUSES
    ):
        errors.append(
            "invalid report status"
        )

    if (
        record.get("publication_state")
        not in PUBLICATION_STATES
    ):
        errors.append(
            "invalid publication state"
        )

    if (
        record.get("publication_state")
        == "PUBLICATION_APPROVED"
        and not record.get(
            "human_gate_decision_reference"
        )
    ):
        errors.append(
            "PUBLICATION_APPROVED requires Human Gate decision reference"
        )

    if (
        record.get("authority_state")
        != "NONE"
    ):
        errors.append(
            "Report authority_state must remain NONE"
        )

    if (
        record.get("human_gate_state")
        != "ACTIVE"
    ):
        errors.append(
            "Report Human Gate state must remain ACTIVE"
        )

    finding_ids = set()

    for finding in record.get(
        "findings",
        []
    ):
        finding_id = finding.get(
            "finding_id"
        )

        if not finding_id:
            errors.append(
                "report finding requires finding_id"
            )
            continue

        if finding_id in finding_ids:
            errors.append(
                "report finding_id must be unique"
            )

        finding_ids.add(
            finding_id
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

        classification = finding.get(
            "classification"
        )

        if (
            finding_id
            and classification != "UNKNOWN"
            and finding_id not in trace_claims
        ):
            errors.append(
                "material report finding requires trace mapping"
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
                "report MC response class must be named"
            )
            continue

        if response_class in seen_classes:
            errors.append(
                "report may not duplicate MC response class"
            )

        seen_classes.add(
            response_class
        )

        if (
            disposition == "CONDITIONAL"
            and not result.get(
                "required_conditions"
            )
        ):
            errors.append(
                "report must preserve conditions for CONDITIONAL class"
            )

        if (
            disposition == "INADMISSIBLE"
            and not result.get(
                "inadmissibility_reasons"
            )
        ):
            errors.append(
                "report must preserve reasons for INADMISSIBLE class"
            )

    for redaction in record.get(
        "redaction_references",
        []
    ):
        if (
            redaction.get(
                "existence_preserved"
            )
            is not True
        ):
            errors.append(
                "report redaction must preserve restricted-content existence"
            )

    return errors


def validate():
    errors = []

    for path, label in (
        (
            CONTRACT,
            "R5-H contract"
        ),
        (
            SCHEMA,
            "R5-H schema"
        ),
        (
            R5E,
            "R5-E Raven binding"
        ),
        (
            R5F,
            "R5-F Human Gate boundary"
        ),
        (
            R5G,
            "R5-G Decision Option lineage"
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
        "A report is a bounded rendering of attributable analytical state.",
        "Report != analytical state.",
        "Report != truth authority.",
        "Report != publication authority.",
        "Report != certification.",
        "Rendering != mutation.",
        "R5-H does not create a new truth-producing pipeline stage.",
        "Rendered text is not source-of-truth.",
        "A report does not create a new Room.",
        "PDF != new Room.",
        "JSON != new Room.",
        "Markdown != new Room.",
        "Audience-specific rendering != new Room.",
        "Report copy != analytical clone.",
        "Rendering != access expansion.",
        "Export != authorization expansion.",
        "Formatting source material != admitting new evidence.",
        "Presentation convenience != evidence admission.",
        "Better presentation != stronger evidence.",
        "Rendered confidence != higher claim ceiling.",
        "Rendering transform != analytical transform.",
        "Presentation may change.",
        "Supported meaning may not.",
        "Unknown != false.",
        "Unknown != omission permission.",
        "Conditional MUST NOT render as approved.",
        "Inadmissible MUST NOT render as recommended.",
        "Admissible MUST NOT render as authorized.",
        "Rendering order MUST NOT silently become analytical rank.",
        "First displayed option != preferred option.",
        "Visual emphasis != decision authority.",
        "PENDING MUST NOT render as likely approval.",
        "APPROVED MUST NOT render as execution completed.",
        "DENIED MUST NOT render as false analysis.",
        "Rendered != published.",
        "Publication-ready != published.",
        "Publication-ready != approved.",
        "Report existence != publication.",
        "Report class does not change analytical truth.",
        "Human-readable != less attributable.",
        "Readable != compressed out.",
        "JSON identity != Room identity.",
        "Serialization != canonical promotion.",
        "Trace map != certification.",
        "Similar findings != same finding.",
        "Summary grouping MUST preserve individual traceability.",
        "No Compression Out applies to unknowns.",
        "Condition != decoration.",
        "Showing inadmissible state != endorsing it.",
        "Restricted content MUST NOT silently become nonexistent.",
        "Redaction != deletion.",
        "Restricted != absent.",
        "Reports do not own Cartography.",
        "Visualization != new analysis.",
        "Aesthetic emphasis != evidence.",
        "Semantic equivalence != byte identity.",
        "Report identity != Room identity.",
        "Report identity != truth.",
        "OK != approved.",
        "DEGRADED != false.",
        "PUBLICATION_APPROVED != published.",
        "Changed report != previously approved report.",
        "Prior approval != standing publication approval.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Report validation != authority.",
        "Render success != authority.",
        "Summary != erasure.",
        "Compact != incomplete truth lineage.",
        "Fail closed.",
        "Do not improve analytical meaning through rendering.",
        "R5-I owns Pipeline Cross-Stage Integrity / No-Responsibility-Absorption.",
    ]

    for lock in locks:
        if (
            " ".join(lock.split())
            not in text
        ):
            errors.append(
                f"missing R5-H lock: {lock}"
            )

    raven = normalized(
        RAVEN
    )

    raven_locks = [
        "Human-Readable Report",
        "Structured Report (JSON)",
        "Trace Map (Mandatory)",
        "Every material claim MUST map",
        "Raven MUST NEVER guess through a failure.",
    ]

    for lock in raven_locks:
        if (
            " ".join(lock.split())
            not in raven
        ):
            errors.append(
                f"existing Raven report semantic missing: {lock}"
            )

    try:
        schema = load(
            SCHEMA
        )
    except Exception as exc:
        return [
            f"invalid R5-H schema JSON: {exc}"
        ]

    properties = set(
        schema.get(
            "properties",
            {}
        )
    )

    forbidden = {
        "new_evidence",
        "pmc_world_selection",
        "mc_disposition_override",
        "decision_authority",
        "execution_authorization",
        "publication_execution",
        "canonical_promotion",
        "room_lifecycle_transition",
        "cartography_mutation",
        "evidence_boundary_override",
        "evidence_ceiling_override",
    }

    leaked = (
        properties
        & forbidden
    )

    if leaked:
        errors.append(
            "R5-H improperly absorbs analysis/authority semantics: "
            + ", ".join(
                sorted(leaked)
            )
        )

    record = {
        "schema_version":
            "1.0",
        "report_class":
            "TECHNICAL",
        "rendering_profile": {
            "format":
                "markdown",
            "audience":
                "technical",
            "density":
                "full",
            "language":
                "en"
        },
        "raven_representation_id":
            "sha512:" + "1" * 128,
        "decision_option_references": [
            "decision-option:a"
        ],
        "human_gate_decision_reference":
            None,
        "object_id":
            "sha512:" + "2" * 128,
        "room_revision_id":
            "revision:a",
        "room_state_root":
            "sha512:" + "3" * 128,
        "authorized_view_root":
            "sha512:" + "4" * 128,
        "evidence_boundary_reference":
            "boundary:a",
        "evidence_ceiling_reference":
            "ceiling:a",
        "coordinate_reference":
            "coordinate:a",
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
            "Attribution remains unknown."
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
                    "mitigation",
                "disposition":
                    "CONDITIONAL",
                "required_conditions": [
                    "condition:a"
                ],
                "inadmissibility_reasons": []
            },
            {
                "response_class":
                    "escalation",
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
                    "pmc:a",
                    "ccr:a",
                    "mc:a",
                    "raven:a"
                ]
            }
        ],
        "redaction_references": [
            {
                "restricted_reference":
                    "restricted:a",
                "existence_preserved":
                    True,
                "governing_reference":
                    "governance:redaction:a"
            }
        ],
        "lineage_reference":
            "lineage:a",
        "provenance_route": [
            "room:a",
            "pmc:a",
            "ccr:a",
            "mc:a",
            "raven:a",
            "report:a"
        ],
        "report_status":
            "DEGRADED",
        "publication_state":
            "RENDERED",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "report_id"
    ] = compute_report_id(
        record
    )

    errors.extend(
        validate_record(
            record
        )
    )

    no_trace = json.loads(
        json.dumps(record)
    )

    no_trace[
        "trace_map"
    ] = []

    no_trace[
        "report_id"
    ] = compute_report_id(
        no_trace
    )

    if not any(
        "material report finding requires trace mapping"
        in error
        for error in validate_record(
            no_trace
        )
    ):
        errors.append(
            "R5-H incorrectly permitted untraceable material report finding"
        )

    lost_condition = json.loads(
        json.dumps(record)
    )

    lost_condition[
        "mc_response_class_results"
    ][1][
        "required_conditions"
    ] = []

    lost_condition[
        "report_id"
    ] = compute_report_id(
        lost_condition
    )

    if not any(
        "preserve conditions"
        in error
        for error in validate_record(
            lost_condition
        )
    ):
        errors.append(
            "R5-H incorrectly erased conditional requirement"
        )

    lost_reason = json.loads(
        json.dumps(record)
    )

    lost_reason[
        "mc_response_class_results"
    ][2][
        "inadmissibility_reasons"
    ] = []

    lost_reason[
        "report_id"
    ] = compute_report_id(
        lost_reason
    )

    if not any(
        "preserve reasons"
        in error
        for error in validate_record(
            lost_reason
        )
    ):
        errors.append(
            "R5-H incorrectly erased inadmissibility reason"
        )

    approved_without_gate = json.loads(
        json.dumps(record)
    )

    approved_without_gate[
        "publication_state"
    ] = "PUBLICATION_APPROVED"

    approved_without_gate[
        "human_gate_decision_reference"
    ] = None

    approved_without_gate[
        "report_id"
    ] = compute_report_id(
        approved_without_gate
    )

    if not any(
        "PUBLICATION_APPROVED requires Human Gate decision reference"
        in error
        for error in validate_record(
            approved_without_gate
        )
    ):
        errors.append(
            "R5-H incorrectly permitted publication approval without Human Gate"
        )

    lost_restriction = json.loads(
        json.dumps(record)
    )

    lost_restriction[
        "redaction_references"
    ][0][
        "existence_preserved"
    ] = False

    lost_restriction[
        "report_id"
    ] = compute_report_id(
        lost_restriction
    )

    if not any(
        "redaction must preserve restricted-content existence"
        in error
        for error in validate_record(
            lost_restriction
        )
    ):
        errors.append(
            "R5-H incorrectly allowed restricted content to become nonexistent"
        )

    promoted = json.loads(
        json.dumps(record)
    )

    promoted[
        "authority_state"
    ] = "WRITE"

    promoted[
        "report_id"
    ] = compute_report_id(
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
            "R5-H incorrectly permitted report authority promotion"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print(
            "R5-H REPORT / RENDERING CONTRACT: FAIL"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 1

    print(
        "R5-H REPORT / RENDERING CONTRACT: PASS"
    )
    print(
        "Raven / Room / evidence / decision lineage: BOUND"
    )
    print(
        "Human-readable / structured / audience rendering: BOUNDED"
    )
    print(
        "Observed / inferred / unknown / MC conditions: PRESERVED"
    )
    print(
        "Material-claim trace map: ENFORCED"
    )
    print(
        "Restricted-content existence-aware redaction: ENFORCED"
    )
    print(
        "Publication-ready / publication-approved / published: SEPARATED"
    )
    print(
        "Truth / certification / execution / canonical authority: NOT ABSORBED"
    )
    print(
        "R5-I Cross-Stage Integrity: DEFERRED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
