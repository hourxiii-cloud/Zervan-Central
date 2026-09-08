#!/usr/bin/env python3
"""Fail-closed semantic validator for the candidate v42 control chain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools" / "generate_artifacts.py"

sys.path.insert(0, str(ROOT / "tools"))
import generate_artifacts as generated  # noqa: E402

REQUIRED_CONTROL = {
    "authority_state": "NONE",
    "human_gate_state": "ACTIVE",
    "canonical": False,
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def record_id(record):
    body = {key: value for key, value in record.items() if key != "record_id"}
    return "sha512:" + hashlib.sha512(canonical(body).encode()).hexdigest()


def validate_shape(record):
    errors = []
    kind = record.get("record_type")
    if kind not in generated.RECORDS:
        return ["UNKNOWN_RECORD_TYPE"]
    required = ["schema_version", "record_type", "record_id", *generated.RECORDS[kind], *REQUIRED_CONTROL]
    for field in required:
        if field not in record or record[field] in (None, ""):
            errors.append(f"MISSING:{field}")
    if record.get("schema_version") != "1.0": errors.append("SCHEMA_VERSION_INVALID")
    if record.get("record_id") != record_id(record): errors.append("RECORD_ID_MISMATCH")
    for field, expected in REQUIRED_CONTROL.items():
        if record.get(field) != expected: errors.append(f"CONTROL_STATE_INVALID:{field}")
    for field, allowed in generated.ENUMS.items():
        if field in record and record[field] not in allowed: errors.append(f"ENUM_INVALID:{field}")
    return errors


def validate_semantics(record):
    errors = []
    kind = record.get("record_type")
    if kind == "plural_path":
        if not record.get("lineage"): errors.append("PLURAL_LINEAGE_REQUIRED")
    elif kind == "harmony_interpretation":
        if record.get("provocation_authority") != "NONE": errors.append("HARMONY_SCHEDULER_FORBIDDEN")
    elif kind == "trigger_evaluation":
        pseudo = {"HUMAN_SILENCE", "INACTIVITY", "NO_NOVELTY", "CAPABILITY_AVAILABLE", "DISSONANCE_ONLY"}
        if record.get("disposition") == "ELIGIBLE" and record.get("expected_discriminating_value") in pseudo:
            errors.append("PSEUDO_TRIGGER_ELIGIBLE")
        if record.get("disposition") == "EXECUTE": errors.append("TRIGGER_EXECUTION_COLLAPSE")
    elif kind == "pressure_route":
        force = record.get("selected_force")
        work = set(record.get("required_work", []))
        if force in {"SQUAD", "PLATOON"} and "multi-route-required" not in work:
            errors.append("FORCE_ESCALATION_WITHOUT_CAPABILITY_GAP")
        if force == "ANIMALKINGDOM" and "canonical-synthetic-adversarial" not in work:
            errors.append("ANIMALKINGDOM_CONTRACT_MISMATCH")
        if force not in {"NON_MOTION", "NO_ADMISSIBLE_ROUTE"} and not record.get("rejected_stronger_force"):
            errors.append("STRONGER_FORCE_REJECTION_REQUIRED")
    elif kind == "carrier_admissibility":
        if record.get("disposition") not in {"ADMISSIBLE", "CONDITIONALLY_ADMISSIBLE", "INADMISSIBLE", "UNKNOWN"}:
            errors.append("CARRIER_SELF_ADMISSION_OR_INVALID_DISPOSITION")
        if record.get("carrier_id", "").lower().startswith("animalkingdom") and record.get("input_class") != "CANONICAL_READ_ONLY":
            errors.append("ANIMALKINGDOM_INPUT_INADMISSIBLE")
    elif kind == "execution_authorization":
        if record.get("external_action") != "DISABLED": errors.append("EXTERNAL_ACTION_FORBIDDEN")
        if record.get("disposition") == "AUTHORIZED" and not record.get("authorization_source"):
            errors.append("POSITIVE_AUTHORIZATION_SOURCE_REQUIRED")
    elif kind == "execution_trace":
        forbidden = {"recruit-helper", "expand-mission", "increase-force", "add-input", "replace-object"}
        if forbidden.intersection(record.get("steps", [])): errors.append("IN_RUN_ENVELOPE_VIOLATION")
        if not record.get("envelope_checks"): errors.append("ENVELOPE_CHECKS_REQUIRED")
    elif kind == "termination_record":
        contaminated = record.get("contamination_status") == "CONTAMINATED"
        if contaminated and record.get("object_evidence_admissibility") != "INADMISSIBLE":
            errors.append("CONTAMINATED_OBJECT_EVIDENCE_LAUNDERED")
        if record.get("boundary_status") == "UNKNOWN" and record.get("object_evidence_admissibility") != "UNKNOWN":
            errors.append("UNKNOWN_BOUNDARY_TREATED_AS_CLEAN")
    elif kind == "return_record":
        same = record.get("returned_object_id") == record.get("object_id")
        if record.get("object_continuity") == "PRESERVED" and not same:
            errors.append("FALSE_OBJECT_RESTORATION")
        if record.get("reconstruction_required") and record.get("object_continuity") == "PRESERVED":
            errors.append("RECONSTRUCTION_LAUNDERED_AS_RETURN")
    elif kind == "evidence_qualification":
        allowed = {"QUALIFIED_AT_CURRENT_CEILING", "QUALIFIED_NON_FINDING", "QUALIFIED_CONTROL_FAILURE", "CONDITIONAL", "INADMISSIBLE", "CONTAMINATED", "UNKNOWN"}
        if record.get("disposition") not in allowed: errors.append("FALSE_RESULT_PROMOTION")
        if record.get("contamination_status") == "CONTAMINATED" and record.get("disposition") == "QUALIFIED_AT_CURRENT_CEILING":
            errors.append("CONTAMINATED_RESULT_QUALIFIED")
    elif kind == "delegation_envelope":
        if record.get("execution_limit", 0) > 1000: errors.append("STANDING_DELEGATION_FORBIDDEN")
        if record.get("revoked") and record.get("disposition") == "ACTIVE": errors.append("REVOKED_ENVELOPE_ACTIVE")
    elif kind == "aggregate_closure":
        if not record.get("v41_regression"): errors.append("V41_REGRESSION_NOT_PASSED")
        if not record.get("lossless_recollapse"): errors.append("LOSSLESS_RECOLLAPSE_NOT_PASSED")
        if len(record.get("removal_results", [])) < 4: errors.append("REMOVAL_TESTS_INCOMPLETE")
    return errors


def validate_record(record):
    return validate_shape(record) + validate_semantics(record)


def validate_pipeline(records):
    errors = []
    by_type = {}
    ids = set()
    for index, item in enumerate(records):
        item_errors = validate_record(item)
        errors.extend(f"{index}:{item.get('record_type')}:{err}" for err in item_errors)
        if item.get("record_id") in ids: errors.append(f"{index}:DUPLICATE_RECORD_ID")
        ids.add(item.get("record_id")); by_type[item.get("record_type")] = item
    expected = set(generated.RECORDS)
    missing = expected - set(by_type)
    errors.extend(f"MISSING_RECORD_TYPE:{name}" for name in sorted(missing))
    if missing: return errors

    object_ids = {item.get("object_id") for item in records}
    if len(object_ids) != 1: errors.append("GOVERNED_OBJECT_IDENTITY_DIVERGED")

    links = [
        ("harmony_interpretation", "mobius_state_id", "mobius_state"),
        ("pressure_route", "trigger_evaluation_id", "trigger_evaluation"),
        ("carrier_admissibility", "pressure_route_id", "pressure_route"),
        ("execution_authorization", "carrier_admissibility_id", "carrier_admissibility"),
        ("execution_trace", "execution_authorization_id", "execution_authorization"),
        ("termination_record", "execution_id", "execution_trace"),
        ("return_record", "execution_id", "execution_trace"),
        ("evidence_qualification", "return_record_id", "return_record"),
    ]
    for child, field, parent in links:
        if by_type[child].get(field) != by_type[parent].get("record_id"):
            errors.append(f"HANDOFF_MISMATCH:{child}:{field}")

    ceilings = [by_type["mobius_state"].get("evidence_ceiling"), by_type["harmony_interpretation"].get("evidence_ceiling")]
    if len(set(ceilings)) != 1: errors.append("HARMONY_EVIDENCE_CEILING_RAISED")
    if by_type["trigger_evaluation"].get("coordinate") != by_type["mobius_state"].get("coordinate"):
        errors.append("TRIGGER_COORDINATE_MISMATCH")
    if by_type["pressure_route"].get("mission_question") != by_type["trigger_evaluation"].get("question"):
        errors.append("ROUTER_INVENTED_MISSION")
    if by_type["execution_trace"].get("carrier_id") != by_type["carrier_admissibility"].get("carrier_id"):
        errors.append("CARRIER_SUBSTITUTED")
    if by_type["return_record"].get("returned_object_id") != by_type["return_record"].get("object_id"):
        errors.append("OBJECT_REPLACED_ON_RETURN")
    closure_refs = set(by_type["aggregate_closure"].get("stage_records", []))
    required_refs = {r["record_id"] for r in records if r["record_type"] != "aggregate_closure"}
    if not required_refs.issubset(closure_refs): errors.append("LOSSLESS_CLOSURE_DROPPED_RECORD")
    return errors


def validate_fixtures():
    positive = json.loads((ROOT / "fixtures" / "positive" / "aggregate_pipeline.json").read_text())
    errors = validate_pipeline(positive)
    if errors: return ["POSITIVE_FIXTURE_FAILED:" + e for e in errors]
    failures = []
    for path in sorted((ROOT / "fixtures" / "negative").glob("*.json")):
        if not validate_record(json.loads(path.read_text())):
            failures.append(f"NEGATIVE_FIXTURE_NOT_REJECTED:{path.name}")
    return failures


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--fixtures", action="store_true"); parser.add_argument("paths", nargs="*"); args = parser.parse_args()
    errors = []
    if args.fixtures or not args.paths: errors.extend(validate_fixtures())
    for value in args.paths:
        path = Path(value); payload = json.loads(path.read_text())
        errors.extend(validate_pipeline(payload) if isinstance(payload, list) else validate_record(payload))
    if errors:
        print("candidate v42 validation: FAIL"); print("\n".join(f"- {e}" for e in errors)); return 1
    print("candidate v42 validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

