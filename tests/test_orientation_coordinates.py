import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_orientation_coordinates.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_orientation_coordinates",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_orientation(
    state="RESOLVED"
):
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "object_id":
            object_id,
        "origin_reference":
            "origin:a",
        "zone_id":
            "sha512:" + "5" * 128,
        "territory_reference":
            "territory:a",
        "space_id":
            "sha512:" + "6" * 128,
        "representation_transform_reference":
            "transform:a",
        "perspective_or_discipline":
            "Audit",
        "time_constraint": {
            "start": "2026-08-01",
            "end": "2026-08-07",
        },
        "evidence_constraints": [
            "restricted:evidence-b"
        ],
        "active_question":
            "what changed?",
        "active_mission":
            "bounded analysis",
        "evidence_boundary": {
            "included": [
                "evidence:a"
            ],
            "excluded": [
                "evidence:b"
            ],
        },
        "evidence_ceiling":
            "CEILING:A",
        "current_coordinates": {
            "representation":
                "audit",
            "position":
                "current",
        },
        "return_coordinates": {
            "representation":
                "origin",
            "position":
                "return",
        },
        "resolution_state":
            state,
        "provenance_route": [
            object_id,
            "origin:a",
        ],
    }

    record["orientation_id"] = (
        module.compute_orientation_id(
            record["object_id"],
            record["origin_reference"],
            record["zone_id"],
            record["territory_reference"],
            record["space_id"],
            record["representation_transform_reference"],
            record["perspective_or_discipline"],
            record["time_constraint"],
            record["evidence_constraints"],
            record["active_question"],
            record["active_mission"],
            record["evidence_boundary"],
            record["evidence_ceiling"],
            record["current_coordinates"],
            record["return_coordinates"],
            record["resolution_state"],
            record["provenance_route"],
        )
    )

    return record


class OrientationCoordinatesTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_resolved_orientation(self):
        record = make_orientation()

        self.assertEqual(
            module.validate_orientation(
                record
            ),
            []
        )

    def test_orientation_id_is_deterministic(self):
        record = make_orientation()

        second = module.compute_orientation_id(
            record["object_id"],
            record["origin_reference"],
            record["zone_id"],
            record["territory_reference"],
            record["space_id"],
            record["representation_transform_reference"],
            record["perspective_or_discipline"],
            {
                "end": "2026-08-07",
                "start": "2026-08-01",
            },
            record["evidence_constraints"],
            record["active_question"],
            record["active_mission"],
            record["evidence_boundary"],
            record["evidence_ceiling"],
            record["current_coordinates"],
            record["return_coordinates"],
            record["resolution_state"],
            record["provenance_route"],
        )

        self.assertEqual(
            record["orientation_id"],
            second
        )

    def test_coordinate_change_changes_orientation(self):
        record = make_orientation()

        changed = module.compute_orientation_id(
            record["object_id"],
            record["origin_reference"],
            record["zone_id"],
            record["territory_reference"],
            record["space_id"],
            record["representation_transform_reference"],
            record["perspective_or_discipline"],
            record["time_constraint"],
            record["evidence_constraints"],
            record["active_question"],
            record["active_mission"],
            record["evidence_boundary"],
            record["evidence_ceiling"],
            {
                "representation": "audit",
                "position": "moved",
            },
            record["return_coordinates"],
            record["resolution_state"],
            record["provenance_route"],
        )

        self.assertNotEqual(
            record["orientation_id"],
            changed
        )

    def test_orientation_id_does_not_replace_object_id(self):
        record = make_orientation()

        self.assertNotEqual(
            record["orientation_id"],
            record["object_id"]
        )

    def test_resolved_requires_question(self):
        record = make_orientation()

        record["active_question"] = None

        errors = module.validate_orientation(
            record
        )

        self.assertTrue(
            any(
                "requires active question"
                in error
                for error in errors
            )
        )

    def test_resolved_requires_mission(self):
        record = make_orientation()

        record["active_mission"] = None

        errors = module.validate_orientation(
            record
        )

        self.assertTrue(
            any(
                "requires active mission"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_pull_cartography_or_occupation_forward(self):
        schema = module.load_schema()

        properties = set(
            schema["properties"]
        )

        for field in {
            "cartography_id",
            "stick_id",
            "passageway_id",
            "occupation_id",
            "capability_position",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
