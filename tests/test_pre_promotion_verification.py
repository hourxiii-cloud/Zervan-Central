import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

PATH = ROOT / (
    "tools/"
    "validate_pre_promotion_verification.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_pre_promotion_verification",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class PrePromotionVerificationTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(cls):
        cls.result = module.build_result()

    def test_validator(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def test_candidate_branch(self):
        self.assertEqual(
            self.result["candidate_branch"],
            "candidate/v41-complete",
        )

    def test_candidate_commit(self):
        self.assertEqual(
            len(self.result["candidate_commit"]),
            40,
        )

    def test_candidate_tree(self):
        self.assertEqual(
            len(self.result["candidate_tree"]),
            40,
        )

    def test_target_branch(self):
        self.assertEqual(
            self.result["target_branch"],
            "main",
        )

    def test_target_commit(self):
        self.assertEqual(
            len(self.result["target_commit"]),
            40,
        )

    def test_ring7_ready(self):
        self.assertTrue(
            self.result["ring7_ready"]
        )

    def test_r8a(self):
        self.assertTrue(
            self.result["r8a_valid"]
        )

    def test_r8b(self):
        self.assertTrue(
            self.result["r8b_valid"]
        )

    def test_r8c(self):
        self.assertTrue(
            self.result["r8c_valid"]
        )

    def test_binding_sha512(self):
        self.assertEqual(
            len(self.result["binding_sha512"]),
            128,
        )

    def test_no_decision(self):
        self.assertEqual(
            self.result["decision_instance"],
            "NONE",
        )

    def test_not_authorized(self):
        self.assertEqual(
            self.result["human_gate_authorization"],
            "NOT_GRANTED",
        )

    def test_authority_none(self):
        self.assertEqual(
            self.result["authority_state"],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.result["human_gate_state"],
            "ACTIVE",
        )

    def test_candidate_state(self):
        self.assertEqual(
            self.result["promotion_state"],
            "CANDIDATE",
        )

    def test_not_canonical(self):
        self.assertFalse(
            self.result["canonical"]
        )

    def test_not_promoted(self):
        self.assertFalse(
            self.result["promoted"]
        )

    def test_not_merged(self):
        self.assertFalse(
            self.result["merged"]
        )

    def test_disposition(self):
        self.assertEqual(
            self.result["disposition"],
            "PRE_PROMOTION_VERIFIED",
        )

    def test_bounded(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Full-tree rerun = NOT REQUIRED.",
            text,
        )

    def test_no_self_invalidating_receipt(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "No self-invalidating verification receipt is permitted.",
            text,
        )

    def test_closure(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "R8-D PRE-PROMOTION VERIFICATION COMPLETE.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
