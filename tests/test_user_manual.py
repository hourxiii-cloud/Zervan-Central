import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_user_manual.py"

spec = importlib.util.spec_from_file_location(
    "validate_user_manual",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UserManualTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = module.MANUAL.read_text(
            encoding="utf-8"
        )

        cls.stability = json.loads(
            module.STABILITY.read_text(
                encoding="utf-8"
            )
        )

    def test_validator(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def test_responsibility(self):
        self.assertIn(
            "UNDERSTANDING AND OPERATION",
            self.text,
        )

    def test_baseline_bound(self):
        self.assertIn(
            self.stability["baseline_commit"],
            self.text,
        )

    def test_stable_source(self):
        self.assertEqual(
            self.stability["disposition"],
            "STABLE_BASELINE",
        )

    def test_freeze_source(self):
        self.assertTrue(
            self.stability["documentation_freeze"]
        )

    def test_room_section(self):
        self.assertIn(
            "## 3. Understand the Room",
            self.text,
        )

    def test_geography_section(self):
        self.assertIn(
            "## 4. Understand Operational Geography",
            self.text,
        )

    def test_qualification_section(self):
        self.assertIn(
            "## 6. Qualify Before Analysis",
            self.text,
        )

    def test_question_section(self):
        self.assertIn(
            "## 8. Ask a Question",
            self.text,
        )

    def test_evidence_section(self):
        self.assertIn(
            "## 10. Evidence Boundary and Evidence Ceiling",
            self.text,
        )

    def test_routing_section(self):
        self.assertIn(
            "## 11. Route Capability Proportionally",
            self.text,
        )

    def test_hydration_section(self):
        self.assertIn(
            "## 12. Hydrate on Need",
            self.text,
        )

    def test_representation_section(self):
        self.assertIn(
            "## 14. Perspective and Representation",
            self.text,
        )

    def test_distinct_section(self):
        self.assertIn(
            "## 15. Distinct Objects and Passageways",
            self.text,
        )

    def test_replay_section(self):
        self.assertIn(
            "## 19. Replay",
            self.text,
        )

    def test_scar_section(self):
        self.assertIn(
            "## 20. Scar and Scar Replay",
            self.text,
        )

    def test_pipeline_section(self):
        self.assertIn(
            "## 21. Analytical Pipeline",
            self.text,
        )

    def test_pipeline_route(self):
        self.assertIn(
            "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
            self.text,
        )

    def test_failure_classes(self):
        for name in (
            "INNER_INVARIANT_CONTRADICTION",
            "OUTER_IMPLEMENTATION_DEFECT",
            "VALIDATOR_DEFECT",
            "COVERAGE_GAP",
            "SOURCE_COLLISION",
            "UNRESOLVED_REQUIRED_SURFACE",
        ):
            self.assertIn(
                name,
                self.text,
            )

    def test_normal_sequence(self):
        self.assertIn(
            "## 28. Normal User Operating Sequence",
            self.text,
        )

    def test_runtime_boundary(self):
        self.assertIn(
            "## 29. Runtime Boundary",
            self.text,
        )

    def test_promotion_boundary(self):
        self.assertIn(
            "## 30. Promotion Boundary",
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

    def test_candidate(self):
        self.assertIn(
            "Promotion State: CANDIDATE",
            self.text,
        )

    def test_no_private_context(self):
        self.assertIn(
            "No prior conversation is required",
            self.text,
        )

    def test_closure(self):
        self.assertIn(
            "USER MANUAL COMPLETE.",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
