import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_canonical_room_object_identity.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_canonical_room_object_identity",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class CanonicalRoomObjectIdentityTests(unittest.TestCase):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_object_identity_is_deterministic(self):
        origin = (
            "sha512:"
            + "2" * 128
        )

        first = module.compute_object_id(
            "manifest:genesis-a",
            origin,
            "nonce"
        )

        second = module.compute_object_id(
            "manifest:genesis-a",
            origin,
            "nonce"
        )

        self.assertEqual(
            first,
            second
        )

    def test_object_nonce_separates_objects(self):
        origin = (
            "sha512:"
            + "3" * 128
        )

        first = module.compute_object_id(
            "manifest:genesis-a",
            origin,
            "nonce-a"
        )

        second = module.compute_object_id(
            "manifest:genesis-a",
            origin,
            "nonce-b"
        )

        self.assertNotEqual(
            first,
            second
        )

    def test_genesis_lineage_is_bound(self):
        origin = (
            "sha512:"
            + "4" * 128
        )

        first = module.compute_object_id(
            "manifest:genesis-a",
            origin,
            "nonce"
        )

        second = module.compute_object_id(
            "manifest:genesis-b",
            origin,
            "nonce"
        )

        self.assertNotEqual(
            first,
            second
        )

    def test_origin_identity_is_bound(self):
        first = module.compute_object_id(
            "manifest:genesis-a",
            "sha512:" + "5" * 128,
            "nonce"
        )

        second = module.compute_object_id(
            "manifest:genesis-a",
            "sha512:" + "6" * 128,
            "nonce"
        )

        self.assertNotEqual(
            first,
            second
        )

    def test_schema_does_not_absorb_ring1_local_ids(self):
        schema = module.load_schema()

        properties = set(
            schema["properties"]
        )

        for field in {
            "state_root",
            "authorized_view_root",
            "branch_id",
            "merge_id",
        }:
            self.assertNotIn(
                field,
                properties
            )

    def test_schema_does_not_pull_geography_forward(self):
        schema = module.load_schema()

        properties = set(
            schema["properties"]
        )

        for field in {
            "terrain",
            "territory",
            "zone_id",
            "space_id",
            "transform_id",
            "cartography",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
