import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = ROOT / "tools" / "validate_authority_resolution.py"

spec = importlib.util.spec_from_file_location(
    "validate_authority_resolution",
    VALIDATOR
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AuthorityResolutionTests(unittest.TestCase):

    def test_r1a_contract_persists(self):
        self.assertEqual(module.validate(), [])


if __name__ == "__main__":
    unittest.main()
