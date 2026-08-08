import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_completeness_receipt.py"

spec = importlib.util.spec_from_file_location(
    "validate_completeness_receipt",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CompletenessReceiptTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(
            module.RECEIPT.read_text(
                encoding="utf-8"
            )
        )

    def test_validator(self):
        self.assertEqual(module.validate(), [])

    def test_type(self):
        self.assertEqual(
            self.r["receipt_type"],
            "COMPLETENESS_RECEIPT",
        )

    def test_ring(self):
        self.assertEqual(
            self.r["ring"],
            "R7-K",
        )

    def test_disposition(self):
        self.assertEqual(
            self.r["disposition"],
            "COMPLETENESS_VALIDATED",
        )

    def test_documentation(self):
        for state in self.r["documentation"].values():
            self.assertEqual(state, "SATISFIED")

    def test_question(self):
        self.assertEqual(
            self.r["machine_readable_surfaces"][
                "QUESTION_CONTRACT"
            ],
            "SATISFIED",
        )

    def test_transition(self):
        self.assertEqual(
            self.r["machine_readable_surfaces"][
                "TRANSITION_RECEIPT"
            ],
            "SATISFIED",
        )

    def test_stability(self):
        self.assertEqual(
            self.r["machine_readable_surfaces"][
                "STABILITY_RECEIPT"
            ],
            "SATISFIED",
        )

    def test_completeness(self):
        self.assertEqual(
            self.r["machine_readable_surfaces"][
                "COMPLETENESS_RECEIPT"
            ],
            "SATISFIED",
        )

    def test_promotion_receipt_deferred(self):
        self.assertEqual(
            self.r["machine_readable_surfaces"][
                "PROMOTION_RECEIPT"
            ],
            "DEFERRED_TO_R7_L",
        )

    def test_remaining(self):
        self.assertEqual(
            self.r["remaining_sections"],
            ["R7-L", "R7-M", "R7-N"],
        )

    def test_blockers(self):
        self.assertEqual(
            len(self.r["promotion_blockers"]),
            4,
        )

    def test_not_promotion_ready(self):
        self.assertFalse(
            self.r["promotion_ready"]
        )

    def test_not_canonical(self):
        self.assertFalse(
            self.r["canonical"]
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

    def test_provenance(self):
        self.assertTrue(
            self.r["provenance"]
        )


if __name__ == "__main__":
    unittest.main()
