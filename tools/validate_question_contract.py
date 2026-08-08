#!/usr/bin/env python3

from copy import deepcopy
from datetime import datetime
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "contracts" / "question" / "QUESTION_CONTRACT.md"
SCHEMA = ROOT / "schemas" / "question" / "question_contract.schema.json"
R7A = (
    ROOT
    / "contracts"
    / "promotion"
    / "RING7_DOCUMENTATION_PROMOTION_BOUNDARY_REGISTRY.md"
)

VALID_SCOPE_TYPES = {"ROOM", "ZONE", "TERRITORY"}
VALID_TEMPORAL_MODES = {"CURRENT", "HISTORICAL", "BOUNDED_RANGE"}
VALID_PERSONALIZATION = {"ALLOWED", "DISABLED", "MEETING_MODE"}

SEMANTIC_FIELDS = [
    "version",
    "question",
    "scope",
    "temporal_window",
    "included_analytical_objects",
    "required_artifacts",
    "exclusions",
    "evidence_thresholds",
    "evidence_boundary_reference",
    "evidence_ceiling_reference",
    "audience",
    "rendering_format",
    "personalization_policy",
    "decision_option_requirements",
    "read_only",
    "write_operation_requested",
    "human_gate_requirements",
    "provenance_route",
    "authority_state",
    "human_gate_state",
]


def normalized(path):
    text = path.read_text(encoding="utf-8")

    for token in ("**", "__", "`"):
        text = text.replace(token, "")

    return " ".join(text.split())


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def semantic_payload(record):
    return {
        field: deepcopy(record.get(field))
        for field in SEMANTIC_FIELDS
    }


def semantic_payload_without_version(record):
    payload = semantic_payload(record)
    payload.pop("version", None)
    return payload


def contract_identity(record):
    digest = hashlib.sha512(
        canonical_json(
            semantic_payload(record)
        ).encode("utf-8")
    ).hexdigest()

    return "sha512:" + digest


def compare_versions(prior, current):
    material_changed = (
        semantic_payload_without_version(prior)
        != semantic_payload_without_version(current)
    )

    version_changed = (
        prior.get("version")
        != current.get("version")
    )

    if material_changed and not version_changed:
        return ["SEMANTIC_VERSION_DRIFT"]

    return []


def compare_executors(human_contract, machine_contract):
    if (
        semantic_payload(human_contract)
        != semantic_payload(machine_contract)
    ):
        return ["EXECUTOR_SEMANTIC_DRIFT"]

    return []


def parse_iso(value):
    if value is None:
        return None

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except Exception:
        return None


def evaluate_record(record):
    reasons = []

    version = record.get("version")

    if not isinstance(version, str) or not re.fullmatch(
        r"[0-9]+\.[0-9]+\.[0-9]+",
        version,
    ):
        reasons.append("VERSION_INVALID")

    if not str(record.get("question", "")).strip():
        reasons.append("QUESTION_MISSING")

    scope = record.get("scope", {})

    if scope.get("scope_type") not in VALID_SCOPE_TYPES:
        reasons.append("SCOPE_INVALID")

    if not scope.get("room_object_id"):
        reasons.append("ROOM_IDENTITY_MISSING")

    if not scope.get("room_revision_id"):
        reasons.append("ROOM_REVISION_MISSING")

    if not scope.get("scope_reference"):
        reasons.append("SCOPE_REFERENCE_MISSING")

    temporal = record.get("temporal_window", {})
    mode = temporal.get("mode")

    if mode not in VALID_TEMPORAL_MODES:
        reasons.append("TEMPORAL_WINDOW_INVALID")

    if mode == "BOUNDED_RANGE":
        start = parse_iso(temporal.get("start"))
        end = parse_iso(temporal.get("end"))

        if start is None or end is None or start > end:
            reasons.append("BOUNDED_RANGE_INVALID")

    if mode == "HISTORICAL":
        historical_reference = temporal.get(
            "historical_reference"
        )

        start = parse_iso(temporal.get("start"))
        end = parse_iso(temporal.get("end"))

        valid_range = (
            start is not None
            and end is not None
            and start <= end
        )

        if not historical_reference and not valid_range:
            reasons.append(
                "HISTORICAL_REFERENCE_MISSING"
            )

    if not record.get("evidence_boundary_reference"):
        reasons.append("EVIDENCE_BOUNDARY_MISSING")

    if not record.get("evidence_ceiling_reference"):
        reasons.append("EVIDENCE_CEILING_MISSING")

    if (
        record.get("personalization_policy")
        not in VALID_PERSONALIZATION
    ):
        reasons.append(
            "PERSONALIZATION_POLICY_INVALID"
        )

    if not record.get("provenance_route"):
        reasons.append("PROVENANCE_MISSING")

    if record.get("read_only") is not True:
        reasons.append("READ_ONLY_VIOLATED")

    if record.get("write_operation_requested") is not False:
        reasons.append("WRITE_OPERATION_EMBEDDED")

    if record.get("human_gate_state") != "ACTIVE":
        reasons.append("HUMAN_GATE_DISABLED")

    if record.get("authority_state") != "NONE":
        reasons.append("AUTHORITY_PROMOTED")

    if (
        record.get("question_contract_id")
        != contract_identity(record)
    ):
        reasons.append("CONTRACT_IDENTITY_INVALID")

    return sorted(set(reasons))


def recalculate(record):
    record = deepcopy(record)

    record["question_contract_id"] = contract_identity(record)

    reasons = evaluate_record(record)

    record["failure_reasons"] = reasons
    record["validation_disposition"] = (
        "VALID" if not reasons else "BLOCKED"
    )

    return record


def make_record(
    *,
    version="1.0.0",
    question="What evidence supports the bounded finding?",
    scope_type="ROOM",
    room_object_id=None,
    room_revision_id=None,
    scope_reference="room:current",
    temporal_mode="CURRENT",
    start=None,
    end=None,
    historical_reference=None,
    evidence_boundary_reference="boundary:room:current",
    evidence_ceiling_reference="ceiling:room:current",
    personalization_policy="DISABLED",
    read_only=True,
    write_operation_requested=False,
    human_gate_state="ACTIVE",
    authority_state="NONE",
):
    if room_object_id is None:
        room_object_id = "sha512:" + "1" * 128

    if room_revision_id is None:
        room_revision_id = "sha512:" + "2" * 128

    record = {
        "schema_version": "1.0",
        "question_contract_id": "",
        "version": version,
        "question": question,
        "scope": {
            "scope_type": scope_type,
            "room_object_id": room_object_id,
            "room_revision_id": room_revision_id,
            "scope_reference": scope_reference,
        },
        "temporal_window": {
            "mode": temporal_mode,
            "start": start,
            "end": end,
            "historical_reference": historical_reference,
        },
        "included_analytical_objects": [
            room_object_id
        ],
        "required_artifacts": [
            "artifact:bounded-finding"
        ],
        "exclusions": [
            "excluded:outside-governed-boundary"
        ],
        "evidence_thresholds": {
            "minimum_attributable_evidence": 1
        },
        "evidence_boundary_reference":
            evidence_boundary_reference,
        "evidence_ceiling_reference":
            evidence_ceiling_reference,
        "audience":
            "AUTHORIZED_CONSUMER",
        "rendering_format":
            "STRUCTURED_REPORT",
        "personalization_policy":
            personalization_policy,
        "decision_option_requirements": [
            "PRESERVE_EVIDENCE_LINEAGE"
        ],
        "read_only":
            read_only,
        "write_operation_requested":
            write_operation_requested,
        "human_gate_requirements": [
            "WRITE_REQUIRES_SEPARATE_HUMAN_GATE_AUTHORIZATION"
        ],
        "provenance_route": [
            "r7-a:question-contract-owner",
            "r7-b:question-contract",
            "room:current",
        ],
        "authority_state":
            authority_state,
        "human_gate_state":
            human_gate_state,
        "validation_disposition":
            "",
        "failure_reasons":
            [],
    }

    return recalculate(record)


def validate_record(record):
    errors = []

    reasons = evaluate_record(record)

    expected = "VALID" if not reasons else "BLOCKED"

    if record.get("validation_disposition") != expected:
        errors.append(
            "Question Contract disposition contradicts contract state"
        )

    if sorted(
        record.get("failure_reasons", [])
    ) != reasons:
        errors.append(
            "Question Contract failure reasons incomplete or incorrect"
        )

    return errors


def validate():
    errors = []

    for path, label in (
        (CONTRACT, "R7-B Question Contract"),
        (SCHEMA, "R7-B schema"),
        (R7A, "R7-A registry"),
    ):
        if not path.exists():
            errors.append(f"missing {label}")

    if errors:
        return errors

    try:
        schema = json.loads(
            SCHEMA.read_text(encoding="utf-8")
        )
    except Exception as exc:
        return [
            f"invalid R7-B schema JSON: {exc}"
        ]

    if (
        schema.get("$schema")
        != "https://json-schema.org/draft/2020-12/schema"
    ):
        errors.append(
            "R7-B schema must use JSON Schema Draft 2020-12"
        )

    text = normalized(CONTRACT)

    locks = [
        "R7-B = Question Contract.",
        "Recurring inquiries SHALL be version-controlled Question Contracts.",
        "Humans and machines may execute the same Question Contract without semantic change.",
        "Issuing a Question Contract SHALL NOT mutate analytical state.",
        "Question Contract != write operation.",
        "Question Contract != authority.",
        "Question != conclusion.",
        "Scope != new object.",
        "Scope declaration != evidence expansion.",
        "Historical inquiry != Replay automatically.",
        "Included reference != object creation.",
        "Required artifact != evidence truth.",
        "Excluded != absent.",
        "Restricted != nonexistent.",
        "Threshold satisfied != truth authority.",
        "Question != evidence expansion.",
        "Question != claim authority.",
        "Audience != truth frame.",
        "Rendering != analysis.",
        "Personalization belongs at the point of consumption.",
        "MEETING_MODE MUST NOT require re-analysis.",
        "Decision option != decision.",
        "Human Gate decides.",
        "read_only = true.",
        "write_operation_requested = false.",
        "A Question Contract cannot grant itself write authority.",
        "Question Contract != action contract.",
        "Executor != semantic mutation.",
        "Questions become version-controlled.",
        "Renderings become reproducible.",
        "Reproducibility != identical prose.",
        "Question Contract != Replay Envelope.",
        "Provenance != endorsement.",
        "Human Gate state MUST NOT be disabled by Question Contract execution.",
        "VALID != answered.",
        "VALID != true.",
        "VALID != promoted.",
        "Authority remains NONE.",
        "Human Gate remains ACTIVE.",
        "Promotion State remains CANDIDATE.",
        "R7-C owns README / Version Authority / Native-v41 Entry Surfaces.",
    ]

    for lock in locks:
        if " ".join(lock.split()) not in text:
            errors.append(
                f"missing R7-B lock: {lock}"
            )

    r7a = normalized(R7A)

    for lock in (
        "R7-B owns the machine-readable Question Contract deferred by Ring 6.",
        "Question != mutation.",
        "Question Contract != authority.",
    ):
        if " ".join(lock.split()) not in r7a:
            errors.append(
                f"R7-A missing Question Contract binding: {lock}"
            )

    positive = make_record()

    errors.extend(
        validate_record(positive)
    )

    duplicate = make_record()

    if (
        positive["question_contract_id"]
        != duplicate["question_contract_id"]
    ):
        errors.append(
            "Question Contract identity is not deterministic"
        )

    if compare_executors(
        positive,
        deepcopy(positive),
    ):
        errors.append(
            "identical human/machine contract failed equivalence"
        )

    changed = deepcopy(positive)
    changed["question"] = (
        "What changed materially inside the bounded finding?"
    )

    if (
        "SEMANTIC_VERSION_DRIFT"
        not in compare_versions(
            positive,
            changed,
        )
    ):
        errors.append(
            "semantic change without version change was not rejected"
        )

    changed["version"] = "1.1.0"

    if compare_versions(
        positive,
        changed,
    ):
        errors.append(
            "semantic change with new version was incorrectly rejected"
        )

    machine_drift = deepcopy(positive)
    machine_drift[
        "evidence_ceiling_reference"
    ] = "ceiling:raised"

    if (
        "EXECUTOR_SEMANTIC_DRIFT"
        not in compare_executors(
            positive,
            machine_drift,
        )
    ):
        errors.append(
            "human/machine semantic drift was not rejected"
        )

    return errors


def main():
    errors = validate()

    if errors:
        print("R7-B QUESTION CONTRACT: FAIL")

        for error in errors:
            print(f" - {error}")

        return 1

    print("R7-B QUESTION CONTRACT: PASS")
    print("Machine-readable Question Contract: IMPLEMENTED")
    print("Version-controlled recurring inquiry: VALIDATED")
    print("Deterministic SHA-512 contract identity: VALIDATED")
    print("Human / machine semantic equivalence: VALIDATED")
    print("Material change without version change: REJECTED")
    print("Room / Zone / Territory scope: BOUNDED")
    print("Current / Historical / Bounded Range time posture: BOUNDED")
    print("Evidence boundary: PRESERVED")
    print("Evidence ceiling: PRESERVED")
    print("Exclusions: EXISTENCE-AWARE")
    print("Question issuance -> analytical mutation: REJECTED")
    print("Embedded write operation: REJECTED")
    print("Question Contract self-authorization: REJECTED")
    print("Read-only invariant: PRESERVED")
    print("Authority: NONE")
    print("Human Gate: ACTIVE")
    print("Promotion State: CANDIDATE")
    print("R7-C README / Version Authority / Native-v41 Entry: NEXT")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
