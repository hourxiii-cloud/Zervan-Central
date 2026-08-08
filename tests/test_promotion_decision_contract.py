import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

PATH = ROOT / (
    "tools/"
    "validate_promotion_decision_contract.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_promotion_decision_contract",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class PromotionDecisionContractTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(cls):
        cls.contract = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        cls.schema = json.loads(
            module.SCHEMA.read_text(
                encoding="utf-8"
            )
        )

    def test_validator(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def test_approve(self):
        self.assertIn(
            "APPROVE",
            self.schema[
                "properties"
            ][
                "decision"
            ][
                "enum"
            ],
        )

    def test_reject(self):
        self.assertIn(
            "REJECT",
            self.schema[
                "properties"
            ][
                "decision"
            ][
                "enum"
            ],
        )

    def test_defer(self):
        self.assertIn(
            "DEFER",
            self.schema[
                "properties"
            ][
                "decision"
            ][
                "enum"
            ],
        )

    def test_exact_enum(self):
        self.assertEqual(
            self.schema[
                "properties"
            ][
                "decision"
            ][
                "enum"
            ],
            [
                "APPROVE",
                "REJECT",
                "DEFER",
            ],
        )

    def test_candidate_branch(self):
        self.assertEqual(
            self.schema[
                "properties"
            ][
                "candidate_branch"
            ][
                "const"
            ],
            "candidate/v41-complete",
        )

    def test_candidate_commit_required(self):
        self.assertIn(
            "candidate_commit",
            self.schema[
                "required"
            ],
        )

    def test_target_main(self):
        self.assertEqual(
            self.schema[
                "properties"
            ][
                "target_branch"
            ][
                "const"
            ],
            "main",
        )

    def test_actor_required(self):
        self.assertIn(
            "decision_actor",
            self.schema[
                "required"
            ],
        )

    def test_decision_not_execution(self):
        self.assertIn(
            "Decision != execution.",
            self.contract,
        )

    def test_approval_not_execution(self):
        self.assertIn(
            "Approval != execution.",
            self.contract,
        )

    def test_no_decision_instance(self):
        self.assertIn(
            "Contract != decision instance.",
            self.contract,
        )

    def test_no_approval_created(self):
        self.assertIn(
            "R8-B creates no approval.",
            self.contract,
        )

    def test_no_rejection_created(self):
        self.assertIn(
            "R8-B creates no rejection.",
            self.contract,
        )

    def test_no_deferral_created(self):
        self.assertIn(
            "R8-B creates no deferral.",
            self.contract,
        )

    def test_authority_none(self):
        self.assertEqual(
            self.schema[
                "properties"
            ][
                "authority_state"
            ][
                "const"
            ],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.schema[
                "properties"
            ][
                "human_gate_state"
            ][
                "const"
            ],
            "ACTIVE",
        )

    def test_closure(self):
        self.assertIn(
            "R8-B PROMOTION DECISION CONTRACT COMPLETE.",
            self.contract,
        )


if __name__ == "__main__":
    unittest.main()
