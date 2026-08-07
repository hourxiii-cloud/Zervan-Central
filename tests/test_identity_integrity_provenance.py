import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_identity_integrity_provenance.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_identity_integrity_provenance",
    VALIDATOR
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class IdentityIntegrityProvenanceTests(unittest.TestCase):

    def test_contract_and_schema(self):
        self.assertEqual(
            module.validate_schema_contract(),
            []
        )

    def test_same_bytes_same_identity(self):
        data = b"same-evidence"

        first = module.sha512_identity(data)
        second = module.sha512_identity(data)

        self.assertEqual(first, second)

    def test_changed_bytes_change_identity(self):
        first = module.sha512_identity(
            b"original-evidence"
        )

        second = module.sha512_identity(
            b"modified-evidence"
        )

        self.assertNotEqual(first, second)

    def test_identity_format(self):
        identity = module.sha512_identity(
            b"format-probe"
        )

        self.assertTrue(
            module.CONTENT_ID_RE.fullmatch(identity)
        )

    def test_integrity_verification(self):
        data = b"integrity-probe"

        identity = module.sha512_identity(data)

        self.assertTrue(
            module.verify_content_identity(
                data,
                identity
            )
        )

        self.assertFalse(
            module.verify_content_identity(
                b"different",
                identity
            )
        )


if __name__ == "__main__":
    unittest.main()
