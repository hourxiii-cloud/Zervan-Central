#!/usr/bin/env python3
"""Deterministically generate strict v42 schemas, fixtures, and integrity manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]

RECORDS = {
    "plural_path": ["object_id", "path_id", "source", "lineage", "independence_status", "uncertainties"],
    "mobius_state": ["object_id", "coordinate", "human_lineage", "zervan_lineage", "evidence_ceiling", "causality_status"],
    "harmony_interpretation": ["object_id", "mobius_state_id", "patterns", "evidence_ceiling", "unresolved_influence", "provocation_authority"],
    "trigger_evaluation": ["object_id", "coordinate", "initiation_class", "question", "evidence_refs", "expected_discriminating_value", "disposition"],
    "pressure_route": ["object_id", "trigger_evaluation_id", "mission_question", "required_work", "selected_force", "rejected_stronger_force", "disposition"],
    "carrier_admissibility": ["object_id", "pressure_route_id", "carrier_id", "contract_ref", "input_class", "pressure_envelope", "disposition"],
    "execution_authorization": ["object_id", "carrier_admissibility_id", "authorization_source", "execution_limit", "external_action", "disposition"],
    "execution_trace": ["object_id", "execution_authorization_id", "carrier_id", "steps", "envelope_checks", "completion_state"],
    "termination_record": ["object_id", "execution_id", "termination_state", "boundary_status", "contamination_status", "object_evidence_admissibility"],
    "return_record": ["object_id", "execution_id", "starting_coordinate", "returned_object_id", "object_continuity", "reconstruction_required", "result_status"],
    "evidence_qualification": ["object_id", "return_record_id", "claim_id", "evidence_class", "independence_status", "contamination_status", "disposition"],
    "delegation_envelope": ["object_id", "permitted_trigger_classes", "permitted_carriers", "max_force", "execution_limit", "expires_at", "revoked", "disposition"],
    "aggregate_closure": ["object_id", "stage_records", "removal_results", "v41_regression", "lossless_recollapse", "disposition"],
}

ENUMS = {
    "independence_status": ["QUALIFIED", "DEPENDENT", "UNKNOWN"],
    "causality_status": ["SUPPORTED", "UNSUPPORTED", "UNKNOWN"],
    "provocation_authority": ["NONE"],
    "initiation_class": ["HUMAN_DIRECTED", "ZERVAN_ENDOGENOUS_CANDIDATE", "SYSTEM_CONTROL_REQUIRED", "UNKNOWN_SOURCE"],
    "selected_force": ["NON_MOTION", "OBSERVATION", "BOUNDED_PROBE", "SPECIALIST", "MULTI_CAPABILITY_SET", "SQUAD", "PLATOON", "ANIMALKINGDOM", "NO_ADMISSIBLE_ROUTE"],
    "external_action": ["DISABLED"],
    "completion_state": ["COMPLETED", "VALID_NON_FINDING", "STOPPED_IN_BOUNDS", "FAILED_IN_BOUNDS", "ABORTED", "CONTAMINATED"],
    "termination_state": ["COMPLETED", "VALID_NON_FINDING", "STOPPED_IN_BOUNDS", "FAILED_IN_BOUNDS", "ABORTED_PRE_VIOLATION", "ABORTED_BOUNDARY_UNKNOWN", "CONTAMINATED", "TERMINATION_FAILED", "RETURN_FAILED", "UNKNOWN_TERMINATION"],
    "boundary_status": ["PRESERVED", "VIOLATED", "UNKNOWN"],
    "contamination_status": ["CLEAN", "CONTAMINATED", "UNKNOWN"],
    "object_evidence_admissibility": ["UNQUALIFIED", "QUALIFICATION_REQUIRED", "INADMISSIBLE", "UNKNOWN"],
    "object_continuity": ["PRESERVED", "BROKEN", "UNKNOWN"],
    "result_status": ["UNQUALIFIED", "QUALIFIED", "NON_FINDING", "CONTAMINATED", "UNKNOWN"],
    "evidence_class": ["OBSERVATION", "INFERENCE", "SYNTHETIC", "SIMULATED", "REPRODUCED", "CONTRADICTION", "NON_FINDING", "CONTROL_FAILURE", "CONTAMINATED", "UNKNOWN"],
}

ARRAY_FIELDS = {
    "lineage", "uncertainties", "human_lineage", "zervan_lineage", "patterns",
    "unresolved_influence", "evidence_refs", "required_work", "rejected_stronger_force",
    "steps", "envelope_checks", "permitted_trigger_classes", "permitted_carriers",
    "stage_records", "removal_results",
}

BOOL_FIELDS = {"reconstruction_required", "revoked", "v41_regression", "lossless_recollapse"}
INT_FIELDS = {"execution_limit"}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return "sha512:" + hashlib.sha512(canonical(value).encode()).hexdigest()


def ref(label):
    return digest({"ref": label})


def schema_for(name, fields):
    props = {
        "schema_version": {"type": "string", "const": "1.0"},
        "record_type": {"type": "string", "const": name},
        "record_id": {"type": "string", "pattern": "^sha512:[0-9a-f]{128}$"},
        "authority_state": {"type": "string", "const": "NONE"},
        "human_gate_state": {"type": "string", "const": "ACTIVE"},
        "canonical": {"type": "boolean", "const": False},
    }
    for field in fields:
        if field in ENUMS:
            props[field] = {"type": "string", "enum": ENUMS[field]}
        elif field in ARRAY_FIELDS:
            props[field] = {"type": "array"}
        elif field in BOOL_FIELDS:
            props[field] = {"type": "boolean"}
        elif field in INT_FIELDS:
            props[field] = {"type": "integer", "minimum": 1}
        else:
            props[field] = {"type": ["string", "object", "array", "boolean", "integer"], "minLength": 1}
    required = ["schema_version", "record_type", "record_id", *fields, "authority_state", "human_gate_state", "canonical"]
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"zervan://candidate/v42/schemas/{name}.schema.json",
        "title": f"Zervan candidate v42 {name}",
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": props,
    }


def record(name, **values):
    body = {
        "schema_version": "1.0", "record_type": name,
        **values, "authority_state": "NONE", "human_gate_state": "ACTIVE", "canonical": False,
    }
    body["record_id"] = digest(body)
    return body


def positive_pipeline():
    obj = ref("governed-object")
    plural = record("plural_path", object_id=obj, path_id="path:zervan:1", source="ZERVAN", lineage=["source:z", "transform:1"], independence_status="QUALIFIED", uncertainties=[])
    mobius = record("mobius_state", object_id=obj, coordinate="c:1", human_lineage=["human:1"], zervan_lineage=[plural["record_id"]], evidence_ceiling="CANDIDATE", causality_status="UNKNOWN")
    harmony = record("harmony_interpretation", object_id=obj, mobius_state_id=mobius["record_id"], patterns=["qualified-material-contradiction"], evidence_ceiling="CANDIDATE", unresolved_influence=["cause:unknown"], provocation_authority="NONE")
    trigger = record("trigger_evaluation", object_id=obj, coordinate="c:1", initiation_class="ZERVAN_ENDOGENOUS_CANDIDATE", question="Can bounded observation discriminate two attributable paths?", evidence_refs=[plural["record_id"], mobius["record_id"], harmony["record_id"]], expected_discriminating_value="distinguish trail from reflection", disposition="ELIGIBLE")
    route = record("pressure_route", object_id=obj, trigger_evaluation_id=trigger["record_id"], mission_question=trigger["question"], required_work=["observe-existing-state"], selected_force="OBSERVATION", rejected_stronger_force=["SQUAD:not-required", "PLATOON:not-required", "ANIMALKINGDOM:contract-not-required"], disposition="ROUTED")
    carrier = record("carrier_admissibility", object_id=obj, pressure_route_id=route["record_id"], carrier_id="goblin:observer:1", contract_ref="candidate:bounded-observer", input_class="CANDIDATE_READ_ONLY", pressure_envelope="OBSERVATION_ONLY", disposition="ADMISSIBLE")
    auth = record("execution_authorization", object_id=obj, carrier_admissibility_id=carrier["record_id"], authorization_source="human-gate:bounded-test-fixture", execution_limit=1, external_action="DISABLED", disposition="AUTHORIZED")
    trace = record("execution_trace", object_id=obj, execution_authorization_id=auth["record_id"], carrier_id=carrier["carrier_id"], steps=["inspect", "report"], envelope_checks=["object:match", "force:observation", "authority:none"], completion_state="COMPLETED")
    term = record("termination_record", object_id=obj, execution_id=trace["record_id"], termination_state="COMPLETED", boundary_status="PRESERVED", contamination_status="CLEAN", object_evidence_admissibility="QUALIFICATION_REQUIRED")
    ret = record("return_record", object_id=obj, execution_id=trace["record_id"], starting_coordinate="c:1", returned_object_id=obj, object_continuity="PRESERVED", reconstruction_required=False, result_status="UNQUALIFIED")
    evidence = record("evidence_qualification", object_id=obj, return_record_id=ret["record_id"], claim_id="claim:two-trails-observed", evidence_class="OBSERVATION", independence_status="UNKNOWN", contamination_status="CLEAN", disposition="QUALIFIED_AT_CURRENT_CEILING")
    delegation = record("delegation_envelope", object_id=obj, permitted_trigger_classes=["MATERIAL_CONTRADICTION"], permitted_carriers=[carrier["carrier_id"]], max_force="OBSERVATION", execution_limit=1, expires_at="2099-01-01T00:00:00Z", revoked=False, disposition="ACTIVE")
    closure = record("aggregate_closure", object_id=obj, stage_records=[plural["record_id"], mobius["record_id"], harmony["record_id"], trigger["record_id"], route["record_id"], carrier["record_id"], auth["record_id"], trace["record_id"], term["record_id"], ret["record_id"], evidence["record_id"], delegation["record_id"]], removal_results=["STAGE1:PASS", "STAGE2:PASS", "STAGE3:PASS", "STAGE4:PASS"], v41_regression=True, lossless_recollapse=True, disposition="CANDIDATE_CLOSED")
    return [plural, mobius, harmony, trigger, route, carrier, auth, trace, term, ret, evidence, delegation, closure]


def negative_fixtures(positive):
    by_type = {r["record_type"]: r for r in positive}
    cases = {}
    def changed(name, **updates):
        item = dict(by_type[name]); item.update(updates); item["record_id"] = digest({k:v for k,v in item.items() if k != "record_id"}); return item
    cases["authority_escalation"] = changed("trigger_evaluation", authority_state="SYSTEM")
    cases["harmony_scheduler"] = changed("harmony_interpretation", provocation_authority="SCHEDULER")
    cases["force_escalation"] = changed("pressure_route", selected_force="PLATOON")
    cases["carrier_self_admission"] = changed("carrier_admissibility", disposition="SELF_AUTHORIZED")
    cases["external_action"] = changed("execution_authorization", external_action="ENABLED")
    cases["overrun"] = changed("execution_trace", steps=["inspect", "recruit-helper", "expand-mission"])
    cases["contamination_launder"] = changed("termination_record", contamination_status="CONTAMINATED", object_evidence_admissibility="QUALIFICATION_REQUIRED")
    cases["false_return"] = changed("return_record", returned_object_id=ref("replacement-object"), object_continuity="PRESERVED")
    cases["result_promotion"] = changed("evidence_qualification", disposition="TRUTH")
    cases["standing_delegation"] = changed("delegation_envelope", execution_limit=999999)
    cases["lossy_closure"] = changed("aggregate_closure", lossless_recollapse=False)
    cases["bad_id"] = dict(by_type["trigger_evaluation"], record_id=ref("wrong"))
    return cases


def outputs():
    out = {}
    for name, fields in RECORDS.items():
        out[ROOT / "schemas" / f"{name}.schema.json"] = json.dumps(schema_for(name, fields), indent=2, ensure_ascii=False) + "\n"
    positive = positive_pipeline()
    out[ROOT / "fixtures" / "positive" / "aggregate_pipeline.json"] = json.dumps(positive, indent=2, ensure_ascii=False) + "\n"
    for name, value in negative_fixtures(positive).items():
        out[ROOT / "fixtures" / "negative" / f"{name}.json"] = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    return out


def manifest_for(generated):
    files = {}
    for path, content in generated.items():
        files[str(path.relative_to(REPO))] = "sha512:" + hashlib.sha512(content.encode()).hexdigest()
    source_paths = sorted(ROOT.glob("*.md"))
    source_paths.extend(sorted((ROOT / "contracts").glob("*.md")))
    source_paths.extend(sorted((ROOT / "tools").glob("*.py")))
    source_paths.extend(sorted((ROOT / "tests").glob("*.py")))
    for path in source_paths:
        files[str(path.relative_to(REPO))] = "sha512:" + hashlib.sha512(path.read_bytes()).hexdigest()
    body = {"schema_version": "1.0", "candidate": "v42", "baseline_commit": "ae898ab803061823b36fb825e0664e3d8d255409", "authority_state": "NONE", "human_gate_state": "ACTIVE", "canonical": False, "files": files}
    body["manifest_id"] = digest(body)
    return json.dumps(body, indent=2, ensure_ascii=False) + "\n"


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    generated = outputs(); generated[ROOT / "CANDIDATE_MANIFEST.json"] = manifest_for(generated)
    drift = []
    for path, content in generated.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content: drift.append(str(path.relative_to(REPO)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content, encoding="utf-8")
    if drift:
        print("generated artifact drift:"); print("\n".join(f"- {p}" for p in drift)); return 1
    print(f"candidate v42 generated artifacts {'verified' if args.check else 'written'}: {len(generated)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
