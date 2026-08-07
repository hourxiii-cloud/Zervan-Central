import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_version_identity.py"

spec = importlib.util.spec_from_file_location(
    "validate_version_identity",
    VALIDATOR
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class VersionIdentityTests(unittest.TestCase):

    def test_repository_version_identity(self):
        errors = module.validate(ROOT)
        self.assertEqual(errors, [])

    def test_version_disagreement_is_detectable(self):
        version = (ROOT / "VERSION").read_text(
            encoding="utf-8"
        ).strip()

        metadata = json.loads(
            (ROOT / "VERSION.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            metadata["version"],
            version
        )

        altered = dict(metadata)
        altered["version"] = "vTemporal.40.0"

        self.assertNotEqual(
            altered["version"],
            version
        )

    def test_candidate_is_not_canonical(self):
        metadata = json.loads(
            (ROOT / "VERSION.json").read_text(
                encoding="utf-8"
            )
        )

        if metadata["promotion_state"] == "CANDIDATE":
            self.assertFalse(metadata["canonical"])


if __name__ == "__main__":
    unittest.main()
