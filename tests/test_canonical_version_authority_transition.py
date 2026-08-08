import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

PATH = ROOT / (
    "tools/"
    "validate_canonical_version_authority_transition.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_canonical_version_authority_transition",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class CanonicalVersionAuthorityTransitionTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(cls):
        cls.metadata = json.loads(
            module.VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )

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

    def test_version_unchanged(self):
        self.assertEqual(
            module.VERSION.read_text(
                encoding="utf-8"
            ).strip(),
            "vTemporal.41.0",
        )

    def test_canonical_state(self):
        self.assertEqual(
            self.metadata[
                "promotion_state"
            ],
            "CANONICAL",
        )

    def test_canonical_true(self):
        self.assertTrue(
            self.metadata[
                "canonical"
            ]
        )

    def test_canonical_branch_main(self):
        self.assertEqual(
            self.metadata[
                "canonical_branch"
            ],
            "main",
        )

    def test_receipt_approve(self):
        self.assertEqual(
            self.receipt[
                "decision"
            ],
            "APPROVE",
        )

    def test_receipt_granted(self):
        self.assertEqual(
            self.receipt[
                "authorization_state"
            ],
            "GRANTED",
        )

    def test_receipt_candidate(self):
        self.assertEqual(
            self.receipt[
                "candidate_commit"
            ],
            module.APPROVED,
        )

    def test_receipt_history_not_rewritten_execution(self):
        self.assertFalse(
            self.receipt[
                "promotion_executed"
            ]
        )

    def test_receipt_history_not_rewritten_canonical(self):
        self.assertFalse(
            self.receipt[
                "canonical"
            ]
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

    def test_contract_transition_complete(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            (
                "R8-H CANONICAL / VERSION AUTHORITY "
                "TRANSITION COMPLETE."
            ),
            text,
        )

    def test_next_r8i(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "R8-I owns Post-Promotion Integrity Verification.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
