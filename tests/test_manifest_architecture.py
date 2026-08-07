import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_manifest_architecture.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_manifest_architecture",
    VALIDATOR
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ManifestArchitectureTests(unittest.TestCase):

    def test_repository_manifest_architecture(self):
        self.assertEqual(module.validate(), [])

    def test_genesis_and_revision_are_separate(self):
        genesis = module.load_json(
            module.SCHEMAS["GENESIS"]
        )
        revision = module.load_json(
            module.SCHEMAS["REVISION"]
        )

        self.assertEqual(
            genesis["properties"]["manifest_type"]["const"],
            "GENESIS"
        )

        self.assertEqual(
            revision["properties"]["manifest_type"]["const"],
            "REVISION"
        )

    def test_revision_references_genesis_and_predecessor(self):
        revision = module.load_json(
            module.SCHEMAS["REVISION"]
        )

        required = set(revision["required"])

        self.assertIn(
            "genesis_manifest_reference",
            required
        )

        self.assertIn(
            "predecessor_manifest_reference",
            required
        )

    def test_pointer_does_not_carry_definition(self):
        pointer = module.load_json(
            module.SCHEMAS["POINTER"]
        )

        properties = pointer["properties"]

        self.assertNotIn("definition", properties)
        self.assertNotIn("definition_change", properties)

    def test_state_roots_not_defined_here(self):
        for path in module.SCHEMAS.values():
            schema = module.load_json(path)
            properties = set(schema["properties"])

            self.assertNotIn(
                "state_root",
                properties
            )

            self.assertNotIn(
                "authorized_view_root",
                properties
            )


if __name__ == "__main__":
    unittest.main()
