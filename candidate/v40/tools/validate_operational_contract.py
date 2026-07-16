#!/usr/bin/env python3
"""Validate the first v40 candidate operational contract and canonical binding."""

from __future__ import annotations

import hashlib
import json
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
