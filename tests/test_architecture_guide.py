import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_architecture_guide.py"

spec = importlib.util.spec_from_file_location(
    "validate_architecture_guide",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ArchitectureGuideTests(unittest.TestCase):

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
            "RATIONALE AND PRIMITIVES",
            self.text,
        )

    def test_baseline(self):
        self.assertIn(
            self.stability["baseline_commit"],
            self.text,
        )

    def test_room(self):
        self.assertIn(
            "## 3. One Analytical Object",
            self.text,
        )

    def test_geography(self):
        self.assertIn(
            "## 7. Operational Geography",
            self.text,
        )

    def test_qualification(self):
        self.assertIn(
            "## 14. Qualification Before Analysis",
            self.text,
        )

    def test_question_contract(self):
        self.assertIn(
            "## 17. Question Contract",
            self.text,
        )

    def test_evidence_boundary(self):
        self.assertIn(
            "## 18. Evidence Boundary",
            self.text,
        )

    def test_evidence_ceiling(self):
        self.assertIn(
            "## 19. Evidence Ceiling",
            self.text,
        )

    def test_routing(self):
        self.assertIn(
            "## 20. Capability Routing",
            self.text,
        )

    def test_hydration(self):
        self.assertIn(
            "## 22. Hydration",
            self.text,
        )

    def test_replay(self):
        self.assertIn(
            "## 27. Replay",
            self.text,
        )

    def test_scar(self):
        self.assertIn(
            "## 28. Scar",
            self.text,
        )

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

    def test_pmc(self):
        self.assertIn(
            "## 33. PMC",
            self.text,
        )

    def test_ccr(self):
        self.assertIn(
            "## 34. CCR",
            self.text,
        )

    def test_mc(self):
        self.assertIn(
            "## 35. MC",
            self.text,
        )

    def test_raven(self):
        self.assertIn(
            "## 36. Raven",
            self.text,
        )

    def test_human_gate(self):
        self.assertIn(
            "## 37. Human Gate",
            self.text,
        )

    def test_failure_taxonomy(self):
        for marker in (
            "INNER_INVARIANT_CONTRADICTION",
            "OUTER_IMPLEMENTATION_DEFECT",
            "VALIDATOR_DEFECT",
            "COVERAGE_GAP",
            "SOURCE_COLLISION",
            "UNRESOLVED_REQUIRED_SURFACE",
        ):
            self.assertIn(marker, self.text)

    def test_implementation_leads(self):
        self.assertIn(
            "Implementation leads.",
            self.text,
        )

    def test_documentation_follows(self):
        self.assertIn(
            "Documentation follows.",
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
            "ARCHITECTURE GUIDE COMPLETE.",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
