import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_ring4_closure.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_ring4_closure",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_receipt():
    record = {
        "schema_version":
            "1.0",
        "native_version":
            "vTemporal.41.0",
        "ring":
            "R4",
        "promotion_state":
            "CANDIDATE",
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "ring1_dependency_state":
            "PASS",
        "ring2_dependency_state":
            "PASS",
        "ring3_dependency_state":
            "PASS",
        "hydration_handoff_state":
            "BOUND",
        "component_states": {
            name: "PASS"
            for name, _, _ in module.COMPONENTS
        },
        "tranche6_coverage_state":
            "COMPLETE",
        "source_boundary_state":
            "PRESERVED",
        "one_object_continuity_state":
            "PRESERVED",
        "state_domain_separation_state":
            "PRESERVED",
        "coordinate_continuity_state":
            "PRESERVED",
        "lineage_continuity_state":
            "PRESERVED",
        "evidence_boundary_continuity_state":
            "PRESERVED",
        "evidence_ceiling_continuity_state":
            "PRESERVED",
        "cartography_continuity_state":
            "PRESERVED",
        "stick_continuity_state":
            "PRESERVED",
        "provenance_continuity_state":
            "PRESERVED",
        "responsibility_integrity_state":
            "PRESERVED",
        "post_convergence_control_state":
            "PRESERVED",
        "replay_fidelity_state":
            "PRESERVED",
        "scar_integrity_state":
            "PRESERVED",
        "failure_lock_state":
            "PRESERVED",
        "closure_state":
            "VALIDATED_CANDIDATE",
        "provenance_route": [
            "ring1:validated",
            "ring2:validated",
            "ring3:validated",
            "r3-i:hydration-handoff",
            "r4-a",
            "r4-b",
            "r4-c",
            "r4-d",
            "r4-e",
            "r4-f",
            "r4-g",
            "r4-h",
            "r4-i",
            "r4-j",
        ],
        "closed_at":
            "2026-08-07T21:10:00-04:00",
    }

    record[
        "ring4_closure_receipt_id"
    ] = module.compute_receipt_id(
        record
    )

    return record


class Ring4ClosureTests(
    unittest.TestCase
):

    def test_repository_closure(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_candidate_receipt(self):
        receipt = make_receipt()

        self.assertEqual(
            module.validate_receipt(
                receipt
            ),
            []
        )

    def test_all_components_exactly_a_through_i(self):
        receipt = make_receipt()

        self.assertEqual(
            set(
                receipt[
                    "component_states"
                ]
            ),
            {
                name
                for name, _, _ in module.COMPONENTS
            }
        )

    def test_component_failure_blocks_closure(self):
        receipt = make_receipt()

        receipt[
            "component_states"
        ][
            "R4-H"
        ] = "FAIL"

        receipt[
            "ring4_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "R4-H closure state must be PASS"
                in error
                for error in errors
            )
        )

    def test_promotion_must_remain_candidate(self):
        receipt = make_receipt()

        receipt[
            "promotion_state"
        ] = "CANONICAL"

        receipt[
            "ring4_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "promotion_state must be CANDIDATE"
                in error
                for error in errors
            )
        )

    def test_authority_must_remain_none(self):
        receipt = make_receipt()

        receipt[
            "authority_state"
        ] = "WRITE"

        receipt[
            "ring4_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "authority_state must be NONE"
                in error
                for error in errors
            )
        )

    def test_human_gate_must_remain_active(self):
        receipt = make_receipt()

        receipt[
            "human_gate_state"
        ] = "INACTIVE"

        receipt[
            "ring4_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "human_gate_state must be ACTIVE"
                in error
                for error in errors
            )
        )

    def test_tranche6_must_be_complete(self):
        receipt = make_receipt()

        receipt[
            "tranche6_coverage_state"
        ] = "PARTIAL"

        receipt[
            "ring4_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "tranche6_coverage_state must be COMPLETE"
                in error
                for error in errors
            )
        )

    def test_one_object_continuity_must_be_preserved(self):
        receipt = make_receipt()

        receipt[
            "one_object_continuity_state"
        ] = "BROKEN"

        receipt[
            "ring4_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "one_object_continuity_state must be PRESERVED"
                in error
                for error in errors
            )
        )

    def test_material_change_changes_receipt_identity(self):
        first = make_receipt()

        changed = json.loads(
            json.dumps(first)
        )

        changed[
            "closed_at"
        ] = "2026-08-07T21:11:00-04:00"

        changed[
            "ring4_closure_receipt_id"
        ] = module.compute_receipt_id(
            changed
        )

        self.assertNotEqual(
            first[
                "ring4_closure_receipt_id"
            ],
            changed[
                "ring4_closure_receipt_id"
            ]
        )

    def test_schema_does_not_absorb_downstream_promotion(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "canonical_promotion",
            "execution_authorization",
            "publication_authorization",
            "certification_authorization",
            "main_branch_promotion",
            "tranche7_completion",
            "pmc_redefinition",
            "ccr_redefinition",
            "mc_redefinition",
            "raven_redefinition",
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
