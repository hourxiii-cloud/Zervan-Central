import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = ROOT / "tools/validate_transition_receipt.py"

spec = importlib.util.spec_from_file_location(
    "validate_transition_receipt",
    VALIDATOR,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TransitionReceiptTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(
            module.RECEIPT.read_text(encoding="utf-8")
        )

    def test_validator_positive(self):
        self.assertEqual(module.validate(), [])

    def test_receipt_type(self):
        self.assertEqual(
            self.receipt["receipt_type"],
            "TRANSITION_RECEIPT",
        )

    def test_ring(self):
        self.assertEqual(self.receipt["ring"], "R7-I")

    def test_native_version(self):
        self.assertEqual(
            self.receipt["native_version"],
            "vTemporal.41.0",
        )

    def test_prior_branch(self):
        self.assertEqual(
            self.receipt["prior_canonical"]["branch"],
            "main",
        )

    def test_prior_version(self):
        self.assertEqual(
            self.receipt["prior_canonical"]["version"],
            "vTemporal.40.0",
        )

    def test_prior_provenance(self):
        self.assertEqual(
            self.receipt["prior_canonical"]["provenance_surface"],
            "canonical/ZERVAN_v40_0_CANONICAL_LOAD.md",
        )

    def test_candidate_branch(self):
        self.assertEqual(
            self.receipt["candidate"]["branch"],
            "candidate/v41-complete",
        )

    def test_candidate_version(self):
        self.assertEqual(
            self.receipt["candidate"]["version"],
            "vTemporal.41.0",
        )

    def test_candidate_state(self):
        self.assertEqual(
            self.receipt["candidate"]["promotion_state"],
            "CANDIDATE",
        )

    def test_candidate_not_canonical(self):
        self.assertFalse(
            self.receipt["candidate"]["canonical"]
        )

    def test_validated_candidate(self):
        self.assertEqual(
            self.receipt["validated_candidate"]["state"],
            "VALIDATED_CANDIDATE",
        )

    def test_ring6_pass(self):
        self.assertEqual(
            self.receipt["validated_candidate"]["ring6_result"],
            "PASS",
        )

    def test_ring7_target(self):
        self.assertEqual(
            self.receipt["ring7_state"]["target"],
            "READY_FOR_HUMAN_GATE",
        )

    def test_future_source(self):
        self.assertEqual(
            self.receipt["future_transition"]["source_branch"],
            "candidate/v41-complete",
        )

    def test_future_target(self):
        self.assertEqual(
            self.receipt["future_transition"]["target_branch"],
            "main",
        )

    def test_future_state(self):
        self.assertEqual(
            self.receipt["future_transition"]["target_state"],
            "CANONICAL",
        )

    def test_future_not_performed(self):
        self.assertFalse(
            self.receipt["future_transition"]["performed"]
        )

    def test_human_gate_required(self):
        self.assertEqual(
            self.receipt["future_transition"]["authorization_required"],
            "EXPLICIT_HUMAN_GATE",
        )

    def test_history_preserved(self):
        self.assertTrue(
            self.receipt["history_preserved"]
        )

    def test_authority_none(self):
        self.assertEqual(
            self.receipt["authority_state"],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.receipt["human_gate_state"],
            "ACTIVE",
        )

    def test_promotion_candidate(self):
        self.assertEqual(
            self.receipt["promotion_state"],
            "CANDIDATE",
        )

    def test_disposition_accounted(self):
        self.assertEqual(
            self.receipt["transition_disposition"],
            "ACCOUNTED",
        )

    def test_provenance_nonempty(self):
        self.assertTrue(
            self.receipt["provenance"]
        )

    def test_deployment_order_corrected(self):
        text = module.PLAY.read_text(encoding="utf-8")

        self.assertIn(
            "R7-I\n->\nR7-J\n->\nR7-D",
            text,
        )

    def test_implementation_leads(self):
        text = module.PLAY.read_text(encoding="utf-8")

        self.assertIn(
            "Implementation leads.",
            text,
        )

    def test_documentation_follows(self):
        text = module.PLAY.read_text(encoding="utf-8")

        self.assertIn(
            "Documentation follows.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
