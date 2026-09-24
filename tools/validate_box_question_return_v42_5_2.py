#!/usr/bin/env python3
"""Validate candidate Box returns without treating return as truth or promotion."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/question/box_question_return_v42_5_2.schema.json"
DISPOSITIONS = {
    "ANSWER", "BOUNDED_ALTERNATIVES", "CONTRADICTION", "UNRESOLVED",
    "INSUFFICIENT_EVIDENCE", "MALFORMED_CONDITION", "PARTIAL_RESOLUTION",
}
SCOPES = {"LOCAL", "GLOBAL", "MIXED", "OTHER"}


def validate(record):
    errors = []
    if not isinstance(record, dict):
        return ["record must be an object"]

    # Validate shape first; later comparisons must not turn malformed input into
    # a fabricated return. jsonschema is optional to keep this validator portable.
    try:
        import jsonschema
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        errors.extend(
            f"schema: {error.message} at {'.'.join(map(str, error.path))}"
            for error in jsonschema.Draft202012Validator(schema).iter_errors(record)
        )
    except ImportError:
        errors.extend(_basic_shape(record))

    q = record.get("original_question")
    scope = record.get("question_scope")
    root = record.get("root_box_id")
    obj = record.get("governed_object_id")
    collapse = record.get("collapse") or {}
    returned = record.get("return") or {}
    if not isinstance(collapse, dict) or not isinstance(returned, dict):
        return errors + ["collapse and return must be objects"]

    if not isinstance(q, str) or not q.strip():
        errors.append("ORIGINAL_Q_MISSING")
    if not isinstance(root, str) or not root.strip() or not isinstance(obj, str) or not obj.strip():
        errors.append("ROOT_OR_OBJECT_MISSING")
    if scope not in SCOPES:
        errors.append("QUESTION_SCOPE_INVALID")
    if record.get("authority_state") != "NONE" or record.get("human_gate_state") != "ACTIVE":
        errors.append("AUTHORITY_OR_HUMAN_GATE_DRIFT")
    if returned.get("question") != q:
        errors.append("ORIGINAL_Q_NOT_RETURNED")
    if returned.get("root_box_id") != root or returned.get("governed_object_id") != obj:
        errors.append("RETURN_IDENTITY_DRIFT")
    receipt = returned.get("identity_receipt") or {}
    if not isinstance(receipt, dict) or (
        receipt.get("question") != q or receipt.get("root_box_id") != root
        or receipt.get("governed_object_id") != obj
    ):
        errors.append("IDENTITY_RECEIPT_DRIFT")

    representations = record.get("representations") or []
    if not isinstance(representations, list):
        representations = []
        errors.append("REPRESENTATIONS_INVALID")
    ids = set()
    unactualized = set()
    for i, item in enumerate(representations):
        if not isinstance(item, dict):
            errors.append(f"REPRESENTATION_INVALID:{i}")
            continue
        rid = item.get("id")
        if not isinstance(rid, str) or not rid or rid in ids:
            errors.append(f"REPRESENTATION_ID_INVALID:{i}")
        ids.add(rid)
        if item.get("root_box_id") != root or item.get("governed_object_id") != obj:
            errors.append(f"REPRESENTATION_IDENTITY_DRIFT:{i}")
        if item.get("question") != q:
            errors.append(f"REPRESENTATION_QUESTION_DRIFT:{i}")
        refs = item.get("observation_refs")
        if not isinstance(refs, list):
            errors.append(f"OBSERVATION_REFS_INVALID:{i}")
            refs = []
        if item.get("possibility_state") == "OBSERVED":
            if not refs:
                errors.append(f"POSSIBILITY_PROMOTED_WITHOUT_OBSERVATION:{i}")
        elif refs:
            errors.append(f"UNACTUALIZED_WITH_OBSERVATION:{i}")
        if item.get("possibility_state") in ("AVAILABLE_UNACTUALIZED", "UNRESOLVED"):
            unactualized.add(rid)

    disposition = collapse.get("disposition")
    standing = collapse.get("standing_refs")
    unresolved = collapse.get("unresolved_scope")
    retained = collapse.get("retained_possibilities")
    if disposition not in DISPOSITIONS:
        errors.append("COLLAPSE_DISPOSITION_INVALID")
    if not isinstance(standing, list) or not isinstance(unresolved, list) or not isinstance(retained, list):
        errors.append("COLLAPSE_LINEAGE_MISSING")
        standing, unresolved, retained = [], [], []
    if disposition in ("ANSWER", "PARTIAL_RESOLUTION", "BOUNDED_ALTERNATIVES") and not standing:
        errors.append("ANSWER_WITHOUT_EARNED_STANDING")
    if scope == "GLOBAL" and returned.get("answer_scope") == "LOCAL" and not unresolved:
        errors.append("GLOBAL_Q_SHRUNK_TO_LOCAL_ANSWER")
    if unresolved and disposition == "ANSWER":
        errors.append("COMPLETE_ANSWER_WITH_UNRESOLVED_SCOPE")
    for rid in unactualized:
        if rid not in retained:
            errors.append(f"UNCOLLAPSED_POSSIBILITY_ERASED:{rid}")
    if returned.get("answer_scope") not in SCOPES | {"NONE"}:
        errors.append("ANSWER_SCOPE_INVALID")
    if disposition in ("UNRESOLVED", "INSUFFICIENT_EVIDENCE") and returned.get("answer_scope") not in ("NONE", "OTHER"):
        errors.append("UNRESOLVED_REPRESENTED_AS_ANSWER")

    traversals = returned.get("traversal_receipts") or []
    if not isinstance(traversals, list):
        traversals = []
        errors.append("TRAVERSAL_RECEIPTS_INVALID")
    for i, receipt in enumerate(traversals):
        if not isinstance(receipt, dict) or receipt.get("representation_id") not in ids:
            errors.append(f"TRAVERSAL_WITHOUT_REPRESENTATION:{i}")
        elif not isinstance(receipt.get("evidence_refs"), list) or not receipt["evidence_refs"]:
            errors.append(f"TRAVERSAL_WITHOUT_EVIDENCE:{i}")
    if returned.get("observed") is True and returned.get("opened") is not True:
        errors.append("OBSERVATION_BEFORE_OPENING")
    if returned.get("qualified") is True and (
        returned.get("opened") is not True or returned.get("observed") is not True
    ):
        errors.append("QUALIFICATION_ON_RETURN_ALONE")
    return errors


def _basic_shape(record):
    """Structural fallback when jsonschema is unavailable in Codespaces."""
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = []

    def walk(value, definition, path):
        if not isinstance(value, dict):
            errors.append(f"schema: {path} must be an object")
            return
        for key in definition.get("required", []):
            if key not in value:
                errors.append(f"schema: missing {path}.{key}")
        for key in value:
            if key not in definition.get("properties", {}):
                errors.append(f"schema: unexpected {path}.{key}")
        for key, child in definition.get("properties", {}).items():
            if key not in value:
                continue
            if child.get("type") == "object":
                walk(value[key], child, f"{path}.{key}")
            elif child.get("type") == "array":
                if not isinstance(value[key], list):
                    errors.append(f"schema: {path}.{key} must be an array")
                elif child.get("items", {}).get("type") == "object":
                    for i, item in enumerate(value[key]):
                        walk(item, child["items"], f"{path}.{key}[{i}]")
            elif child.get("type") == "string" and not isinstance(value[key], str):
                errors.append(f"schema: {path}.{key} must be a string")
            if "const" in child and value[key] != child["const"]:
                errors.append(f"schema: {path}.{key} must equal {child['const']}")
            if "enum" in child and value[key] not in child["enum"]:
                errors.append(f"schema: {path}.{key} has invalid value")

    walk(record, schema, "record")
    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_box_question_return_v42_5_2.py RECORD.json", file=sys.stderr)
        sys.exit(2)
    try:
        document = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        sys.exit(2)
    failures = validate(document)
    print(json.dumps({"disposition": "BLOCKED" if failures else "VALID", "failures": failures}, indent=2))
    sys.exit(1 if failures else 0)
