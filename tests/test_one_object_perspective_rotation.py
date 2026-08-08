import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_one_object_perspective_rotation.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_one_object_perspective_rotation",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class OneObjectPerspectiveRotationTests(
    unittest.TestCase
):

    def test_valid_rotation(self):
        record = module.make_valid_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_requires_three_perspectives(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ] = record[
            "perspectives"
        ][:2]

        record[
            "stick_transitions"
        ] = record[
            "stick_transitions"
        ][:1]

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "at least three perspectives"
                in error
                for error in errors
            )
        )

    def test_object_identity_drift_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][1][
            "object_id"
        ] = (
            "sha512:"
            + "9" * 128
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "changed canonical object identity"
                in error
                for error in errors
            )
        )

    def test_revision_drift_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][1][
            "room_revision_id"
        ] = "revision:different"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "changed Room revision"
                in error
                for error in errors
            )
        )

    def test_state_root_drift_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][2][
            "room_state_root"
        ] = (
            "sha512:"
            + "8" * 128
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "changed Room state root"
                in error
                for error in errors
            )
        )

    def test_authorized_views_may_differ(self):
        record = module.make_valid_record()

        roots = {
            perspective[
                "authorized_view_root"
            ]
            for perspective in record[
                "perspectives"
            ]
        }

        self.assertGreater(
            len(roots),
            1
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_evidence_boundary_drift_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][1][
            "evidence_boundary_reference"
        ] = "boundary:expanded"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "changed evidence boundary"
                in error
                for error in errors
            )
        )

    def test_evidence_ceiling_drift_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][1][
            "evidence_ceiling_reference"
        ] = "ceiling:higher"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "changed evidence ceiling"
                in error
                for error in errors
            )
        )

    def test_provenance_loss_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][1][
            "provenance_anchors"
        ] = [
            "provenance:origin:a"
        ]

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "lost provenance"
                in error
                for error in errors
            )
        )

    def test_exclusion_loss_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][1][
            "exclusion_references"
        ] = []

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "lost governing exclusions"
                in error
                for error in errors
            )
        )

    def test_disagreement_erasure_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][2][
            "disagreement_references"
        ] = []

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "erased disagreement"
                in error
                for error in errors
            )
        )

    def test_duplicate_perspective_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][2][
            "perspective_id"
        ] = record[
            "perspectives"
        ][1][
            "perspective_id"
        ]

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "perspective_id must be unique"
                in error
                for error in errors
            )
        )

    def test_missing_transform_rejected(self):
        record = module.make_valid_record()

        record[
            "perspectives"
        ][1][
            "representation_transform_reference"
        ] = ""

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "representation_transform_reference"
                in error
                for error in errors
            )
        )

    def test_stick_object_drift_rejected(self):
        record = module.make_valid_record()

        record[
            "stick_transitions"
        ][0][
            "destination_object_id"
        ] = (
            "sha512:"
            + "9" * 128
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "Stick transition does not preserve object identity"
                in error
                for error in errors
            )
        )

    def test_stick_order_rejected(self):
        record = module.make_valid_record()

        record[
            "stick_transitions"
        ][0][
            "destination_perspective_id"
        ] = "perspective:3"

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "Stick transition ordering"
                in error
                for error in errors
            )
        )

    def test_branch_semantics_rejected(self):
        record = module.make_valid_record()

        record[
            "branch_references"
        ] = [
            "branch:should-not-exist"
        ]

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "may not create branch semantics"
                in error
                for error in errors
            )
        )

    def test_passageway_semantics_rejected(self):
        record = module.make_valid_record()

        record[
            "passageway_references"
        ] = [
            "passageway:should-not-exist"
        ]

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "may not create Passageway semantics"
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

    def test_schema_does_not_create_branch_or_authority(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "branch_id",
            "new_room_id",
            "passageway_id",
            "genesis_manifest",
            "lifecycle_transition",
            "evidence_admission",
            "claim_ceiling_override",
            "execution_authorization",
            "canonical_promotion",
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
