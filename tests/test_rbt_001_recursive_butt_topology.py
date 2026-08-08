import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_rbt_001_recursive_butt_topology.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_rbt_001_recursive_butt_topology",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class Rbt001RecursiveButtTopologyTests(
    unittest.TestCase
):

    def test_positive_carrier_valid(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_carrier_identity_locked(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "carrier_id"
            ],
            "RBT-001"
        )

        self.assertEqual(
            record[
                "carrier_name"
            ],
            "Recursive Butt Topology"
        )

    def test_primary_and_control_objects_distinct(self):
        record = module.make_record()

        self.assertNotEqual(
            record[
                "primary_object_id"
            ],
            record[
                "control_object_id"
            ]
        )

    def test_control_identity_collision_rejected(self):
        object_id = (
            "sha512:"
            + "1" * 128
        )

        record = module.make_record(
            primary_object_id=object_id,
            control_object_id=object_id,
        )

        self.assertIn(
            "CONTROL_OBJECT_IDENTITY_COLLISION",
            record[
                "failure_reasons"
            ]
        )

    def test_control_state_absorption_rejected(self):
        record = module.make_record(
            control_state_absorbed=True
        )

        self.assertIn(
            "OBJECT_ISOLATION_FAILED",
            record[
                "failure_reasons"
            ]
        )

    def test_signals_remain_distinct(self):
        record = module.make_record()

        ids = {
            signal[
                "signal_id"
            ]
            for signal in record[
                "signals"
            ]
        }

        self.assertEqual(
            len(ids),
            2
        )

    def test_signal_identity_collapse_rejected(self):
        signals = [
            module.make_signal(
                "signal:a",
                "source:left",
                "route:left",
            ),
            module.make_signal(
                "signal:a",
                "source:left",
                "route:left",
            ),
        ]

        record = module.make_record(
            signals=signals
        )

        self.assertIn(
            "SIGNAL_DIFFERENTIATION_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_signal_provenance_required(self):
        signals = [
            module.make_signal(
                "signal:a",
                "source:left",
                "route:left",
            ),
            module.make_signal(
                "signal:b",
                "source:right",
                "route:right",
            ),
        ]

        signals[1][
            "provenance_route"
        ] = []

        record = module.make_record(
            signals=signals
        )

        self.assertIn(
            "SIGNAL_PROVENANCE_LOST",
            record[
                "failure_reasons"
            ]
        )

    def test_boundary_preserved(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "primary_boundary_before"
            ],
            record[
                "primary_boundary_after"
            ]
        )

    def test_boundary_change_rejected(self):
        record = module.make_record(
            primary_boundary_after="boundary:wider"
        )

        self.assertIn(
            "PRIMARY_BOUNDARY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_control_boundary_absorption_rejected(self):
        record = module.make_record(
            primary_boundary_after="boundary:control"
        )

        self.assertIn(
            "CONTROL_BOUNDARY_ABSORBED",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_ceiling_change_rejected(self):
        record = module.make_record(
            primary_evidence_ceiling_after="ceiling:higher"
        )

        self.assertIn(
            "EVIDENCE_CEILING_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_landing_witness_required(self):
        record = module.make_record(
            landing_witness_reference=None
        )

        self.assertIn(
            "LANDING_WITNESS_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_landing_same_object(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "landing_object_id"
            ],
            record[
                "primary_object_id"
            ]
        )

    def test_landing_object_change_rejected(self):
        record = module.make_record(
            landing_object_id=(
                "sha512:"
                + "3" * 128
            )
        )

        self.assertIn(
            "LANDING_OBJECT_IDENTITY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_landing_coordinate_required(self):
        record = module.make_record(
            landing_coordinate=None
        )

        self.assertIn(
            "LANDING_COORDINATE_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_signal_split_reflight_valid(self):
        record = module.make_record(
            reflight_trigger_type="SIGNAL_SPLIT"
        )

        self.assertEqual(
            record[
                "reflight_eligibility"
            ],
            "ELIGIBLE"
        )

    def test_signal_split_requires_prior_state(self):
        record = module.make_record(
            prior_signal_state_reference=None
        )

        self.assertIn(
            "SIGNAL_STATE_REFERENCE_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_signal_split_requires_current_state(self):
        record = module.make_record(
            current_signal_state_reference=None
        )

        self.assertIn(
            "SIGNAL_STATE_REFERENCE_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_signal_split_requires_evidence(self):
        record = module.make_record(
            reflight_trigger_evidence=[]
        )

        self.assertIn(
            "REFLIGHT_TRIGGER_EVIDENCE_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_reflight_material_change_required(self):
        record = module.make_record(
            reflight_material_change_basis=None
        )

        self.assertIn(
            "REFLIGHT_MATERIAL_CHANGE_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_celebration_is_not_reflight_trigger(self):
        record = module.make_record(
            reflight_trigger_type="CELEBRATION"
        )

        self.assertIn(
            "REFLIGHT_TRIGGER_INVALID",
            record[
                "failure_reasons"
            ]
        )

    def test_repetition_is_not_reflight_trigger(self):
        record = module.make_record(
            reflight_trigger_type="REPETITION"
        )

        self.assertIn(
            "REFLIGHT_TRIGGER_INVALID",
            record[
                "failure_reasons"
            ]
        )

    def test_capability_availability_is_not_trigger(self):
        record = module.make_record(
            reflight_trigger_type="CAPABILITY_AVAILABLE"
        )

        self.assertIn(
            "REFLIGHT_TRIGGER_INVALID",
            record[
                "failure_reasons"
            ]
        )

    def test_return_same_object(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "returned_object_id"
            ],
            record[
                "primary_object_id"
            ]
        )

    def test_return_object_change_rejected(self):
        record = module.make_record(
            returned_object_id=(
                "sha512:"
                + "3" * 128
            )
        )

        self.assertIn(
            "RETURN_OBJECT_IDENTITY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_return_coordinate_preserved(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "return_coordinate"
            ],
            record[
                "returned_coordinate"
            ]
        )

    def test_return_coordinate_change_rejected(self):
        record = module.make_record(
            returned_coordinate="coord:rbt:approximate"
        )

        self.assertIn(
            "RETURN_COORDINATE_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_reconstruction_rejected(self):
        record = module.make_record(
            reconstruction_used=True
        )

        self.assertIn(
            "RECONSTRUCTION_USED",
            record[
                "failure_reasons"
            ]
        )

    def test_stick_required(self):
        record = module.make_record(
            primary_stick_reference=None
        )

        self.assertIn(
            "STICK_NOT_PRESERVED",
            record[
                "failure_reasons"
            ]
        )

    def test_control_provenance_absorption_rejected(self):
        record = module.make_record(
            control_provenance_absorbed=True
        )

        self.assertIn(
            "CONTROL_PROVENANCE_ABSORBED",
            record[
                "failure_reasons"
            ]
        )

    def test_lifecycle_mutation_rejected(self):
        record = module.make_record(
            lifecycle_mutated=True
        )

        self.assertIn(
            "LIFECYCLE_MUTATED",
            record[
                "failure_reasons"
            ]
        )

    def test_occupancy_invention_rejected(self):
        record = module.make_record(
            occupancy_invented=True
        )

        self.assertIn(
            "OCCUPANCY_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_formation_invention_rejected(self):
        record = module.make_record(
            formation_invented=True
        )

        self.assertIn(
            "FORMATION_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_full_payload_hydration_rejected(self):
        record = module.make_record(
            full_payload_hydration_requested=True
        )

        self.assertIn(
            "FULL_PAYLOAD_HYDRATION_REQUESTED",
            record[
                "failure_reasons"
            ]
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
