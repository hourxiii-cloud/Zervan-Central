import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT / "tools/validate_revision_branch_merge.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_revision_branch_merge",
    VALIDATOR
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RevisionBranchMergeTests(unittest.TestCase):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_branch_identity_is_deterministic(self):
        root = "sha512:" + "1" * 128

        first = module.compute_branch_id(
            "manifest:a",
            root,
            "alternate path",
            "nonce"
        )

        second = module.compute_branch_id(
            "manifest:a",
            root,
            "alternate path",
            "nonce"
        )

        self.assertEqual(
            first,
            second
        )

    def test_branch_nonce_separates_branches(self):
        root = "sha512:" + "2" * 128

        first = module.compute_branch_id(
            "manifest:a",
            root,
            "alternate path",
            "nonce-1"
        )

        second = module.compute_branch_id(
            "manifest:a",
            root,
            "alternate path",
            "nonce-2"
        )

        self.assertNotEqual(
            first,
            second
        )

    def test_merge_parent_order_is_preserved(self):
        root = "sha512:" + "3" * 128

        left_right = module.compute_merge_id(
            "left",
            "right",
            root,
            root,
            "merge",
            "nonce"
        )

        right_left = module.compute_merge_id(
            "right",
            "left",
            root,
            root,
            "merge",
            "nonce"
        )

        self.assertNotEqual(
            left_right,
            right_left
        )

    def test_distinct_object_states_are_exact(self):
        schema = module.load(
            module.DISTINCT_SCHEMA
        )

        states = set(
            schema[
                "properties"
            ][
                "determination"
            ][
                "enum"
            ]
        )

        self.assertEqual(
            states,
            {
                "SAME_OBJECT",
                "DISTINCT_OBJECT",
                "UNRESOLVED",
            }
        )

    def test_branch_schema_does_not_create_room_id(self):
        schema = module.load(
            module.BRANCH_SCHEMA
        )

        properties = set(
            schema["properties"]
        )

        self.assertNotIn(
            "room_id",
            properties
        )

        self.assertNotIn(
            "object_id",
            properties
        )

    def test_merge_schema_preserves_both_parents(self):
        schema = module.load(
            module.MERGE_SCHEMA
        )

        required = set(
            schema["required"]
        )

        for field in {
            "left_lineage_reference",
            "right_lineage_reference",
            "left_manifest_reference",
            "right_manifest_reference",
            "left_state_root",
            "right_state_root",
        }:
            self.assertIn(
                field,
                required
            )


if __name__ == "__main__":
    unittest.main()
