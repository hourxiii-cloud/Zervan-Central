import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_promotion_receipt.py"

spec = importlib.util.spec_from_file_location(
    "validate_promotion_receipt",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PromotionReceiptTests(unittest.TestCase):

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
            "PROMOTION_RECEIPT",
        )

    def test_ring(self):
        self.assertEqual(
            self.r["ring"],
            "R7-L",
        )

    def test_transition(self):
        self.assertEqual(
            self.r["transition_state"],
            "ACCOUNTED",
        )

    def test_stability(self):
        self.assertEqual(
            self.r["stability_state"],
            "STABLE_BASELINE",
        )

    def test_completeness(self):
        self.assertEqual(
            self.r["completeness_state"],
            "COMPLETENESS_VALIDATED",
        )

    def test_source_branch(self):
        self.assertEqual(
            self.r["source_branch"],
            "candidate/v41-complete",
        )

    def test_target_branch(self):
        self.assertEqual(
            self.r["target_branch"],
            "main",
        )

    def test_fresh_reader_pending(self):
        self.assertEqual(
            self.r["fresh_reader_state"],
            "PENDING_R7_M",
        )

    def test_aggregate_pending(self):
        self.assertEqual(
            self.r["aggregate_state"],
            "PENDING_R7_N",
        )

    def test_human_gate_not_granted(self):
        self.assertEqual(
            self.r["human_gate_authorization"],
            "NOT_GRANTED",
        )

    def test_pre_authorization_ready(self):
        self.assertEqual(
            self.r["promotion_readiness"],
            "PRE_AUTHORIZATION_READY",
        )

    def test_not_promoted(self):
        self.assertFalse(
            self.r["promoted"]
        )

    def test_not_canonical(self):
        self.assertFalse(
            self.r["canonical"]
        )

    def test_not_merged(self):
        self.assertFalse(
            self.r["merged"]
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

    def test_remaining_preconditions(self):
        self.assertEqual(
            len(self.r["remaining_preconditions"]),
            3,
        )

    def test_disposition(self):
        self.assertEqual(
            self.r["disposition"],
            "PRE_AUTHORIZATION_READY",
        )


if __name__ == "__main__":
    unittest.main()
