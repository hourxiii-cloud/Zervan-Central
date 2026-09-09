from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NativeV42EntryTests(unittest.TestCase):
    def test_active_version(self):
        self.assertEqual((ROOT / "VERSION").read_text().strip(), "vTemporal.42.0")

    def test_machine_identity(self):
        data = json.loads((ROOT / "VERSION.json").read_text())
        self.assertEqual(data["version"], "vTemporal.42.0")
        self.assertEqual(data["implementation_identity"], "v42 Complete")
        self.assertEqual(data["promotion_state"], "CANONICAL")
        self.assertTrue(data["canonical"])

    def test_active_entry_surfaces(self):
        self.assertTrue((ROOT / "call" / "INITIATION_STATEMENT_V42_0.md").exists())
        self.assertTrue((ROOT / "canonical" / "ZERVAN_v42_0_CANONICAL_ENTRY.md").exists())

    def test_human_gate_and_authority(self):
        text = (ROOT / "canonical" / "ZERVAN_v42_0_CANONICAL_ENTRY.md").read_text()
        self.assertIn("Authority: NONE", text)
        self.assertIn("Human Gate: ACTIVE", text)

    def test_four_stage_identity(self):
        text = (ROOT / "canonical" / "ZERVAN_v42_0_CANONICAL_ENTRY.md").read_text()
        for term in ("ONE↔MANY", "MÖBIUS", "HARMONY INTERPRETS MÖBIUS", "QUALIFIED ENDOGENOUS PROVOCATION"):
            self.assertIn(term, text)

    def test_historical_v41_preserved(self):
        self.assertTrue((ROOT / "call" / "INITIATION_STATEMENT_V41_0.md").exists())
        self.assertTrue((ROOT / "canonical" / "ZERVAN_v41_0_CANONICAL_ENTRY.md").exists())

    def test_promotion_receipt(self):
        data = json.loads((ROOT / "receipts" / "promotion" / "V42_CANONICAL_PROMOTION_RECEIPT.json").read_text())
        self.assertEqual(data["human_gate_decision"], "APPROVE")
        self.assertEqual(data["authority_state"], "NONE")
        self.assertTrue(data["canonical"])


if __name__ == "__main__":
    unittest.main()
