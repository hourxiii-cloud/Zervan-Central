from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]


class CandidateV42RegressionTests(unittest.TestCase):
    def test_promoted_identity(self):
        self.assertEqual("vTemporal.42.0", (ROOT / "VERSION").read_text().strip())

    def test_canonical_animalkingdom_unchanged(self):
        text = (ROOT / "Modules" / "AnimalKingdom" / "animalkingdom_contract.md").read_text()
        self.assertIn("Authority Scope:** Evidence only", text)
        self.assertIn("AnimalKingdom **never** influences live execution paths", text)

    def test_admission_routing_jurisdiction_unchanged(self):
        text = (ROOT / "Admission" / "Routing.md").read_text()
        self.assertIn("Routing determines **how evidence enters the system**", text)
        self.assertIn("Routing decides **path only**", text)

    def test_promoted_surface_preserves_candidate_lineage(self):
        self.assertTrue((ROOT / "candidate" / "v42" / "CANDIDATE_MANIFEST.json").exists())
        self.assertTrue((ROOT / "receipts" / "promotion" / "V42_CANONICAL_PROMOTION_RECEIPT.json").exists())


if __name__ == "__main__": unittest.main()
