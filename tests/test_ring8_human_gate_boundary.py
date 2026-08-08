import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

path = ROOT / "tools/validate_ring8_human_gate_boundary.py"

spec = importlib.util.spec_from_file_location(
    "validate_ring8_human_gate_boundary",
    path,
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Ring8HumanGateBoundaryTests(unittest.TestCase):

    def test_validator(self):
        self.assertEqual(
            module.validate(),
            [],
        )

    def test_r7_handoff(self):
        text = module.R7.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "PROMOTION READINESS READY_FOR_HUMAN_GATE",
            text,
        )

    def test_authority_none(self):
        text = module.R8.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Authority remains NONE.",
            text,
        )

    def test_human_gate_active(self):
        text = module.R8.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Human Gate remains ACTIVE.",
            text,
        )

    def test_not_authorized(self):
        text = module.R8.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Human Gate Authorization remains NOT_GRANTED.",
            text,
        )

    def test_not_promoted(self):
        text = module.R8.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Promoted remains FALSE.",
            text,
        )

    def test_not_canonical(self):
        text = module.R8.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Canonical remains FALSE.",
            text,
        )

    def test_not_merged(self):
        text = module.R8.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Merged remains FALSE.",
            text,
        )

    def test_instantiated(self):
        text = module.R8.read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "R8-A INSTANTIATED.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
