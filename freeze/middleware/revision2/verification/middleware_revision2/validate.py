#!/usr/bin/env python3
"""Source-bound candidate route checks; no deployed middleware execution."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "staged/middleware/CR_GENERIC_CHAT_MIDDLEWARE_ONLY_EXPLICIT_V42_5_4_REVISION_2.md"
SCHEMA = ROOT / "staged/middleware/middleware_route.schema.json"
FIXTURES = Path(__file__).with_name("cases.json")
SOURCES = {
    "canonical/ZERVAN_v40_0_CANONICAL_LOAD.md": "f8328e04b2704b36f4e065b80fa14c65a3a2f1f635bddaaf79ebddbb0e11b158",
    "canonical/Spider/SPIDER_R2_PERSONA_CONTRACT.md": "ab5a01d9c3e3e267a80b33651761a8f9f47d95f14517a72b652ff66af968ccfa",
    "canonical/Spider/SPIDER_R2_FULL_PERSONA_SPECIFICATION.md": "c62e21831129aebccfd397f33003db6cea8955e475a863b2f12a3dced3afcfbe",
    "canonical/incident_response/IN_CHANNEL_CANON_RESET_REQUIREMENTS.md": "8e4d4214a68fd1b4063434fa9c175e578f8019cbba9b65108ff4039dc0dfe0fb",
    "canonical/incident_response/CLEAN_INITIALIZATION_REQUIREMENTS.md": "571a7151b41fce5830598ce2882c8270b0889558b01a07933d38344ffdf53e47",
    "canonical/incident_response/RETRIEVABLE_NOT_SELF_RETURNING.md": "cd9d785a7aa8fab60d1bf79d9598af5af0c0d351e294232d2210a7b6ae829264",
    "change_requests/CR_CHATGPT_CODEX_MIDDLEWARE_CONDITION_V42_5_4.md": "16ed3a1dbf1f715953bdcec0638b1063c910e6a2925cf416b2d5cf35858abf0d",
}
SPIDER_FIELDS = {
    "PERSONA", "SPECIFICATION_VERSION", "REPOSITORY_COMMIT", "PRODUCER",
    "WORK_ID", "INITIATOR", "OPERATION", "QUESTION_REFERENCE",
    "INPUT_REFERENCES", "INPUT_PROVENANCE", "GENERATION_CONSTRAINT",
    "ACCESS_LEDGER", "OUTPUT_REFERENCE", "AUTHORITY_STATE",
    "HUMAN_GATE_STATE", "EVENT_ORDER", "EXECUTION_EVIDENCE",
}


def check(event):
    """Return independent invariant failures for a proposed route/outcome."""
    errors = set()
    mode = event["mode"]
    active = event["disposition"] in {"contribute", "run", "return"}
    if event["reset_pending"] and active:
        errors.add("RESET_REHYDRATION")
    if not event["canon_loaded"] and active:
        errors.add("CANON_NOT_LOADED")
    if event["historical_return"] == "retrieved" and active:
        errors.add("SELF_RETURN")
    if mode == "historical_return" and event["disposition"] == "return" and event["historical_return"] != "qualified_authorized":
        errors.add("RETURN_NOT_QUALIFIED")
    if mode == "full_run" and event["disposition"] == "run" and (not event["question"] or not event["inputs"]):
        errors.add("RUN_GATE")
    if event["access"] != "available" and event["disposition"] == "run":
        errors.add("ACCESS_CEILING")
    if not event["permission"] and active:
        errors.add("PERMISSION_CEILING")
    if event["native_opt_out"] and event["access"] == "available" and event["permission"] and event["canon_loaded"] and not event["reset_pending"]:
        errors.add("NATIVE_VETO")
    if event["attempt_claimed"] and not event["attempt_evidence"]:
        errors.add("INVENTED_ATTEMPT")
    if event["disposition"] == "report_boundary" and event["access"] == "available" and not event["failure_boundary"]:
        errors.add("INVENTED_BOUNDARY")
    if event["persona"] == "SPIDER" and active and not SPIDER_FIELDS.issubset(event["fields"]):
        errors.add("SPIDER_ATTRIBUTION")
    if event["persona"] == "SPIDER" and mode == "full_run" and event["disposition"] == "run" and set(range(1, 14)) != set(event["portable_sections"]):
        errors.add("PORTABLE_RECORD")
    if event["producer"] == "CHAT" and event["persona"] == "SPIDER" and active and event["response_work_id"] != "NONE":
        errors.add("CHAT_RESPONSE_WORK_ID")
    if event["independent_execution_claim"] and (not event["component_issuance"] or not event["component_work_id"] or not event["execution_receipt"]):
        errors.add("UNSUPPORTED_COMPONENT_EXECUTION")
    if event["component_work_id"] and not event["component_issuance"]:
        errors.add("UNISSUED_COMPONENT_ID")
    return errors


def schema_check(event, schema):
    assert set(event) == set(schema["required"])
    assert schema["additionalProperties"] is False
    for field, definition in schema["properties"].items():
        value = event[field]
        if "enum" in definition:
            assert value in definition["enum"], field
        allowed = definition.get("type")
        if allowed:
            types = allowed if isinstance(allowed, list) else [allowed]
            matches = {"string": lambda v: isinstance(v, str),
                       "null": lambda v: v is None,
                       "boolean": lambda v: type(v) is bool,
                       "array": lambda v: isinstance(v, list)}
            assert any(matches[t](value) for t in types), field
        if definition.get("type") == "array":
            item = definition["items"]
            for entry in value:
                assert (isinstance(entry, str) if item["type"] == "string" else type(entry) is int), field
                if "minimum" in item:
                    assert item["minimum"] <= entry <= item["maximum"], field
            if definition.get("uniqueItems"):
                assert len(value) == len(set(value)), field


def main():
    assert hashlib.sha256((ROOT / "freeze/middleware/CR_GENERIC_CHAT_MIDDLEWARE_ONLY_EXPLICIT_V42_5_4.md").read_bytes()).hexdigest() == "8d3f5957274ac40d3e94e74ac6feb65bde1d07b9c8b0e307bd721899fc0f9f92"
    for path, digest in SOURCES.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, f"source changed: {path}"
    spider = (ROOT / "canonical/Spider/SPIDER_R2_PERSONA_CONTRACT.md").read_text()
    reset = (ROOT / "canonical/incident_response/IN_CHANNEL_CANON_RESET_REQUIREMENTS.md").read_text()
    assert "`PRODUCER=CHAT`, `WORK_ID=NONE`" in spider
    assert "Historical return is explicit and qualified" in reset
    assert "RETRIEVABLE ≠ SELF-RETURNING" in (ROOT / "canonical/incident_response/RETRIEVABLE_NOT_SELF_RETURNING.md").read_text()
    source = SPEC.read_text()
    assert "REVISION 2" in source and "COMPONENT_WORK_ID" in source
    for field in SPIDER_FIELDS:
        assert f"`{field}`" in source, f"missing contract field: {field}"
    assert "section 12" in source and "Beagle-validated runtime telemetry" in source
    schema = json.loads(SCHEMA.read_text())
    cases = json.loads(FIXTURES.read_text())
    assert schema["additionalProperties"] is False and len(cases) >= 12
    for case in cases:
        event = case["event"]
        schema_check(event, schema)
        assert case["id"] == event["case_id"]
        observed = check(event)
        assert observed == set(case["expected_errors"]), (case["id"], sorted(observed), case["expected_errors"])
        print(f"{case['id']}: {'PASS' if not observed else 'REJECT ' + ','.join(sorted(observed))}")
    print(f"PASS: {len(cases)} source-bound candidate cases; no runtime or formal observer validation claimed")


if __name__ == "__main__":
    main()
