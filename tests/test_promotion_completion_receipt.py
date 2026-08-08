import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

PATH = ROOT / (
    "tools/"
    "validate_promotion_completion_receipt.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_promotion_completion_receipt",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class PromotionCompletionReceiptTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(
            module.RECEIPT.read_text(
                encoding="utf-8"
            )
        )

    def test_validator(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def test_disposition(self):
        self.assertEqual(
            self.receipt[
                "disposition"
            ],
            "PROMOTION_COMPLETED",
        )

    def test_approved_candidate(self):
        self.assertEqual(
            self.receipt[
                "approved_candidate_commit"
            ],
            module.APPROVED,
        )

    def test_completion_anchor(self):
        self.assertEqual(
            self.receipt[
                "completion_anchor_commit"
            ],
            module.R8J_COMMIT,
        )

    def test_human_gate(self):
        self.assertEqual(
            self.receipt[
                "human_gate_authorization"
            ],
            "GRANTED",
        )

    def test_promotion_executed(self):
        self.assertTrue(
            self.receipt[
                "promotion_executed"
            ]
        )

    def test_candidate_preserved(self):
        self.assertTrue(
            self.receipt[
                "candidate_preserved"
            ]
        )

    def test_fast_forward(self):
        self.assertTrue(
            self.receipt[
                "fast_forward_promotion"
            ]
        )

    def test_no_merge_commit(self):
        self.assertFalse(
            self.receipt[
                "merge_commit_created"
            ]
        )

    def test_canonical(self):
        self.assertTrue(
            self.receipt[
                "canonical"
            ]
        )

    def test_integrity(self):
        self.assertEqual(
            self.receipt[
                "post_promotion_integrity"
            ],
            "VERIFIED",
        )

    def test_fresh_reader(self):
        self.assertEqual(
            self.receipt[
                "post_promotion_fresh_reader"
            ],
            "VALIDATED",
        )

    def test_authority_none(self):
        self.assertEqual(
            self.receipt[
                "authority_state"
            ],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.receipt[
                "human_gate_state"
            ],
            "ACTIVE",
        )

    def test_next_r8l(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "R8-L owns Aggregate Human Gate / Promotion Closure.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
