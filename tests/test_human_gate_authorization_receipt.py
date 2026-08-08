import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

PATH = ROOT / (
    "tools/"
    "validate_human_gate_authorization_receipt.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_human_gate_authorization_receipt",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class HumanGateAuthorizationReceiptTests(
    unittest.TestCase
):

    @classmethod
    def setUpClass(cls):
        cls.issuer = module.load_issuer()

    def test_validator(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def receipt(self, decision):
        return self.issuer.issue(
            decision=decision,
            actor="TEST_HUMAN",
            scope="TEST_SCOPE",
            rationale="TEST_RATIONALE",
            timestamp="2026-01-01T00:00:00+00:00",
        )

    def test_approve_granted(self):
        self.assertEqual(
            self.receipt(
                "APPROVE"
            )[
                "authorization_state"
            ],
            "GRANTED",
        )

    def test_reject_denied(self):
        self.assertEqual(
            self.receipt(
                "REJECT"
            )[
                "authorization_state"
            ],
            "DENIED",
        )

    def test_defer_deferred(self):
        self.assertEqual(
            self.receipt(
                "DEFER"
            )[
                "authorization_state"
            ],
            "DEFERRED",
        )

    def test_candidate_exact(self):
        self.assertEqual(
            len(
                self.receipt(
                    "APPROVE"
                )[
                    "candidate_commit"
                ]
            ),
            40,
        )

    def test_tree_exact(self):
        self.assertEqual(
            len(
                self.receipt(
                    "APPROVE"
                )[
                    "candidate_tree"
                ]
            ),
            40,
        )

    def test_binding_hash(self):
        self.assertEqual(
            len(
                self.receipt(
                    "APPROVE"
                )[
                    "binding_sha512"
                ]
            ),
            128,
        )

    def test_target_main(self):
        self.assertEqual(
            self.receipt(
                "APPROVE"
            )[
                "target_branch"
            ],
            "main",
        )

    def test_authority_none(self):
        self.assertEqual(
            self.receipt(
                "APPROVE"
            )[
                "authority_state"
            ],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.receipt(
                "APPROVE"
            )[
                "human_gate_state"
            ],
            "ACTIVE",
        )

    def test_approval_not_execution(self):
        self.assertFalse(
            self.receipt(
                "APPROVE"
            )[
                "promotion_executed"
            ]
        )

    def test_approval_not_canonical(self):
        self.assertFalse(
            self.receipt(
                "APPROVE"
            )[
                "canonical"
            ]
        )

    def test_approval_not_promoted(self):
        self.assertFalse(
            self.receipt(
                "APPROVE"
            )[
                "promoted"
            ]
        )

    def test_approval_not_merged(self):
        self.assertFalse(
            self.receipt(
                "APPROVE"
            )[
                "merged"
            ]
        )

    def test_blank_actor_rejected(self):
        with self.assertRaises(
            ValueError
        ):
            self.issuer.issue(
                decision="APPROVE",
                actor="",
                scope="TEST_SCOPE",
                rationale="TEST_RATIONALE",
            )

    def test_blank_scope_rejected(self):
        with self.assertRaises(
            ValueError
        ):
            self.issuer.issue(
                decision="APPROVE",
                actor="TEST_HUMAN",
                scope="",
                rationale="TEST_RATIONALE",
            )

    def test_blank_rationale_rejected(self):
        with self.assertRaises(
            ValueError
        ):
            self.issuer.issue(
                decision="APPROVE",
                actor="TEST_HUMAN",
                scope="TEST_SCOPE",
                rationale="",
            )

    def test_contract_waits_for_human(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "RING 8 STATE = WAITING_FOR_HUMAN_GATE.",
            text,
        )

    def test_r8f_blocked(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            (
                "R8-F is blocked until explicit Human Gate "
                "APPROVE authorization exists."
            ),
            text,
        )


if __name__ == "__main__":
    unittest.main()
