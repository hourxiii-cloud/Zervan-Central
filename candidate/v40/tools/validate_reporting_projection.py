#!/usr/bin/env python3
"""Run an inert integrated validation of the v40 Report Projection boundary."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from candidate.v40.runtime.reporting_inventories import (  # noqa: E402
    seal_analytical_inventory_freeze,
    seal_requirement_inventory,
)
from candidate.v40.runtime.reporting_projection import (  # noqa: E402
    projection_digest,
    report_element_digest,
    seal_report_projection,
    validate_report_projection,
)
from candidate.v40.runtime.reporting_records import (  # noqa: E402
    seal_analysis_record,
    seal_evidence_record,
)
from candidate.v40.tools.validate_reporting_inventories import (  # noqa: E402
    analytical_freeze,
    git_bindings,
    requirement_inventory,
)
from candidate.v40.tools.validate_reporting_records import (  # noqa: E402
    analysis_record,
    evidence_record,
)


PROJECTION_SCHEMA_PATH = ROOT / "candidate/v40/contracts/report_projection.schema.json"


def forbidden_transformations() -> list[str]:
    schema = json.loads(PROJECTION_SCHEMA_PATH.read_text(encoding="utf-8"))
    return list(schema["$defs"]["forbidden_transformation_class"]["enum"])


def report_projection(requirement: dict, freeze: dict, analysis: dict) -> dict:
    claims = analysis["claim_objects"]
    claim_refs = [claim["claim_id"] for claim in claims]
    evidence_refs = sorted({ref for claim in claims for ref in claim["evidence_refs"]})
    uncertainty_refs = sorted(
        {ref for claim in claims for ref in claim["uncertainty_refs"]}
    )
    limitation_refs = sorted(
        {ref for claim in claims for ref in claim["limitation_refs"]}
    )
    required_requirements = [
        value["requirement_id"]
        for value in requirement["requirements"]
        if value["required"] and value["status"] != "EXPLICITLY_EXCLUDED"
    ]
    required_items = [
        item["inventory_item_id"]
        for item in freeze["ordered_inventory_items"]
        if item["required"] and item["inclusion_state"] == "INCLUDED"
    ]
    return {
        "projection_version": "v40-candidate.1",
        "projection_id": "RP-RUNTIME-VALIDATION-001",
        "request_ref": freeze["reporting_request_ref"],
        "contract_ref": freeze["contract_ref"],
        "route_ref": freeze["route_ref"],
        "freeze_ref": freeze["freeze_id"],
        "freeze_sha512": freeze["freeze_sha512"],
        "audience_profile": {
            "audience_profile_id": "AUD-RUNTIME-VALIDATION",
            "audience_class": "TECHNICAL",
            "description": "Inert technical validation audience.",
            "language_tag": "en-US",
            "assumed_context_refs": [],
            "required_context_refs": ["README-RUNTIME-VALIDATION"],
            "accessibility_requirements": ["TEXT_ALTERNATIVES"],
        },
        "reporting_lane": "insider_threat_reporting_lane",
        "allowed_transformations": [
            {
                "transformation_id": "TR-RUNTIME-ORGANIZE-001",
                "transformation_class": "ORGANIZE",
                "source_object_refs": [analysis["analysis_id"], *claim_refs],
                "output_element_refs": ["RE-RUNTIME-CLAIMS-001"],
                "parameters": [
                    {
                        "parameter_id": "TP-RUNTIME-ORDER-001",
                        "parameter_class": "ORDER",
                        "name": "section_order",
                        "value": None,
                        "value_ref": "ORDER-RUNTIME-VALIDATION",
                        "description": "Preserve the declared risk sequence.",
                    }
                ],
                "justification": "Organize frozen claims for the declared audience.",
            }
        ],
        "forbidden_transformations": forbidden_transformations(),
        "required_requirement_refs": required_requirements,
        "required_inventory_refs": required_items,
        "report_elements": [
            {
                "element_id": "RE-RUNTIME-CLAIMS-001",
                "element_class": "CLAIM_PROJECTION",
                "source_analysis_refs": [analysis["analysis_id"]],
                "source_claim_refs": claim_refs,
                "source_semantic_digests": [
                    {
                        "claim_ref": claim["claim_id"],
                        "semantic_sha512": claim["semantic"]["semantic_sha512"],
                    }
                    for claim in claims
                ],
                "evidence_refs": evidence_refs,
                "transformation_ref": "TR-RUNTIME-ORGANIZE-001",
                "rendered_artifact_path": "reports/runtime_claims.md",
                "anchor_ref": "runtime-claims",
                "uncertainty_refs": uncertainty_refs,
                "limitation_refs": limitation_refs,
                "requirement_refs": required_requirements,
                "inventory_refs": required_items,
                "content_status": "SUBSTANTIVE",
                "analytical_completion_credit": True,
                "presentation_only_reason": None,
                "visualization_binding": None,
                "element_sha512": "0" * 128,
                "human_review_status": "REVIEW_REQUIRED",
            }
        ],
        "omission_records": [],
        "presentation_only_elements": [],
        "human_readable_claim_map_ref": "reports/claim_map.md#runtime-claims",
        "claim_ceiling": analysis["claim_ceiling"],
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "projection_status": "LOCKED",
        "created_at_utc": "2026-07-16T20:45:00+00:00",
        "previous_projection_ref": None,
        "projection_sha512": "0" * 128,
    }


def validate(
    projection: dict,
    freeze: dict,
    requirement: dict,
    analysis: dict,
    evidence: dict,
    canonical_binding: dict,
    candidate_binding: dict,
) -> list[str]:
    return validate_report_projection(
        projection,
        freeze,
        requirement,
        [analysis],
        [evidence],
        expected_canonical_binding=canonical_binding,
        expected_candidate_binding=candidate_binding,
    )


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
        projection = seal_report_projection(
            report_projection(requirement, freeze, analysis),
            freeze,
            requirement,
            [analysis],
            [evidence],
            expected_canonical_binding=canonical_binding,
            expected_candidate_binding=candidate_binding,
        )
    except Exception as exc:  # noqa: BLE001 - validator converts unknown failure to FAIL
        print(f"FAIL: unable to seal normative Report Projection: {exc}", file=sys.stderr)
        return 1

    errors = validate(
        projection,
        freeze,
        requirement,
        analysis,
        evidence,
        canonical_binding,
        candidate_binding,
    )
    if errors:
        print(f"FAIL: normative Report Projection failed: {'; '.join(errors)}", file=sys.stderr)
        return 1

    mutated = copy.deepcopy(projection)
    mutated["report_elements"][0]["source_semantic_digests"][0][
        "semantic_sha512"
    ] = "f" * 128
    mutated["report_elements"][0]["element_sha512"] = report_element_digest(
        mutated["report_elements"][0]
    )
    mutated["projection_sha512"] = projection_digest(mutated)
    mutation_errors = validate(
        mutated,
        freeze,
        requirement,
        analysis,
        evidence,
        canonical_binding,
        candidate_binding,
    )
    if not any("semantic digest mismatch" in error for error in mutation_errors):
        print("FAIL: semantic mutation did not fail closed", file=sys.stderr)
        return 1

    omitted = copy.deepcopy(projection)
    omitted["report_elements"][0]["inventory_refs"].pop()
    omitted["report_elements"][0]["element_sha512"] = report_element_digest(
        omitted["report_elements"][0]
    )
    omitted["projection_sha512"] = projection_digest(omitted)
    omission_errors = validate(
        omitted,
        freeze,
        requirement,
        analysis,
        evidence,
        canonical_binding,
        candidate_binding,
    )
    if not any("lack analytical completion coverage" in error for error in omission_errors):
        print("FAIL: required inventory omission did not fail closed", file=sys.stderr)
        return 1

    print(
        "PASS: v40 Report Projection verified "
        "(frozen semantics; closed lineage; completion coverage; semantic mutation and "
        "inventory omission rejected; no output)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
