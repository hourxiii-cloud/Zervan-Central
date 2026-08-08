import importlib.util
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_native_v41_entry.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_native_v41_entry",
    VALIDATOR,
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


class NativeV41EntryTests(unittest.TestCase):

    def test_validator_positive(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def test_version_file(self):
        self.assertEqual(
            module.VERSION.read_text(
                encoding="utf-8"
            ).strip(),
            "vTemporal.41.0",
        )

    def test_version_json_version(self):
        data = json.loads(
            module.VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            data["version"],
            "vTemporal.41.0",
        )

    def test_version_json_candidate(self):
        data = json.loads(
            module.VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            data["promotion_state"],
            "CANDIDATE",
        )

    def test_version_json_not_canonical(self):
        data = json.loads(
            module.VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )

        self.assertFalse(
            data["canonical"]
        )

    def test_canonical_branch_main(self):
        data = json.loads(
            module.VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            data["canonical_branch"],
            "main",
        )

    def test_development_branch(self):
        data = json.loads(
            module.VERSION_JSON.read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            data["development_branch"],
            "candidate/v41-complete",
        )

    def test_version_authority_surface(self):
        self.assertTrue(
            module.AUTHORITY.exists()
        )

    def test_readme_exists(self):
        self.assertTrue(
            module.README.exists()
        )

    def test_readme_has_active_version(self):
        text = module.README.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "vTemporal.41.0",
            text,
        )

    def test_readme_is_orientation(self):
        text = module.README.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "README owns orientation.",
            text,
        )

    def test_readme_does_not_own_version_authority(self):
        text = module.README.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "README does not own version authority.",
            text,
        )

    def test_v41_initiation_exists(self):
        self.assertTrue(
            module.INIT.exists()
        )

    def test_v41_entry_exists(self):
        self.assertTrue(
            module.ENTRY.exists()
        )

    def test_initiation_active_version(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Version: vTemporal.41.0",
            text,
        )

    def test_initiation_candidate(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Promotion State: CANDIDATE",
            text,
        )

    def test_initiation_authority_none(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Authority: NONE",
            text,
        )

    def test_initiation_human_gate_active(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Human Gate: ACTIVE",
            text,
        )

    def test_initiation_rejects_v39_fallback(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Do not fall back to v39.",
            text,
        )

    def test_initiation_rejects_v40_fallback(self):
        text = module.INIT.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Do not fall back to v40.",
            text,
        )

    def test_entry_candidate_not_canonical(self):
        text = module.ENTRY.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Canonical: FALSE",
            text,
        )

        self.assertIn(
            "Promotion State: CANDIDATE",
            text,
        )

    def test_entry_one_room(self):
        text = module.ENTRY.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "THE ROOM IS ONE ANALYTICAL OBJECT.",
            text,
        )

    def test_entry_operational_territory(self):
        text = module.ENTRY.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "THE ROOM IS VERIFIED OPERATIONAL TERRITORY.",
            text,
        )

    def test_entry_rotation_lock(self):
        text = module.ENTRY.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "TURN THE OBJECT. DO NOT CLONE THE WORLD.",
            text,
        )

    def test_entry_qualification_lock(self):
        text = module.ENTRY.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "QUALIFICATION PRECEDES ANALYSIS.",
            text,
        )

    def test_entry_pipeline(self):
        text = module.ENTRY.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Evidence\n->\nPMC\n->\nCCR\n->\nMC\n->\nRaven\n->\nHuman Gate",
            text,
        )

    def test_historical_v39_preserved(self):
        self.assertTrue(
            (
                ROOT
                / "call"
                / "INITIATION_STATEMENT_V39_0.md"
            ).exists()
        )

    def test_historical_v40_preserved(self):
        self.assertTrue(
            (
                ROOT
                / "call"
                / "INITIATION_STATEMENT_V40_0.md"
            ).exists()
        )

    def test_entry_record_version(self):
        record = module.make_entry_record()

        self.assertEqual(
            record["version"],
            "vTemporal.41.0",
        )

    def test_entry_record_authority(self):
        record = module.make_entry_record()

        self.assertEqual(
            record["authority_state"],
            "NONE",
        )

    def test_entry_record_human_gate(self):
        record = module.make_entry_record()

        self.assertEqual(
            record["human_gate_state"],
            "ACTIVE",
        )

    def test_entry_record_target(self):
        record = module.make_entry_record()

        self.assertEqual(
            record["target_state"],
            "READY_FOR_HUMAN_GATE",
        )


if __name__ == "__main__":
    unittest.main()
