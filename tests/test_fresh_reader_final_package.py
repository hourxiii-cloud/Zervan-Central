import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/validate_fresh_reader_final_package.py"

spec = importlib.util.spec_from_file_location(
    "validate_fresh_reader_final_package",
    PATH,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FreshReaderFinalPackageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.version = module.VERSION.read_text(
            encoding="utf-8"
        ).strip()

        cls.version_json = json.loads(
            module.VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )

        cls.entry = module.ENTRY.read_text(
            encoding="utf-8"
        )

        cls.promotion = json.loads(
            module.PROMOTION.read_text(
                encoding="utf-8"
            )
        )

    def test_validator(self):
        self.assertEqual(module.validate(), [])

    def test_version(self):
        self.assertEqual(
            self.version,
            "vTemporal.41.0",
        )

    def test_implementation_identity(self):
        self.assertEqual(
            self.version_json["implementation_identity"],
            "v41 Complete",
        )

    def test_candidate(self):
        self.assertEqual(
            self.version_json["promotion_state"],
            "CANDIDATE",
        )

    def test_not_canonical(self):
        self.assertFalse(
            self.version_json["canonical"]
        )

    def test_candidate_branch(self):
        self.assertEqual(
            self.version_json["development_branch"],
            "candidate/v41-complete",
        )

    def test_room(self):
        self.assertIn(
            "THE ROOM IS ONE ANALYTICAL OBJECT.",
            self.entry,
        )

    def test_operational_geography(self):
        self.assertIn(
            "Origin\n->\nIngress\n->\nGenesis\n->\nRoom",
            self.entry,
        )

    def test_qualification(self):
        self.assertIn(
            "QUALIFICATION PRECEDES ANALYSIS.",
            self.entry,
        )

    def test_question(self):
        self.assertIn(
            "contracts/question/QUESTION_CONTRACT.md",
            self.entry,
        )

    def test_routing(self):
        self.assertIn(
            "Need determines force.",
            self.entry,
        )

    def test_hydration(self):
        self.assertIn(
            "Hydration occurs on mission need.",
            self.entry,
        )

    def test_replay(self):
        self.assertIn(
            "Replay != new Room.",
            self.entry,
        )

    def test_pipeline(self):
        self.assertIn(
            "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
            self.entry,
        )

    def test_no_v40_overlay(self):
        self.assertIn(
            "Native v41 does not require v40 as an interpretive overlay.",
            self.entry,
        )

    def test_authority_none(self):
        self.assertEqual(
            self.promotion["authority_state"],
            "NONE",
        )

    def test_human_gate_active(self):
        self.assertEqual(
            self.promotion["human_gate_state"],
            "ACTIVE",
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

    def test_not_merged(self):
        self.assertFalse(
            self.promotion["merged"]
        )

    def test_pre_authorization_ready(self):
        self.assertEqual(
            self.promotion["promotion_readiness"],
            "PRE_AUTHORIZATION_READY",
        )

    def test_fresh_reader_historical_pending(self):
        self.assertEqual(
            self.promotion["fresh_reader_state"],
            "PENDING_R7_M",
        )

    def test_aggregate_pending(self):
        self.assertEqual(
            self.promotion["aggregate_state"],
            "PENDING_R7_N",
        )

    def test_private_context_none(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "PRIVATE_CONVERSATIONAL_PREREQUISITE = NONE",
            text,
        )

    def test_final_package_closure(self):
        text = module.CONTRACT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "FRESH-READER FINAL PACKAGE VALIDATION COMPLETE.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
