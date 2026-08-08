import importlib.util
from copy import deepcopy
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = ROOT / "tools" / "validate_question_contract.py"

spec = importlib.util.spec_from_file_location(
    "validate_question_contract",
    VALIDATOR,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class QuestionContractTests(unittest.TestCase):

    def test_positive_valid(self):
        self.assertEqual(
            module.make_record()["validation_disposition"],
            "VALID",
        )

    def test_identity_deterministic(self):
        self.assertEqual(
            module.make_record()["question_contract_id"],
            module.make_record()["question_contract_id"],
        )

    def test_empty_question_blocked(self):
        self.assertIn(
            "QUESTION_MISSING",
            module.make_record(
                question=""
            )["failure_reasons"],
        )

    def test_room_identity_required(self):
        self.assertIn(
            "ROOM_IDENTITY_MISSING",
            module.make_record(
                room_object_id=""
            )["failure_reasons"],
        )

    def test_room_revision_required(self):
        self.assertIn(
            "ROOM_REVISION_MISSING",
            module.make_record(
                room_revision_id=""
            )["failure_reasons"],
        )

    def test_room_scope_valid(self):
        self.assertEqual(
            module.make_record(
                scope_type="ROOM"
            )["validation_disposition"],
            "VALID",
        )

    def test_zone_scope_valid(self):
        self.assertEqual(
            module.make_record(
                scope_type="ZONE",
                scope_reference="zone:a",
            )["validation_disposition"],
            "VALID",
        )

    def test_territory_scope_valid(self):
        self.assertEqual(
            module.make_record(
                scope_type="TERRITORY",
                scope_reference="territory:a",
            )["validation_disposition"],
            "VALID",
        )

    def test_invalid_scope_blocked(self):
        self.assertIn(
            "SCOPE_INVALID",
            module.make_record(
                scope_type="WORLD"
            )["failure_reasons"],
        )

    def test_scope_reference_required(self):
        self.assertIn(
            "SCOPE_REFERENCE_MISSING",
            module.make_record(
                scope_reference=""
            )["failure_reasons"],
        )

    def test_current_valid(self):
        self.assertEqual(
            module.make_record(
                temporal_mode="CURRENT"
            )["validation_disposition"],
            "VALID",
        )

    def test_bounded_range_valid(self):
        self.assertEqual(
            module.make_record(
                temporal_mode="BOUNDED_RANGE",
                start="2026-08-01T00:00:00+00:00",
                end="2026-08-08T00:00:00+00:00",
            )["validation_disposition"],
            "VALID",
        )

    def test_reverse_range_blocked(self):
        self.assertIn(
            "BOUNDED_RANGE_INVALID",
            module.make_record(
                temporal_mode="BOUNDED_RANGE",
                start="2026-08-08T00:00:00+00:00",
                end="2026-08-01T00:00:00+00:00",
            )["failure_reasons"],
        )

    def test_historical_reference_valid(self):
        self.assertEqual(
            module.make_record(
                temporal_mode="HISTORICAL",
                historical_reference="replay:historical:a",
            )["validation_disposition"],
            "VALID",
        )

    def test_historical_reference_required(self):
        self.assertIn(
            "HISTORICAL_REFERENCE_MISSING",
            module.make_record(
                temporal_mode="HISTORICAL"
            )["failure_reasons"],
        )

    def test_evidence_boundary_required(self):
        self.assertIn(
            "EVIDENCE_BOUNDARY_MISSING",
            module.make_record(
                evidence_boundary_reference=""
            )["failure_reasons"],
        )

    def test_evidence_ceiling_required(self):
        self.assertIn(
            "EVIDENCE_CEILING_MISSING",
            module.make_record(
                evidence_ceiling_reference=""
            )["failure_reasons"],
        )

    def test_invalid_personalization_blocked(self):
        self.assertIn(
            "PERSONALIZATION_POLICY_INVALID",
            module.make_record(
                personalization_policy="MAGIC"
            )["failure_reasons"],
        )

    def test_read_only_true(self):
        self.assertTrue(
            module.make_record()["read_only"]
        )

    def test_read_only_false_blocked(self):
        self.assertIn(
            "READ_ONLY_VIOLATED",
            module.make_record(
                read_only=False
            )["failure_reasons"],
        )

    def test_embedded_write_blocked(self):
        self.assertIn(
            "WRITE_OPERATION_EMBEDDED",
            module.make_record(
                write_operation_requested=True
            )["failure_reasons"],
        )

    def test_human_gate_active(self):
        self.assertEqual(
            module.make_record()["human_gate_state"],
            "ACTIVE",
        )

    def test_human_gate_disable_blocked(self):
        self.assertIn(
            "HUMAN_GATE_DISABLED",
            module.make_record(
                human_gate_state="DISABLED"
            )["failure_reasons"],
        )

    def test_authority_none(self):
        self.assertEqual(
            module.make_record()["authority_state"],
            "NONE",
        )

    def test_authority_promotion_blocked(self):
        self.assertIn(
            "AUTHORITY_PROMOTED",
            module.make_record(
                authority_state="WRITE"
            )["failure_reasons"],
        )

    def test_identity_tamper_blocked(self):
        record = module.make_record()
        record["question_contract_id"] = "sha512:" + "f" * 128

        self.assertIn(
            "CONTRACT_IDENTITY_INVALID",
            module.evaluate_record(record),
        )

    def test_semantic_change_requires_version_change(self):
        prior = module.make_record()
        current = deepcopy(prior)
        current["audience"] = "EXECUTIVE"

        self.assertIn(
            "SEMANTIC_VERSION_DRIFT",
            module.compare_versions(prior, current),
        )

    def test_semantic_change_with_new_version_valid(self):
        prior = module.make_record()
        current = deepcopy(prior)
        current["audience"] = "EXECUTIVE"
        current["version"] = "1.1.0"

        self.assertEqual(
            module.compare_versions(prior, current),
            [],
        )

    def test_human_machine_equivalent(self):
        human = module.make_record()

        self.assertEqual(
            module.compare_executors(
                human,
                deepcopy(human),
            ),
            [],
        )

    def test_human_machine_drift_blocked(self):
        human = module.make_record()
        machine = deepcopy(human)
        machine["evidence_ceiling_reference"] = "ceiling:raised"

        self.assertIn(
            "EXECUTOR_SEMANTIC_DRIFT",
            module.compare_executors(
                human,
                machine,
            ),
        )

    def test_provenance_required(self):
        record = module.make_record()
        record["provenance_route"] = []
        record = module.recalculate(record)

        self.assertIn(
            "PROVENANCE_MISSING",
            record["failure_reasons"],
        )

    def test_contract_validator_positive(self):
        self.assertEqual(
            module.validate(),
            [],
        )


if __name__ == "__main__":
    unittest.main()
