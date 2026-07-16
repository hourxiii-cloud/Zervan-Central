#!/usr/bin/env python3
"""Run an inert integrated validation of v40 reporting-boundary records."""

from __future__ import annotations

import copy
import sys
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from candidate.v40.runtime.reporting_records import (  # noqa: E402
    seal_analysis_record,
    seal_evidence_record,
    validate_reporting_records,
)


def attribution() -> dict:
    return {
        "origin_class": "SYSTEM_DERIVED",
        "origin_ref": "METHOD-RUNTIME-VALIDATION",
        "source_claim_ref": None,
        "transformation_refs": ["METHOD-RUNTIME-VALIDATION"],
        "attributed_at_utc": "2026-07-16T19:35:00+00:00",
        "notes": "Derived inside the inert reporting-record validator",
    }


def evidence_record() -> dict:
    return {
        "evidence_version": "v40-candidate.1",
        "evidence_id": "EV-RUNTIME-VALIDATION-001",
        "evidence_class": "DERIVED_MEASUREMENT",
        "source_ref": "SOURCE-RUNTIME-VALIDATION",
        "source_object_ref": "OBJECT-RUNTIME-VALIDATION",
        "source_sha512": "a" * 128,
        "source_sha512_state": "AVAILABLE",
        "source_sha512_reason": None,
        "object_ref": "IDENTITY-RUNTIME-VALIDATION",
        "value_ref": "SIGNATURE-RUNTIME-VALIDATION",
        "content_ref": None,
        "scope": "Inert local reporting-record validation",
        "observation_time_utc": "2026-07-16T19:34:00+00:00",
        "observation_time_unknown_reason": None,
        "source_time_utc": None,
        "source_time_unknown_reason": "The inert fixture has no external source time",
        "acquired_at_utc": "2026-07-16T19:34:30+00:00",
        "reliability_state": "NOT_ASSESSED",
        "limitations": ["Synthetic control fixture; not operational evidence"],
        "provenance_refs": ["PROV-RUNTIME-VALIDATION"],
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "evidence_sha512": "0" * 128,
    }


def claim(claim_id: str, risk_category: str, inheritance_refs: list[str]) -> dict:
    return {
        "claim_id": claim_id,
        "claim_text": f"Inert validation claim for {risk_category}.",
        "semantic": {
            "subject_ref": "IDENTITY-RUNTIME-VALIDATION",
            "predicate": "has_inert_validation_category",
            "object_ref": risk_category,
            "polarity": "AFFIRMED",
            "quantitative": {
                "applicable": False,
                "magnitude": None,
                "unit": None,
                "value_ref": None,
            },
            "population_ref": "POPULATION-RUNTIME-VALIDATION",
            "denominator_ref": None,
            "scope": "Inert local reporting-record validation",
            "temporal_boundary": {
                "start_utc": None,
                "end_utc": None,
                "as_of_utc": "2026-07-16T19:35:00+00:00",
                "description": "In-memory validator execution",
            },
            "classification_ref": None,
            "risk_category": risk_category,
            "ordering_ref": "ORDER-RUNTIME-VALIDATION",
            "inheritance_refs": inheritance_refs,
            "claim_ceiling": "ANALYTICAL_ONLY",
            "semantic_sha512": "0" * 128,
        },
        "support_state": "SUPPORTED",
        "evidence_refs": ["EV-RUNTIME-VALIDATION-001"],
        "uncertainty_refs": ["UNC-RUNTIME-VALIDATION"],
        "contradiction_refs": [],
        "limitation_refs": ["LIM-RUNTIME-VALIDATION"],
        "attribution": attribution(),
    }


def analysis_record() -> dict:
    return {
        "analysis_version": "v40-candidate.1",
        "analysis_id": "AN-RUNTIME-VALIDATION-001",
        "inquiry_ref": "INQUIRY-RUNTIME-VALIDATION",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "method_refs": ["METHOD-RUNTIME-VALIDATION"],
        "claim_objects": [
            claim("CL-RUNTIME-ANOMALY", "ANOMALY", []),
            claim("CL-RUNTIME-THREAT", "THREAT", ["RIE-RUNTIME-ANOMALY-THREAT"]),
        ],
        "finding_refs": ["FINDING-RUNTIME-VALIDATION"],
        "count_refs": [],
        "identity_refs": ["IDENTITY-RUNTIME-VALIDATION"],
        "evidence_refs": ["EV-RUNTIME-VALIDATION-001"],
        "uncertainty_objects": [
            {
                "uncertainty_id": "UNC-RUNTIME-VALIDATION",
                "uncertainty_class": "NO_MATERIAL_UNCERTAINTY_IDENTIFIED",
                "description": "No material uncertainty is asserted inside this structural fixture.",
                "affected_claim_refs": ["CL-RUNTIME-ANOMALY", "CL-RUNTIME-THREAT"],
                "evidence_refs": ["EV-RUNTIME-VALIDATION-001"],
                "quantification_ref": None,
                "state": "ACTIVE",
            }
        ],
        "contradiction_refs": [],
        "limitation_objects": [
            {
                "limitation_id": "LIM-RUNTIME-VALIDATION",
                "limitation_class": "SCOPE",
                "description": "The fixture validates controls and makes no operational claim.",
                "affected_claim_refs": ["CL-RUNTIME-ANOMALY", "CL-RUNTIME-THREAT"],
                "evidence_refs": ["EV-RUNTIME-VALIDATION-001"],
            }
        ],
        "eliminated_world_refs": [],
        "surviving_world_refs": ["WORLD-CONTROL-FIXTURE"],
        "risk_inheritance_edges": [
            {
                "edge_id": "RIE-RUNTIME-ANOMALY-THREAT",
                "from_claim_ref": "CL-RUNTIME-ANOMALY",
                "to_claim_ref": "CL-RUNTIME-THREAT",
                "inheritance_class": "RISK_ESCALATION",
                "evidence_refs": ["EV-RUNTIME-VALIDATION-001"],
                "rationale": "The inert threat claim carries the same declared evidence as the anomaly claim.",
            }
        ],
        "classification_refs": [],
        "framework_mapping_refs": [],
        "attribution": attribution(),
        "analysis_time_utc": "2026-07-16T19:35:00+00:00",
        "provenance_refs": ["PROV-RUNTIME-VALIDATION"],
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "claim_ceiling": "ANALYTICAL_ONLY",
        "status": "FROZEN",
        "analysis_sha512": "0" * 128,
    }


def main() -> int:
    try:
        evidence = seal_evidence_record(evidence_record())
        analysis = seal_analysis_record(analysis_record(), [evidence])
    except Exception as exc:  # noqa: BLE001 - validator must convert unknown failure to FAIL
        print(f"FAIL: unable to seal normative reporting records: {exc}", file=sys.stderr)
        return 1

    errors = validate_reporting_records([evidence], analysis)
    if errors:
        print(f"FAIL: normative reporting records failed: {'; '.join(errors)}", file=sys.stderr)
        return 1

    tampered = copy.deepcopy(evidence)
    tampered["object_ref"] = "TAMPERED-AFTER-SEAL"
    tamper_errors = validate_reporting_records([tampered], analysis)
    if not any("Evidence digest mismatch" in error for error in tamper_errors):
        print("FAIL: evidence tampering did not fail closed", file=sys.stderr)
        return 1

    print(
        "PASS: v40 reporting records verified "
        "(canonical digests; closed references; Anomaly -> Threat inheritance; tamper rejected; no output)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
