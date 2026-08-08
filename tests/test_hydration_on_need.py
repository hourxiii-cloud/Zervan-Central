import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_hydration_on_need.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_hydration_on_need",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class HydrationOnNeedTests(
    unittest.TestCase
):

    def test_mission_required_scope_valid(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_full_payload_scope_rejected(self):
        record = module.make_record(
            payload_scope="FULL_PAYLOAD"
        )

        self.assertIn(
            "FULL_PAYLOAD_SCOPE_FORBIDDEN",
            record[
                "failure_reasons"
            ]
        )

    def test_load_everything_rejected(self):
        record = module.make_record(
            payload_scope="LOAD_EVERYTHING"
        )

        self.assertIn(
            "FULL_PAYLOAD_SCOPE_FORBIDDEN",
            record[
                "failure_reasons"
            ]
        )

    def test_active_mission_required(self):
        record = module.make_record(
            active_mission_reference=None
        )

        self.assertIn(
            "ACTIVE_MISSION_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_active_question_required(self):
        record = module.make_record(
            active_question=None
        )

        self.assertIn(
            "ACTIVE_QUESTION_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_narrow_question_hydrates_subset(self):
        record = module.make_record(
            operation_context="NARROW_QUESTION",
            requested_payload=[
                "payload:a"
            ],
            mission_required_payload=[
                "payload:a"
            ],
            restored_payload=[
                "payload:a"
            ],
            retained_at_rest_payload=[
                "payload:b",
                "payload:c",
            ],
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_unverified_territory_rejected(self):
        record = module.make_record(
            verified_territory_available=[
                "territory:a"
            ],
            requested_verified_territory=[
                "territory:z"
            ],
            restored_verified_territory=[],
        )

        self.assertIn(
            "UNVERIFIED_TERRITORY_REQUESTED",
            record[
                "failure_reasons"
            ]
        )

    def test_restored_territory_must_be_requested(self):
        record = module.make_record(
            requested_verified_territory=[
                "territory:a"
            ],
            restored_verified_territory=[
                "territory:a",
                "territory:b",
            ],
        )

        self.assertIn(
            "RESTORED_TERRITORY_OUTSIDE_REQUEST",
            record[
                "failure_reasons"
            ]
        )

    def test_restored_payload_must_be_requested(self):
        record = module.make_record(
            requested_payload=[
                "payload:a"
            ],
            mission_required_payload=[
                "payload:a"
            ],
            restored_payload=[
                "payload:a",
                "payload:b",
            ],
        )

        self.assertIn(
            "RESTORED_PAYLOAD_OUTSIDE_REQUEST",
            record[
                "failure_reasons"
            ]
        )

    def test_restored_payload_must_be_mission_required(self):
        record = module.make_record(
            requested_payload=[
                "payload:a",
                "payload:b",
            ],
            mission_required_payload=[
                "payload:a"
            ],
            restored_payload=[
                "payload:a",
                "payload:b",
            ],
        )

        self.assertIn(
            "RESTORED_PAYLOAD_OUTSIDE_MISSION_NEED",
            record[
                "failure_reasons"
            ]
        )

    def test_unnecessary_requested_payload_rejected(self):
        record = module.make_record(
            requested_payload=[
                "payload:a",
                "payload:b",
            ],
            mission_required_payload=[
                "payload:a"
            ],
            restored_payload=[
                "payload:a"
            ],
            retained_at_rest_payload=[
                "payload:b"
            ],
        )

        self.assertIn(
            "MISSION_NECESSITY_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_landing_partition_valid(self):
        record = module.make_record(
            operation_context="LANDING",
            pre_landing_active_payload=[
                "payload:a",
                "payload:b",
                "payload:c",
            ],
            landing_released_payload=[
                "payload:b",
                "payload:c",
            ],
            landing_retained_payload=[
                "payload:a"
            ],
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_landing_partition_overlap_rejected(self):
        record = module.make_record(
            operation_context="LANDING",
            pre_landing_active_payload=[
                "payload:a",
                "payload:b"
            ],
            landing_released_payload=[
                "payload:b"
            ],
            landing_retained_payload=[
                "payload:a",
                "payload:b",
            ],
        )

        self.assertIn(
            "LANDING_PAYLOAD_PARTITION_INVALID",
            record[
                "failure_reasons"
            ]
        )

    def test_landing_partition_loss_rejected(self):
        record = module.make_record(
            operation_context="LANDING",
            pre_landing_active_payload=[
                "payload:a",
                "payload:b",
                "payload:c",
            ],
            landing_released_payload=[
                "payload:b"
            ],
            landing_retained_payload=[
                "payload:a"
            ],
        )

        self.assertIn(
            "LANDING_PAYLOAD_PARTITION_INVALID",
            record[
                "failure_reasons"
            ]
        )

    def test_replay_bounded_hydration_valid(self):
        record = module.make_record(
            operation_context="REPLAY",
            requested_payload=[
                "payload:a"
            ],
            mission_required_payload=[
                "payload:a"
            ],
            restored_payload=[
                "payload:a"
            ],
            retained_at_rest_payload=[
                "payload:b",
                "payload:c",
            ],
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_bounded_revisit_does_not_require_prior_full_payload(self):
        record = module.make_record(
            operation_context="BOUNDED_REVISIT",
            requested_payload=[
                "payload:a"
            ],
            mission_required_payload=[
                "payload:a"
            ],
            restored_payload=[
                "payload:a"
            ],
            retained_at_rest_payload=[
                "payload:b",
                "payload:c",
                "payload:d",
            ],
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_blocked_payload_cannot_be_restored(self):
        record = module.make_record(
            requested_payload=[
                "payload:a"
            ],
            mission_required_payload=[
                "payload:a"
            ],
            restored_payload=[
                "payload:a"
            ],
            blocked_payload=[
                "payload:a"
            ],
            restriction_references=[
                "restriction:a"
            ],
        )

        self.assertIn(
            "RESTRICTION_BYPASSED",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_boundary_broadening_rejected(self):
        record = module.make_record(
            provenance_route=[
                "hydration-request:r6-h",
                "evidence-boundary:broadened",
            ],
        )

        self.assertIn(
            "EVIDENCE_BOUNDARY_BROADENED",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_ceiling_elevation_rejected(self):
        record = module.make_record(
            provenance_route=[
                "hydration-request:r6-h",
                "evidence-ceiling:elevated",
            ],
        )

        self.assertIn(
            "EVIDENCE_CEILING_ELEVATED",
            record[
                "failure_reasons"
            ]
        )

    def test_object_identity_replacement_rejected(self):
        record = module.make_record(
            object_identity_changed=True
        )

        self.assertIn(
            "OBJECT_IDENTITY_REPLACED",
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

    def test_occupancy_mutation_rejected(self):
        record = module.make_record(
            occupancy_mutated=True
        )

        self.assertIn(
            "OCCUPANCY_MUTATED",
            record[
                "failure_reasons"
            ]
        )

    def test_formation_mutation_rejected(self):
        record = module.make_record(
            formation_mutated=True
        )

        self.assertIn(
            "FORMATION_MUTATED",
            record[
                "failure_reasons"
            ]
        )

    def test_stick_required(self):
        record = module.make_record(
            stick_reference=None
        )

        self.assertIn(
            "STICK_NOT_PRESERVED",
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
