import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_ring6_closure.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_ring6_closure",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class Ring6ClosureTests(
    unittest.TestCase
):

    def test_required_family_count(self):
        self.assertEqual(
            len(
                module.REQUIRED_FAMILIES
            ),
            12
        )

    def test_required_families_unique(self):
        self.assertEqual(
            len(
                module.REQUIRED_FAMILIES
            ),
            len(
                set(
                    module.REQUIRED_FAMILIES
                )
            )
        )

    def test_named_vector_count(self):
        self.assertEqual(
            len(
                module.NAMED_VECTORS
            ),
            12
        )

    def test_all_named_vectors_have_ring(self):
        self.assertEqual(
            set(
                module.NAMED_VECTORS
            ),
            set(
                module.VECTOR_TO_RING
            )
        )

    def test_failure_taxonomy_exact(self):
        self.assertEqual(
            set(
                module.FAILURE_TAXONOMY
            ),
            {
                "INNER_INVARIANT_CONTRADICTION",
                "OUTER_IMPLEMENTATION_DEFECT",
                "VALIDATOR_DEFECT",
                "COVERAGE_GAP",
                "SOURCE_COLLISION",
                "UNRESOLVED_REQUIRED_SURFACE",
            }
        )

    def test_ring_sections_a_through_p(self):
        self.assertEqual(
            module.RING_SECTIONS,
            [
                f"R6-{letter}"
                for letter in "ABCDEFGHIJKLMNOP"
            ]
        )

    def test_family_coverage_complete(self):
        coverage = module.family_coverage()

        self.assertEqual(
            set(
                coverage
            ),
            set(
                module.REQUIRED_FAMILIES
            )
        )

    def test_all_family_coverage_validated(self):
        coverage = module.family_coverage()

        self.assertTrue(
            all(
                item[
                    "state"
                ]
                == "VALIDATED"
                for item in coverage.values()
            )
        )

    def test_schema_audit_passes(self):
        self.assertEqual(
            module.audit_ring6_schemas(),
            []
        )

    def test_valid_replacement_allows_location_change(self):
        reasons = module.evaluate_replacement_case(
            location_changed=True,
            capability_preserved=True,
            behavior_preserved=True,
            invariant_meaning_preserved=True,
            provenance_preserved=True,
        )

        self.assertEqual(
            reasons,
            []
        )

    def test_replacement_lost_capability_rejected(self):
        reasons = module.evaluate_replacement_case(
            location_changed=True,
            capability_preserved=False,
            behavior_preserved=True,
            invariant_meaning_preserved=True,
            provenance_preserved=True,
        )

        self.assertIn(
            "LOST_CAPABILITY",
            reasons
        )

    def test_replacement_changed_behavior_rejected(self):
        reasons = module.evaluate_replacement_case(
            location_changed=True,
            capability_preserved=True,
            behavior_preserved=False,
            invariant_meaning_preserved=True,
            provenance_preserved=True,
        )

        self.assertIn(
            "CHANGED_BEHAVIOR",
            reasons
        )

    def test_replacement_changed_semantics_rejected(self):
        reasons = module.evaluate_replacement_case(
            location_changed=True,
            capability_preserved=True,
            behavior_preserved=True,
            invariant_meaning_preserved=False,
            provenance_preserved=True,
        )

        self.assertIn(
            "CHANGED_SEMANTICS",
            reasons
        )

    def test_replacement_lost_provenance_rejected(self):
        reasons = module.evaluate_replacement_case(
            location_changed=True,
            capability_preserved=True,
            behavior_preserved=True,
            invariant_meaning_preserved=True,
            provenance_preserved=False,
        )

        self.assertIn(
            "LOST_PROVENANCE",
            reasons
        )

    def test_lossless_receipt_implemented(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "audit_surface_states"
            ][
                "LOSSLESS_COLLAPSE_RECEIPT"
            ],
            "IMPLEMENTED"
        )

    def test_question_contract_accounted_for(self):
        record = module.build_record()

        self.assertIn(
            record[
                "audit_surface_states"
            ][
                "QUESTION_CONTRACT"
            ],
            (
                "IMPLEMENTED",
                "DEFERRED_TO_RING9",
            )
        )

    def test_promotion_receipt_accounted_for(self):
        record = module.build_record()

        self.assertIn(
            record[
                "audit_surface_states"
            ][
                "PROMOTION_RECEIPT"
            ],
            (
                "IMPLEMENTED",
                "DEFERRED_TO_RING9",
            )
        )

    def test_no_blocking_coverage_gaps(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "blocking_coverage_gaps"
            ],
            []
        )

    def test_no_unclassified_failures(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "unclassified_failures"
            ],
            []
        )

    def test_authority_none(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "authority_state"
            ],
            "NONE"
        )

    def test_human_gate_active(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "human_gate_state"
            ],
            "ACTIVE"
        )

    def test_promotion_state_candidate(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "promotion_state"
            ],
            "CANDIDATE"
        )

    def test_closure_disposition_validated_candidate(self):
        record = module.build_record()

        self.assertEqual(
            record[
                "closure_disposition"
            ],
            "VALIDATED_CANDIDATE"
        )

    def test_validate_record_accepts_positive(self):
        record = module.build_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )


if __name__ == "__main__":
    unittest.main()
