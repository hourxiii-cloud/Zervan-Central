#!/usr/bin/env python3
"""Verify the committed Spider R1/R2 admission bindings for the current release.

This verifies repository documents only. It does not initialize a component,
issue credentials, validate a deployed runtime, or authorize an operation.
"""

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
RELEASE = "vTemporal." + "42.5.4"
R1 = "canonical/Spider/SPIDER_R1_ADMISSION.json"
R2 = "canonical/Spider/SPIDER_R2_PERSONA_ADMISSION.json"
STANDING = "verification/" + "v" + "42.5.4/SPIDER_PERSONA_STANDING_CORRECTION.json"
REQUIRED_R2 = [
    "canonical/Spider/SPIDER_R2_PERSONA_CONTRACT.md",
    "canonical/Spider/SPIDER_R2_FULL_PERSONA_SPECIFICATION.md",
    "canonical/Spider/ONE_RUN_SPIDER_PERSONA_INITIALIZATION_R2.txt",
]


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def check_payloads(admission, errors, label):
    ordered = admission.get("load_order")
    payloads = admission.get("payloads")
    if not isinstance(ordered, list) or not isinstance(payloads, list):
        errors.append(f"{label}: load_order and payloads must be arrays")
        return
    paths = [item.get("path") for item in payloads if isinstance(item, dict)]
    if paths != ordered or not all(isinstance(path, str) for path in paths) or len(set(path for path in paths if isinstance(path, str))) != len(paths):
        errors.append(f"{label}: payloads differ from ordered, unique load paths")
    for item in payloads:
        if not isinstance(item, dict):
            errors.append(f"{label}: malformed payload record")
            continue
        relative = item.get("path")
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
            errors.append(f"{label}: unsafe payload path {relative!r}")
            continue
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"{label}: missing {relative}")
            continue
        data = path.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        if len(data) != item.get("size_bytes"):
            errors.append(f"{label}: byte count mismatch for {relative}")
        if actual_hash != item.get("sha256"):
            errors.append(f"{label}: SHA-256 mismatch for {relative}")


def check_equal(value, expected, label, errors):
    if value != expected:
        errors.append(f"{label}: expected {expected!r}, got {value!r}")


def validate():
    errors = []
    try:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        identity = read_json("VERSION.json")
        r1 = read_json(R1)
        r2 = read_json(R2)
        correction = read_json(STANDING)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"required document unavailable or invalid: {exc}"]

    check_equal(version, RELEASE, "VERSION", errors)
    check_equal(identity.get("version"), version, "VERSION.json version", errors)
    check_equal(identity.get("promotion_state"), "CANONICAL", "promotion state", errors)
    check_equal(identity.get("canonical_branch"), "main", "canonical branch", errors)
    check_equal(identity.get("spider_admission"), R2, "active Spider admission", errors)
    release_suffix = RELEASE.removeprefix("vTemporal.").replace(".", "_")
    check_equal(identity.get("initiation_call"), f"call/INITIATION_STATEMENT_V{release_suffix}.md", "initiation call", errors)
    check_equal(identity.get("canonical_entry"), f"canonical/ZERVAN_v{release_suffix}_CANONICAL_ENTRY.md", "canonical entry", errors)
    check_equal(r2.get("target_release"), RELEASE, "R2 release", errors)
    check_equal(r2.get("persona"), "SPIDER", "R2 persona", errors)
    check_equal(r2.get("seat"), "ANALYTICAL_PERSONA_ARTIFACT_CONTEXT_CLAIM_QUALIFICATION", "R2 seat", errors)
    check_equal(r2.get("standing"), "CANONICAL PERSONA SPECIFICATION", "R2 standing", errors)
    check_equal(r2.get("promotion"), "CANONICAL", "R2 promotion", errors)
    check_equal(r2.get("canonical"), True, "R2 canonical", errors)
    check_equal(r2.get("load_order"), REQUIRED_R2, "R2 load order", errors)
    check_equal(r2.get("parent_release"), r1.get("release"), "R2 parent release", errors)
    check_equal(r1.get("standing"), "CANONICAL SPECIFICATION", "R1 admitted standing", errors)
    check_equal(r1.get("source_preserved_byte_for_byte"), True, "R1 source preservation", errors)
    check_equal(r2.get("source_preserved_byte_for_byte"), True, "R2 source preservation", errors)
    r1_payloads = r1.get("payloads")
    r1_source_hash = r1_payloads[0].get("sha256") if isinstance(r1_payloads, list) and r1_payloads and isinstance(r1_payloads[0], dict) else None
    check_equal(r2.get("source_document_sha256"), r1_source_hash, "frozen R1 source hash", errors)
    for name, object_ in (("identity", identity), ("R1", r1), ("R2", r2), ("standing correction", correction)):
        check_equal(object_.get("authority"), "NONE", f"{name} authority", errors)
        check_equal(object_.get("human_gate"), "ACTIVE", f"{name} Human Gate", errors)
    for name, object_ in (("identity", identity), ("R1", r1), ("R2", r2)):
        check_equal(object_.get("no_compression_out"), "ACTIVE", f"{name} No Compression Out", errors)
    check_equal(r2.get("originating_data_mutation"), "DISALLOWED", "R2 source mutation", errors)
    check_equal(r2.get("component_credentials_issued"), False, "R2 credentials", errors)
    check_equal(r2.get("runtime_validation"), "NOT PERFORMED", "R2 runtime validation", errors)
    check_equal(correction.get("release"), RELEASE, "correction release", errors)
    check_equal(correction.get("independent_component_runtime_claimed"), False, "correction runtime claim", errors)
    check_equal(correction.get("historical_candidate_qualification_preserved"), True, "candidate provenance", errors)
    check_equal(correction.get("full_analytical_run_gate_unchanged"), True, "full run gate", errors)
    check_payloads(r1, errors, "R1")
    check_payloads(r2, errors, "R2")
    after = correction.get("changed_payload_sha256_after")
    if not isinstance(after, dict):
        errors.append("standing correction: missing final payload hash map")
    else:
        r2_payloads = r2.get("payloads")
        expected = {x.get("path"): x.get("sha256") for x in r2_payloads if isinstance(x, dict)} if isinstance(r2_payloads, list) else {}
        check_equal(after, expected, "standing correction final hashes", errors)
    for relative in (identity.get("initiation_call"), identity.get("canonical_entry"), identity.get("authority_contract")):
        if not isinstance(relative, str) or not (ROOT / relative).is_file():
            errors.append(f"missing release load path: {relative!r}")
    return errors


if __name__ == "__main__":
    failures = validate()
    if failures:
        print("SPIDER PERSONA ADMISSION: FAIL")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)
    print("SPIDER PERSONA ADMISSION: PASS (R1/R2 files, standing, and SHA-256 bindings)")
    print("Deployed runtime and independent component credentials: NOT VALIDATED")
