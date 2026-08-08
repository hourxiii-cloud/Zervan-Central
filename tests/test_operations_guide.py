import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_operations_guide.py"

spec = importlib.util.spec_from_file_location(
    "validate_operations_guide",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OperationsGuideTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = module.GUIDE.read_text(
            encoding="utf-8"
        )

        cls.stability = json.loads(
            module.STABILITY.read_text(
                encoding="utf-8"
            )
        )

    def test_validator(self):
        self.assertEqual(module.validate(), [])

    def test_responsibility(self):
        self.assertIn(
            "CONSISTENT RUNTIME OPERATION",
            self.text,
        )

    def test_baseline(self):
        self.assertIn(
            self.stability["baseline_commit"],
            self.text,
        )

    def test_runtime_disabled(self):
        self.assertIn(
            "External Runtime: DISABLED",
            self.text,
        )

    def test_external_action_disabled(self):
        self.assertIn(
            "External Action: DISABLED",
            self.text,
        )

    def test_population_disallowed(self):
        self.assertIn(
            "System Population: DISALLOWED",
            self.text,
        )

    def test_room(self):
        self.assertIn(
            "## 5. Operating Object",
            self.text,
        )

    def test_orientation(self):
        self.assertIn(
            "## 6. Orientation",
            self.text,
        )

    def test_qualification(self):
        self.assertIn(
            "## 7. Qualification Gate",
            self.text,
        )

    def test_question(self):
        self.assertIn(
            "contracts/question/QUESTION_CONTRACT.md",
            self.text,
        )

    def test_routing(self):
        for marker in (
            "Need determines force.",
            "Question determines mission.",
            "Evidence determines escalation.",
        ):
            self.assertIn(marker, self.text)

    def test_identity_outcomes(self):
        for marker in (
            "SAME_OBJECT",
            "DISTINCT_OBJECT",
            "UNRESOLVED",
        ):
            self.assertIn(marker, self.text)

    def test_pipeline(self):
        self.assertIn(
            "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
            self.text,
        )

    def test_replay(self):
        self.assertIn(
            "## 27. Replay Operation",
            self.text,
        )

    def test_scar(self):
        self.assertIn(
            "## 28. Scar Operation",
            self.text,
        )

    def test_failure_classes(self):
        for marker in (
            "INNER_INVARIANT_CONTRADICTION",
            "OUTER_IMPLEMENTATION_DEFECT",
            "VALIDATOR_DEFECT",
            "COVERAGE_GAP",
            "SOURCE_COLLISION",
            "UNRESOLVED_REQUIRED_SURFACE",
        ):
            self.assertIn(marker, self.text)

    def test_fast_gate(self):
        self.assertIn(
            "git diff --check",
            self.text,
        )

    def test_cached_gate(self):
        self.assertIn(
            "git diff --cached --check",
            self.text,
        )

    def test_return(self):
        self.assertIn(
            "## 39. Return to Existing Work",
            self.text,
        )

    def test_recovery(self):
        self.assertIn(
            "## 51. Operational Recovery",
            self.text,
        )

    def test_no_default_drift(self):
        self.assertIn(
            "## 52. No-Default Drift",
            self.text,
        )

    def test_promotion_boundary(self):
        self.assertIn(
            "READY_FOR_HUMAN_GATE is not CANONICAL.",
            self.text,
        )

    def test_authority_none(self):
        self.assertIn(
            "Authority: NONE",
            self.text,
        )

    def test_human_gate_active(self):
        self.assertIn(
            "Human Gate: ACTIVE",
            self.text,
        )

    def test_closure(self):
        self.assertIn(
            "OPERATIONS GUIDE COMPLETE.",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
