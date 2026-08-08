import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_closing_witness.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_closing_witness",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_witness(
    disposition="CLOSED"
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
        "landing_witness_reference":
            "landing:test",
        "convergence_state_reference":
            "convergence:test",
        "closure_basis": [
            "bounded analytical movement converged"
        ],
        "preserved_question":
            "what remains supportable?",
        "representation_reference":
            "representation:test",
        "zone_reference":
            "zone:test",
        "space_reference":
            "space:test",
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "unresolved_terrain_references": [
            "terrain:unresolved:test"
        ],
        "restriction_constriction_references": [
            "restriction:test"
        ],
        "collapse_boundary_references": [
            "collapse:test"
        ],
        "reflight_trigger_references": [],
        "outstanding_analytical_obligations": [],
        "preserved_lineage_reference":
            "lineage:test",
        "replay_coordinates": {
            "coordinate": "observational:test"
        },
        "return_coordinates": {
            "coordinate": "return:test"
        },
        "current_rendering_reference":
            "rendering:test",
        "closure_disposition":
            disposition,
        "blocking_reasons": [],
        "audit_witness_reference":
            "audit:test",
        "registry_reference":
            "registry:test",
        "governance_reference":
            "governance:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "landing:test",
            "lineage:test",
            "stick:test"
        ],
        "closed_at":
            "2026-08-07T20:33:00-04:00",
    }

    if disposition == "BLOCKED":
        record[
            "outstanding_analytical_obligations"
        ] = [
            "active obligation"
        ]

        record[
            "blocking_reasons"
        ] = [
            "active obligation blocks closure"
        ]

        record[
            "audit_witness_reference"
        ] = None

    record[
        "closing_witness_id"
    ] = module.compute_closing_witness_id(
        record
    )

    return record


class ClosingWitnessTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_closed_witness(self):
        record = make_witness(
            "CLOSED"
        )

        self.assertEqual(
            module.validate_witness(
                record
            ),
            []
        )

    def test_valid_blocked_witness(self):
        record = make_witness(
            "BLOCKED"
        )

        self.assertEqual(
            module.validate_witness(
                record
            ),
            []
        )

    def test_closed_cannot_have_active_obligation(self):
        record = make_witness(
            "CLOSED"
        )

        record[
            "outstanding_analytical_obligations"
        ] = [
            "active obligation"
        ]

        record[
            "closing_witness_id"
        ] = module.compute_closing_witness_id(
            record
        )

        errors = module.validate_witness(
            record
        )

        self.assertTrue(
            any(
                "active outstanding analytical obligations"
                in error
                for error in errors
            )
        )

    def test_closed_requires_audit_witness(self):
        record = make_witness(
            "CLOSED"
        )

        record[
            "audit_witness_reference"
        ] = None

        record[
            "closing_witness_id"
        ] = module.compute_closing_witness_id(
            record
        )

        errors = module.validate_witness(
            record
        )

        self.assertTrue(
            any(
                "requires Audit witness reference"
                in error
                for error in errors
            )
        )

    def test_blocked_requires_reason(self):
        record = make_witness(
            "BLOCKED"
        )

        record[
            "blocking_reasons"
        ] = []

        record[
            "closing_witness_id"
        ] = module.compute_closing_witness_id(
            record
        )

        errors = module.validate_witness(
            record
        )

        self.assertTrue(
            any(
                "requires blocking reasons"
                in error
                for error in errors
            )
        )

    def test_unresolved_terrain_does_not_block_closed(self):
        record = make_witness(
            "CLOSED"
        )

        self.assertTrue(
            record[
                "unresolved_terrain_references"
            ]
        )

        self.assertEqual(
            module.validate_witness(
                record
            ),
            []
        )

    def test_material_coordinate_change_changes_identity(self):
        first = make_witness()

        changed = dict(
            first
        )

        changed[
            "replay_coordinates"
        ] = {
            "coordinate": "different"
        }

        changed[
            "closing_witness_id"
        ] = module.compute_closing_witness_id(
            changed
        )

        self.assertNotEqual(
            first[
                "closing_witness_id"
            ],
            changed[
                "closing_witness_id"
            ]
        )

    def test_schema_does_not_pull_replay_or_lifecycle_mutation_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "lifecycle_transition_id",
            "sealed_state_mutation",
            "reopened_state_mutation",
            "replay_envelope_id",
            "scar_record_id",
            "publication_authorization",
            "canonical_promotion",
            "reflight_execution_id",
            "rendering_contract_id",
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
