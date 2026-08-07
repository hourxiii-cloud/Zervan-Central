import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_occupancy_witness.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_occupancy_witness",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_witness(
    event="ENTERED"
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
        "occupant_capability":
            "Goblin:test",
        "occupancy_event":
            event,
        "lifecycle_readiness_reference":
            "lifecycle:ready:test",
        "qualification_record_reference":
            "qualification:record:test",
        "occupied_zone_id":
            "sha512:" + "5" * 128,
        "occupied_space_id":
            "sha512:" + "6" * 128,
        "orientation_reference":
            "orientation:test",
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "entry_authorization_reference":
            "authorization:test",
        "governance_constraint_reference":
            "governance:test",
        "human_gate_reference":
            "human-gate:test",
        "evidence_boundary": {
            "included": [
                "evidence:test"
            ]
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "current_coordinates": {
            "position": "test"
        },
        "return_coordinates": {
            "position": "return"
        },
        "occupancy_basis": [
            "Room lifecycle READY",
            "entry authorized",
        ],
        "provenance_route": [
            object_id,
            "lifecycle:ready:test",
        ],
        "witnessed_at":
            "2026-08-07T19:25:00-04:00",
    }

    record[
        "occupancy_witness_id"
    ] = module.compute_occupancy_witness_id(
        record
    )

    return record


class OccupancyWitnessTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_entered_witness(self):
        record = make_witness()

        self.assertEqual(
            module.validate_witness(
                record
            ),
            []
        )

    def test_all_witness_events_validate(self):
        for event in (
            "ENTERED",
            "PRESENT",
            "EXITED",
        ):
            record = make_witness(
                event
            )

            self.assertEqual(
                module.validate_witness(
                    record
                ),
                []
            )

    def test_witness_identity_is_deterministic(self):
        record = make_witness()

        self.assertEqual(
            record["occupancy_witness_id"],
            module.compute_occupancy_witness_id(
                record
            )
        )

    def test_event_change_changes_witness_identity(self):
        record = make_witness()

        changed = dict(
            record
        )

        changed[
            "occupancy_event"
        ] = "PRESENT"

        changed[
            "occupancy_witness_id"
        ] = module.compute_occupancy_witness_id(
            changed
        )

        self.assertNotEqual(
            record["occupancy_witness_id"],
            changed["occupancy_witness_id"]
        )

    def test_witness_id_does_not_replace_object_id(self):
        record = make_witness()

        self.assertNotEqual(
            record["occupancy_witness_id"],
            record["object_id"]
        )

    def test_entry_authorization_is_required(self):
        record = make_witness()

        record[
            "entry_authorization_reference"
        ] = None

        record[
            "occupancy_witness_id"
        ] = module.compute_occupancy_witness_id(
            record
        )

        errors = module.validate_witness(
            record
        )

        self.assertTrue(
            any(
                "entry_authorization_reference"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_pull_mission_or_runtime_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        properties = set(
            schema["properties"]
        )

        for field in {
            "capability_mission_id",
            "mission_request_id",
            "movement_state",
            "movement_vector",
            "formation_selection_id",
            "selected_formation",
            "goblin_signal_event_id",
            "active_lifecycle_transition_id",
            "landing_witness_id",
            "hydration_request_id",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
