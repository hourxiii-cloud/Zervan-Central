import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_replay_fidelity.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_replay_fidelity",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class ReplayFidelityTests(
    unittest.TestCase
):

    def test_exact_replay_valid(self):
        record = module.make_record()

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

        self.assertEqual(
            record[
                "replay_eligibility"
            ],
            "ELIGIBLE"
        )

    def test_object_identity_change_blocked(self):
        record = module.make_record(
            replay_object_id=(
                "sha512:"
                + "2" * 128
            )
        )

        self.assertIn(
            "OBJECT_IDENTITY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_closing_witness_required(self):
        record = module.make_record(
            closing_witness_reference=None
        )

        self.assertIn(
            "CLOSING_WITNESS_MISSING",
            record[
                "failure_reasons"
            ]
        )

    def test_lineage_change_blocked(self):
        record = module.make_record(
            replay_lineage_reference="lineage:new"
        )

        self.assertIn(
            "LINEAGE_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_question_substitution_blocked(self):
        record = module.make_record(
            replay_question_reference="question:current"
        )

        self.assertIn(
            "HISTORICAL_QUESTION_SUBSTITUTED",
            record[
                "failure_reasons"
            ]
        )

    def test_inquiry_substitution_blocked(self):
        record = module.make_record(
            replay_inquiry_envelope_reference="inquiry:current"
        )

        self.assertIn(
            "INQUIRY_ENVELOPE_SUBSTITUTED",
            record[
                "failure_reasons"
            ]
        )

    def test_coordinate_reconstruction_blocked(self):
        record = module.make_record(
            replay_observational_coordinate="coord:approximate"
        )

        self.assertIn(
            "OBSERVATIONAL_COORDINATE_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_zone_substitution_blocked(self):
        record = module.make_record(
            replay_zone_reference="zone:default"
        )

        self.assertIn(
            "ZONE_SUBSTITUTED",
            record[
                "failure_reasons"
            ]
        )

    def test_space_substitution_blocked(self):
        record = module.make_record(
            replay_space_reference="space:default"
        )

        self.assertIn(
            "SPACE_SUBSTITUTED",
            record[
                "failure_reasons"
            ]
        )

    def test_transform_history_change_blocked(self):
        record = module.make_record(
            replay_transform_references=[
                "transform:a"
            ]
        )

        self.assertIn(
            "TRANSFORM_HISTORY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_use_change_blocked(self):
        record = module.make_record(
            replay_evidence_used_references=[
                "evidence:a",
                "evidence:b",
                "evidence:new",
            ]
        )

        self.assertIn(
            "EVIDENCE_USED_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_capability_route_change_blocked(self):
        record = module.make_record(
            replay_capability_movement_references=[
                "movement:a"
            ]
        )

        self.assertIn(
            "CAPABILITY_MOVEMENT_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_boundary_change_blocked(self):
        record = module.make_record(
            replay_evidence_boundary_reference="boundary:wider"
        )

        self.assertIn(
            "EVIDENCE_BOUNDARY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_evidence_ceiling_change_blocked(self):
        record = module.make_record(
            replay_evidence_ceiling_reference="ceiling:higher"
        )

        self.assertIn(
            "EVIDENCE_CEILING_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_restriction_history_change_blocked(self):
        record = module.make_record(
            replay_restriction_references=[]
        )

        self.assertIn(
            "RESTRICTION_HISTORY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_collapse_history_change_blocked(self):
        record = module.make_record(
            replay_collapse_references=[]
        )

        self.assertIn(
            "COLLAPSE_HISTORY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_finding_history_change_blocked(self):
        record = module.make_record(
            replay_finding_references=[
                "finding:new"
            ]
        )

        self.assertIn(
            "FINDING_HISTORY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_missing_rendering_remains_missing(self):
        record = module.make_record(
            historical_rendering_reference=None,
            replay_rendering_reference=None,
        )

        self.assertEqual(
            record[
                "validation_disposition"
            ],
            "VALID"
        )

    def test_missing_rendering_cannot_be_synthesized(self):
        record = module.make_record(
            historical_rendering_reference=None,
            replay_rendering_reference="rendering:synthetic",
        )

        self.assertIn(
            "HISTORICAL_RENDERING_SUBSTITUTED",
            record[
                "failure_reasons"
            ]
        )

    def test_return_coordinate_change_blocked(self):
        record = module.make_record(
            replay_return_coordinate="coord:return:new"
        )

        self.assertIn(
            "RETURN_COORDINATE_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_cartography_change_blocked(self):
        record = module.make_record(
            replay_cartography_reference="cartography:new"
        )

        self.assertIn(
            "CARTOGRAPHY_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_stick_change_blocked(self):
        record = module.make_record(
            replay_stick_reference="stick:new"
        )

        self.assertIn(
            "STICK_CHANGED",
            record[
                "failure_reasons"
            ]
        )

    def test_approximate_reconstruction_blocked(self):
        record = module.make_record(
            approximate_reconstruction_used=True
        )

        self.assertIn(
            "APPROXIMATE_RECONSTRUCTION_USED",
            record[
                "failure_reasons"
            ]
        )

    def test_new_room_blocked(self):
        record = module.make_record(
            new_room_created=True
        )

        self.assertIn(
            "NEW_ROOM_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_branch_creation_blocked(self):
        record = module.make_record(
            branch_created=True
        )

        self.assertIn(
            "BRANCH_INVENTED",
            record[
                "failure_reasons"
            ]
        )

    def test_lifecycle_mutation_blocked(self):
        record = module.make_record(
            lifecycle_mutated=True
        )

        self.assertIn(
            "LIFECYCLE_MUTATED",
            record[
                "failure_reasons"
            ]
        )

    def test_reflight_execution_blocked(self):
        record = module.make_record(
            reflight_executed=True
        )

        self.assertIn(
            "REFLIGHT_EXECUTED",
            record[
                "failure_reasons"
            ]
        )

    def test_full_payload_hydration_blocked(self):
        record = module.make_record(
            full_payload_hydration_requested=True
        )

        self.assertIn(
            "FULL_PAYLOAD_HYDRATION_REQUESTED",
            record[
                "failure_reasons"
            ]
        )

    def test_authority_promotion_blocked(self):
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
