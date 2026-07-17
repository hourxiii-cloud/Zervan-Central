from __future__ import annotations

import copy
import unittest

from candidate.v40.runtime.reporting_inventories import (
    ReportingInventoryError,
    analytical_inventory_freeze_digest,
    requirement_inventory_digest,
    seal_analytical_inventory_freeze,
    seal_requirement_inventory,
    validate_reporting_inventories,
    validate_requirement_inventory,
)
from candidate.v40.runtime.reporting_records import seal_analysis_record
from tests.test_v40_candidate_reporting_inventories import (
    valid_freeze,
    valid_requirement,
    valid_requirement_inventory,
)
from tests.test_v40_candidate_reporting_records import sealed_records


def inventory_item(
    item_id: str,
    item_class: str,
    item_ref: str,
    ordering_index: int,
    analysis: dict,
) -> dict:
    return {
        "inventory_item_id": item_id,
        "item_class": item_class,
        "item_ref": item_ref,
        "source_ref": analysis["analysis_id"],
        "source_sha512": analysis["analysis_sha512"],
        "availability_state": "AVAILABLE",
        "availability_reason": None,
        "description": f"Frozen {item_class.lower()} object {item_ref}.",
        "required": True,
        "ordering_index": ordering_index,
        "dependency_refs": [],
        "requirement_refs": ["REQ-REPORT-ORDER-001"],
        "ambiguity_refs": [],
        "inclusion_state": "INCLUDED",
        "exclusion_ref": None,
    }


def runtime_bundle() -> tuple[dict, dict, list[dict], list[dict], dict, dict]:
    evidence, analysis = sealed_records()
    requirement = valid_requirement_inventory()
    requirement["requirements"][0]["claim_or_inventory_refs"] = ["CL-ANOMALY-001"]
    requirement = seal_requirement_inventory(requirement)

    freeze = valid_freeze()
    freeze["source_analysis_records"] = [
        {
            "analysis_id": analysis["analysis_id"],
            "analysis_sha512": analysis["analysis_sha512"],
            "claim_refs": ["CL-ANOMALY-001"],
            "status": "FROZEN",
        }
    ]
    material = (
        ("METHOD", "METHOD-SIGNATURE-001"),
        ("FINDING", "FINDING-ANOMALY-001"),
        ("IDENTITY", "IDENTITY-001"),
        ("EVIDENCE", "EV-REPORTING-001"),
        ("UNCERTAINTY", "UNC-ANOMALY-001"),
        ("LIMITATION", "LIM-TIME-001"),
        ("ORDERING_REQUIREMENT", "ORDER-ANOMALY-TO-OFFENDING-ID"),
    )
    freeze["ordered_inventory_items"] = [
        inventory_item(f"AII-RUNTIME-{index:03d}", item_class, item_ref, index, analysis)
        for index, (item_class, item_ref) in enumerate(material, start=1)
    ]
    freeze["ordered_inventory_items"][1]["dependency_refs"] = ["EV-REPORTING-001"]
    freeze["requirement_inventory_ref"] = requirement["requirement_inventory_id"]
    freeze["requirement_inventory_sha512"] = requirement[
        "requirement_inventory_sha512"
    ]
    canonical_binding = copy.deepcopy(freeze["canonical_git_binding"])
    candidate_binding = copy.deepcopy(freeze["candidate_git_binding"])
    freeze = seal_analytical_inventory_freeze(
        freeze,
        requirement,
        [analysis],
        [evidence],
        expected_canonical_binding=canonical_binding,
        expected_candidate_binding=candidate_binding,
    )
    return (
        requirement,
        freeze,
        [analysis],
        [evidence],
        canonical_binding,
        candidate_binding,
    )


def reseal_requirement(record: dict) -> None:
    record["requirement_inventory_sha512"] = requirement_inventory_digest(record)


def reseal_freeze(record: dict) -> None:
    record["freeze_sha512"] = analytical_inventory_freeze_digest(record)


def bind_requirement(freeze: dict, requirement: dict) -> None:
    freeze["requirement_inventory_ref"] = requirement["requirement_inventory_id"]
    freeze["requirement_inventory_sha512"] = requirement[
        "requirement_inventory_sha512"
    ]
    reseal_freeze(freeze)


def inventory_errors(
    requirement: dict,
    freeze: dict,
    analyses: list[dict],
    evidence: list[dict],
    canonical_binding: dict,
    candidate_binding: dict,
) -> list[str]:
    return validate_reporting_inventories(
        freeze,
        requirement,
        analyses,
        evidence,
        expected_canonical_binding=canonical_binding,
        expected_candidate_binding=candidate_binding,
    )


class ReportingInventoryRuntimeFixtures(unittest.TestCase):
    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            msg=f"Expected error containing {fragment!r}; observed {errors!r}",
        )

    def test_fixture_01_sealed_inventory_boundary_validates_without_mutating_inputs(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        requirement_before = copy.deepcopy(requirement)
        freeze_before = copy.deepcopy(freeze)

        self.assertEqual(
            inventory_errors(
                requirement, freeze, analyses, evidence, canonical, candidate
            ),
            [],
        )
        self.assertEqual(requirement, requirement_before)
        self.assertEqual(freeze, freeze_before)

    def test_fixture_02_requirement_sealer_returns_copy_and_rejects_tamper(self):
        source = valid_requirement_inventory()
        source_before = copy.deepcopy(source)
        sealed = seal_requirement_inventory(source)
        self.assertEqual(source, source_before)
        self.assertNotEqual(
            sealed["requirement_inventory_sha512"],
            source["requirement_inventory_sha512"],
        )

        sealed["requirements"][0]["description"] = "Tampered after sealing"
        errors = validate_requirement_inventory(sealed)
        self.assert_error(errors, "Requirement inventory digest mismatch")

    def test_fixture_03_freeze_tamper_is_rejected(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        freeze["ordered_inventory_items"][0]["description"] = "Tampered after seal"
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Analytical inventory digest mismatch")

    def test_fixture_04_duplicate_requirement_identifier_is_rejected(self):
        requirement = valid_requirement_inventory()
        duplicate = copy.deepcopy(requirement["requirements"][0])
        duplicate["description"] = "Different body with the same identifier"
        requirement["requirements"].append(duplicate)
        with self.assertRaises(ReportingInventoryError) as context:
            seal_requirement_inventory(requirement)
        self.assert_error(list(context.exception.errors), "Duplicate requirement identifier")

    def test_fixture_05_requirement_sequence_must_be_unique_and_contiguous(self):
        requirement = valid_requirement_inventory()
        second = valid_requirement()
        second["requirement_id"] = "REQ-REPORT-ORDER-002"
        second["ordering_constraint"]["sequence_index"] = 3
        requirement["requirements"].append(second)
        with self.assertRaises(ReportingInventoryError) as context:
            seal_requirement_inventory(requirement)
        self.assert_error(list(context.exception.errors), "unique and contiguous")

    def test_fixture_06_nonsequence_constraint_cannot_carry_sequence_index(self):
        requirement = valid_requirement_inventory()
        constraint = requirement["requirements"][0]["ordering_constraint"]
        constraint["constraint_class"] = "BEFORE"
        with self.assertRaises(ReportingInventoryError) as context:
            seal_requirement_inventory(requirement)
        self.assert_error(list(context.exception.errors), "Non-sequence ordering")

    def test_fixture_07_requirement_inventory_cannot_self_chain(self):
        requirement = valid_requirement_inventory()
        requirement["previous_requirement_inventory_ref"] = requirement[
            "requirement_inventory_id"
        ]
        with self.assertRaises(ReportingInventoryError) as context:
            seal_requirement_inventory(requirement)
        self.assert_error(list(context.exception.errors), "cannot reference itself")

    def test_fixture_08_freeze_requirement_digest_binding_is_enforced(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        freeze["requirement_inventory_sha512"] = "f" * 128
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Freeze requirement inventory digest mismatch")

    def test_fixture_09_freeze_contract_route_and_request_must_match_requirements(self):
        for field, replacement in (
            ("contract_ref", "OC-V40.DIFFERENT"),
            ("route_ref", "different_route"),
            ("reporting_request_ref", "DIFFERENT-REQUEST"),
        ):
            with self.subTest(field=field):
                requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
                freeze[field] = replacement
                reseal_freeze(freeze)
                errors = inventory_errors(
                    requirement, freeze, analyses, evidence, canonical, candidate
                )
                self.assert_error(errors, f"Freeze {field} differs")

    def test_fixture_10_git_binding_drift_is_rejected(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        expected_candidate = copy.deepcopy(candidate)
        expected_candidate["commit"] = "f" * 40
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, expected_candidate
        )
        self.assert_error(errors, "candidate Git binding mismatch")

    def test_fixture_11_source_analysis_digest_status_and_claim_set_are_bound(self):
        cases = (
            ("analysis_sha512", "f" * 128, "source Analysis digest mismatch"),
            ("status", "SUPERSEDED", "source Analysis status mismatch"),
            ("claim_refs", ["CL-NOT-PRESENT"], "source Analysis claim set mismatch"),
        )
        for field, replacement, fragment in cases:
            with self.subTest(field=field):
                requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
                freeze["source_analysis_records"][0][field] = replacement
                reseal_freeze(freeze)
                errors = inventory_errors(
                    requirement, freeze, analyses, evidence, canonical, candidate
                )
                self.assert_error(errors, fragment)

    def test_fixture_12_mutated_source_analysis_is_rejected_even_when_freeze_is_unchanged(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        analyses[0]["finding_refs"] = ["FINDING-TAMPERED"]
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Analysis digest mismatch")

    def test_fixture_13_provided_analysis_set_must_equal_declared_set(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        extra = copy.deepcopy(analyses[0])
        extra["analysis_id"] = "AN-REPORTING-EXTRA"
        extra = seal_analysis_record(extra, evidence)
        errors = inventory_errors(
            requirement, freeze, analyses + [extra], evidence, canonical, candidate
        )
        self.assert_error(errors, "provided source analyses absent from freeze")
        self.assert_error(errors, "Duplicate cross-Analysis claim identifier")

    def test_fixture_14_inventory_order_must_match_contiguous_array_order(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        freeze["ordered_inventory_items"][1]["ordering_index"] = 8
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "contiguous array order")

    def test_fixture_15_duplicate_item_identifier_and_item_ref_are_rejected(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        duplicate = copy.deepcopy(freeze["ordered_inventory_items"][0])
        duplicate["description"] = "Different body with same identifier"
        duplicate["ordering_index"] = len(freeze["ordered_inventory_items"]) + 1
        freeze["ordered_inventory_items"].append(duplicate)
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Duplicate inventory item identifier")

        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        duplicate = copy.deepcopy(freeze["ordered_inventory_items"][0])
        duplicate["inventory_item_id"] = "AII-RUNTIME-DUPLICATE-REF"
        duplicate["ordering_index"] = len(freeze["ordered_inventory_items"]) + 1
        freeze["ordered_inventory_items"].append(duplicate)
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Duplicate inventory item_ref")

    def test_fixture_16_unresolved_requirement_and_dependency_refs_are_rejected(self):
        for field, fragment in (
            ("requirement_refs", "requirement_refs has unresolved"),
            ("dependency_refs", "dependency_refs has unresolved"),
        ):
            with self.subTest(field=field):
                requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
                freeze["ordered_inventory_items"][0][field] = ["MISSING-REF"]
                reseal_freeze(freeze)
                errors = inventory_errors(
                    requirement, freeze, analyses, evidence, canonical, candidate
                )
                self.assert_error(errors, fragment)

    def test_fixture_17_requirement_claim_reference_must_resolve(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        requirement["requirements"][0]["claim_or_inventory_refs"] = ["CL-MISSING"]
        reseal_requirement(requirement)
        bind_requirement(freeze, requirement)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "claim_or_inventory_refs has unresolved")

    def test_fixture_18_item_source_digest_and_source_object_are_bound(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        freeze["ordered_inventory_items"][0]["source_sha512"] = "f" * 128
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Inventory item source digest mismatch")

        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        freeze["ordered_inventory_items"][0]["item_ref"] = "METHOD-NOT-PRESENT"
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "absent from source Analysis")

    def test_fixture_19_material_analysis_object_cannot_be_omitted(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        freeze["ordered_inventory_items"].pop(0)
        for index, item in enumerate(freeze["ordered_inventory_items"], start=1):
            item["ordering_index"] = index
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Analytical inventory omits METHOD references")

    def test_fixture_20_every_requirement_must_be_represented(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        for item in freeze["ordered_inventory_items"]:
            item["requirement_refs"] = []
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Analytical inventory omits requirement references")

    def test_fixture_21_exclusion_must_be_reciprocal_and_decision_bound(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        req = requirement["requirements"][0]
        req.update(
            required=False,
            status="EXPLICITLY_EXCLUDED",
            exclusion_reason="The user explicitly excluded this material item.",
            exclusion_ref="HG-EXCLUSION-001",
        )
        requirement = seal_requirement_inventory(requirement)
        bind_requirement(freeze, requirement)
        item = freeze["ordered_inventory_items"][0]
        item.update(inclusion_state="EXCLUDED", exclusion_ref="EX-METHOD-001")
        freeze["known_exclusions"] = [
            {
                "exclusion_id": "EX-METHOD-001",
                "inventory_item_refs": [item["inventory_item_id"]],
                "reason": "Explicit user exclusion.",
                "decision_source_class": "USER_EXPLICIT",
                "decision_ref": "HG-EXCLUSION-001",
            }
        ]
        reseal_freeze(freeze)
        self.assertEqual(
            inventory_errors(
                requirement, freeze, analyses, evidence, canonical, candidate
            ),
            [],
        )

        freeze["known_exclusions"][0]["inventory_item_refs"] = [
            freeze["ordered_inventory_items"][1]["inventory_item_id"]
        ]
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "absent from reciprocal exclusion")

    def test_fixture_22_exclusion_decision_must_resolve_to_requirement_source(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        item = freeze["ordered_inventory_items"][0]
        item.update(inclusion_state="EXCLUDED", exclusion_ref="EX-METHOD-001")
        freeze["known_exclusions"] = [
            {
                "exclusion_id": "EX-METHOD-001",
                "inventory_item_refs": [item["inventory_item_id"]],
                "reason": "An active requirement cannot authorize exclusion.",
                "decision_source_class": "USER_EXPLICIT",
                "decision_ref": "USER-REQUEST-REPORT-001",
            }
        ]
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Exclusion decision is unresolved")

    def test_fixture_23_ambiguity_must_be_bidirectionally_bound(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        item = freeze["ordered_inventory_items"][0]
        item["ambiguity_refs"] = ["AMB-METHOD-001"]
        freeze["unresolved_ambiguities"] = [
            {
                "ambiguity_id": "AMB-METHOD-001",
                "inventory_item_refs": [item["inventory_item_id"]],
                "description": "The method scope requires Human Gate clarification.",
                "clarification_required": True,
                "status": "OPEN",
            }
        ]
        reseal_freeze(freeze)
        self.assertEqual(
            inventory_errors(
                requirement, freeze, analyses, evidence, canonical, candidate
            ),
            [],
        )

        item["ambiguity_refs"] = []
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "not carried reciprocally")

    def test_fixture_24_blocked_requirement_requires_known_unavailable_item(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        requirement["requirements"][0]["status"] = "BLOCKED_UNAVAILABLE"
        requirement = seal_requirement_inventory(requirement)
        bind_requirement(freeze, requirement)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Blocked requirement lacks KNOWN_UNAVAILABLE")

    def test_fixture_25_freeze_cannot_self_chain(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        freeze["previous_freeze_ref"] = freeze["freeze_id"]
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "cannot reference itself as previous")

    def test_fixture_26_requirement_sourced_artifact_binds_inventory_digest(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        req = requirement["requirements"][0]
        req.update(
            requirement_class="REPORT_ARTIFACT",
            completion_test={
                "test_class": "ARTIFACT_EXISTS",
                "description": "The requested report artifact exists.",
                "expected_refs": ["ARTIFACT-REPORT-001"],
            },
            ordering_constraint=None,
        )
        requirement = seal_requirement_inventory(requirement)
        bind_requirement(freeze, requirement)
        artifact = {
            "inventory_item_id": "AII-RUNTIME-ARTIFACT",
            "item_class": "REQUESTED_ARTIFACT",
            "item_ref": "ARTIFACT-REPORT-001",
            "source_ref": req["requirement_id"],
            "source_sha512": requirement["requirement_inventory_sha512"],
            "availability_state": "AVAILABLE",
            "availability_reason": None,
            "description": "Requested standalone report artifact.",
            "required": True,
            "ordering_index": len(freeze["ordered_inventory_items"]) + 1,
            "dependency_refs": [],
            "requirement_refs": [req["requirement_id"]],
            "ambiguity_refs": [],
            "inclusion_state": "INCLUDED",
            "exclusion_ref": None,
        }
        freeze["ordered_inventory_items"].append(artifact)
        reseal_freeze(freeze)
        self.assertEqual(
            inventory_errors(
                requirement, freeze, analyses, evidence, canonical, candidate
            ),
            [],
        )

        artifact["source_sha512"] = "f" * 128
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Inventory item requirement digest mismatch")

    def test_fixture_27_excluded_item_must_carry_decision_requirement(self):
        requirement, freeze, analyses, evidence, canonical, candidate = runtime_bundle()
        req = requirement["requirements"][0]
        req.update(
            required=False,
            status="EXPLICITLY_EXCLUDED",
            exclusion_reason="The user explicitly excluded this material item.",
            exclusion_ref="HG-EXCLUSION-001",
        )
        requirement = seal_requirement_inventory(requirement)
        bind_requirement(freeze, requirement)
        item = freeze["ordered_inventory_items"][0]
        item.update(
            requirement_refs=[],
            inclusion_state="EXCLUDED",
            exclusion_ref="EX-METHOD-001",
        )
        freeze["known_exclusions"] = [
            {
                "exclusion_id": "EX-METHOD-001",
                "inventory_item_refs": [item["inventory_item_id"]],
                "reason": "Explicit user exclusion.",
                "decision_source_class": "USER_EXPLICIT",
                "decision_ref": "HG-EXCLUSION-001",
            }
        ]
        reseal_freeze(freeze)
        errors = inventory_errors(
            requirement, freeze, analyses, evidence, canonical, candidate
        )
        self.assert_error(errors, "Excluded item lacks its exclusion requirement")


if __name__ == "__main__":
    unittest.main()
