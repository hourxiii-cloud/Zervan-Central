import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_ring7_aggregate_closure.py"

spec = importlib.util.spec_from_file_location(
    "validate_ring7_aggregate_closure",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Ring7AggregateClosureTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.closure = module.CLOSURE.read_text(
            encoding="utf-8"
        )

        cls.promotion = json.loads(
            module.PROMOTION.read_text(
                encoding="utf-8"
            )
        )

    def test_static_validator(self):
        self.assertEqual(
            module.validate(run_dependency=False),
            [],
        )

    def test_ring6_dependency_exists(self):
        self.assertTrue(
            module.RING6.exists()
        )

    def test_readiness(self):
        self.assertIn(
            "PROMOTION READINESS READY_FOR_HUMAN_GATE",
            self.closure,
        )

    def test_ring7_pass(self):
        self.assertIn(
            "RING 7 RESULT: PASS",
            self.closure,
        )

    def test_documentation_complete(self):
        self.assertIn(
            "DOCUMENTATION COMPLETE",
            self.closure,
        )

    def test_question_complete(self):
        self.assertIn(
            "QUESTION CONTRACT COMPLETE",
            self.closure,
        )

    def test_entry_complete(self):
        self.assertIn(
            "NATIVE-v41 ENTRY COMPLETE",
            self.closure,
        )

    def test_transition_complete(self):
        self.assertIn(
            "TRANSITION ACCOUNTING COMPLETE",
            self.closure,
        )

    def test_stability_validated(self):
        self.assertIn(
            "STABILITY VALIDATED",
            self.closure,
        )

    def test_completeness_validated(self):
        self.assertIn(
            "COMPLETENESS VALIDATED",
            self.closure,
        )

    def test_fresh_reader_validated(self):
        self.assertIn(
            "FRESH-READER VALIDATED",
            self.closure,
        )

    def test_promotion_package_complete(self):
        self.assertIn(
            "PROMOTION PACKAGE COMPLETE",
            self.closure,
        )

    def test_human_gate_not_granted(self):
        self.assertEqual(
            self.promotion["human_gate_authorization"],
            "NOT_GRANTED",
        )

    def test_not_promoted(self):
        self.assertFalse(
            self.promotion["promoted"]
        )

    def test_not_canonical(self):
        self.assertFalse(
            self.promotion["canonical"]
        )

    def test_not_merged(self):
        self.assertFalse(
            self.promotion["merged"]
        )

    def test_authority_none(self):
        self.assertIn(
            "Authority: NONE",
            self.closure,
        )

    def test_human_gate_active(self):
        self.assertIn(
            "Human Gate: ACTIVE",
            self.closure,
        )

    def test_candidate(self):
        self.assertIn(
            "Promotion State: CANDIDATE",
            self.closure,
        )

    def test_ready_not_authorization(self):
        self.assertIn(
            "READY_FOR_HUMAN_GATE != authorization.",
            self.closure,
        )

    def test_ready_not_promoted(self):
        self.assertIn(
            "READY_FOR_HUMAN_GATE != PROMOTED.",
            self.closure,
        )

    def test_ready_not_canonical(self):
        self.assertIn(
            "READY_FOR_HUMAN_GATE != CANONICAL.",
            self.closure,
        )

    def test_ready_not_merged(self):
        self.assertIn(
            "READY_FOR_HUMAN_GATE != MERGED.",
            self.closure,
        )

    def test_closure_complete(self):
        self.assertIn(
            "RING 7 AGGREGATE DOCUMENTATION / "
            "PROMOTION READINESS CLOSURE COMPLETE.",
            self.closure,
        )


if __name__ == "__main__":
    unittest.main()
