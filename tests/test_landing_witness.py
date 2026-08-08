import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_landing_witness.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_landing_witness",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_witness():
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "occupant_capability":
            "Goblin:test",
        "occupancy_witness_reference":
            "occupancy:test",
        "mission_reference":
            "mission:test",
        "formation_reference":
            "formation:test",
        "zone_reference":
            "zone:test",
        "space_reference":
            "space:test",
        "orientation_reference":
            "orientation:test",
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "prior_question":
            "what remains unresolved?",
        "prior_rendering_reference":
            "rendering:test",
        "unresolved_terrain_references": [
            "terrain:unresolved:test"
        ],
        "readiness_reference":
            "readiness:test",
        "restriction_constriction_references": [
            "restriction:test"
        ],
        "collapse_boundary_references": [
            "collapse:test"
        ],
        "active_payload_before_landing": [
            "payload:a",
            "payload:b"
        ],
        "payload_released_at_landing": [
            "payload:b"
        ],
        "active_payload_retained_after_landing": [
            "payload:a"
        ],
        "current_coordinates": {
            "position": "landed:test"
        },
        "return_coordinates": {
            "position": "return:test"
        },
        "landing_basis": [
            "movement may cease while readiness is preserved"
        ],
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "occupancy:test",
            "stick:test"
        ],
        "landed_at":
            "2026-08-07T20:19:00-04:00",
    }

    record[
        "landing_witness_id"
    ] = module.compute_landing_witness_id(
        record
    )

    return record


class LandingWitnessTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_landing(self):
        record = make_witness()

        self.assertEqual(
            module.validate_witness(
                record
            ),
            []
        )

    def test_payload_sets_must_not_overlap(self):
        record = make_witness()

        record[
            "payload_released_at_landing"
        ] = [
            "payload:a",
            "payload:b"
        ]

        record[
            "landing_witness_id"
        ] = module.compute_landing_witness_id(
            record
        )

        errors = module.validate_witness(
            record
        )

        self.assertTrue(
            any(
                "both released and retained"
                in error
                for error in errors
            )
        )

    def test_payload_partition_must_be_complete(self):
        record = make_witness()

        record[
            "payload_released_at_landing"
        ] = []

        record[
            "landing_witness_id"
        ] = module.compute_landing_witness_id(
            record
        )

        errors = module.validate_witness(
            record
        )

        self.assertTrue(
            any(
                "exactly partition"
                in error
                for error in errors
            )
        )

    def test_cannot_retain_payload_not_previously_active(self):
        record = make_witness()

        record[
            "active_payload_retained_after_landing"
        ] = [
            "payload:a",
            "payload:new"
        ]

        record[
            "landing_witness_id"
        ] = module.compute_landing_witness_id(
            record
        )

        errors = module.validate_witness(
            record
        )

        self.assertTrue(
            any(
                "retained payload must originate"
                in error
                for error in errors
            )
        )

    def test_occupancy_witness_required(self):
        record = make_witness()

        record[
            "occupancy_witness_reference"
        ] = ""

        record[
            "landing_witness_id"
        ] = module.compute_landing_witness_id(
            record
        )

        errors = module.validate_witness(
            record
        )

        self.assertTrue(
            any(
                "occupancy_witness_reference"
                in error
                for error in errors
            )
        )

    def test_material_coordinate_change_changes_identity(self):
        first = make_witness()

        changed = dict(
            first
        )

        changed[
            "current_coordinates"
        ] = {
            "position": "different"
        }

        changed[
            "landing_witness_id"
        ] = module.compute_landing_witness_id(
            changed
        )

        self.assertNotEqual(
            first[
                "landing_witness_id"
            ],
            changed[
                "landing_witness_id"
            ]
        )

    def test_schema_does_not_pull_reflight_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "reflight_trigger_id",
            "closing_witness_id",
            "replay_envelope_id",
            "scar_record_id",
            "occupancy_exit",
            "new_room_object_id",
            "lifecycle_transition_id",
            "mission_completion",
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
