import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_lossless_collapse.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_lossless_collapse",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class LosslessCollapseTests(
    unittest.TestCase
):

    def test_positive_collapse_valid(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_all_preservation_classes_present(self):
        record = module.make_record()

        self.assertEqual(
            set(
                record[
                    "observed_preservation_classes"
                ]
            ),
            set(
                module.REQUIRED_CLASSES
            )
        )

    def test_object_identity_preserved(self):
        record = module.make_record()

        self.assertIn(
            "OBJECT_IDENTITY",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_capability_preserved(self):
        record = module.make_record()

        self.assertIn(
            "CAPABILITY",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_behavior_preserved(self):
        record = module.make_record()

        self.assertIn(
            "BEHAVIOR",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_rationale_preserved(self):
        record = module.make_record()

        self.assertIn(
            "RATIONALE",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_provenance_preserved(self):
        record = module.make_record()

        self.assertIn(
            "PROVENANCE",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_coordinates_preserved(self):
        record = module.make_record()

        self.assertIn(
            "COORDINATES",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_transform_history_preserved(self):
        record = module.make_record()

        self.assertIn(
            "TRANSFORM_HISTORY",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_contracts_preserved(self):
        record = module.make_record()

        self.assertIn(
            "CONTRACTS",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_tests_preserved(self):
        record = module.make_record()

        self.assertIn(
            "TESTS",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_evidence_boundaries_preserved(self):
        record = module.make_record()

        self.assertIn(
            "EVIDENCE_BOUNDARIES",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_known_failure_conditions_preserved(self):
        record = module.make_record()

        self.assertIn(
            "KNOWN_FAILURE_CONDITIONS",
            record[
                "observed_preservation_classes"
            ]
        )

    def test_missing_class_rejected(self):
        record = module.make_record(
            observed_classes=[
                value
                for value in module.REQUIRED_CLASSES
                if value != "RATIONALE"
            ]
        )

        self.assertIn(
            "PRESERVATION_CLASS_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_collapsed_surface_has_destination(self):
        record = module.make_record()

        destinations = {
            item[
                "surface_reference"
            ]
            for item in record[
                "retained_surfaces"
            ]
        }

        for item in record[
            "collapsed_surfaces"
        ]:
            self.assertIn(
                item[
                    "retained_destination_reference"
                ],
                destinations
            )

    def test_missing_collapse_destination_rejected(self):
        record = module.make_record()

        record[
            "collapsed_surfaces"
        ][0][
            "retained_destination_reference"
        ] = "missing:surface"

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "COLLAPSED_SURFACE_DESTINATION_MISSING",
            reasons
        )

    def test_invalid_collapse_basis_rejected(self):
        record = module.make_record()

        record[
            "collapsed_surfaces"
        ][0][
            "removal_basis"
        ] = ""

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "COLLAPSE_BASIS_MISSING",
            reasons
        )

    def test_invalid_retention_basis_rejected(self):
        record = module.make_record()

        record[
            "retained_surfaces"
        ][0][
            "retention_basis"
        ] = ""

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "RETENTION_BASIS_MISSING",
            reasons
        )

    def test_all_invariants_map_to_retained_surface(self):
        record = module.make_record()

        mapped = {
            item[
                "preservation_class"
            ]
            for item in record[
                "invariant_mappings"
            ]
        }

        self.assertTrue(
            set(
                module.REQUIRED_CLASSES
            ).issubset(
                mapped
            )
        )

    def test_missing_invariant_mapping_rejected(self):
        record = module.make_record()

        record[
            "invariant_mappings"
        ] = [
            item
            for item in record[
                "invariant_mappings"
            ]
            if item[
                "preservation_class"
            ]
            != "RATIONALE"
        ]

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "INVARIANT_MAPPING_MISSING",
            reasons
        )

    def test_test_coverage_preserved(self):
        record = module.make_record()

        self.assertTrue(
            record[
                "test_mappings"
            ]
        )

    def test_test_coverage_loss_rejected(self):
        record = module.make_record()

        record[
            "test_mappings"
        ] = []

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "TEST_COVERAGE_LOST",
            reasons
        )

    def test_failure_conditions_preserved(self):
        record = module.make_record()

        self.assertTrue(
            record[
                "failure_condition_mappings"
            ]
        )

    def test_failure_condition_loss_rejected(self):
        record = module.make_record()

        record[
            "failure_condition_mappings"
        ] = []

        reasons = module.evaluate_record(
            record
        )

        self.assertIn(
            "KNOWN_FAILURE_CONDITION_LOST",
            reasons
        )

    def test_unexplained_vanishing_rejected(self):
        record = module.make_record(
            unexplained_vanishing_detected=True
        )

        self.assertIn(
            "UNEXPLAINED_VANISHING",
            record[
                "failure_reasons"
            ]
        )

    def test_unresolved_item_rejected(self):
        record = module.make_record(
            unresolved_items=[
                "unknown invariant fate"
            ]
        )

        self.assertIn(
            "UNRESOLVED_ITEM_PRESENT",
            record[
                "failure_reasons"
            ]
        )

    def test_semantic_loss_rejected(self):
        record = module.make_record(
            semantic_loss_detected=True
        )

        self.assertIn(
            "SEMANTIC_LOSS_DETECTED",
            record[
                "failure_reasons"
            ]
        )

    def test_provenance_loss_rejected(self):
        record = module.make_record(
            provenance_lost=True
        )

        self.assertIn(
            "PROVENANCE_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_coordinate_history_loss_rejected(self):
        record = module.make_record(
            coordinate_history_lost=True
        )

        self.assertIn(
            "COORDINATE_HISTORY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_transform_history_loss_rejected(self):
        record = module.make_record(
            transform_history_lost=True
        )

        self.assertIn(
            "TRANSFORM_HISTORY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_boundary_loss_rejected(self):
        record = module.make_record(
            evidence_boundary_semantics_lost=True
        )

        self.assertIn(
            "EVIDENCE_BOUNDARY_SEMANTICS_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_contract_semantic_loss_rejected(self):
        record = module.make_record(
            contract_semantics_lost=True
        )

        self.assertIn(
            "CONTRACT_SEMANTICS_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_capability_loss_rejected(self):
        record = module.make_record(
            capability_lost=True
        )

        self.assertIn(
            "CAPABILITY_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_behavior_change_rejected(self):
        record = module.make_record(
            behavior_changed=True
        )

        self.assertIn(
            "BEHAVIOR_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_rationale_loss_rejected(self):
        record = module.make_record(
            rationale_lost=True
        )

        self.assertIn(
            "RATIONALE_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_receipt_type(self):
        record = module.make_record()
        receipt = module.build_receipt(
            record
        )

        self.assertEqual(
            receipt[
                "receipt_type"
            ],
            "LOSSLESS_COLLAPSE_RECEIPT"
        )

    def test_receipt_positive_is_lossless(self):
        record = module.make_record()
        receipt = module.build_receipt(
            record
        )

        self.assertEqual(
            receipt[
                "collapse_disposition"
            ],
            "LOSSLESS"
        )

    def test_receipt_contains_all_classes(self):
        record = module.make_record()
        receipt = module.build_receipt(
            record
        )

        self.assertEqual(
            set(
                receipt[
                    "preservation_classes"
                ]
            ),
            set(
                module.REQUIRED_CLASSES
            )
        )

    def test_receipt_validation_positive(self):
        record = module.make_record()
        receipt = module.build_receipt(
            record
        )

        self.assertEqual(
            module.validate_receipt(
                receipt
            ),
            []
        )

    def test_authority_promotion_rejected(self):
        record = module.make_record(
            authority_state="WRITE"
        )

        self.assertIn(
            "AUTHORITY_PROMOTED",
            record[
                "failure_reasons"
            ]
        )

    def test_human_gate_remains_active(self):
        record = module.make_record()

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
