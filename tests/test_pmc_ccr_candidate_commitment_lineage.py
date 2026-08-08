import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_pmc_ccr_candidate_commitment_lineage.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_pmc_ccr_candidate_commitment_lineage",
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

    intake_id = (
        "sha512:"
        + "7" * 128
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
        "pmc_intake_binding_id":
            intake_id,
        "pmc_run_id":
            "pmc:test",
        "pmc_output_reference":
            "pmc-output:test",
        "selected_world_id":
            "world:a",
        "candidate_ordering": [
            "world:a",
            "world:b"
        ],
        "rejection_references": [
            "rejection:world:b"
        ],
        "evidence_references": [
            "evidence:test"
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
        "uncertainty_references": [
            "uncertainty:test"
        ],
        "unresolved_state_references": [
            "unknown:test"
        ],
        "invariants_checked_references": [
            "invariant:test"
        ],
        "replay_reference":
            "replay:test",
        "lineage_reference":
            "lineage:test",
        "provenance_route": [
            object_id,
            intake_id,
            "pmc:test",
            "world:a"
        ],
        "commitment_disposition":
            "CANDIDATE_RECORDED",
        "blocking_reasons": [],
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
    }

    record[
        "ccr_id"
    ] = module.compute_ccr_id(
        record
    )

    return record


class PMCCCRCandidateCommitmentLineageTests(
    unittest.TestCase
):

    def test_valid_ccr(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_selected_world_must_exist_in_ordering(self):
        record = make_record()

        record[
            "selected_world_id"
        ] = "world:missing"

        record[
            "ccr_id"
        ] = module.compute_ccr_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "selected_world_id must appear"
                in error
                for error in errors
            )
        )

    def test_null_pmc_result_is_valid(self):
        record = make_record()

        record[
            "selected_world_id"
        ] = None

        record[
            "commitment_disposition"
        ] = "NULL_RECORDED"

        record[
            "ccr_id"
        ] = module.compute_ccr_id(
            record
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_null_cannot_be_candidate_recorded(self):
        record = make_record()

        record[
            "selected_world_id"
        ] = None

        record[
            "commitment_disposition"
        ] = "CANDIDATE_RECORDED"

        record[
            "ccr_id"
        ] = module.compute_ccr_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requires selected_world_id"
                in error
                for error in errors
            )
        )

    def test_room_identity_required(self):
        record = make_record()

        record[
            "object_id"
        ] = ""

        record[
            "ccr_id"
        ] = module.compute_ccr_id(
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

    def test_evidence_boundary_required(self):
        record = make_record()

        record[
            "evidence_boundary_reference"
        ] = ""

        record[
            "ccr_id"
        ] = module.compute_ccr_id(
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

    def test_replay_reference_required(self):
        record = make_record()

        record[
            "replay_reference"
        ] = ""

        record[
            "ccr_id"
        ] = module.compute_ccr_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "replay_reference"
                in error
                for error in errors
            )
        )

    def test_blocked_requires_reason(self):
        record = make_record()

        record[
            "commitment_disposition"
        ] = "BLOCKED"

        record[
            "blocking_reasons"
        ] = []

        record[
            "ccr_id"
        ] = module.compute_ccr_id(
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
            "ccr_id"
        ] = module.compute_ccr_id(
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
            "candidate_ordering"
        ] = [
            "world:b",
            "world:a"
        ]

        second[
            "ccr_id"
        ] = module.compute_ccr_id(
            second
        )

        self.assertNotEqual(
            first[
                "ccr_id"
            ],
            second[
                "ccr_id"
            ]
        )

    def test_schema_does_not_absorb_mc_or_downstream(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "mc_admissibility",
            "admissible_response_classes",
            "raven_report",
            "human_gate_decision",
            "execution_authorization",
            "publication_authorization",
            "canonical_promotion",
            "room_lifecycle_transition",
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
