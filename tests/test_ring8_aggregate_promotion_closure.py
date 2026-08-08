import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

PATH = ROOT / (
    "tools/"
    "validate_ring8_aggregate_promotion_closure.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_ring8_aggregate_promotion_closure",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class Ring8AggregatePromotionClosureTests(
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

    def test_closed(self):
        self.assertEqual(
            self.receipt["disposition"],
            "RING8_CLOSED_CANONICAL",
        )

    def test_approval(self):
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

    def test_completion_recorded(self):
        self.assertEqual(
            self.receipt[
                "promotion_completion"
            ],
            "RECORDED",
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

    def test_candidate_anchor(self):
        self.assertEqual(
            self.receipt[
                "approved_candidate_commit"
            ],
            module.APPROVED,
        )

    def test_r8k_anchor(self):
        self.assertEqual(
            self.receipt[
                "r8k_commit"
            ],
            module.R8K,
        )


if __name__ == "__main__":
    unittest.main()
