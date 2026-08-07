import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_capability_mission.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_capability_mission",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_mission():
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "occupancy_witness_reference":
            "occupancy:test",
        "active_question":
            "what evidence is needed next?",
        "mission_objective":
            "inspect bounded terrain",
        "mission_justification": [
            "unresolved signal"
        ],
        "target_zone_id":
            "sha512:" + "5" * 128,
        "target_space_id":
            "sha512:" + "6" * 128,
        "orientation_reference":
            "orientation:test",
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "territory_reference":
            "territory:test",
        "permitted_movement": {
            "scope": "reachable terrain"
        },
        "permitted_actions": [
            "observe"
        ],
        "prohibited_actions": [
            "canonical mutation"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "evidence_obligations": [
            "preserve provenance"
        ],
        "expected_return_obligations": [
            "bounded findings"
        ],
        "completion_conditions": [
            "question sufficiently improved or blocked"
        ],
        "governance_reference":
            "governance:test",
        "toc_coordination_reference":
            "toc:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "occupancy:test"
        ],
        "requested_at":
            "2026-08-07T19:28:00-04:00",
    }

    record[
        "capability_mission_request_id"
    ] = module.compute_mission_request_id(
        record
    )

    return record


def make_return(
    mission,
    completion="COMPLETED"
):
    record = {
        "schema_version":
            "1.0",
        "capability_mission_request_reference":
            mission[
                "capability_mission_request_id"
            ],
        "object_id":
            mission["object_id"],
        "occupancy_witness_reference":
            mission[
                "occupancy_witness_reference"
            ],
        "returning_capability":
            "Goblin:test",
        "bounded_findings": [
            "bounded finding"
        ],
        "evidence_references": [
            "evidence:test"
        ],
        "observed_effects": [],
        "unresolved_signals": [],
        "discriminating_evidence_needs": [],
        "cartographic_change_references": [],
        "restriction_findings": [],
        "continuity_state":
            "CONTINUOUS",
        "stick_reference":
            mission["stick_reference"],
        "final_coordinates": {
            "position": "final"
        },
        "return_coordinates": {
            "position": "return"
        },
        "completion_assessment":
            completion,
        "provenance_route": [
            mission["object_id"],
            mission[
                "capability_mission_request_id"
            ],
        ],
        "returned_at":
            "2026-08-07T19:28:00-04:00",
    }

    if completion == "BLOCKED":
        record[
            "restriction_findings"
        ] = [
            "surface inaccessible"
        ]

    record[
        "capability_return_id"
    ] = module.compute_capability_return_id(
        record
    )

    return record


class CapabilityMissionTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_mission(self):
        mission = make_mission()

        self.assertEqual(
            module.validate_mission_request(
                mission
            ),
            []
        )

    def test_valid_return(self):
        mission = make_mission()
        returned = make_return(
            mission
        )

        self.assertEqual(
            module.validate_capability_return(
                returned
            ),
            []
        )

    def test_all_completion_states(self):
        mission = make_mission()

        for state in (
            "COMPLETED",
            "PARTIAL",
            "BLOCKED",
        ):
            returned = make_return(
                mission,
                state
            )

            self.assertEqual(
                module.validate_capability_return(
                    returned
                ),
                []
            )

    def test_mission_identity_is_deterministic(self):
        mission = make_mission()

        self.assertEqual(
            mission[
                "capability_mission_request_id"
            ],
            module.compute_mission_request_id(
                mission
            )
        )

    def test_return_identity_is_deterministic(self):
        mission = make_mission()
        returned = make_return(
            mission
        )

        self.assertEqual(
            returned[
                "capability_return_id"
            ],
            module.compute_capability_return_id(
                returned
            )
        )

    def test_question_change_changes_mission_identity(self):
        mission = make_mission()

        changed = dict(
            mission
        )

        changed[
            "active_question"
        ] = "which evidence path is unresolved?"

        changed[
            "capability_mission_request_id"
        ] = module.compute_mission_request_id(
            changed
        )

        self.assertNotEqual(
            mission[
                "capability_mission_request_id"
            ],
            changed[
                "capability_mission_request_id"
            ]
        )

    def test_blocked_return_requires_blocking_basis(self):
        mission = make_mission()
        returned = make_return(
            mission,
            "BLOCKED"
        )

        returned[
            "restriction_findings"
        ] = []

        returned[
            "unresolved_signals"
        ] = []

        returned[
            "capability_return_id"
        ] = module.compute_capability_return_id(
            returned
        )

        errors = module.validate_capability_return(
            returned
        )

        self.assertTrue(
            any(
                "BLOCKED Capability Return"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_select_force_or_formation(self):
        mission_schema = module.load(
            module.MISSION_SCHEMA
        )

        return_schema = module.load(
            module.RETURN_SCHEMA
        )

        forbidden = {
            "selected_force",
            "force_scale",
            "selected_formation",
            "formation_selection_id",
            "goblin_signal_event_id",
            "active_lifecycle_transition_id",
            "landing_witness_id",
        }

        self.assertFalse(
            set(
                mission_schema[
                    "properties"
                ]
            )
            & forbidden
        )

        self.assertFalse(
            set(
                return_schema[
                    "properties"
                ]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
