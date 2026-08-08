import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_room_bound_evidence_pmc_intake.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_room_bound_evidence_pmc_intake",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_record():
    object_id = (
        "sha512:"
        + "4" * 128
    )

    state_root = (
        "sha512:"
        + "5" * 128
    )

    view_root = (
        "sha512:"
        + "6" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "room_revision_id":
            "revision:test",
        "room_state_root":
            state_root,
        "authorized_view_root":
            view_root,
        "evidence_references": [
            "evidence:test"
        ],
        "evidence_integrity_references": [
            "hash:test"
        ],
        "evidence_classes": [
            "STRUCTURAL"
        ],
        "evidence_boundary_reference":
            "boundary:test",
        "evidence_ceiling_reference":
            "ceiling:test",
        "coordinate_reference":
            "coordinate:test",
        "representation_reference":
            "representation:test",
        "transform_references": [
            "transform:test"
        ],
        "lineage_reference":
            "lineage:test",
        "unresolved_state_references": [
            "unknown:test"
        ],
        "qualification_reference":
            "qualification:test",
        "deterministic_parameter_references": [
            "parameters:test"
        ],
        "provenance_route": [
            object_id,
            "evidence:test",
            "boundary:test"
        ],
        "intake_disposition":
            "ADMISSIBLE",
        "blocking_reasons": [],
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "created_at":
            "2026-08-07T22:31:00-04:00",
    }

    record[
        "intake_binding_id"
    ] = module.compute_intake_binding_id(
        record
    )

    return record


class RoomBoundEvidencePMCIntakeTests(
    unittest.TestCase
):

    def test_valid_intake(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_room_identity_required(self):
        record = make_record()

        record[
            "object_id"
        ] = ""

        record[
            "intake_binding_id"
        ] = module.compute_intake_binding_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "object_id"
                in error
                for error in errors
            )
        )

    def test_authorized_view_required(self):
        record = make_record()

        record[
            "authorized_view_root"
        ] = ""

        record[
            "intake_binding_id"
        ] = module.compute_intake_binding_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "authorized_view_root"
                in error
                for error in errors
            )
        )

    def test_evidence_boundary_required(self):
        record = make_record()

        record[
            "evidence_boundary_reference"
        ] = ""

        record[
            "intake_binding_id"
        ] = module.compute_intake_binding_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "evidence_boundary_reference"
                in error
                for error in errors
            )
        )

    def test_claim_ceiling_required(self):
        record = make_record()

        record[
            "evidence_ceiling_reference"
        ] = ""

        record[
            "intake_binding_id"
        ] = module.compute_intake_binding_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "evidence_ceiling_reference"
                in error
                for error in errors
            )
        )

    def test_evidence_class_required(self):
        record = make_record()

        record[
            "evidence_classes"
        ] = []

        record[
            "intake_binding_id"
        ] = module.compute_intake_binding_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "evidence_classes"
                in error
                for error in errors
            )
        )

    def test_blocked_requires_reason(self):
        record = make_record()

        record[
            "intake_disposition"
        ] = "BLOCKED"

        record[
            "blocking_reasons"
        ] = []

        record[
            "intake_binding_id"
        ] = module.compute_intake_binding_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requires blocking reasons"
                in error
                for error in errors
            )
        )

    def test_authority_remains_none(self):
        record = make_record()

        record[
            "authority_state"
        ] = "WRITE"

        record[
            "intake_binding_id"
        ] = module.compute_intake_binding_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "authority_state must remain NONE"
                in error
                for error in errors
            )
        )

    def test_material_change_changes_identity(self):
        first = make_record()
        second = make_record()

        second[
            "coordinate_reference"
        ] = "coordinate:different"

        second[
            "intake_binding_id"
        ] = module.compute_intake_binding_id(
            second
        )

        self.assertNotEqual(
            first[
                "intake_binding_id"
            ],
            second[
                "intake_binding_id"
            ]
        )

    def test_schema_does_not_absorb_pmc_or_downstream(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "candidate_worlds",
            "selected_world_id",
            "pmc_collapse_result",
            "ccr_record",
            "mc_admissibility",
            "publication_authorization",
            "execution_authorization",
            "canonical_promotion",
            "room_lifecycle_transition",
            "full_payload",
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
