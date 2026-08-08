import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_developer_guide.py"

spec = importlib.util.spec_from_file_location(
    "validate_developer_guide",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DeveloperGuideTests(unittest.TestCase):

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
            "IMPLEMENTATION AND EXTENSION",
            self.text,
        )

    def test_baseline(self):
        self.assertIn(
            self.stability["baseline_commit"],
            self.text,
        )

    def test_repository_structure(self):
        for marker in (
            "contracts/",
            "schemas/",
            "receipts/",
            "tools/",
            "tests/",
            "docs/",
        ):
            self.assertIn(marker, self.text)

    def test_contracts(self):
        self.assertIn(
            "## 5. Contracts",
            self.text,
        )

    def test_schemas(self):
        self.assertIn(
            "## 6. Schemas",
            self.text,
        )

    def test_validators(self):
        self.assertIn(
            "## 7. Validators",
            self.text,
        )

    def test_tests(self):
        self.assertIn(
            "## 8. Tests",
            self.text,
        )

    def test_identity(self):
        self.assertIn(
            "## 10. Identity Implementation",
            self.text,
        )

    def test_sha512(self):
        self.assertIn(
            "## 11. SHA-512",
            self.text,
        )

    def test_question_contract(self):
        self.assertIn(
            "contracts/question/QUESTION_CONTRACT.md",
            self.text,
        )

    def test_pipeline(self):
        self.assertIn(
            "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
            self.text,
        )

    def test_provenance(self):
        self.assertIn(
            "## 35. Provenance",
            self.text,
        )

    def test_extension_rule(self):
        self.assertIn(
            "## 36. Extension Rule",
            self.text,
        )

    def test_new_contract_rule(self):
        self.assertIn(
            "## 37. New Contract Rule",
            self.text,
        )

    def test_new_schema_rule(self):
        self.assertIn(
            "## 38. New Schema Rule",
            self.text,
        )

    def test_new_validator_rule(self):
        self.assertIn(
            "## 39. New Validator Rule",
            self.text,
        )

    def test_new_test_rule(self):
        self.assertIn(
            "## 40. New Test Rule",
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

    def test_git_discipline(self):
        self.assertIn(
            "## 48. Git Discipline",
            self.text,
        )

    def test_version_references(self):
        self.assertIn(
            "## 49. VERSION_REFERENCES.json",
            self.text,
        )

    def test_fast_gate(self):
        self.assertIn(
            "git diff --check",
            self.text,
        )

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
            "DEVELOPER GUIDE COMPLETE.",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
