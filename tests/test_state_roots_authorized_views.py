import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT / "tools/validate_state_roots_authorized_views.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_state_roots_authorized_views",
    VALIDATOR
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class StateRootsAuthorizedViewsTests(unittest.TestCase):

    def test_repository_contract(self):
        self.assertEqual(module.validate(), [])

    def test_state_root_is_deterministic(self):
        first = module.compute_state_root(
            "manifest:x",
            7,
            {"b": 2, "a": 1}
        )

        second = module.compute_state_root(
            "manifest:x",
            7,
            {"a": 1, "b": 2}
        )

        self.assertEqual(first, second)

    def test_state_change_changes_root(self):
        first = module.compute_state_root(
            "manifest:x",
            7,
            {"value": 1}
        )

        second = module.compute_state_root(
            "manifest:x",
            8,
            {"value": 2}
        )

        self.assertNotEqual(first, second)

    def test_manifest_reference_is_bound(self):
        first = module.compute_state_root(
            "manifest:a",
            1,
            {"value": 1}
        )

        second = module.compute_state_root(
            "manifest:b",
            1,
            {"value": 1}
        )

        self.assertNotEqual(first, second)

    def test_multiple_views_same_state(self):
        state_root = module.compute_state_root(
            "manifest:x",
            3,
            {"secret": 1, "public": 2}
        )

        public_view = module.compute_authorized_view_root(
            state_root,
            "auth:public",
            {"fields": ["public"]},
            {"public": 2},
            ["secret"]
        )

        privileged_view = module.compute_authorized_view_root(
            state_root,
            "auth:privileged",
            {"fields": ["public", "secret"]},
            {"public": 2, "secret": 1},
            []
        )

        self.assertNotEqual(
            public_view,
            privileged_view
        )

    def test_view_root_does_not_replace_state_root(self):
        state_root = module.compute_state_root(
            "manifest:x",
            1,
            {"value": 1}
        )

        view_root = module.compute_authorized_view_root(
            state_root,
            "auth:x",
            {},
            {"value": 1},
            []
        )

        self.assertNotEqual(
            state_root,
            view_root
        )


if __name__ == "__main__":
    unittest.main()
