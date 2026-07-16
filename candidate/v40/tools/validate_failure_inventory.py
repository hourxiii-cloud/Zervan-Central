#!/usr/bin/env python3
"""Validate the inert v40 candidate failure inventory with the standard library."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INVENTORY = ROOT / "candidate/v40/governance/failure_inventory.json"
SCHEMA = ROOT / "candidate/v40/governance/failure_inventory.schema.json"
TAXONOMY = (
    "P0 identifies the single parent failure operation; Critical, High, and Medium "
    "identify individual finding severity. P0 does not encode individual finding priority."
)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_inventory(inventory: dict, schema: dict) -> list[str]:
    errors: list[str] = []
    required = set(schema.get("required", []))
    missing = sorted(required - set(inventory))
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")

    expected_constants = {
        "schema_version": "v40-candidate.1",
        "candidate_state": "CANDIDATE_ONLY",
        "authority_state": "NONE",
        "human_gate": "ACTIVE",
        "parent_finding_id": "P0-040",
        "identifier_taxonomy": TAXONOMY,
    }
    for key, expected in expected_constants.items():
        if inventory.get(key) != expected:
            errors.append(f"{key}: expected {expected!r}, got {inventory.get(key)!r}")

    operation = inventory.get("operation", {})
    if operation.get("id") != "P0":
        errors.append("operation.id must be P0")
    if operation.get("name") != "Zervan Production Route Failure":
        errors.append("operation.name mismatch")
    if operation.get("state") != "OPEN":
        errors.append("candidate operation must remain OPEN")

    findings = inventory.get("findings", [])
    if not isinstance(findings, list):
        return errors + ["findings must be an array"]

    expected_ids = [f"P0-{number:03d}" for number in range(1, 41)]
    actual_ids = [finding.get("id") for finding in findings if isinstance(finding, dict)]
    if actual_ids != expected_ids:
        errors.append("finding identifiers must be exactly P0-001 through P0-040 in order")

    allowed_severities = {"Critical", "High", "Medium"}
    allowed_states = {"OPEN", "CONTROL_IMPLEMENTED", "VERIFIED", "HUMAN_GATE_REVIEW", "CLOSED"}
    required_finding_fields = {
        "id", "severity", "title", "implementation_wave", "primary_control", "acceptance_evidence", "state"
    }
    for index, finding in enumerate(findings, 1):
        if not isinstance(finding, dict):
            errors.append(f"finding {index} is not an object")
            continue
        absent = sorted(required_finding_fields - set(finding))
        if absent:
            errors.append(f"{finding.get('id', index)} missing fields: {', '.join(absent)}")
        if finding.get("severity") not in allowed_severities:
            errors.append(f"{finding.get('id', index)} invalid severity")
        if finding.get("state") not in allowed_states:
            errors.append(f"{finding.get('id', index)} invalid state")
        waves = finding.get("implementation_wave")
        if not isinstance(waves, list) or not waves or any(not isinstance(wave, int) or wave < 0 or wave > 5 for wave in waves):
            errors.append(f"{finding.get('id', index)} invalid implementation wave")
        if len(str(finding.get("primary_control", ""))) < 10:
            errors.append(f"{finding.get('id', index)} primary control is not substantive")
        if len(str(finding.get("acceptance_evidence", ""))) < 10:
            errors.append(f"{finding.get('id', index)} acceptance evidence is not substantive")

    duplicates = [item for item, count in Counter(actual_ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate finding identifiers: {', '.join(duplicates)}")

    parent = next((finding for finding in findings if finding.get("id") == "P0-040"), None)
    if not parent or parent.get("title") != "Contract Enforcement Failure" or parent.get("severity") != "Critical":
        errors.append("P0-040 must remain the Critical parent Contract Enforcement Failure")

    return errors


def main() -> int:
    try:
        inventory = load_json(INVENTORY)
        schema = load_json(SCHEMA)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    errors = validate_inventory(inventory, schema)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    severities = Counter(finding["severity"] for finding in inventory["findings"])
    print(
        "PASS: v40 candidate failure inventory verified "
        f"(40 findings; Critical={severities['Critical']}, High={severities['High']}, Medium={severities['Medium']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
