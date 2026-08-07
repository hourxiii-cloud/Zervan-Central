import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_terrain_territory.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_terrain_territory",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class TerrainTerritoryTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_terrain_identity_is_deterministic(self):
        object_id = (
            "sha512:"
            + "2" * 128
        )

        args = (
            object_id,
            "representation:a",
            "observation:a",
            {
                "records": ["a"],
                "fractures": ["f"],
            },
            "OBSERVED",
            "2026-08-07T18:30:00-04:00",
        )

        self.assertEqual(
            module.compute_terrain_record_id(
                *args
            ),
            module.compute_terrain_record_id(
                *args
            )
        )

    def test_representation_change_can_change_terrain_record(self):
        object_id = (
            "sha512:"
            + "3" * 128
        )

        first = module.compute_terrain_record_id(
            object_id,
            "representation:a",
            "observation:a",
            {"records": ["a"]},
            "OBSERVED",
            "2026-08-07T18:30:00-04:00"
        )

        second = module.compute_terrain_record_id(
            object_id,
            "representation:b",
            "observation:a",
            {"records": ["a"]},
            "OBSERVED",
            "2026-08-07T18:30:00-04:00"
        )

        self.assertNotEqual(
            first,
            second
        )

    def test_reachable_enters_active_territory(self):
        self.assertTrue(
            module.enters_active_territory(
                "REACHABLE"
            )
        )

    def test_unresolved_does_not_enter_active_territory(self):
        self.assertFalse(
            module.enters_active_territory(
                "UNRESOLVED"
            )
        )

    def test_unreachable_does_not_enter_active_territory(self):
        self.assertFalse(
            module.enters_active_territory(
                "UNREACHABLE"
            )
        )

    def test_terrain_and_territory_ids_are_distinct(self):
        object_id = (
            "sha512:"
            + "4" * 128
        )

        terrain = module.compute_terrain_record_id(
            object_id,
            "representation:a",
            "observation:a",
            {"records": ["a"]},
            "OBSERVED",
            "2026-08-07T18:30:00-04:00"
        )

        territory = module.compute_territory_record_id(
            object_id,
            [terrain],
            ["relationship:a"],
            ["surface:a"],
            [],
            [],
            "2026-08-07T18:31:00-04:00"
        )

        self.assertNotEqual(
            terrain,
            territory
        )

    def test_schemas_do_not_define_zone_or_space(self):
        terrain = module.load(
            module.TERRAIN_SCHEMA
        )

        territory = module.load(
            module.TERRITORY_SCHEMA
        )

        for schema in (
            terrain,
            territory,
        ):
            properties = set(
                schema["properties"]
            )

            self.assertNotIn(
                "zone_id",
                properties
            )

            self.assertNotIn(
                "space_id",
                properties
            )

            self.assertNotIn(
                "cartography_id",
                properties
            )


if __name__ == "__main__":
    unittest.main()
