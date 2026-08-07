import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_bounded_space.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_bounded_space",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_space(
    mode="ZONE"
):
    object_id = (
        "sha512:"
        + "3" * 128
    )

    zone_id = (
        "sha512:"
        + "4" * 128
    )

    if mode == "ZONE":
        binding_zone = zone_id
        transform_ref = None
    else:
        binding_zone = None
        transform_ref = "transform:direct-a"

    space = {
        "object_id":
            object_id,
        "representation_binding_mode":
            mode,
        "zone_id":
            binding_zone,
        "direct_transform_reference":
            transform_ref,
        "field":
            "security",
        "discipline":
            "audit",
        "question_set": [
            "what changed?"
        ],
        "controls": [
            "control:a"
        ],
        "capabilities": [
            "capability:a"
        ],
        "evidence_ceiling":
            "CEILING:A",
        "allowed_mission":
            "bounded analysis",
        "prohibited_assumptions": [
            "no unsupported attribution"
        ],
        "rendering_obligations": [
            "preserve provenance"
        ],
    }

    space["space_id"] = (
        module.compute_space_id(
            space["object_id"],
            space["representation_binding_mode"],
            space["zone_id"],
            space["direct_transform_reference"],
            space["field"],
            space["discipline"],
            space["question_set"],
            space["controls"],
            space["capabilities"],
            space["evidence_ceiling"],
            space["allowed_mission"],
            space["prohibited_assumptions"],
            space["rendering_obligations"],
        )
    )

    return space


class BoundedSpaceTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_zone_bound_space(self):
        space = make_space(
            "ZONE"
        )

        self.assertEqual(
            module.validate_space(
                space
            ),
            []
        )

    def test_valid_direct_transform_space(self):
        space = make_space(
            "DIRECT_TRANSFORM"
        )

        self.assertEqual(
            module.validate_space(
                space
            ),
            []
        )

    def test_zone_binding_requires_zone_id(self):
        space = make_space(
            "ZONE"
        )

        space["zone_id"] = None

        errors = module.validate_binding(
            space
        )

        self.assertTrue(
            any(
                "requires zone_id"
                in error
                for error in errors
            )
        )

    def test_direct_transform_binding_rejects_zone_id(self):
        space = make_space(
            "DIRECT_TRANSFORM"
        )

        space["zone_id"] = (
            "sha512:"
            + "5" * 128
        )

        errors = module.validate_binding(
            space
        )

        self.assertTrue(
            any(
                "must not carry zone_id"
                in error
                for error in errors
            )
        )

    def test_mission_change_changes_space_identity(self):
        space = make_space(
            "ZONE"
        )

        changed = module.compute_space_id(
            space["object_id"],
            space["representation_binding_mode"],
            space["zone_id"],
            space["direct_transform_reference"],
            space["field"],
            space["discipline"],
            [
                "what changed?",
                "why?"
            ],
            space["controls"],
            space["capabilities"],
            space["evidence_ceiling"],
            space["allowed_mission"],
            space["prohibited_assumptions"],
            space["rendering_obligations"],
        )

        self.assertNotEqual(
            space["space_id"],
            changed
        )

    def test_space_identity_does_not_replace_object_identity(self):
        space = make_space(
            "ZONE"
        )

        self.assertNotEqual(
            space["space_id"],
            space["object_id"]
        )

    def test_schema_does_not_pull_transform_or_occupation_forward(self):
        schema = module.load_schema()

        properties = set(
            schema["properties"]
        )

        for field in {
            "transform_id",
            "source_orientation",
            "target_orientation",
            "cartography_id",
            "stick_id",
            "occupation_id",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
