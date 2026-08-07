import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_stick_contact_continuity.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_stick_contact_continuity",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_stick(
    state="CONTINUOUS"
):
    object_id = (
        "sha512:"
        + "2" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "origin_reference":
            "origin:a",
        "ingress_envelope_reference":
            "ingress:a",
        "cartography_reference":
            "cartography:a",
        "source_orientation_reference":
            "orientation:a",
        "target_orientation_reference":
            "orientation:b",
        "transform_reference":
            "transform:a",
        "space_reference":
            "space:a",
        "evidence_lineage_references": [
            "evidence:a"
        ],
        "provenance_route": [
            object_id,
            "origin:a",
        ],
        "observation_references": [
            "observation:a"
        ],
        "restriction_references": [
            "restriction:a"
        ],
        "source_coordinates": {
            "position": "a"
        },
        "target_coordinates": {
            "position": "b"
        },
        "return_coordinates": {
            "position": "return"
        },
        "continuity_state":
            state,
        "continuity_reason":
            "test continuity",
        "recorded_at":
            "2026-08-07T18:55:00-04:00",
    }

    record[
        "stick_id"
    ] = module.compute_stick_id(
        record
    )

    return record


class StickContactContinuityTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_continuous_stick(self):
        record = make_stick()

        self.assertEqual(
            module.validate_stick(
                record
            ),
            []
        )

    def test_stick_id_is_deterministic(self):
        record = make_stick()

        self.assertEqual(
            record["stick_id"],
            module.compute_stick_id(
                record
            )
        )

    def test_target_orientation_change_changes_stick_id(self):
        record = make_stick()

        changed = dict(
            record
        )

        changed[
            "target_orientation_reference"
        ] = "orientation:c"

        changed[
            "stick_id"
        ] = module.compute_stick_id(
            changed
        )

        self.assertNotEqual(
            record["stick_id"],
            changed["stick_id"]
        )

    def test_stick_id_does_not_replace_object_id(self):
        record = make_stick()

        self.assertNotEqual(
            record["stick_id"],
            record["object_id"]
        )

    def test_continuous_requires_evidence_lineage(self):
        record = make_stick()

        record[
            "evidence_lineage_references"
        ] = []

        record[
            "stick_id"
        ] = module.compute_stick_id(
            record
        )

        errors = module.validate_stick(
            record
        )

        self.assertTrue(
            any(
                "requires evidence lineage"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_pull_passageway_or_occupation_forward(self):
        schema = module.load_schema()

        properties = set(
            schema["properties"]
        )

        for field in {
            "passageway_id",
            "passage_state",
            "passage_authorization",
            "occupation_id",
            "occupant_id",
            "capability_position",
            "movement_execution",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
