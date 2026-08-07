import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_proportional_force.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_proportional_force",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_selection(
    profile="FAINT_LOCALIZED",
    complexity="NOT_PRIMARY",
    scale="SINGLE",
    capability_class="GOBLIN",
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
        "capability_mission_request_reference":
            "mission:test",
        "active_question":
            "what capability is minimally sufficient?",
        "unresolved_signal_profile":
            profile,
        "territory_complexity":
            complexity,
        "evidence_boundary": {
            "scope": "test"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "selection_basis": [
            "source baseline",
            "smallest justified force"
        ],
        "selected_scale":
            scale,
        "selected_capability_class":
            capability_class,
        "selected_capability_allocation":
            1,
        "alternatives_considered": [
            "larger capability"
        ],
        "rejected_larger_force_alternatives": [
            "not justified"
        ],
        "escalation_conditions": [
            "unresolved signal expands"
        ],
        "deescalation_conditions": [],
        "toc_reference":
            "toc:test",
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "provenance_route": [
            object_id,
            "mission:test"
        ],
        "selected_at":
            "2026-08-07T19:33:00-04:00",
    }

    if scale in {
        "TEAM",
        "PLATOON",
    }:
        record[
            "selection_basis"
        ] = [
            "source baseline",
            "smaller force is insufficient"
        ]

    record[
        "proportional_force_selection_id"
    ] = module.compute_selection_id(
        record
    )

    return record


class ProportionalForceTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_faint_localized_single_goblin(self):
        record = make_selection()

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_split_signal_intel(self):
        record = make_selection(
            profile="SPLIT_PLAUSIBLE_SOURCES",
            scale="SIGNAL_OR_INTEL",
            capability_class="INTEL_SQUAD",
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_split_signal_goblin_signal(self):
        record = make_selection(
            profile="SPLIT_PLAUSIBLE_SOURCES",
            scale="SIGNAL_OR_INTEL",
            capability_class="GOBLIN_SIGNAL",
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_distributed_scar_platoon(self):
        record = make_selection(
            profile="DISTRIBUTED_RECURSIVE_SCAR",
            complexity="LARGE_DISTRIBUTED",
            scale="PLATOON",
            capability_class="GOBLIN_PLATOON",
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_medium_room_team(self):
        record = make_selection(
            profile="ROOM_COMPLEXITY",
            complexity="MEDIUM",
            scale="TEAM",
            capability_class="GOBLIN_TEAM",
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_large_room_platoon(self):
        record = make_selection(
            profile="ROOM_COMPLEXITY",
            complexity="LARGE_DISTRIBUTED",
            scale="PLATOON",
            capability_class="GOBLIN_PLATOON",
        )

        self.assertEqual(
            module.validate_selection(
                record
            ),
            []
        )

    def test_scale_class_mismatch_fails(self):
        record = make_selection(
            scale="SINGLE",
            capability_class="GOBLIN_TEAM",
        )

        errors = module.validate_selection(
            record
        )

        self.assertTrue(
            any(
                "does not match selected scale"
                in error
                for error in errors
            )
        )

    def test_larger_force_requires_smaller_force_basis(self):
        record = make_selection(
            profile="OTHER_BOUNDED",
            scale="PLATOON",
            capability_class="GOBLIN_PLATOON",
        )

        record[
            "selection_basis"
        ] = [
            "Platoon available"
        ]

        record[
            "alternatives_considered"
        ] = []

        record[
            "proportional_force_selection_id"
        ] = module.compute_selection_id(
            record
        )

        errors = module.validate_selection(
            record
        )

        self.assertTrue(
            any(
                (
                    "alternatives considered"
                    in error
                    or "smaller force is insufficient"
                    in error
                )
                for error in errors
            )
        )

    def test_selection_identity_changes_with_force(self):
        first = make_selection()

        changed = dict(
            first
        )

        changed[
            "selected_scale"
        ] = "TEAM"

        changed[
            "selected_capability_class"
        ] = "GOBLIN_TEAM"

        changed[
            "selection_basis"
        ] = [
            "departure from source baseline because evidence expanded",
            "smaller force is insufficient"
        ]

        changed[
            "proportional_force_selection_id"
        ] = module.compute_selection_id(
            changed
        )

        self.assertNotEqual(
            first[
                "proportional_force_selection_id"
            ],
            changed[
                "proportional_force_selection_id"
            ]
        )

    def test_schema_does_not_pull_formation_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "formation_selection_id",
            "formation_type",
            "single_route",
            "stack_analysis",
            "expanded_analysis",
            "swarm",
            "goblin_signal_event_id",
            "active_lifecycle_transition_id",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
