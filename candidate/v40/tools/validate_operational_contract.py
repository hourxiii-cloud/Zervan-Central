#!/usr/bin/env python3
"""Validate the first v40 candidate operational contract and canonical binding."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "candidate/v40/contracts/wave0_tranche1.operational_contract.json"
SCHEMAS = [
    ROOT / "candidate/v40/contracts/operational_contract.schema.json",
    ROOT / "candidate/v40/contracts/runtime_state.schema.json",
    ROOT / "candidate/v40/contracts/transition_event.schema.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "origin/main"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def validate_contract(contract: dict) -> list[str]:
    errors: list[str] = []
    constants = {
        "contract_version": "v40-candidate.1",
        "candidate_state": "CANDIDATE_ONLY",
        "authority_state": "NONE",
        "human_gate": "ACTIVE",
    }
    for key, expected in constants.items():
        if contract.get(key) != expected:
            errors.append(f"{key}: expected {expected!r}, got {contract.get(key)!r}")
    if not re.fullmatch(r"OCI-[A-Z0-9._-]+", str(contract.get("contract_instance_id", ""))):
        errors.append("contract_instance_id is missing or malformed")

    posture = contract.get("posture", {})
    expected_posture = {
        "runtime_state": "DISCUSSION / TECH / NONE / NON-DOCTRINAL / STABLE",
        "mode": "CONTROLLED / READ-ONLY",
        "external_runtime": "DISABLED",
        "system_population": "DISALLOWED",
    }
    for key, expected in expected_posture.items():
        if posture.get(key) != expected:
            errors.append(f"posture.{key}: expected {expected!r}, got {posture.get(key)!r}")

    scope = contract.get("mutation_scope", {})
    if scope != {
        "canonical_mutation": "DISALLOWED",
        "candidate_local_edits": "ALLOWED",
        "external_mutation": "DISALLOWED",
    }:
        errors.append("mutation_scope does not preserve candidate-only local editing")

    binding = contract.get("canonical_binding", {})
    if binding.get("repository") != "https://github.com/hourxiii-cloud/Zervan-Core-v39.git":
        errors.append("canonical repository mismatch")
    if binding.get("branch") != "main":
        errors.append("canonical branch must be main")
    try:
        current_head = canonical_head()
    except (OSError, subprocess.CalledProcessError) as exc:
        errors.append(f"unable to resolve origin/main: {exc}")
    else:
        if binding.get("commit") != current_head:
            errors.append(f"canonical commit mismatch: contract={binding.get('commit')}, origin/main={current_head}")

    seen_paths: set[str] = set()
    for artifact in binding.get("artifacts", []):
        relative = artifact.get("path", "")
        if relative in seen_paths:
            errors.append(f"duplicate canonical artifact: {relative}")
            continue
        seen_paths.add(relative)
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing canonical artifact: {relative}")
            continue
        actual = sha256(path)
        if artifact.get("sha256") != actual:
            errors.append(f"canonical artifact hash mismatch: {relative}")

    for field in ("invariants", "completion_criteria", "stop_conditions", "escalation_triggers"):
        value = contract.get(field)
        if not isinstance(value, list) or not value or len(value) != len(set(value)):
            errors.append(f"{field} must be a non-empty unique list")

    route = contract.get("route", {})
    if not route.get("route_id") or not route.get("purpose"):
        errors.append("route identity and purpose are required")
    if not route.get("permitted_actions") or not route.get("prohibited_actions"):
        errors.append("route must define permitted and prohibited actions")
    action_sets = {
        "permitted_actions": set(route.get("permitted_actions", [])),
        "prohibited_actions": set(route.get("prohibited_actions", [])),
        "human_gate_required_actions": set(route.get("human_gate_required_actions", [])),
    }
    action_pattern = re.compile(r"^[a-z][a-z0-9_.-]*$")
    for name, actions in action_sets.items():
        if any(not action_pattern.fullmatch(str(action)) for action in actions):
            errors.append(f"{name} contains a non-normalized action identifier")
    names = list(action_sets)
    for index, left_name in enumerate(names):
        for right_name in names[index + 1:]:
            overlap = sorted(action_sets[left_name] & action_sets[right_name])
            if overlap:
                errors.append(f"action sets overlap between {left_name} and {right_name}: {', '.join(overlap)}")

    if contract.get("canonicalization") != "zervan://candidate/v40/canonical-json/1":
        errors.append("canonicalization identifier mismatch")
    if contract.get("transition_ledger_policy") != {
        "format": "one_canonical_json_object_per_event",
        "digest": "sha512",
        "atomic_write": True,
        "overwrite": False,
        "sequence_start": 1,
    }:
        errors.append("transition_ledger_policy mismatch")
    if contract.get("audit_policy") != {
        "fail_is_interrupt": True,
        "unknown_is_failure": True,
        "scar_on_stop": True,
    }:
        errors.append("audit_policy mismatch")

    return errors


def main() -> int:
    try:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        for schema in SCHEMAS:
            json.loads(schema.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    errors = validate_contract(contract)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(
        "PASS: v40 candidate operational contract verified "
        f"({contract['contract_id']}; canonical commit {contract['canonical_binding']['commit']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
