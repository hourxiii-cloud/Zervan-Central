from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class LocalCallVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verifier = load_module("verify_local_call", "call/verify_local_call.py")

    def test_boundary_marker_accepts_plain_text(self):
        self.assertTrue(self.verifier.contains_semantic_marker("Authority State: NONE", "Authority State: NONE"))

    def test_boundary_marker_accepts_inline_code_formatting(self):
        self.assertTrue(self.verifier.contains_semantic_marker("Authority State: `NONE`", "Authority State: NONE"))

    def test_boundary_marker_accepts_terminal_period(self):
        self.assertTrue(self.verifier.contains_semantic_marker("No external action.", "No external action"))

    def test_boundary_marker_does_not_accept_wrong_value(self):
        self.assertFalse(self.verifier.contains_semantic_marker("Authority State: FULL", "Authority State: NONE"))

    def test_boundary_marker_does_not_accept_negated_context(self):
        self.assertFalse(self.verifier.contains_semantic_marker("Not Authority State: NONE", "Authority State: NONE"))


class BridgeValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_module("validate_zervan_5_6_bridge", "tools/validate_zervan_5_6_bridge.py")

    def test_emit_is_opt_in(self):
        self.assertIsNone(self.validator.build_parser().parse_args([]).emit)

    def test_python_validation_does_not_create_bytecode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "example.py").write_text("value = 1\n", encoding="utf-8")
            checks = []
            self.validator.validate_python(root, checks)
            self.assertEqual(checks[0].status, "PASS")
            self.assertFalse(any(root.rglob("__pycache__")))
            self.assertFalse(any(root.rglob("*.pyc")))


class FailureInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_module(
            "validate_failure_inventory",
            "candidate/v40/tools/validate_failure_inventory.py",
        )

    def test_inventory_is_complete_and_stable(self):
        inventory = json.loads(self.registry.INVENTORY.read_text(encoding="utf-8"))
        schema = json.loads(self.registry.SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(self.registry.validate_inventory(inventory, schema), [])
        self.assertEqual(len(inventory["findings"]), 40)
        self.assertEqual(inventory["findings"][-1]["id"], "P0-040")


class OperationalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract_validator = load_module(
            "validate_operational_contract",
            "candidate/v40/tools/validate_operational_contract.py",
        )

    def test_contract_is_bound_to_current_canonical_head(self):
        contract = json.loads(self.contract_validator.CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(self.contract_validator.validate_contract(contract), [])

    def test_contract_rejects_authority_promotion(self):
        contract = json.loads(self.contract_validator.CONTRACT.read_text(encoding="utf-8"))
        contract["authority_state"] = "FULL"
        errors = self.contract_validator.validate_contract(contract)
        self.assertTrue(any(error.startswith("authority_state:") for error in errors))

    def test_contract_rejects_canonical_hash_drift(self):
        contract = json.loads(self.contract_validator.CONTRACT.read_text(encoding="utf-8"))
        contract["canonical_binding"]["artifacts"][0]["sha256"] = "0" * 64
        errors = self.contract_validator.validate_contract(contract)
        self.assertIn("canonical artifact hash mismatch: call/INITIATION_STATEMENT_V39_0.md", errors)


if __name__ == "__main__":
    unittest.main()
