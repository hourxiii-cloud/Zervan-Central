#!/usr/bin/env python3
"""Validate active and immutable historical v40 Operational Contracts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ACTIVE_CONTRACT = ROOT / "candidate/v40/contracts/wave1_reporting_production.operational_contract.json"
HISTORICAL_CONTRACT = ROOT / "candidate/v40/contracts/wave0_tranche1.operational_contract.json"
CONTRACT = ACTIVE_CONTRACT
ACTIVE_CONTRACT_ID = "OC-V40.WAVE1.REPORTING-PRODUCTION"
ACTIVE_CANDIDATE_PARENT = "23040f1cbc94b2d6094ccd64f4ed5f0554ccf360"
ACTIVE_SPECIFICATION = ROOT / "candidate/v40/specifications/tranche4_reporting_production_boundary_specification.md"
ACTIVE_SPECIFICATION_RELATIVE = ACTIVE_SPECIFICATION.relative_to(ROOT).as_posix()
ACTIVE_SPECIFICATION_SHA512 = "5b74fb31e56a9ad56759038e6ba98ce464cc28f60c703cc7910d9ab394151f8e489466fcb9ff5ca8ad7b2d0b7768299378a1dbc4e1587e330344a64df63e6cc0"
HISTORICAL_CONTRACT_COMMIT = "b9460bf2955246ff3b1f61ed0b398496d7ad49c1"
HISTORICAL_CONTRACT_SHA512 = "5a2b62997a03a7c71d5a929916285409198a5f4754accf54fcea0fa1bd3f8efb12a283442a90daa0bbb9395af6a4cfe86554755cea59f9f64e0a7d8786d1edd1"
SCHEMAS = [
    ROOT / "candidate/v40/contracts/operational_contract.schema.json",
    ROOT / "candidate/v40/contracts/runtime_state.schema.json",
    ROOT / "candidate/v40/contracts/transition_event.schema.json",
]


def sha512(path: Path) -> str:
    digest = hashlib.sha512()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_blob(commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def git_commit_exists(commit: str) -> bool:
    return subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    ).returncode == 0


def git_is_ancestor(ancestor: str, descendant: str = "HEAD") -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        check=False,
        capture_output=True,
    ).returncode == 0


def canonical_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "origin/main"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def validate_contract(contract: dict, *, require_current_canonical: bool = True) -> list[str]:
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
    if require_current_canonical:
        try:
            current_head = canonical_head()
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append(f"unable to resolve origin/main: {exc}")
        else:
            if binding.get("commit") != current_head:
                errors.append(f"canonical commit mismatch: contract={binding.get('commit')}, origin/main={current_head}")

    binding_commit = str(binding.get("commit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", binding_commit) or not git_commit_exists(binding_commit):
        errors.append(f"canonical binding commit is unavailable: {binding_commit}")

    seen_paths: set[str] = set()
    for artifact in binding.get("artifacts", []):
        relative = artifact.get("path", "")
        if relative in seen_paths:
            errors.append(f"duplicate canonical artifact: {relative}")
            continue
        seen_paths.add(relative)
        try:
            actual = hashlib.sha256(git_blob(binding_commit, relative)).hexdigest()
        except (OSError, subprocess.CalledProcessError):
            errors.append(f"missing canonical artifact at {binding_commit}: {relative}")
            continue
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

    if contract.get("contract_id") == ACTIVE_CONTRACT_ID:
        invariants = set(contract.get("invariants", []))
        parent_invariant = f"candidate parent binding remains {ACTIVE_CANDIDATE_PARENT}"
        specification_invariant = (
            f"reporting-production specification remains {ACTIVE_SPECIFICATION_RELATIVE} "
            f"at SHA-512 {ACTIVE_SPECIFICATION_SHA512}"
        )
        if parent_invariant not in invariants:
            errors.append("active candidate parent binding invariant mismatch")
        if specification_invariant not in invariants:
            errors.append("active reporting-production specification invariant mismatch")
        if not git_commit_exists(ACTIVE_CANDIDATE_PARENT):
            errors.append("active candidate parent commit is unavailable")
        elif not git_is_ancestor(ACTIVE_CANDIDATE_PARENT):
            errors.append("active candidate parent is not an ancestor of HEAD")
        try:
            committed_specification_sha512 = hashlib.sha512(
                git_blob(ACTIVE_CANDIDATE_PARENT, ACTIVE_SPECIFICATION_RELATIVE)
            ).hexdigest()
        except (OSError, subprocess.CalledProcessError):
            errors.append("active reporting-production specification is unavailable at candidate parent")
        else:
            if committed_specification_sha512 != ACTIVE_SPECIFICATION_SHA512:
                errors.append("active reporting-production specification Git digest mismatch")
        try:
            working_specification_sha512 = sha512(ACTIVE_SPECIFICATION)
        except OSError:
            errors.append("active reporting-production specification is unavailable in the working tree")
        else:
            if working_specification_sha512 != ACTIVE_SPECIFICATION_SHA512:
                errors.append("active reporting-production specification working-tree digest mismatch")

    return errors


def validate_historical_contract(contract: dict, *, path: Path = HISTORICAL_CONTRACT) -> list[str]:
    errors: list[str] = []
    try:
        actual_digest = sha512(path)
    except OSError as exc:
        return [f"historical Wave 0 contract is unavailable: {exc}"]
    if actual_digest != HISTORICAL_CONTRACT_SHA512:
        errors.append("historical Wave 0 contract digest mismatch")
    if contract.get("canonical_binding", {}).get("commit") != HISTORICAL_CONTRACT_COMMIT:
        errors.append("historical Wave 0 canonical binding changed")
    errors.extend(validate_contract(contract, require_current_canonical=False))
    return errors


def main() -> int:
    try:
        active_contract = json.loads(ACTIVE_CONTRACT.read_text(encoding="utf-8"))
        historical_contract = json.loads(HISTORICAL_CONTRACT.read_text(encoding="utf-8"))
        for schema in SCHEMAS:
            json.loads(schema.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    errors = validate_contract(active_contract)
    errors.extend(validate_historical_contract(historical_contract))
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(
        "PASS: v40 candidate Operational Contracts verified "
        f"(active={active_contract['contract_id']}@{active_contract['canonical_binding']['commit']}; "
        f"historical={historical_contract['contract_id']}@{historical_contract['canonical_binding']['commit']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
