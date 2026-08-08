import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_collapse_boundary.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_collapse_boundary",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_boundary():
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "restriction_constriction_reference":
            "restriction:test",
        "source_representation_references": [
            "representation:test"
        ],
        "collapse_trigger":
            "evidence changed supported possibility geometry",
        "collapse_justification": [
            "prior possibility range no longer supportable"
        ],
        "governing_evidence_references": [
            "evidence:test"
        ],
        "pre_collapse_possibilities": [
            "A",
            "B",
            "C"
        ],
        "removed_possibilities": [
            "B"
        ],
        "retained_possibilities": [
            "A"
        ],
        "deferred_possibilities": [
            "C"
        ],
        "surviving_uncertainty": [
            "C remains unresolved"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "preserved_invariants": [
            "object identity",
            "provenance",
            "Stick"
        ],
        "newly_available_frontier": {
            "frontier": "next discriminating evidence"
        },
        "re_expansion_considerations": [
            "new evidence"
        ],
        "pre_collapse_state_reference":
            "state:pre:test",
        "return_route": {
            "reference": "state:pre:test"
        },
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "provenance_anchors": [
            "provenance:test"
        ],
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "restriction:test",
            "evidence:test"
        ],
        "collapsed_at":
            "2026-08-07T20:12:00-04:00",
    }

    record[
        "collapse_boundary_id"
    ] = module.compute_collapse_boundary_id(
        record
    )

    return record


class CollapseBoundaryTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_boundary(self):
        record = make_boundary()

        self.assertEqual(
            module.validate_boundary(
                record
            ),
            []
        )

    def test_partition_must_cover_all_prior_possibilities(self):
        record = make_boundary()

        record[
            "deferred_possibilities"
        ] = []

        record[
            "collapse_boundary_id"
        ] = module.compute_collapse_boundary_id(
            record
        )

        errors = module.validate_boundary(
            record
        )

        self.assertTrue(
            any(
                "exactly partition"
                in error
                for error in errors
            )
        )

    def test_dispositions_may_not_overlap(self):
        record = make_boundary()

        record[
            "removed_possibilities"
        ] = [
            "A",
            "B"
        ]

        record[
            "collapse_boundary_id"
        ] = module.compute_collapse_boundary_id(
            record
        )

        errors = module.validate_boundary(
            record
        )

        self.assertTrue(
            any(
                "both removed and retained"
                in error
                for error in errors
            )
        )

    def test_cannot_invent_possibility(self):
        record = make_boundary()

        record[
            "retained_possibilities"
        ] = [
            "A",
            "NEW"
        ]

        record[
            "collapse_boundary_id"
        ] = module.compute_collapse_boundary_id(
            record
        )

        errors = module.validate_boundary(
            record
        )

        self.assertTrue(
            any(
                "originate in pre-collapse set"
                in error
                for error in errors
            )
        )

    def test_surviving_uncertainty_is_required(self):
        record = make_boundary()

        record[
            "surviving_uncertainty"
        ] = []

        record[
            "collapse_boundary_id"
        ] = module.compute_collapse_boundary_id(
            record
        )

        errors = module.validate_boundary(
            record
        )

        self.assertTrue(
            any(
                "surviving_uncertainty"
                in error
                for error in errors
            )
        )

    def test_material_change_changes_identity(self):
        first = make_boundary()

        changed = dict(first)

        changed[
            "collapse_trigger"
        ] = "different evidence-driven trigger"

        changed[
            "collapse_boundary_id"
        ] = module.compute_collapse_boundary_id(
            changed
        )

        self.assertNotEqual(
            first[
                "collapse_boundary_id"
            ],
            changed[
                "collapse_boundary_id"
            ]
        )

    def test_schema_does_not_pull_downstream_semantics_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "landing_witness_id",
            "reflight_trigger_id",
            "closing_witness_id",
            "replay_envelope_id",
            "scar_record_id",
            "lifecycle_transition_id",
            "new_room_object_id",
            "canonical_promotion",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
