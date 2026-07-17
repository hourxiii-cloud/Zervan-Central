from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from candidate.v40.runtime.schema_validation import SchemaValidationError, validate_schema


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENT_SCHEMA_PATH = (
    ROOT / "candidate/v40/contracts/reporting_requirement_inventory.schema.json"
)
FREEZE_SCHEMA_PATH = ROOT / "candidate/v40/contracts/analytical_inventory_freeze.schema.json"


def requirement_schema() -> dict:
    return json.loads(REQUIREMENT_SCHEMA_PATH.read_text(encoding="utf-8"))


def freeze_schema() -> dict:
    return json.loads(FREEZE_SCHEMA_PATH.read_text(encoding="utf-8"))


def valid_requirement() -> dict:
    return {
        "requirement_id": "REQ-REPORT-ORDER-001",
        "requirement_class": "ORDERING",
        "source_class": "USER_EXPLICIT",
        "source_ref": "USER-REQUEST-REPORT-001",
        "required": True,
        "description": (
            "The report must escalate from anomaly through insider threat and end "
            "with offending identities."
        ),
        "completion_test": {
            "test_class": "ORDER_PRESERVED",
            "description": "The rendered report preserves the required risk sequence.",
            "expected_refs": ["ORDER-ANOMALY-TO-OFFENDING-ID"],
        },
        "ordering_constraint": {
            "constraint_class": "SEQUENCE",
            "target_refs": [
                "ANOMALY",
                "THREAT",
                "HIDDEN_THREAT",
                "INSIDER_THREAT",
                "OFFENDING_IDENTITIES",
            ],
            "sequence_index": 1,
            "description": "Offending identities are the terminal report section.",
        },
        "artifact_role": "CORE_REPORT",
        "claim_or_inventory_refs": ["CL-ANOMALY-001", "CL-THREAT-001"],
        "status": "ACTIVE",
        "exclusion_reason": None,
        "exclusion_ref": None,
    }


def valid_requirement_inventory() -> dict:
    return {
        "requirement_inventory_version": "v40-candidate.1",
        "requirement_inventory_id": "RRI-REPORTING-001",
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "reporting_request_ref": "USER-REQUEST-REPORT-001",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "inventory_state": "CLOSED",
        "requirements": [valid_requirement()],
        "created_at_utc": "2026-07-16T18:30:00+00:00",
        "previous_requirement_inventory_ref": None,
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "requirement_inventory_sha512": "a" * 128,
    }


def valid_inventory_item() -> dict:
    return {
        "inventory_item_id": "AII-FINDING-001",
        "item_class": "FINDING",
        "item_ref": "FINDING-ANOMALY-001",
        "source_ref": "AN-REPORTING-001",
        "source_sha512": "b" * 128,
        "availability_state": "AVAILABLE",
        "availability_reason": None,
        "description": "Identity 001 exhibits execution signature B0.",
        "required": True,
        "ordering_index": 1,
        "dependency_refs": ["EV-REPORTING-001"],
        "requirement_refs": ["REQ-REPORT-ORDER-001"],
        "ambiguity_refs": [],
        "inclusion_state": "INCLUDED",
        "exclusion_ref": None,
    }


def valid_freeze() -> dict:
    return {
        "freeze_version": "v40-candidate.1",
        "freeze_id": "AIF-REPORTING-001",
        "freeze_state": "FROZEN",
        "canonical_git_binding": {
            "repository": "https://github.com/hourxiii-cloud/Zervan-Core-v39",
            "branch": "main",
            "commit": "d07023f028833f3ed1b61eebbd3298ed61c28d72",
        },
        "candidate_git_binding": {
            "repository": "https://github.com/hourxiii-cloud/Zervan-Core-v39",
            "branch": "candidate/v40-wave0",
            "commit": "65f56d30caee4fccacdbbe76763f7623592e84e1",
        },
        "contract_ref": "OC-V40.WAVE1.REPORTING-PRODUCTION",
        "reporting_request_ref": "USER-REQUEST-REPORT-001",
        "route_ref": "v40_candidate_wave1_reporting_production",
        "ordered_inventory_items": [valid_inventory_item()],
        "source_analysis_records": [
            {
                "analysis_id": "AN-REPORTING-001",
                "analysis_sha512": "b" * 128,
                "claim_refs": ["CL-ANOMALY-001"],
                "status": "FROZEN",
            }
        ],
        "requirement_inventory_ref": "RRI-REPORTING-001",
        "requirement_inventory_sha512": "a" * 128,
        "known_exclusions": [],
        "unresolved_ambiguities": [],
        "created_at_utc": "2026-07-16T18:31:00+00:00",
        "authority_state": "NONE",
        "human_gate_state": "ACTIVE",
        "previous_freeze_ref": None,
        "freeze_sha512": "c" * 128,
    }


class InventorySchemaTestCase(unittest.TestCase):
    def assert_valid(self, value: dict, schema: dict) -> None:
        validate_schema(value, schema)

    def assert_invalid(self, value: dict, schema: dict) -> None:
        with self.assertRaises(SchemaValidationError):
            validate_schema(value, schema)


class ReportingRequirementInventoryFixtures(InventorySchemaTestCase):
    def test_valid_closed_requirement_inventory(self):
        value = valid_requirement_inventory()
        self.assert_valid(value, requirement_schema())
        self.assertEqual(value["inventory_state"], "CLOSED")
        self.assertEqual(value["authority_state"], "NONE")
        self.assertEqual(value["human_gate_state"], "ACTIVE")

    def test_all_declared_source_classes_are_accepted(self):
        source_classes = (
            "USER_EXPLICIT",
            "OPERATIONAL_CONTRACT",
            "ROUTE_REQUIRED",
            "ANALYTICAL_ESTABLISHED",
            "GOVERNANCE_REQUIRED",
            "HUMAN_GATE_DECISION",
        )
        for source_class in source_classes:
            with self.subTest(source_class=source_class):
                value = valid_requirement_inventory()
                value["requirements"][0]["source_class"] = source_class
                self.assert_valid(value, requirement_schema())

    def test_commentary_cannot_be_requirement_source(self):
        value = valid_requirement_inventory()
        value["requirements"][0]["source_class"] = "COMMENTARY"
        self.assert_invalid(value, requirement_schema())

    def test_planning_cannot_be_requirement_source(self):
        value = valid_requirement_inventory()
        value["requirements"][0]["source_class"] = "PLANNING"
        self.assert_invalid(value, requirement_schema())

    def test_requirement_inventory_cannot_be_empty(self):
        value = valid_requirement_inventory()
        value["requirements"] = []
        self.assert_invalid(value, requirement_schema())

    def test_ordering_requirement_cannot_omit_its_constraint(self):
        value = valid_requirement_inventory()
        value["requirements"][0]["ordering_constraint"] = None
        self.assert_invalid(value, requirement_schema())

    def test_completion_test_requires_expected_reference(self):
        value = valid_requirement_inventory()
        value["requirements"][0]["completion_test"]["expected_refs"] = []
        self.assert_invalid(value, requirement_schema())

    def test_explicit_exclusion_requires_nonrequired_state_and_evidence(self):
        value = valid_requirement_inventory()
        requirement = value["requirements"][0]
        requirement.update(
            required=False,
            status="EXPLICITLY_EXCLUDED",
            exclusion_reason="The Human Gate explicitly excluded this optional appendix.",
            exclusion_ref="HG-DECISION-EXCLUSION-001",
        )
        self.assert_valid(value, requirement_schema())

        requirement["required"] = True
        self.assert_invalid(value, requirement_schema())

    def test_active_requirement_cannot_carry_exclusion_fields(self):
        value = valid_requirement_inventory()
        value["requirements"][0]["exclusion_reason"] = "Assistant-selected omission"
        value["requirements"][0]["exclusion_ref"] = "ASSISTANT-PREFERENCE-001"
        self.assert_invalid(value, requirement_schema())

    def test_authority_promotion_and_human_gate_bypass_are_rejected(self):
        value = valid_requirement_inventory()
        value["authority_state"] = "ASSISTANT"
        self.assert_invalid(value, requirement_schema())

        value = valid_requirement_inventory()
        value["human_gate_state"] = "BYPASSED"
        self.assert_invalid(value, requirement_schema())

    def test_unknown_nested_requirement_field_is_rejected(self):
        value = valid_requirement_inventory()
        value["requirements"][0]["assistant_completion"] = True
        self.assert_invalid(value, requirement_schema())

    def test_invalid_ordering_index_and_digest_are_rejected(self):
        value = valid_requirement_inventory()
        value["requirements"][0]["ordering_constraint"]["sequence_index"] = 0
        self.assert_invalid(value, requirement_schema())

        value = valid_requirement_inventory()
        value["requirement_inventory_sha512"] = "not-a-digest"
        self.assert_invalid(value, requirement_schema())


class AnalyticalInventoryFreezeFixtures(InventorySchemaTestCase):
    def test_valid_freeze_binds_analysis_requirements_and_git(self):
        value = valid_freeze()
        self.assert_valid(value, freeze_schema())
        self.assertEqual(value["freeze_state"], "FROZEN")
        self.assertEqual(value["requirement_inventory_ref"], "RRI-REPORTING-001")

    def test_all_required_inventory_classes_are_accepted(self):
        item_classes = (
            "FINDING",
            "COUNT",
            "DENOMINATOR",
            "IDENTITY",
            "RANKED_ENTITY",
            "METHOD",
            "LIMITATION",
            "EVIDENCE",
            "UNCERTAINTY",
            "CONTRADICTION",
            "CLASSIFICATION",
            "FRAMEWORK_MAPPING",
            "RISK_INHERITANCE",
            "ORDERING_REQUIREMENT",
            "REQUESTED_ARTIFACT",
            "APPENDIX_OR_EVIDENCE_FILE",
            "COMPLETION_CRITERION",
            "KNOWN_UNAVAILABLE",
            "OTHER_DECLARED",
        )
        for item_class in item_classes:
            with self.subTest(item_class=item_class):
                value = valid_freeze()
                value["ordered_inventory_items"][0]["item_class"] = item_class
                self.assert_valid(value, freeze_schema())

    def test_freeze_requires_source_analysis_id_hash_and_claims(self):
        for field in ("analysis_id", "analysis_sha512", "claim_refs"):
            with self.subTest(field=field):
                value = valid_freeze()
                del value["source_analysis_records"][0][field]
                self.assert_invalid(value, freeze_schema())

        value = valid_freeze()
        value["source_analysis_records"] = []
        self.assert_invalid(value, freeze_schema())

    def test_available_item_requires_hash_and_no_unavailable_reason(self):
        value = valid_freeze()
        value["ordered_inventory_items"][0]["source_sha512"] = None
        self.assert_invalid(value, freeze_schema())

        value = valid_freeze()
        value["ordered_inventory_items"][0]["availability_reason"] = "Maybe unavailable"
        self.assert_invalid(value, freeze_schema())

    def test_known_unavailable_item_requires_null_hash_and_reason(self):
        value = valid_freeze()
        item = value["ordered_inventory_items"][0]
        item.update(
            item_class="KNOWN_UNAVAILABLE",
            item_ref="UNAVAILABLE-EVENT-TIME-001",
            source_sha512=None,
            availability_state="UNAVAILABLE",
            availability_reason="The supplied dataset contains no source event time.",
        )
        self.assert_valid(value, freeze_schema())

        item["availability_reason"] = None
        self.assert_invalid(value, freeze_schema())

    def test_excluded_item_requires_traceable_exclusion(self):
        value = valid_freeze()
        item = value["ordered_inventory_items"][0]
        item.update(inclusion_state="EXCLUDED", exclusion_ref="EX-OPTIONAL-001")
        value["known_exclusions"] = [
            {
                "exclusion_id": "EX-OPTIONAL-001",
                "inventory_item_refs": ["AII-FINDING-001"],
                "reason": "The Human Gate excluded this optional output.",
                "decision_source_class": "HUMAN_GATE_DECISION",
                "decision_ref": "HG-DECISION-EXCLUSION-001",
            }
        ]
        self.assert_valid(value, freeze_schema())

        item["exclusion_ref"] = None
        self.assert_invalid(value, freeze_schema())

    def test_included_item_cannot_carry_exclusion_reference(self):
        value = valid_freeze()
        value["ordered_inventory_items"][0]["exclusion_ref"] = "EX-ASSISTANT-001"
        self.assert_invalid(value, freeze_schema())

    def test_open_ambiguity_is_explicit_and_requires_clarification(self):
        value = valid_freeze()
        value["ordered_inventory_items"][0]["ambiguity_refs"] = ["AMB-SCOPE-001"]
        value["unresolved_ambiguities"] = [
            {
                "ambiguity_id": "AMB-SCOPE-001",
                "inventory_item_refs": ["AII-FINDING-001"],
                "description": "The requested audience is not yet identified.",
                "clarification_required": True,
                "status": "OPEN",
            }
        ]
        self.assert_valid(value, freeze_schema())

        value["unresolved_ambiguities"][0]["clarification_required"] = False
        self.assert_invalid(value, freeze_schema())

    def test_git_bindings_require_full_commit_hashes(self):
        value = valid_freeze()
        value["candidate_git_binding"]["commit"] = "65f56d3"
        self.assert_invalid(value, freeze_schema())

    def test_freeze_ordering_begins_at_one(self):
        value = valid_freeze()
        value["ordered_inventory_items"][0]["ordering_index"] = 0
        self.assert_invalid(value, freeze_schema())

    def test_authority_human_gate_and_closed_shape_are_immutable(self):
        value = valid_freeze()
        value["authority_state"] = "SYSTEM"
        self.assert_invalid(value, freeze_schema())

        value = valid_freeze()
        value["human_gate_state"] = "INACTIVE"
        self.assert_invalid(value, freeze_schema())

        value = valid_freeze()
        value["ordered_inventory_items"][0]["reporting_guess"] = "added claim"
        self.assert_invalid(value, freeze_schema())

    def test_invalid_freeze_and_requirement_digests_are_rejected(self):
        value = valid_freeze()
        value["freeze_sha512"] = "invalid"
        self.assert_invalid(value, freeze_schema())

        value = valid_freeze()
        value["requirement_inventory_sha512"] = "invalid"
        self.assert_invalid(value, freeze_schema())

    def test_previous_freeze_reference_is_typed(self):
        value = valid_freeze()
        value["previous_freeze_ref"] = "AIF-REPORTING-000"
        self.assert_valid(value, freeze_schema())

        value["previous_freeze_ref"] = "AN-REPORTING-000"
        self.assert_invalid(value, freeze_schema())


if __name__ == "__main__":
    unittest.main()
