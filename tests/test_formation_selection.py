import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_formation_selection.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_formation_selection",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_selection(
    formation="SINGLE_ROUTE"
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
        "formation_type":
            formation,
        "capability_mission_request_references": [
            "mission:test"
        ],
        "proportional_force_selection_references": [
            "force:test"
        ],
        "occupancy_witness_references": [
            "occupancy:test"
        ],
        "active_questions": [
            "what is the bounded question?"
        ],
        "selected_capability_references": [
            "Goblin:test"
        ],
        "target_room_references": [
            object_id
        ],
        "zone_references": [
            "zone:test"
        ],
        "space_references": [
            "space:test"
        ],
        "representation_coordinate_references": [
            "orientation:test"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "independent_finding_policy":
            "preserve independent findings before correlation",
        "correlation_policy":
            "correlate attributable findings only",
        "integration_basis": [
            "bounded formation justification"
        ],
        "rejustification_triggers": [
            "terrain contact changes"
        ],
        "stick_reference":
            "stick:test",
        "toc_reference":
            "toc:test",
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "provenance_route": [
            object_id,
            "mission:test",
            "force:test"
        ],
        "selected_at":
            "2026-08-07T19:37:00-04:00",
    }

    if formation == "STACK_ANALYSIS":
        record[
            "selected_capability_references"
        ] = [
            "Goblin:a",
            "Goblin:b"
        ]

        record[
            "capability_mission_request_references"
        ] = [
            "mission:a",
            "mission:b"
        ]

        record[
            "occupancy_witness_references"
        ] = [
            "occupancy:a",
            "occupancy:b"
        ]

    if formation == "EXPANDED_ANALYSIS":
        record[
            "selected_capability_references"
        ] = [
            "Goblin:a",
            "Goblin:b"
        ]

        record[
            "space_references"
        ] = [
            "space:a",
            "space:b"
        ]

    if formation == "SWARM":
        record[
            "selected_capability_references"
        ] = [
            "Goblin:a",
            "Goblin:b",
            "Goblin:c"
        ]

        record[
            "occupancy_witness_references"
        ] = [
            "occupancy:a",
            "occupancy:b",
            "occupancy:c"
        ]

    record[
        "formation_selection_id"
    ] = module.compute_formation_selection_id(
        record
    )

    return record


class FormationSelectionTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_single_route(self):
        record = make_selection(
            "SINGLE_ROUTE"
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_stack(self):
        record = make_selection(
            "STACK_ANALYSIS"
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_expanded(self):
        record = make_selection(
            "EXPANDED_ANALYSIS"
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_swarm(self):
        record = make_selection(
            "SWARM"
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_single_route_requires_one_capability(self):
        record = make_selection(
            "SINGLE_ROUTE"
        )

        record[
            "selected_capability_references"
        ] = [
            "Goblin:a",
            "Goblin:b"
        ]

        record[
            "formation_selection_id"
        ] = module.compute_formation_selection_id(
            record
        )

        errors = module.validate_selection(
            record
        )

        self.assertTrue(
            any(
                "exactly one"
                in error
                for error in errors
            )
        )

    def test_stack_requires_same_room(self):
        record = make_selection(
            "STACK_ANALYSIS"
        )

        record[
            "target_room_references"
        ] = [
            record["object_id"],
            "sha512:" + "9" * 128
        ]

        record[
            "formation_selection_id"
        ] = module.compute_formation_selection_id(
            record
        )

        errors = module.validate_selection(
            record
        )

        self.assertTrue(
            any(
                "one canonical Room target"
                in error
                for error in errors
            )
        )

    def test_expanded_requires_expanded_surface(self):
        record = make_selection(
            "EXPANDED_ANALYSIS"
        )

        record[
            "space_references"
        ] = [
            "space:a"
        ]

        record[
            "active_questions"
        ] = [
            "question:a"
        ]

        record[
            "formation_selection_id"
        ] = module.compute_formation_selection_id(
            record
        )

        errors = module.validate_selection(
            record
        )

        self.assertTrue(
            any(
                "expanded bounded analytical surface"
                in error
                for error in errors
            )
        )

    def test_formation_change_changes_identity(self):
        first = make_selection(
            "SINGLE_ROUTE"
        )

        changed = make_selection(
            "STACK_ANALYSIS"
        )

        self.assertNotEqual(
            first[
                "formation_selection_id"
            ],
            changed[
                "formation_selection_id"
            ]
        )

    def test_schema_does_not_pull_downstream_semantics_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "goblin_signal_event_id",
            "active_lifecycle_transition_id",
            "hydration_request_id",
            "landing_witness_id",
            "closing_witness_id",
            "replay_envelope_id",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
