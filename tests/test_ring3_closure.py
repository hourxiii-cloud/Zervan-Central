import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_ring3_closure.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_ring3_closure",
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
            "R3",
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
        "component_states": {
            name: "PASS"
            for name, _, _ in module.ALL_COMPONENTS
        },
        "qualification_occupation_core_state":
            "PASS",
        "runtime_state_handoff_state":
            "BOUND",
        "source_tranche_boundary_state":
            "PRESERVED",
        "responsibility_integrity_state":
            "PRESERVED",
        "one_object_continuity_state":
            "PRESERVED",
        "state_separation_state":
            "PRESERVED",
        "failure_lock_state":
            "PRESERVED",
        "closure_state":
            "VALIDATED_CANDIDATE",
        "provenance_route": [
            "ring1:validated",
            "ring2:validated",
            "ring3:a-i",
        ],
        "closed_at":
            "2026-08-07T19:51:00-04:00",
    }

    record[
        "ring3_closure_receipt_id"
    ] = module.compute_receipt_id(
        record
    )

    return record


class Ring3ClosureTests(
    unittest.TestCase
):

    def test_repository_closure(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_receipt(self):
        receipt = make_receipt()

        self.assertEqual(
            module.validate_receipt(
                receipt
            ),
            []
        )

    def test_receipt_identity_is_deterministic(self):
        receipt = make_receipt()

        self.assertEqual(
            receipt[
                "ring3_closure_receipt_id"
            ],
            module.compute_receipt_id(
                receipt
            )
        )

    def test_exact_component_set(self):
        receipt = make_receipt()

        self.assertEqual(
            set(
                receipt[
                    "component_states"
                ]
            ),
            {
                "R3-A",
                "R3-B",
                "R3-C",
                "R3-D",
                "R3-E",
                "R3-F",
                "R3-G",
                "R3-H",
                "R3-I",
            }
        )

    def test_failed_component_cannot_close(self):
        receipt = make_receipt()

        receipt[
            "component_states"
        ][
            "R3-F"
        ] = "FAIL"

        receipt[
            "ring3_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "R3-F closure state must be PASS"
                in error
                for error in errors
            )
        )

    def test_source_boundary_must_be_preserved(self):
        receipt = make_receipt()

        receipt[
            "source_tranche_boundary_state"
        ] = "BROKEN"

        receipt[
            "ring3_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "source_tranche_boundary_state"
                in error
                for error in errors
            )
        )

    def test_hydration_handoff_must_be_bound(self):
        receipt = make_receipt()

        receipt[
            "runtime_state_handoff_state"
        ] = "COMPLETE"

        receipt[
            "ring3_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "runtime_state_handoff_state"
                in error
                for error in errors
            )
        )

    def test_closure_cannot_promote_candidate(self):
        receipt = make_receipt()

        receipt[
            "promotion_state"
        ] = "CANONICAL"

        receipt[
            "ring3_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "promotion_state"
                in error
                for error in errors
            )
        )

    def test_authority_remains_none(self):
        receipt = make_receipt()

        receipt[
            "authority_state"
        ] = "WRITE"

        receipt[
            "ring3_closure_receipt_id"
        ] = module.compute_receipt_id(
            receipt
        )

        errors = module.validate_receipt(
            receipt
        )

        self.assertTrue(
            any(
                "authority_state"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_pull_runtime_state_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "restriction_transition_id",
            "constriction_transition_id",
            "collapse_boundary_id",
            "landing_witness_id",
            "reflight_trigger_id",
            "closing_witness_id",
            "replay_envelope_id",
            "scar_replay_id",
            "canonical_promotion",
            "execution_authorization",
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
