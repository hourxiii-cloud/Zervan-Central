import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

PATH = ROOT / (
    "tools/"
    "validate_post_promotion_integrity.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_post_promotion_integrity",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class PostPromotionIntegrityTests(
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

    def test_candidate_preserved(self):
        self.assertTrue(
            self.result[
                "candidate_preserved"
            ]
        )

    def test_approved_candidate_in_main(self):
        self.assertTrue(
            self.result[
                "approved_candidate_in_main"
            ]
        )

    def test_r8h_in_main(self):
        self.assertTrue(
            self.result[
                "canonical_transition_in_main"
            ]
        )

    def test_authorized_delta_exact(self):
        self.assertTrue(
            self.result[
                "authorized_delta_exact"
            ]
        )

    def test_authorized_delta_count(self):
        self.assertEqual(
            self.result[
                "authorized_delta_count"
            ],
            11,
        )

    def test_authorized_delta_names(self):
        self.assertEqual(
            module.committed_r8h_delta(),
            module.AUTHORIZED_R8H_DELTA,
        )

    def test_human_gate_granted(self):
        self.assertEqual(
            self.result[
                "human_gate_authorization"
            ],
            "GRANTED",
        )

    def test_canonical(self):
        self.assertTrue(
            self.result[
                "canonical"
            ]
        )

    def test_authority_none(self):
        self.assertEqual(
            self.result[
                "authority_state"
            ],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.result[
                "human_gate_state"
            ],
            "ACTIVE",
        )

    def test_disposition(self):
        self.assertEqual(
            self.result[
                "disposition"
            ],
            "POST_PROMOTION_INTEGRITY_VERIFIED",
        )

    def test_runner_canonical(self):
        text = module.RUNNER.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'print("Promotion State: CANONICAL")',
            text,
        )

    def test_runner_granted(self):
        text = module.RUNNER.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            (
                'print("R8-E Human Gate '
                'Authorization: GRANTED")'
            ),
            text,
        )

    def test_runner_no_stale_candidate_footer(self):
        text = module.RUNNER.read_text(
            encoding="utf-8"
        )

        footer = text[
            text.index(
                'print("CURRENT: R8-I PASS")'
            ):
        ]

        self.assertNotIn(
            'print("Promotion State: CANDIDATE")',
            footer,
        )

    def test_runner_no_stale_authorization_footer(self):
        text = module.RUNNER.read_text(
            encoding="utf-8"
        )

        footer = text[
            text.index(
                'print("CURRENT: R8-I PASS")'
            ):
        ]

        self.assertNotIn(
            (
                'print("Human Gate Authorization: '
                'NOT_GRANTED")'
            ),
            footer,
        )

    def test_next_r8j(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "R8-J owns Post-Promotion Fresh Reader.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
