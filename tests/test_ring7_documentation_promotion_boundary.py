import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_ring7_documentation_promotion_boundary.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_ring7_documentation_promotion_boundary",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class Ring7BoundaryTests(
    unittest.TestCase
):

    def test_validator_passes(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_ring(self):
        record = module.make_registry()

        self.assertEqual(
            record["ring"],
            "R7-A"
        )

    def test_domain(self):
        record = module.make_registry()

        self.assertEqual(
            record["domain"],
            "DOCUMENTATION_AND_PROMOTION"
        )

    def test_inherited_state(self):
        record = module.make_registry()

        self.assertEqual(
            record["inherited_state"],
            "R6-P VALIDATED_CANDIDATE"
        )

    def test_fourteen_sections_registered(self):
        record = module.make_registry()

        self.assertEqual(
            len(record["sections"]),
            14
        )

    def test_sections_a_through_n(self):
        record = module.make_registry()

        self.assertEqual(
            set(record["sections"]),
            {
                f"R7-{letter}"
                for letter in "ABCDEFGHIJKLMN"
            }
        )

    def test_documentation_ownership_complete(self):
        record = module.make_registry()

        self.assertEqual(
            set(record["documentation_ownership"]),
            {
                "README",
                "USER_MANUAL",
                "ARCHITECTURE_GUIDE",
                "DEVELOPER_GUIDE",
                "AUDIT_GUIDE",
                "OPERATIONS_GUIDE",
            }
        )

    def test_question_contract_registered(self):
        record = module.make_registry()

        self.assertIn(
            "QUESTION_CONTRACT",
            record["required_machine_surfaces"]
        )

    def test_transition_receipt_registered(self):
        record = module.make_registry()

        self.assertIn(
            "TRANSITION_RECEIPT",
            record["required_machine_surfaces"]
        )

    def test_stability_receipt_registered(self):
        record = module.make_registry()

        self.assertIn(
            "STABILITY_RECEIPT",
            record["required_machine_surfaces"]
        )

    def test_completeness_receipt_registered(self):
        record = module.make_registry()

        self.assertIn(
            "COMPLETENESS_RECEIPT",
            record["required_machine_surfaces"]
        )

    def test_promotion_receipt_registered(self):
        record = module.make_registry()

        self.assertIn(
            "PROMOTION_RECEIPT",
            record["required_machine_surfaces"]
        )

    def test_lossless_receipt_satisfied(self):
        record = module.make_registry()

        self.assertEqual(
            record[
                "surface_states"
            ][
                "LOSSLESS_COLLAPSE_RECEIPT"
            ],
            "SATISFIED"
        )

    def test_question_contract_deferred_to_b(self):
        record = module.make_registry()

        self.assertEqual(
            record[
                "surface_states"
            ][
                "QUESTION_CONTRACT"
            ],
            "DEFERRED_TO_R7_B"
        )

    def test_native_entry_deferred_to_c(self):
        record = module.make_registry()

        self.assertEqual(
            record[
                "surface_states"
            ][
                "NATIVE_V41_ENTRY"
            ],
            "DEFERRED_TO_R7_C"
        )

    def test_promotion_blockers_explicit(self):
        record = module.make_registry()

        self.assertTrue(
            record["promotion_blockers"]
        )

    def test_human_gate_blocker_present(self):
        record = module.make_registry()

        self.assertIn(
            "HUMAN_GATE_AUTHORIZATION_NOT_GRANTED",
            record["promotion_blockers"]
        )

    def test_authority_none(self):
        record = module.make_registry()

        self.assertEqual(
            record["authority_state"],
            "NONE"
        )

    def test_human_gate_active(self):
        record = module.make_registry()

        self.assertEqual(
            record["human_gate_state"],
            "ACTIVE"
        )

    def test_candidate_state(self):
        record = module.make_registry()

        self.assertEqual(
            record["promotion_state"],
            "CANDIDATE"
        )

    def test_target_ready_for_human_gate(self):
        record = module.make_registry()

        self.assertEqual(
            record["target_state"],
            "READY_FOR_HUMAN_GATE"
        )

    def test_registry_validated(self):
        record = module.make_registry()

        self.assertEqual(
            record["registry_disposition"],
            "VALIDATED"
        )


if __name__ == "__main__":
    unittest.main()
