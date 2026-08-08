import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_validation_audit_boundary.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_validation_audit_boundary",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class ValidationAuditBoundaryTests(
    unittest.TestCase
):

    def test_valid_registry(self):
        record = module.make_valid_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_ring5_dependency_locked(self):
        record = module.make_valid_record()

        record[
            "ring5_dependency"
        ] = "R5-I"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "must depend on closed Ring 5 R5-J"
                in error
                for error in errors
            )
        )

    def test_all_validation_families_required(self):
        record = module.make_valid_record()

        record[
            "required_validation_families"
        ] = record[
            "required_validation_families"
        ][:-1]

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "validation-family inventory"
                in error
                for error in errors
            )
        )

    def test_all_named_vectors_required(self):
        record = module.make_valid_record()

        record[
            "named_validation_vectors"
        ].remove(
            "RBT_001"
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "validation-vector inventory"
                in error
                for error in errors
            )
        )

    def test_question_contract_audit_surface_registered(self):
        record = module.make_valid_record()

        self.assertIn(
            "QUESTION_CONTRACT",
            record[
                "required_contract_audit_surfaces"
            ]
        )

    def test_lossless_receipt_audit_surface_registered(self):
        record = module.make_valid_record()

        self.assertIn(
            "LOSSLESS_COLLAPSE_RECEIPT",
            record[
                "required_contract_audit_surfaces"
            ]
        )

    def test_failure_classes_preserved(self):
        record = module.make_valid_record()

        record[
            "failure_classes"
        ].remove(
            "VALIDATOR_DEFECT"
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "failure classification inventory"
                in error
                for error in errors
            )
        )

    def test_promotion_remains_candidate(self):
        record = module.make_valid_record()

        record[
            "promotion_state"
        ] = "CANONICAL"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "promotion state must remain CANDIDATE"
                in error
                for error in errors
            )
        )

    def test_authority_remains_none(self):
        record = module.make_valid_record()

        record[
            "authority_state"
        ] = "WRITE"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "authority state must remain NONE"
                in error
                for error in errors
            )
        )

    def test_human_gate_remains_active(self):
        record = module.make_valid_record()

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

    def test_registry_is_not_validation_completion(self):
        record = module.make_valid_record()

        self.assertEqual(
            record[
                "registry_disposition"
            ],
            "REGISTERED"
        )

    def test_schema_does_not_absorb_repair_or_authority(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "test_execution_authority",
            "canonical_promotion",
            "doctrine_rewrite",
            "room_lifecycle_transition",
            "evidence_boundary_override",
            "evidence_ceiling_override",
            "human_gate_bypass",
            "automatic_repair",
        }

        self.assertFalse(
            set(
                schema[
                    "properties"
                ]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
