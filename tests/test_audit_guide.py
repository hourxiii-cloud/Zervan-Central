import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_audit_guide.py"

spec = importlib.util.spec_from_file_location(
    "validate_audit_guide",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AuditGuideTests(unittest.TestCase):

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
            "VERIFICATION / REPLACEMENT / RESILIENCE / "
            "PROVENANCE / COMPLETION CRITERIA",
            self.text,
        )

    def test_baseline(self):
        self.assertIn(
            self.stability["baseline_commit"],
            self.text,
        )

    def test_identity_outcomes(self):
        for marker in (
            "SAME_OBJECT",
            "DISTINCT_OBJECT",
            "UNRESOLVED",
        ):
            self.assertIn(marker, self.text)

    def test_hash_boundaries(self):
        for marker in (
            "Hash != truth.",
            "Signature != correctness.",
            "Integrity != semantic correctness.",
        ):
            self.assertIn(marker, self.text)

    def test_qualification(self):
        self.assertIn(
            "## 12. Qualification Verification",
            self.text,
        )

    def test_question(self):
        self.assertIn(
            "## 14. Question Contract Verification",
            self.text,
        )

    def test_evidence_boundary(self):
        self.assertIn(
            "## 15. Evidence Boundary Verification",
            self.text,
        )

    def test_evidence_ceiling(self):
        self.assertIn(
            "## 16. Evidence Ceiling Verification",
            self.text,
        )

    def test_routing(self):
        for marker in (
            "Need determines force.",
            "Question determines mission.",
            "Evidence determines escalation.",
        ):
            self.assertIn(marker, self.text)

    def test_replay(self):
        self.assertIn(
            "## 24. Replay Verification",
            self.text,
        )

    def test_scar(self):
        self.assertIn(
            "## 25. Scar Verification",
            self.text,
        )

    def test_representation(self):
        self.assertIn(
            "## 26. Representation Independence Verification",
            self.text,
        )

    def test_replacement(self):
        self.assertIn(
            "## 27. Replacement Verification",
            self.text,
        )

    def test_resilience(self):
        self.assertIn(
            "## 28. Resilience Verification",
            self.text,
        )

    def test_pipeline(self):
        self.assertIn(
            "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
            self.text,
        )

    def test_provenance(self):
        self.assertIn(
            "## 35. Provenance Verification",
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

    def test_completion(self):
        self.assertIn(
            "## 47. Completion Criteria",
            self.text,
        )

    def test_fresh_reader(self):
        self.assertIn(
            "## 49. Fresh-Reader Criterion",
            self.text,
        )

    def test_lossless(self):
        self.assertIn(
            "## 50. Lossless-Collapse Criterion",
            self.text,
        )

    def test_audit_independence(self):
        self.assertIn(
            "## 54. Audit Independence",
            self.text,
        )

    def test_promotion_boundary(self):
        self.assertIn(
            "## 56. Promotion Audit Boundary",
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
            "AUDIT GUIDE COMPLETE.",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
