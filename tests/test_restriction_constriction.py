import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_restriction_constriction.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_restriction_constriction",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_record(
    operation="RESTRICTION"
):
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "operation_type":
            operation,
        "active_question":
            "which supported states remain?",
        "mission_reference":
            "mission:test",
        "representation_reference":
            "representation:test",
        "prior_operation_reference":
            None,
        "evidence_references": [
            "evidence:a"
        ],
        "further_evidence_references": [],
        "pre_supported_states": [
            "A",
            "B",
            "C"
        ],
        "post_supported_states": [
            "A",
            "B"
        ],
        "removed_from_support_states": [
            "C"
        ],
        "unresolved_states": [
            "A",
            "B"
        ],
        "operation_basis": [
            "evidence removes C from current support"
        ],
        "evidence_boundary": {
            "scope": "test"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "provenance_anchors": [
            "provenance:test"
        ],
        "representation_history_references": [
            "representation:test"
        ],
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "return_state_reference":
            "state:pre:test",
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "evidence:a",
            "stick:test"
        ],
        "operated_at":
            "2026-08-07T20:00:00-04:00",
    }

    if operation == "CONSTRICTION":
        record[
            "prior_operation_reference"
        ] = "restriction:test"

        record[
            "evidence_references"
        ] = [
            "evidence:a",
            "evidence:b"
        ]

        record[
            "further_evidence_references"
        ] = [
            "evidence:b"
        ]

        record[
            "pre_supported_states"
        ] = [
            "A",
            "B"
        ]

        record[
            "post_supported_states"
        ] = [
            "A"
        ]

        record[
            "removed_from_support_states"
        ] = [
            "B"
        ]

        record[
            "unresolved_states"
        ] = []

    record[
        "restriction_constriction_id"
    ] = module.compute_record_id(
        record
    )

    return record


class RestrictionConstrictionTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_restriction(self):
        record = make_record(
            "RESTRICTION"
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_valid_constriction(self):
        record = make_record(
            "CONSTRICTION"
        )

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_post_states_must_be_subset(self):
        record = make_record()

        record[
            "post_supported_states"
        ] = [
            "A",
            "NEW"
        ]

        record[
            "removed_from_support_states"
        ] = [
            "B",
            "C"
        ]

        record[
            "restriction_constriction_id"
        ] = module.compute_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "subset of pre-supported"
                in error
                for error in errors
            )
        )

    def test_removed_must_come_from_pre_set(self):
        record = make_record()

        record[
            "removed_from_support_states"
        ] = [
            "C",
            "NEVER_SUPPORTED"
        ]

        record[
            "restriction_constriction_id"
        ] = module.compute_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "originate in pre-supported"
                in error
                for error in errors
            )
        )

    def test_state_cannot_be_retained_and_removed(self):
        record = make_record()

        record[
            "removed_from_support_states"
        ] = [
            "B",
            "C"
        ]

        record[
            "restriction_constriction_id"
        ] = module.compute_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "both post-supported and removed"
                in error
                for error in errors
            )
        )

    def test_constriction_requires_further_evidence(self):
        record = make_record(
            "CONSTRICTION"
        )

        record[
            "further_evidence_references"
        ] = []

        record[
            "restriction_constriction_id"
        ] = module.compute_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requires further evidence"
                in error
                for error in errors
            )
        )

    def test_constriction_requires_prior_operation(self):
        record = make_record(
            "CONSTRICTION"
        )

        record[
            "prior_operation_reference"
        ] = None

        record[
            "restriction_constriction_id"
        ] = module.compute_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "requires prior operation reference"
                in error
                for error in errors
            )
        )

    def test_operation_must_reduce_state_set(self):
        record = make_record()

        record[
            "post_supported_states"
        ] = [
            "A",
            "B",
            "C"
        ]

        record[
            "removed_from_support_states"
        ] = []

        record[
            "restriction_constriction_id"
        ] = module.compute_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "must reduce the supported-state set"
                in error
                for error in errors
            )
        )

    def test_material_state_change_changes_identity(self):
        first = make_record()

        changed = dict(
            first
        )

        changed[
            "post_supported_states"
        ] = [
            "A"
        ]

        changed[
            "removed_from_support_states"
        ] = [
            "B",
            "C"
        ]

        changed[
            "restriction_constriction_id"
        ] = module.compute_record_id(
            changed
        )

        self.assertNotEqual(
            first[
                "restriction_constriction_id"
            ],
            changed[
                "restriction_constriction_id"
            ]
        )

    def test_schema_does_not_pull_collapse_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "collapse_boundary_id",
            "landing_witness_id",
            "reflight_trigger_id",
            "closing_witness_id",
            "replay_envelope_id",
            "scar_record_id",
            "lifecycle_transition_id",
            "formation_selection_id",
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
