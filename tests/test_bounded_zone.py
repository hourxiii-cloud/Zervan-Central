import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_bounded_zone.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_bounded_zone",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_zone():
    object_id = (
        "sha512:"
        + "2" * 128
    )

    frame = {
        "object_id":
            object_id,
        "transform_type":
            "PERSPECTIVE",
        "perspective_owner_or_discipline":
            "Audit",
        "included_evidence": [
            "evidence:a",
        ],
        "excluded_evidence": [
            "evidence:b",
        ],
        "time_frame": {
            "start": "2026-08-01",
            "end": "2026-08-07",
        },
        "evidence_ceiling":
            "CEILING:DECLARED",
        "prohibited_assumptions": [
            "no unsupported attribution",
        ],
        "provenance_route": [
            object_id,
            "origin:a",
        ],
        "return_coordinates": {
            "reference": "return:a",
        },
    }

    frame["zone_id"] = (
        module.compute_zone_id(
            frame["object_id"],
            frame["transform_type"],
            frame[
                "perspective_owner_or_discipline"
            ],
            frame["included_evidence"],
            frame["excluded_evidence"],
            frame["time_frame"],
            frame["evidence_ceiling"],
            frame["prohibited_assumptions"],
            frame["provenance_route"],
            frame["return_coordinates"],
        )
    )

    return frame


class BoundedZoneTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_zone(self):
        zone = make_zone()

        self.assertEqual(
            module.validate_zone(
                zone
            ),
            []
        )

    def test_zone_identity_is_deterministic(self):
        zone = make_zone()

        second = module.compute_zone_id(
            zone["object_id"],
            zone["transform_type"],
            zone[
                "perspective_owner_or_discipline"
            ],
            zone["included_evidence"],
            zone["excluded_evidence"],
            {
                "end": "2026-08-07",
                "start": "2026-08-01",
            },
            zone["evidence_ceiling"],
            zone["prohibited_assumptions"],
            zone["provenance_route"],
            zone["return_coordinates"],
        )

        self.assertEqual(
            zone["zone_id"],
            second
        )

    def test_material_frame_change_changes_zone_id(self):
        zone = make_zone()

        changed = module.compute_zone_id(
            zone["object_id"],
            zone["transform_type"],
            "Security",
            zone["included_evidence"],
            zone["excluded_evidence"],
            zone["time_frame"],
            zone["evidence_ceiling"],
            zone["prohibited_assumptions"],
            zone["provenance_route"],
            zone["return_coordinates"],
        )

        self.assertNotEqual(
            zone["zone_id"],
            changed
        )

    def test_zone_id_does_not_replace_object_id(self):
        zone = make_zone()

        self.assertNotEqual(
            zone["zone_id"],
            zone["object_id"]
        )

    def test_evidence_cannot_be_included_and_excluded(self):
        zone = make_zone()

        zone[
            "excluded_evidence"
        ].append(
            "evidence:a"
        )

        zone["zone_id"] = (
            module.compute_zone_id(
                zone["object_id"],
                zone["transform_type"],
                zone[
                    "perspective_owner_or_discipline"
                ],
                zone["included_evidence"],
                zone["excluded_evidence"],
                zone["time_frame"],
                zone["evidence_ceiling"],
                zone["prohibited_assumptions"],
                zone["provenance_route"],
                zone["return_coordinates"],
            )
        )

        errors = module.validate_zone(
            zone
        )

        self.assertTrue(
            any(
                "simultaneously included and excluded"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_pull_space_forward(self):
        schema = module.load_schema()

        properties = set(
            schema["properties"]
        )

        for field in {
            "space_id",
            "mission",
            "question",
            "transform_id",
            "cartography_id",
            "occupation_id",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
