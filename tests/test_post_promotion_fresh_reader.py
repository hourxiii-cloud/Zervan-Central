import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

PATH = ROOT / (
    "tools/"
    "validate_post_promotion_fresh_reader.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_post_promotion_fresh_reader",
    PATH,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class PostPromotionFreshReaderTests(
    unittest.TestCase
):

    def test_validator(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def test_main(self):
        self.assertEqual(
            module.git(
                "branch",
                "--show-current",
            ),
            "main",
        )

    def test_version(self):
        self.assertEqual(
            module.VERSION.read_text(
                encoding="utf-8"
            ).strip(),
            "vTemporal.41.0",
        )

    def test_init_canonical(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Promotion State: CANONICAL",
            text,
        )

    def test_init_not_candidate(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "Promotion State: CANDIDATE",
            text,
        )

    def test_init_canonical_true(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Canonical: TRUE",
            text,
        )

    def test_init_no_false(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "Canonical: FALSE",
            text,
        )

    def test_repository_truth(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Current Git is implementation truth.",
            text,
        )

    def test_no_memory_dependency(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Do not use stored memory as implementation authority.",
            text,
        )

    def test_no_conversation_dependency(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            (
                "Do not use prior conversation as implementation "
                "authority when Git can answer."
            ),
            text,
        )

    def test_no_v39_v40_dependency(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Native-v41 initialization MUST NOT require v39 or v40 knowledge.",
            text,
        )

    def test_next_r8k(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "R8-K owns Promotion Completion Receipt.",
            text,
        )

    def test_authority_none(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Authority remains NONE.",
            text,
        )

    def test_human_gate_active(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Human Gate remains ACTIVE.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
