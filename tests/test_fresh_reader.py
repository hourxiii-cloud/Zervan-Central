import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_fresh_reader.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_fresh_reader",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class FreshReaderTests(
    unittest.TestCase
):

    def test_candidate_readable(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "candidate_readability"
            ],
            "CANDIDATE_READABLE"
        )

    def test_candidate_disposition(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALIDATED_CANDIDATE"
        )

    def test_readme_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "repository_orientation_present"
            ]
        )

    def test_inventory_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "inventory_present"
            ]
        )

    def test_contracts_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "contracts_present"
            ]
        )

    def test_schemas_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "schemas_present"
            ]
        )

    def test_tools_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "tools_present"
            ]
        )

    def test_tests_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "tests_present"
            ]
        )

    def test_registry_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "r6_registry_present"
            ]
        )

    def test_ring6_runner_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "ring6_runner_present"
            ]
        )

    def test_candidate_version_identity_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "candidate_version_identity_present"
            ]
        )

    def test_authority_none_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "authority_none_present"
            ]
        )

    def test_human_gate_active_present(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "human_gate_active_present"
            ]
        )

    def test_v40_knowledge_not_required(self):
        record = module.build_record()

        self.assertFalse(
            record[
                "requires_v40_knowledge"
            ]
        )

    def test_v40_dependency_rejected(self):
        record = module.build_record(
            requires_v40_knowledge=True
        )

        self.assertIn(
            "V40_KNOWLEDGE_REQUIRED",
            record[
                "failure_reasons"
            ]
        )

    def test_conversation_not_required(self):
        record = module.build_record()

        self.assertFalse(
            record[
                "requires_prior_conversation"
            ]
        )

    def test_conversation_dependency_rejected(self):
        record = module.build_record(
            requires_prior_conversation=True
        )

        self.assertIn(
            "PRIOR_CONVERSATION_REQUIRED",
            record[
                "failure_reasons"
            ]
        )

    def test_architect_interpretation_not_required(self):
        record = module.build_record()

        self.assertFalse(
            record[
                "requires_architect_interpretation"
            ]
        )

    def test_architect_dependency_rejected(self):
        record = module.build_record(
            requires_architect_interpretation=True
        )

        self.assertIn(
            "ARCHITECT_INTERPRETATION_REQUIRED",
            record[
                "failure_reasons"
            ]
        )

    def test_emotional_history_not_required(self):
        record = module.build_record()

        self.assertFalse(
            record[
                "requires_emotional_discovery_history"
            ]
        )

    def test_emotional_history_dependency_rejected(self):
        record = module.build_record(
            requires_emotional_discovery_history=True
        )

        self.assertIn(
            "EMOTIONAL_HISTORY_REQUIRED",
            record[
                "failure_reasons"
            ]
        )

    def test_historical_v40_material_preserved(self):
        record = module.build_record()

        self.assertTrue(
            record[
                "historical_v40_initiation_present"
            ]
        )

        self.assertTrue(
            record[
                "historical_v40_canonical_present"
            ]
        )

    def test_historical_substitution_not_used(self):
        record = module.build_record()

        self.assertFalse(
            record[
                "historical_substitution_used"
            ]
        )

    def test_historical_substitution_rejected(self):
        record = module.build_record(
            historical_substitution_used=True
        )

        self.assertIn(
            "HISTORICAL_VERSION_SUBSTITUTED",
            record[
                "failure_reasons"
            ]
        )

    def test_promoted_entry_state_matches_actual_surfaces(self):
        record = module.build_record()

        actual_ready = (
            record[
                "v41_initiation_present"
            ]
            and record[
                "v41_canonical_entry_present"
            ]
        )

        expected = (
            "READY"
            if actual_ready
            else "DEFERRED_TO_PROMOTION"
        )

        self.assertEqual(
            record[
                "promoted_entry_state"
            ],
            expected
        )

    def test_false_promoted_ready_rejected_when_missing(self):
        record = module.build_record(
            force_promoted_ready=True
        )

        if (
            not record[
                "v41_initiation_present"
            ]
            or not record[
                "v41_canonical_entry_present"
            ]
        ):
            self.assertIn(
                "PROMOTED_ENTRY_FALSELY_CLAIMED",
                record[
                    "failure_reasons"
                ]
            )

    def test_authority_promotion_rejected(self):
        record = module.build_record(
            authority_state="WRITE"
        )

        self.assertIn(
            "AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_human_gate_remains_active(self):
        record = module.build_record()

        record[
            "human_gate_state"
        ] = "DISABLED"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "Human Gate state must remain ACTIVE"
                in error
                for error in errors
            )
        )


if __name__ == "__main__":
    unittest.main()
