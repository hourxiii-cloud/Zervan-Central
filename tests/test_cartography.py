import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_cartography.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_cartography",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_cartography():
    object_id = (
        "sha512:"
        + "2" * 128
    )

    record = {
        "schema_version": "1.0",
        "object_id": object_id,
        "object_topology": {
            "nodes": ["room"],
            "edges": [],
        },
        "room_geometry": {
            "coordinate_system": "analytical",
        },
        "zone_references": [
            "zone:a"
        ],
        "transform_references": [
            "transform:a"
        ],
        "space_references": [
            "space:a"
        ],
        "orientation_references": [
            "orientation:a"
        ],
        "terrain_references": [
            "terrain:a"
        ],
        "territory_references": [
            "territory:a"
        ],
        "provenance_anchors": [
            "provenance:a"
        ],
        "evidence_boundaries": [
            {
                "reference": "boundary:a"
            }
        ],
        "evidence_ceilings": [
            "CEILING:A"
        ],
        "stable_regions": [
            {
                "reference": "stable:a"
            }
        ],
        "uncertainty_frontiers": [
            {
                "reference": "uncertainty:a"
            }
        ],
        "deformation_regions": [
            {
                "reference": "deformation:a"
            }
        ],
        "invariant_anchors": [
            object_id,
            "origin:a",
        ],
        "return_routes": [
            {
                "reference": "return:a"
            }
        ],
        "perspective_overlays": [
            {
                "reference": "overlay:a"
            }
        ],
        "evolution_references": [],
        "capability_position_references": [],
        "collapse_boundary_references": [],
        "passageway_references": [],
        "propagation_vector_references": [],
        "recorded_at":
            "2026-08-07T18:51:00-04:00",
    }

    record[
        "cartography_id"
    ] = module.compute_cartography_id(
        record
    )

    return record


class CartographyTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_cartography(self):
        record = make_cartography()

        self.assertEqual(
            module.validate_cartography(
                record
            ),
            []
        )

    def test_cartography_identity_is_deterministic(self):
        record = make_cartography()

        self.assertEqual(
            record["cartography_id"],
            module.compute_cartography_id(
                record
            )
        )

    def test_geometry_change_changes_cartography_id(self):
        record = make_cartography()

        changed = dict(
            record
        )

        changed[
            "room_geometry"
        ] = {
            "coordinate_system":
                "analytical",
            "region":
                "changed",
        }

        changed[
            "cartography_id"
        ] = module.compute_cartography_id(
            changed
        )

        self.assertNotEqual(
            record["cartography_id"],
            changed["cartography_id"]
        )

    def test_cartography_id_does_not_replace_object_id(self):
        record = make_cartography()

        self.assertNotEqual(
            record["cartography_id"],
            record["object_id"]
        )

    def test_downstream_objects_are_references_only(self):
        schema = module.load_schema()

        properties = set(
            schema["properties"]
        )

        for field in {
            "capability_position_references",
            "collapse_boundary_references",
            "passageway_references",
            "propagation_vector_references",
        }:
            self.assertIn(
                field,
                properties
            )

        for field in {
            "stick_id",
            "occupation_id",
            "occupant_id",
            "passageway_state",
            "passage_authorization",
            "collapse_operation",
        }:
            self.assertNotIn(
                field,
                properties
            )

    def test_uncertainty_and_deformation_are_preserved(self):
        record = make_cartography()

        self.assertTrue(
            record["uncertainty_frontiers"]
        )

        self.assertTrue(
            record["deformation_regions"]
        )


if __name__ == "__main__":
    unittest.main()
