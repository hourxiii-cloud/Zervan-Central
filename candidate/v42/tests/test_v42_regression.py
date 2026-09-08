from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]


class CandidateV42RegressionTests(unittest.TestCase):
    def test_baseline_identity_unchanged(self):
        self.assertEqual("vTemporal.41.0", (ROOT / "VERSION").read_text().strip())

    def test_canonical_animalkingdom_unchanged(self):
        text = (ROOT / "Modules" / "AnimalKingdom" / "animalkingdom_contract.md").read_text()
        self.assertIn("Authority Scope:** Evidence only", text)
        self.assertIn("AnimalKingdom **never** influences live execution paths", text)

    def test_admission_routing_jurisdiction_unchanged(self):
        text = (ROOT / "Admission" / "Routing.md").read_text()
        self.assertIn("Routing determines **how evidence enters the system**", text)
        self.assertIn("Routing decides **path only**", text)

    def test_candidate_is_removable_surface(self):
        status = subprocess.run(["git", "diff", "--name-only", "ae898ab803061823b36fb825e0664e3d8d255409..HEAD"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.splitlines()
        paths = status
        self.assertTrue(paths, "candidate implementation must be visible to Git")
        self.assertTrue(all(p == "Makefile" or p.startswith("candidate/v42/") for p in paths), paths)


if __name__ == "__main__": unittest.main()
