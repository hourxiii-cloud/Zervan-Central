import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_raven_human_gate_publication_action_boundary.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_raven_human_gate_publication_action_boundary",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_record():
    record = {
        "schema_version":
            "1.0",
        "raven_representation_id":
            "sha512:" + "1" * 128,
        "mc_evaluation_id":
            "sha512:" + "2" * 128,
        "ccr_id":
            "sha512:" + "3" * 128,
        "object_id":
            "sha512:" + "4" * 128,
        "room_revision_id":
            "revision:test",
        "room_state_root":
            "sha512:" + "5" * 128,
        "authorized_view_root":
            "sha512:" + "6" * 128,
        "evidence_boundary_reference":
            "boundary:test",
        "evidence_ceiling_reference":
            "ceiling:test",
        "coordinate_reference":
            "coordinate:test",
        "transition_class":
            "PUBLICATION",
        "transition_target":
            "report:test",
        "requested_scope":
            "publish exact report:test representation",
        "mc_admissibility_references": [
            "mc:test"
        ],
        "governance_constraint_references": [
            "governance:test"
        ],
        "human_decision_reference":
            None,
        "decision_state":
            "PENDING",
        "decision_reasons": [],
        "lineage_reference":
            "lineage:test",
        "provenance_route": [
            "sha512:" + "4" * 128,
            "sha512:" + "3" * 128,
            "sha512:" + "2" * 128,
            "sha512:" + "1" * 128
        ],
        "authority_state":
            "NONE",
        "human_gate_state":
            "ACTIVE",
        "decision_time_reference":
            None,
    }

    record[
        "human_gate_decision_id"
    ] = module.compute_human_gate_decision_id(
        record
    )

    return record


class RavenHumanGatePublicationActionBoundaryTests(
    unittest.TestCase
):

    def test_valid_pending_request(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_raven_representation_required(self):
        record = make_record()

        record[
            "raven_representation_id"
        ] = ""

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "raven_representation_id"
                in error
                for error in errors
            )
        )

    def test_unknown_transition_rejected(self):
        record = make_record()

        record[
            "transition_class"
        ] = "UNKNOWN"

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "unknown Human Gate transition class"
                in error
                for error in errors
            )
        )

    def test_approval_requires_human_reference(self):
        record = make_record()

        record[
            "decision_state"
        ] = "APPROVED"

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "APPROVED requires human_decision_reference"
                in error
                for error in errors
            )
        )

    def test_approval_requires_time_reference(self):
        record = make_record()

        record[
            "decision_state"
        ] = "APPROVED"

        record[
            "human_decision_reference"
        ] = "human:test"

        record[
            "decision_time_reference"
        ] = None

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "APPROVED requires decision_time_reference"
                in error
                for error in errors
            )
        )

    def test_valid_approval(self):
        record = make_record()

        record[
            "decision_state"
        ] = "APPROVED"

        record[
            "human_decision_reference"
        ] = "human:test"

        record[
            "decision_time_reference"
        ] = "decision-time:test"

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            record
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_denial_requires_reason(self):
        record = make_record()

        record[
            "decision_state"
        ] = "DENIED"

        record[
            "human_decision_reference"
        ] = "human:test"

        record[
            "decision_time_reference"
        ] = "decision-time:test"

        record[
            "decision_reasons"
        ] = []

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "DENIED requires decision reasons"
                in error
                for error in errors
            )
        )

    def test_transition_target_required(self):
        record = make_record()

        record[
            "transition_target"
        ] = ""

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "transition_target"
                in error
                for error in errors
            )
        )

    def test_scope_required(self):
        record = make_record()

        record[
            "requested_scope"
        ] = ""

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requested_scope"
                in error
                for error in errors
            )
        )

    def test_zervan_authority_remains_none(self):
        record = make_record()

        record[
            "authority_state"
        ] = "AUTONOMOUS"

        record[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
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

    def test_material_change_changes_decision_identity(self):
        first = make_record()
        second = make_record()

        second[
            "transition_target"
        ] = "report:different"

        second[
            "human_gate_decision_id"
        ] = module.compute_human_gate_decision_id(
            second
        )

        self.assertNotEqual(
            first[
                "human_gate_decision_id"
            ],
            second[
                "human_gate_decision_id"
            ]
        )

    def test_schema_does_not_absorb_execution(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "execution_result",
            "publication_result",
            "external_side_effect",
            "room_lifecycle_transition",
            "evidence_boundary_override",
            "evidence_ceiling_override",
            "mc_disposition_override",
            "canonical_truth",
            "system_authority",
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
