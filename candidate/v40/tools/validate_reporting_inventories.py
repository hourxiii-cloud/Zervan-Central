#!/usr/bin/env python3
"""Run an inert integrated validation of v40 reporting inventories."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from candidate.v40.runtime.reporting_inventories import (  # noqa: E402
    analytical_inventory_freeze_digest,
    seal_analytical_inventory_freeze,
    seal_requirement_inventory,
    validate_reporting_inventories,
)
from candidate.v40.runtime.reporting_records import (  # noqa: E402
    seal_analysis_record,
    seal_evidence_record,
)
from candidate.v40.tools.validate_reporting_records import (  # noqa: E402
    analysis_record,
    evidence_record,
)


CONTRACT_PATH = (
    ROOT / "candidate/v40/contracts/wave1_reporting_production.operational_contract.json"
)


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()


def git_bindings() -> tuple[dict, dict]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    canonical = {
        "repository": contract["canonical_binding"]["repository"],
        "branch": contract["canonical_binding"]["branch"],
        "commit": contract["canonical_binding"]["commit"],
    }
    candidate = {
        "repository": contract["canonical_binding"]["repository"],
        "branch": "candidate/v40-wave0",
        "commit": git_head(),
    }
    return canonical, candidate


def requirement_inventory() -> dict:
    return {
        "requirement_inventory_version": "v40-candidate.1",
        "requirement_inventory_id": "RRI-RUNTIME-VALIDATION-001",
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "reporting_request_ref": "REQUEST-RUNTIME-VALIDATION",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "inventory_state": "CLOSED",
        "requirements": [
            {
                "requirement_id": "REQ-RUNTIME-ORDER-001",
                "requirement_class": "ORDERING",
                "source_class": "ROUTE_REQUIRED",
                "source_ref": "ROUTE-v40_candidate_wave1_reporting_production",
                "required": True,
                "description": "Preserve the declared risk escalation order.",
                "completion_test": {
                    "test_class": "ORDER_PRESERVED",
                    "description": "The report carries the declared escalation order.",
                    "expected_refs": ["ORDER-RUNTIME-VALIDATION"],
                },
                "ordering_constraint": {
                    "constraint_class": "SEQUENCE",
                    "target_refs": ["ANOMALY", "THREAT"],
                    "sequence_index": 1,
                    "description": "Anomaly precedes Threat.",
                },
                "artifact_role": "CORE_REPORT",
                "claim_or_inventory_refs": [
                    "CL-RUNTIME-ANOMALY",
                    "CL-RUNTIME-THREAT",
                ],
                "status": "ACTIVE",
                "exclusion_reason": None,
                "exclusion_ref": None,
            }
        ],
        "created_at_utc": "2026-07-16T20:10:00+00:00",
        "previous_requirement_inventory_ref": None,
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "requirement_inventory_sha512": "0" * 128,
    }


def inventory_item(
    index: int,
    item_class: str,
    item_ref: str,
    analysis: dict,
) -> dict:
    return {
        "inventory_item_id": f"AII-RUNTIME-{index:03d}",
        "item_class": item_class,
        "item_ref": item_ref,
        "source_ref": analysis["analysis_id"],
        "source_sha512": analysis["analysis_sha512"],
        "availability_state": "AVAILABLE",
        "availability_reason": None,
        "description": f"Inert {item_class.lower()} validation object.",
        "required": True,
        "ordering_index": index,
        "dependency_refs": [],
        "requirement_refs": ["REQ-RUNTIME-ORDER-001"],
        "ambiguity_refs": [],
        "inclusion_state": "INCLUDED",
        "exclusion_ref": None,
    }


def analytical_freeze(
    requirement: dict,
    analysis: dict,
    canonical_binding: dict,
    candidate_binding: dict,
) -> dict:
    material = (
        ("METHOD", "METHOD-RUNTIME-VALIDATION"),
        ("FINDING", "FINDING-RUNTIME-VALIDATION"),
        ("IDENTITY", "IDENTITY-RUNTIME-VALIDATION"),
        ("EVIDENCE", "EV-RUNTIME-VALIDATION-001"),
        ("UNCERTAINTY", "UNC-RUNTIME-VALIDATION"),
        ("LIMITATION", "LIM-RUNTIME-VALIDATION"),
        ("RISK_INHERITANCE", "RIE-RUNTIME-ANOMALY-THREAT"),
        ("ORDERING_REQUIREMENT", "ORDER-RUNTIME-VALIDATION"),
    )
    return {
        "freeze_version": "v40-candidate.1",
        "freeze_id": "AIF-RUNTIME-VALIDATION-001",
        "freeze_state": "FROZEN",
        "canonical_git_binding": canonical_binding,
        "candidate_git_binding": candidate_binding,
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "reporting_request_ref": "REQUEST-RUNTIME-VALIDATION",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "ordered_inventory_items": [
            inventory_item(index, item_class, item_ref, analysis)
            for index, (item_class, item_ref) in enumerate(material, start=1)
        ],
        "source_analysis_records": [
            {
                "analysis_id": analysis["analysis_id"],
                "analysis_sha512": analysis["analysis_sha512"],
                "claim_refs": ["CL-RUNTIME-ANOMALY", "CL-RUNTIME-THREAT"],
                "status": "FROZEN",
            }
        ],
        "requirement_inventory_ref": requirement["requirement_inventory_id"],
        "requirement_inventory_sha512": requirement[
            "requirement_inventory_sha512"
        ],
        "known_exclusions": [],
        "unresolved_ambiguities": [],
        "created_at_utc": "2026-07-16T20:11:00+00:00",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "previous_freeze_ref": None,
        "freeze_sha512": "0" * 128,
    }


def main() -> int:
    try:
        canonical_binding, candidate_binding = git_bindings()
        evidence = seal_evidence_record(evidence_record())
        analysis = seal_analysis_record(analysis_record(), [evidence])
        requirement = seal_requirement_inventory(requirement_inventory())
        freeze = seal_analytical_inventory_freeze(
            analytical_freeze(
                requirement,
                analysis,
                canonical_binding,
                candidate_binding,
            ),
            requirement,
            [analysis],
            [evidence],
            expected_canonical_binding=canonical_binding,
            expected_candidate_binding=candidate_binding,
        )
    except Exception as exc:  # noqa: BLE001 - validator converts unknown failure to FAIL
        print(f"FAIL: unable to seal normative reporting inventories: {exc}", file=sys.stderr)
        return 1

    errors = validate_reporting_inventories(
        freeze,
        requirement,
        [analysis],
        [evidence],
        expected_canonical_binding=canonical_binding,
        expected_candidate_binding=candidate_binding,
    )
    if errors:
        print(f"FAIL: normative reporting inventories failed: {'; '.join(errors)}", file=sys.stderr)
        return 1

    tampered = copy.deepcopy(freeze)
    tampered["ordered_inventory_items"][0]["description"] = "TAMPERED-AFTER-SEAL"
    tamper_errors = validate_reporting_inventories(
        tampered,
        requirement,
        [analysis],
        [evidence],
        expected_canonical_binding=canonical_binding,
        expected_candidate_binding=candidate_binding,
    )
    if not any("Analytical inventory digest mismatch" in error for error in tamper_errors):
        print("FAIL: analytical inventory tampering did not fail closed", file=sys.stderr)
        return 1

    omitted = copy.deepcopy(freeze)
    omitted["ordered_inventory_items"] = [
        item
        for item in omitted["ordered_inventory_items"]
        if item["item_class"] != "RISK_INHERITANCE"
    ]
    for index, item in enumerate(omitted["ordered_inventory_items"], start=1):
        item["ordering_index"] = index
    omitted["freeze_sha512"] = analytical_inventory_freeze_digest(omitted)
    omission_errors = validate_reporting_inventories(
        omitted,
        requirement,
        [analysis],
        [evidence],
        expected_canonical_binding=canonical_binding,
        expected_candidate_binding=candidate_binding,
    )
    if not any("omits RISK_INHERITANCE" in error for error in omission_errors):
        print("FAIL: analytical inventory omission did not fail closed", file=sys.stderr)
        return 1

    print(
        "PASS: v40 reporting inventories verified "
        "(sealed requirements; frozen analysis; closed references; ordering integrity; "
        "tamper and omission rejected; no output)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
