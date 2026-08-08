import importlib.util
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_stability_receipt.py"

spec = importlib.util.spec_from_file_location(
    "validate_stability_receipt",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class StabilityReceiptTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(
            module.RECEIPT.read_text(
                encoding="utf-8"
            )
        )

    def test_validator(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def test_type(self):
        self.assertEqual(
            self.r["receipt_type"],
            "STABILITY_RECEIPT",
        )

    def test_ring(self):
        self.assertEqual(
            self.r["ring"],
            "R7-J",
        )

    def test_baseline_commit(self):
        self.assertRegex(
            self.r["baseline_commit"],
            r"^[0-9a-f]{40}$",
        )

    def test_branch(self):
        self.assertEqual(
            self.r["baseline_branch"],
            "candidate/v41-complete",
        )

    def test_version(self):
        self.assertEqual(
            self.r["native_version"],
            "vTemporal.41.0",
        )

    def test_ring6(self):
        self.assertEqual(
            self.r["ring6_state"],
            "VALIDATED_CANDIDATE",
        )

    def test_transition(self):
        self.assertEqual(
            self.r["transition_state"],
            "ACCOUNTED",
        )

    def test_freeze(self):
        self.assertTrue(
            self.r["documentation_freeze"]
        )

    def test_known_conditions(self):
        self.assertTrue(
            self.r["known_conditions"]
        )

    def test_runtime_disabled(self):
        self.assertEqual(
            self.r[
                "runtime_assumptions"
            ][
                "external_runtime"
            ],
            "DISABLED",
        )

    def test_action_disabled(self):
        self.assertEqual(
            self.r[
                "runtime_assumptions"
            ][
                "external_action"
            ],
            "DISABLED",
        )

    def test_population_disallowed(self):
        self.assertEqual(
            self.r[
                "runtime_assumptions"
            ][
                "system_population"
            ],
            "DISALLOWED",
        )

    def test_mutation_human_gate(self):
        self.assertEqual(
            self.r[
                "runtime_assumptions"
            ][
                "canonical_mutation"
            ],
            "HUMAN_GATE_ONLY",
        )

    def test_authority_none(self):
        self.assertEqual(
            self.r["authority_state"],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.r["human_gate_state"],
            "ACTIVE",
        )

    def test_candidate(self):
        self.assertEqual(
            self.r["promotion_state"],
            "CANDIDATE",
        )

    def test_stable(self):
        self.assertEqual(
            self.r["disposition"],
            "STABLE_BASELINE",
        )

    def test_provenance(self):
        self.assertTrue(
            self.r["provenance"]
        )


if __name__ == "__main__":
    unittest.main()
