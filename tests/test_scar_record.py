import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_scar_record.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_scar_record",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_scar():
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "terrain_reference":
            "terrain:test",
        "affected_movement_references": [
            "movement:test"
        ],
        "effect_evidence_references": [
            "evidence:test"
        ],
        "effect_description": [
            "terrain altered the bounded capability route"
        ],
        "observational_coordinate": {
            "coordinate": "scar:test"
        },
        "question_contract_reference":
            "question:test",
        "inquiry_envelope_reference":
            "inquiry:test",
        "occupied_zone_reference":
            "zone:test",
        "occupied_space_reference":
            "space:test",
        "transform_references": [
            "transform:test"
        ],
        "capability_route_references": [
            "movement:test",
            "route:test"
        ],
        "restriction_constriction_references": [
            "restriction:test"
        ],
        "collapse_boundary_references": [
            "collapse:test"
        ],
        "finding_references": [
            "finding:test"
        ],
        "evidence_boundary": {
            "scope": "historical"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "replay_envelope_reference":
            "replay:test",
        "effect_persistence":
            "HISTORICAL",
        "unresolved_implications": [
            "future recurrence unknown"
        ],
        "provenance_route": [
            object_id,
            "terrain:test",
            "movement:test",
            "evidence:test",
            "stick:test"
        ],
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "recorded_at":
            "2026-08-07T20:52:00-04:00",
    }

    record[
        "scar_record_id"
    ] = module.compute_scar_record_id(
        record
    )

    return record


class ScarRecordTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_scar(self):
        record = make_scar()

        self.assertEqual(
            module.validate_scar(
                record
            ),
            []
        )

    def test_terrain_required(self):
        record = make_scar()

        record[
            "terrain_reference"
        ] = ""

        record[
            "scar_record_id"
        ] = module.compute_scar_record_id(
            record
        )

        errors = module.validate_scar(
            record
        )

        self.assertTrue(
            any(
                "terrain_reference"
                in error
                for error in errors
            )
        )

    def test_prior_movement_required(self):
        record = make_scar()

        record[
            "affected_movement_references"
        ] = []

        record[
            "scar_record_id"
        ] = module.compute_scar_record_id(
            record
        )

        errors = module.validate_scar(
            record
        )

        self.assertTrue(
            any(
                "affected_movement_references"
                in error
                for error in errors
            )
        )

    def test_effect_evidence_required(self):
        record = make_scar()

        record[
            "effect_evidence_references"
        ] = []

        record[
            "scar_record_id"
        ] = module.compute_scar_record_id(
            record
        )

        errors = module.validate_scar(
            record
        )

        self.assertTrue(
            any(
                "effect_evidence_references"
                in error
                for error in errors
            )
        )

    def test_effect_description_required(self):
        record = make_scar()

        record[
            "effect_description"
        ] = []

        record[
            "scar_record_id"
        ] = module.compute_scar_record_id(
            record
        )

        errors = module.validate_scar(
            record
        )

        self.assertTrue(
            any(
                "effect_description"
                in error
                for error in errors
            )
        )

    def test_movement_must_remain_on_capability_route(self):
        record = make_scar()

        record[
            "capability_route_references"
        ] = [
            "route:unrelated"
        ]

        record[
            "scar_record_id"
        ] = module.compute_scar_record_id(
            record
        )

        errors = module.validate_scar(
            record
        )

        self.assertTrue(
            any(
                "attributable"
                in error
                for error in errors
            )
        )

    def test_replay_envelope_is_optional(self):
        record = make_scar()

        record[
            "replay_envelope_reference"
        ] = None

        record[
            "scar_record_id"
        ] = module.compute_scar_record_id(
            record
        )

        self.assertEqual(
            module.validate_scar(
                record
            ),
            []
        )

    def test_material_effect_change_changes_identity(self):
        first = make_scar()

        changed = dict(
            first
        )

        changed[
            "effect_description"
        ] = [
            "different effect"
        ]

        changed[
            "scar_record_id"
        ] = module.compute_scar_record_id(
            changed
        )

        self.assertNotEqual(
            first[
                "scar_record_id"
            ],
            changed[
                "scar_record_id"
            ]
        )

    def test_schema_does_not_pull_scar_replay_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "scar_replay_id",
            "scar_replay_action",
            "selected_future_route",
            "automatic_reflight",
            "new_object_id",
            "lifecycle_transition_id",
            "publication_authorization",
            "canonical_promotion",
            "confidence_score",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
