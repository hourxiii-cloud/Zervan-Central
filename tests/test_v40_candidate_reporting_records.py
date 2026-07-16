from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from test_v40_candidate_continuity import SchemaValidationError, validate_schema


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SCHEMA_PATH = ROOT / "candidate/v40/contracts/evidence_record.schema.json"
ANALYSIS_SCHEMA_PATH = ROOT / "candidate/v40/contracts/analysis_record.schema.json"


def evidence_schema() -> dict:
    return json.loads(EVIDENCE_SCHEMA_PATH.read_text(encoding="utf-8"))


def analysis_schema() -> dict:
    return json.loads(ANALYSIS_SCHEMA_PATH.read_text(encoding="utf-8"))


def valid_evidence() -> dict:
    return {
        "evidence_version": "v40-candidate.1",
        "evidence_id": "EV-REPORTING-001",
        "evidence_class": "DATASET_OBJECT",
        "source_ref": "SOURCE-DATASET-001",
        "source_object_ref": "ROW-0001",
        "source_sha512": "a" * 128,
        "source_sha512_state": "AVAILABLE",
        "source_sha512_reason": None,
        "object_ref": "OBJECT-IDENTITY-001",
        "value_ref": "VALUE-SIGNATURE-B0",
        "content_ref": None,
        "scope": "Authorized insider-threat dataset review",
        "observation_time_utc": "2026-07-16T18:00:00+00:00",
        "observation_time_unknown_reason": None,
        "source_time_utc": None,
        "source_time_unknown_reason": "The supplied dataset does not contain source event time",
        "acquired_at_utc": "2026-07-16T18:05:00+00:00",
        "reliability_state": "SOURCE_REPORTED",
        "limitations": ["Source event time is unavailable"],
        "provenance_refs": ["PROV-DATASET-001"],
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "evidence_sha512": "b" * 128,
    }


def attribution(origin_class: str = "SYSTEM_DERIVED", origin_ref: str | None = "METHOD-SIGNATURE-001") -> dict:
    return {
        "origin_class": origin_class,
        "origin_ref": origin_ref,
        "source_claim_ref": None,
        "transformation_refs": ["METHOD-SIGNATURE-001"],
        "attributed_at_utc": "2026-07-16T18:10:00+00:00",
        "notes": "Derived by the declared analytical method",
    }


def valid_claim() -> dict:
    return {
        "claim_id": "CL-ANOMALY-001",
        "claim_text": "Identity 001 exhibits execution signature B0.",
        "semantic": {
            "subject_ref": "IDENTITY-001",
            "predicate": "exhibits_execution_signature",
            "object_ref": "SIGNATURE-B0",
            "polarity": "AFFIRMED",
            "quantitative": {
                "applicable": False,
                "magnitude": None,
                "unit": None,
                "value_ref": None,
            },
            "population_ref": "POPULATION-AUTHORIZED-DATASET",
            "denominator_ref": None,
            "scope": "Authorized insider-threat dataset review",
            "temporal_boundary": {
                "start_utc": None,
                "end_utc": None,
                "as_of_utc": "2026-07-16T18:00:00+00:00",
                "description": "Dataset state as supplied for analysis",
            },
            "classification_ref": None,
            "risk_category": "ANOMALY",
            "ordering_ref": "ORDER-ANOMALY-TO-OFFENDING-ID",
            "inheritance_refs": [],
            "claim_ceiling": "ANALYTICAL_ONLY",
            "semantic_sha512": "c" * 128,
        },
        "support_state": "SUPPORTED",
        "evidence_refs": ["EV-REPORTING-001"],
        "uncertainty_refs": ["UNC-ANOMALY-001"],
        "contradiction_refs": [],
        "limitation_refs": ["LIM-TIME-001"],
        "attribution": attribution(),
    }


def valid_analysis() -> dict:
    return {
        "analysis_version": "v40-candidate.1",
        "analysis_id": "AN-REPORTING-001",
        "inquiry_ref": "INQUIRY-INSIDER-THREAT-001",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "method_refs": ["METHOD-SIGNATURE-001"],
        "claim_objects": [valid_claim()],
        "finding_refs": ["FINDING-ANOMALY-001"],
        "count_refs": [],
        "identity_refs": ["IDENTITY-001"],
        "evidence_refs": ["EV-REPORTING-001"],
        "uncertainty_objects": [
            {
                "uncertainty_id": "UNC-ANOMALY-001",
                "uncertainty_class": "TEMPORAL_UNCERTAINTY",
                "description": "The source dataset does not include event time.",
                "affected_claim_refs": ["CL-ANOMALY-001"],
                "evidence_refs": ["EV-REPORTING-001"],
                "quantification_ref": None,
                "state": "ACTIVE",
            }
        ],
        "contradiction_refs": [],
        "limitation_objects": [
            {
                "limitation_id": "LIM-TIME-001",
                "limitation_class": "TEMPORAL",
                "description": "No event-time ordering can be claimed.",
                "affected_claim_refs": ["CL-ANOMALY-001"],
                "evidence_refs": ["EV-REPORTING-001"],
            }
        ],
        "eliminated_world_refs": [],
        "surviving_world_refs": ["WORLD-FUNCTIONAL-IDENTITY"],
        "risk_inheritance_edges": [],
        "classification_refs": [],
        "framework_mapping_refs": [],
        "attribution": attribution(),
        "analysis_time_utc": "2026-07-16T18:10:00+00:00",
        "provenance_refs": ["PROV-DATASET-001", "PROV-METHOD-001"],
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "claim_ceiling": "ANALYTICAL_ONLY",
        "status": "FROZEN",
        "analysis_sha512": "d" * 128,
    }


class RecordSchemaTestCase(unittest.TestCase):
    def assert_valid(self, value: dict, schema: dict) -> None:
        validate_schema(value, schema)

    def assert_invalid(self, value: dict, schema: dict) -> None:
        with self.assertRaises(SchemaValidationError):
            validate_schema(value, schema)


class EvidenceRecordSchemaFixtures(RecordSchemaTestCase):
    def test_fixture_04_valid_evidence_preserves_authority_none(self):
        value = valid_evidence()
        self.assert_valid(value, evidence_schema())
        self.assertEqual(value["authority_state"], "NONE")
        self.assertEqual(value["human_gate_state"], "ACTIVE")

    def test_fixture_05_unknown_provenance_remains_explicitly_unknown(self):
        value = valid_evidence()
        value.update(
            source_ref="SOURCE-UNKNOWN-001",
            source_object_ref=None,
            source_sha512=None,
            source_sha512_state="UNKNOWN",
            source_sha512_reason="The source hash was not supplied",
            reliability_state="UNKNOWN",
            provenance_refs=["PROV-UNKNOWN-001"],
        )
        self.assert_valid(value, evidence_schema())
        self.assertEqual(value["source_sha512_state"], "UNKNOWN")
        self.assertIsNone(value["source_sha512"])

    def test_available_source_hash_requires_sha512_and_no_unavailable_reason(self):
        value = valid_evidence()
        value["source_sha512"] = None
        self.assert_invalid(value, evidence_schema())
        value = valid_evidence()
        value["source_sha512_reason"] = "should not coexist with an available hash"
        self.assert_invalid(value, evidence_schema())

    def test_unavailable_source_hash_requires_null_and_reason(self):
        value = valid_evidence()
        value["source_sha512_state"] = "UNAVAILABLE"
        self.assert_invalid(value, evidence_schema())
        value["source_sha512"] = None
        value["source_sha512_reason"] = "The source container cannot be recovered"
        self.assert_valid(value, evidence_schema())

    def test_evidence_requires_value_or_content_reference(self):
        value = valid_evidence()
        value["value_ref"] = None
        value["content_ref"] = None
        self.assert_invalid(value, evidence_schema())

    def test_unknown_time_requires_null_and_reason(self):
        value = valid_evidence()
        value["source_time_unknown_reason"] = None
        self.assert_invalid(value, evidence_schema())
        value = valid_evidence()
        value["observation_time_utc"] = None
        value["observation_time_unknown_reason"] = "Observation time was not recorded"
        self.assert_valid(value, evidence_schema())

    def test_known_time_rejects_unknown_reason(self):
        value = valid_evidence()
        value["observation_time_unknown_reason"] = "incorrect uncertainty"
        self.assert_invalid(value, evidence_schema())

    def test_evidence_rejects_authority_promotion_and_unknown_fields(self):
        value = valid_evidence()
        value["authority_state"] = "FULL"
        self.assert_invalid(value, evidence_schema())
        value = valid_evidence()
        value["verdict"] = "PROVEN"
        self.assert_invalid(value, evidence_schema())

    def test_evidence_rejects_invalid_digest_and_empty_provenance(self):
        value = valid_evidence()
        value["evidence_sha512"] = "not-a-digest"
        self.assert_invalid(value, evidence_schema())
        value = valid_evidence()
        value["provenance_refs"] = []
        self.assert_invalid(value, evidence_schema())


class AnalysisRecordSchemaFixtures(RecordSchemaTestCase):
    def test_fixture_07_valid_analysis_carries_structured_claim_and_evidence(self):
        value = valid_analysis()
        self.assert_valid(value, analysis_schema())
        claim = value["claim_objects"][0]
        self.assertEqual(claim["support_state"], "SUPPORTED")
        self.assertEqual(claim["evidence_refs"], ["EV-REPORTING-001"])

    def test_fixture_08_claim_without_attribution_is_rejected(self):
        value = valid_analysis()
        del value["claim_objects"][0]["attribution"]
        self.assert_invalid(value, analysis_schema())

    def test_fixture_09_claim_without_uncertainty_state_is_rejected(self):
        value = valid_analysis()
        value["claim_objects"][0]["uncertainty_refs"] = []
        self.assert_invalid(value, analysis_schema())
        value = valid_analysis()
        del value["claim_objects"][0]["uncertainty_refs"]
        self.assert_invalid(value, analysis_schema())

    def test_supported_claim_requires_evidence(self):
        value = valid_analysis()
        value["claim_objects"][0]["evidence_refs"] = []
        self.assert_invalid(value, analysis_schema())

    def test_explicitly_unresolved_claim_may_record_missing_evidence(self):
        value = valid_analysis()
        claim = value["claim_objects"][0]
        claim["support_state"] = "UNRESOLVED"
        claim["evidence_refs"] = []
        value["evidence_refs"] = []
        uncertainty = value["uncertainty_objects"][0]
        uncertainty["uncertainty_class"] = "MISSING_EVIDENCE"
        uncertainty["evidence_refs"] = []
        self.assert_valid(value, analysis_schema())

    def test_contradicted_claim_requires_contradiction_reference(self):
        value = valid_analysis()
        claim = value["claim_objects"][0]
        claim["support_state"] = "CONTRADICTED"
        claim["contradiction_refs"] = []
        self.assert_invalid(value, analysis_schema())
        claim["contradiction_refs"] = ["CONTRADICTION-001"]
        self.assert_valid(value, analysis_schema())

    def test_claim_semantics_cannot_be_replaced_by_prose(self):
        value = valid_analysis()
        del value["claim_objects"][0]["semantic"]["scope"]
        self.assert_invalid(value, analysis_schema())

    def test_known_attribution_requires_actual_origin_reference(self):
        value = valid_analysis()
        value["claim_objects"][0]["attribution"]["origin_ref"] = None
        self.assert_invalid(value, analysis_schema())
        value["claim_objects"][0]["attribution"] = attribution("UNKNOWN", None)
        self.assert_valid(value, analysis_schema())

    def test_quantitative_claim_requires_value_and_unit(self):
        value = valid_analysis()
        quantitative = value["claim_objects"][0]["semantic"]["quantitative"]
        quantitative["applicable"] = True
        self.assert_invalid(value, analysis_schema())
        quantitative["magnitude"] = 7
        quantitative["unit"] = "identities"
        self.assert_valid(value, analysis_schema())

    def test_risk_inheritance_edge_requires_evidence_and_rationale(self):
        value = valid_analysis()
        value["risk_inheritance_edges"] = [
            {
                "edge_id": "RIE-ANOMALY-THREAT-001",
                "from_claim_ref": "CL-ANOMALY-001",
                "to_claim_ref": "CL-THREAT-001",
                "inheritance_class": "RISK_ESCALATION",
                "evidence_refs": [],
                "rationale": "The threat claim inherits the anomaly evidence.",
            }
        ]
        self.assert_invalid(value, analysis_schema())
        value["risk_inheritance_edges"][0]["evidence_refs"] = ["EV-REPORTING-001"]
        self.assert_valid(value, analysis_schema())

    def test_analysis_rejects_authority_promotion_and_nested_unknown_fields(self):
        value = valid_analysis()
        value["authority_state"] = "FULL"
        self.assert_invalid(value, analysis_schema())
        value = valid_analysis()
        value["claim_objects"][0]["semantic"]["confidence"] = 0.99
        self.assert_invalid(value, analysis_schema())

    def test_analysis_rejects_invalid_semantic_digest_and_empty_claim_set(self):
        value = valid_analysis()
        value["claim_objects"][0]["semantic"]["semantic_sha512"] = "invalid"
        self.assert_invalid(value, analysis_schema())
        value = valid_analysis()
        value["claim_objects"] = []
        self.assert_invalid(value, analysis_schema())


if __name__ == "__main__":
    unittest.main()
