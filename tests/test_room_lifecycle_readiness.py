import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_room_lifecycle_readiness.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_room_lifecycle_readiness",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_transition(
    source="QUALIFYING",
    target="QUALIFIED",
    disposition="QUALIFIED"
):
    object_id = (
        "sha512:"
        + "5" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "source_state":
            source,
        "target_state":
            target,
        "qualification_request_reference":
            "request:test",
        "qualification_record_reference":
            "record:test",
        "qualification_disposition":
            disposition,
        "declared_mission":
            "bounded mission",
        "evidence_ceiling":
            "CEILING:TEST",
        "readiness_requirements":
            [],
        "unresolved_readiness_blockers":
            [],
        "transition_basis": [
            "test transition basis"
        ],
        "registry_reference":
            "registry:test",
        "audit_reference":
            "audit:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "record:test",
        ],
        "transitioned_at":
            "2026-08-07T19:22:00-04:00",
    }

    if (
        source == "QUALIFIED"
        and target == "READY"
    ):
        record[
            "readiness_requirements"
        ] = [
            "qualification integrity verified"
        ]

    record[
        "lifecycle_transition_id"
    ] = module.compute_lifecycle_transition_id(
        record
    )

    return record


class RoomLifecycleReadinessTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_qualifying_to_qualified(self):
        record = make_transition()

        self.assertEqual(
            module.validate_transition(
                record
            ),
            []
        )

    def test_qualified_to_ready(self):
        record = make_transition(
            source="QUALIFIED",
            target="READY",
            disposition="QUALIFIED"
        )

        self.assertEqual(
            module.validate_transition(
                record
            ),
            []
        )

    def test_provisional_maps_to_provisional(self):
        record = make_transition(
            source="QUALIFYING",
            target="PROVISIONAL",
            disposition="PROVISIONAL"
        )

        self.assertEqual(
            module.validate_transition(
                record
            ),
            []
        )

    def test_rejected_maps_to_rejected(self):
        record = make_transition(
            source="QUALIFYING",
            target="REJECTED",
            disposition="REJECTED"
        )

        self.assertEqual(
            module.validate_transition(
                record
            ),
            []
        )

    def test_degraded_maps_to_degraded(self):
        record = make_transition(
            source="QUALIFYING",
            target="DEGRADED",
            disposition="DEGRADED"
        )

        self.assertEqual(
            module.validate_transition(
                record
            ),
            []
        )

    def test_wrong_disposition_cannot_create_qualified(self):
        record = make_transition(
            source="QUALIFYING",
            target="QUALIFIED",
            disposition="PROVISIONAL"
        )

        errors = module.validate_transition(
            record
        )

        self.assertTrue(
            any(
                "does not support target lifecycle state"
                in error
                for error in errors
            )
        )

    def test_ready_rejects_blockers(self):
        record = make_transition(
            source="QUALIFIED",
            target="READY",
            disposition="QUALIFIED"
        )

        record[
            "unresolved_readiness_blockers"
        ] = [
            "transition integrity unresolved"
        ]

        record[
            "lifecycle_transition_id"
        ] = module.compute_lifecycle_transition_id(
            record
        )

        errors = module.validate_transition(
            record
        )

        self.assertTrue(
            any(
                "unresolved readiness blockers"
                in error
                for error in errors
            )
        )

    def test_active_is_not_in_r3c_transition_surface(self):
        record = make_transition(
            source="READY",
            target="ACTIVE",
            disposition="QUALIFIED"
        )

        errors = module.validate_transition(
            record
        )

        self.assertTrue(
            any(
                "outside R3-C transition surface"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_pull_occupation_or_runtime_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        properties = set(
            schema["properties"]
        )

        for field in {
            "occupancy_witness_id",
            "occupant_id",
            "selected_formation",
            "formation_selection_id",
            "capability_mission_id",
            "landing_witness_id",
            "reflight_trigger_id",
            "closing_witness_id",
            "replay_envelope_id",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
