import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_orthogonal_transition.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_orthogonal_transition",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class OrthogonalTransitionTests(
    unittest.TestCase
):

    def test_a_to_b_to_a_valid(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_source_target_must_be_distinct(self):
        object_id = (
            "sha512:"
            + "1" * 128
        )

        record = module.make_record(
            source_object_id=object_id,
            target_object_id=object_id,
        )

        self.assertIn(
            "SOURCE_TARGET_IDENTITY_COLLISION",
            record[
                "failure_reasons"
            ]
        )

    def test_return_must_be_original_source(self):
        record = module.make_record(
            returned_object_id=(
                "sha512:"
                + "3" * 128
            )
        )

        self.assertIn(
            "RETURNED_SOURCE_IDENTITY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_source_genesis_required(self):
        record = module.make_record(
            source_genesis_reference=None
        )

        self.assertIn(
            "SOURCE_GENESIS_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_target_genesis_required(self):
        record = module.make_record(
            target_genesis_reference=None
        )

        self.assertIn(
            "TARGET_GENESIS_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_independent_origins_required(self):
        record = module.make_record(
            target_origin_reference=None
        )

        self.assertIn(
            "TARGET_ORIGIN_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_independent_cartography_required(self):
        record = module.make_record(
            target_cartography_reference=None
        )

        self.assertIn(
            "TARGET_CARTOGRAPHY_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_source_stick_required(self):
        record = module.make_record(
            source_stick_reference=None
        )

        self.assertIn(
            "SOURCE_STICK_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_target_stick_required(self):
        record = module.make_record(
            target_stick_reference=None
        )

        self.assertIn(
            "TARGET_STICK_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_outbound_passageway_must_be_established(self):
        record = module.make_record(
            outbound_passageway_state="PROPOSED"
        )

        self.assertIn(
            "OUTBOUND_PASSAGEWAY_NOT_ESTABLISHED",
            record[
                "failure_reasons"
            ]
        )

    def test_return_passageway_must_be_established(self):
        record = module.make_record(
            return_passageway_state="BLOCKED"
        )

        self.assertIn(
            "RETURN_PASSAGEWAY_NOT_ESTABLISHED",
            record[
                "failure_reasons"
            ]
        )

    def test_outbound_direction_must_be_authorized(self):
        record = module.make_record(
            outbound_direction_authorized=False
        )

        self.assertIn(
            "OUTBOUND_DIRECTION_UNAUTHORIZED",
            record[
                "failure_reasons"
            ]
        )

    def test_return_direction_must_be_authorized(self):
        record = module.make_record(
            return_direction_authorized=False
        )

        self.assertIn(
            "RETURN_DIRECTION_UNAUTHORIZED",
            record[
                "failure_reasons"
            ]
        )

    def test_occupancy_order_exact(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "occupancy_events"
            ],
            module.expected_occupancy_events(
                record[
                    "source_object_id"
                ],
                record[
                    "target_object_id"
                ],
            )
        )

    def test_b_presence_before_entry_rejected(self):
        record = module.make_record()

        events = list(
            record[
                "occupancy_events"
            ]
        )

        events[1], events[2] = (
            events[2],
            events[1],
        )

        record = module.make_record(
            occupancy_events=events
        )

        self.assertIn(
            "OCCUPANCY_EVENT_ORDER_INVALID",
            record[
                "failure_reasons"
            ]
        )

    def test_return_before_b_exit_rejected(self):
        record = module.make_record()

        events = list(
            record[
                "occupancy_events"
            ]
        )

        events[3], events[4] = (
            events[4],
            events[3],
        )

        record = module.make_record(
            occupancy_events=events
        )

        self.assertIn(
            "OCCUPANCY_EVENT_ORDER_INVALID",
            record[
                "failure_reasons"
            ]
        )

    def test_wrong_room_occupancy_binding_rejected(self):
        record = module.make_record()

        events = list(
            record[
                "occupancy_events"
            ]
        )

        events[1] = {
            "object_id":
                "sha512:"
                + "3" * 128,
            "event":
                "ENTERED",
        }

        record = module.make_record(
            occupancy_events=events
        )

        self.assertIn(
            "OCCUPANCY_OBJECT_BINDING_INVALID",
            record[
                "failure_reasons"
            ]
        )

    def test_return_coordinate_preserved(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "source_return_coordinate"
            ],
            record[
                "returned_source_coordinate"
            ]
        )

    def test_return_coordinate_change_rejected(self):
        record = module.make_record(
            returned_source_coordinate="coord:a:approximate"
        )

        self.assertIn(
            "SOURCE_RETURN_COORDINATE_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_source_boundary_preserved_on_return(self):
        record = module.make_record(
            returned_source_evidence_boundary_reference="boundary:b"
        )

        self.assertIn(
            "SOURCE_EVIDENCE_BOUNDARY_CONTAMINATED",
            record[
                "failure_reasons"
            ]
        )

    def test_source_ceiling_preserved_on_return(self):
        record = module.make_record(
            returned_source_evidence_ceiling_reference="ceiling:b"
        )

        self.assertIn(
            "SOURCE_EVIDENCE_CEILING_CONTAMINATED",
            record[
                "failure_reasons"
            ]
        )

    def test_shared_provenance_is_allowed(self):
        record = module.make_record()

        self.assertTrue(
            record[
                "shared_provenance"
            ]
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_unauthorized_transfer_rejected(self):
        record = module.make_record(
            unauthorized_cross_object_transfers=[
                "target-only -> source",
            ]
        )

        self.assertIn(
            "UNAUTHORIZED_CROSS_OBJECT_TRANSFER",
            record[
                "failure_reasons"
            ]
        )

    def test_source_contamination_rejected(self):
        record = module.make_record(
            source_contamination_detected=True
        )

        self.assertIn(
            "SOURCE_CONTAMINATION_DETECTED",
            record[
                "failure_reasons"
            ]
        )

    def test_target_contamination_rejected(self):
        record = module.make_record(
            target_contamination_detected=True
        )

        self.assertIn(
            "TARGET_CONTAMINATION_DETECTED",
            record[
                "failure_reasons"
            ]
        )

    def test_merge_rejected(self):
        record = module.make_record(
            merge_created=True
        )

        self.assertIn(
            "MERGE_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_synthesized_object_rejected(self):
        record = module.make_record(
            synthesized_object_created=True
        )

        self.assertIn(
            "SYNTHESIZED_OBJECT_INVENTED",
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
