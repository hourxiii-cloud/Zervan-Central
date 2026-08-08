import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_replay_envelope.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_replay_envelope",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_envelope(
    eligibility="ELIGIBLE"
):
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "closing_witness_reference":
            "closing:test",
        "preserved_lineage_reference":
            "lineage:test",
        "question_contract_reference":
            "question:test",
        "inquiry_envelope_reference":
            "inquiry:test",
        "departure_coordinate": {
            "coordinate": "departure:test"
        },
        "replay_observational_coordinate": {
            "coordinate": "observation:test"
        },
        "occupied_zone_reference":
            "zone:test",
        "occupied_space_reference":
            "space:test",
        "transform_references": [
            "transform:test"
        ],
        "evidence_used_references": [
            "evidence:test"
        ],
        "capability_movement_references": [
            "movement:test"
        ],
        "evidence_boundary": {
            "scope": "historical"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "restriction_constriction_references": [
            "restriction:test"
        ],
        "collapse_boundary_references": [
            "collapse:test"
        ],
        "finding_references": [
            "finding:test"
        ],
        "rendering_reference":
            "rendering:test",
        "return_coordinate": {
            "coordinate": "return:test"
        },
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "replay_purpose": [
            "audit historical journey"
        ],
        "replay_eligibility":
            eligibility,
        "blocking_reasons": [],
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "closing:test",
            "observation:test",
            "stick:test"
        ],
        "created_at":
            "2026-08-07T20:42:00-04:00",
    }

    if eligibility == "BLOCKED":
        record[
            "blocking_reasons"
        ] = [
            "historical coordinate unavailable"
        ]

    record[
        "replay_envelope_id"
    ] = module.compute_replay_envelope_id(
        record
    )

    return record


class ReplayEnvelopeTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_eligible_envelope(self):
        record = make_envelope(
            "ELIGIBLE"
        )

        self.assertEqual(
            module.validate_envelope(
                record
            ),
            []
        )

    def test_valid_blocked_envelope(self):
        record = make_envelope(
            "BLOCKED"
        )

        self.assertEqual(
            module.validate_envelope(
                record
            ),
            []
        )

    def test_preserved_coordinate_required(self):
        record = make_envelope()

        record[
            "replay_observational_coordinate"
        ] = {}

        record[
            "replay_envelope_id"
        ] = module.compute_replay_envelope_id(
            record
        )

        errors = module.validate_envelope(
            record
        )

        self.assertTrue(
            any(
                "replay_observational_coordinate"
                in error
                for error in errors
            )
        )

    def test_question_contract_required(self):
        record = make_envelope()

        record[
            "question_contract_reference"
        ] = ""

        record[
            "replay_envelope_id"
        ] = module.compute_replay_envelope_id(
            record
        )

        errors = module.validate_envelope(
            record
        )

        self.assertTrue(
            any(
                "question_contract_reference"
                in error
                for error in errors
            )
        )

    def test_evidence_history_required(self):
        record = make_envelope()

        record[
            "evidence_used_references"
        ] = []

        record[
            "replay_envelope_id"
        ] = module.compute_replay_envelope_id(
            record
        )

        errors = module.validate_envelope(
            record
        )

        self.assertTrue(
            any(
                "evidence_used_references"
                in error
                for error in errors
            )
        )

    def test_capability_movement_required(self):
        record = make_envelope()

        record[
            "capability_movement_references"
        ] = []

        record[
            "replay_envelope_id"
        ] = module.compute_replay_envelope_id(
            record
        )

        errors = module.validate_envelope(
            record
        )

        self.assertTrue(
            any(
                "capability_movement_references"
                in error
                for error in errors
            )
        )

    def test_blocked_requires_reason(self):
        record = make_envelope(
            "BLOCKED"
        )

        record[
            "blocking_reasons"
        ] = []

        record[
            "replay_envelope_id"
        ] = module.compute_replay_envelope_id(
            record
        )

        errors = module.validate_envelope(
            record
        )

        self.assertTrue(
            any(
                "requires blocking reasons"
                in error
                for error in errors
            )
        )

    def test_material_coordinate_change_changes_identity(self):
        first = make_envelope()

        changed = dict(
            first
        )

        changed[
            "replay_observational_coordinate"
        ] = {
            "coordinate": "different"
        }

        changed[
            "replay_envelope_id"
        ] = module.compute_replay_envelope_id(
            changed
        )

        self.assertNotEqual(
            first[
                "replay_envelope_id"
            ],
            changed[
                "replay_envelope_id"
            ]
        )

    def test_schema_does_not_pull_scar_or_reopen_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "new_object_id",
            "reconstructed_coordinate",
            "reflight_execution_id",
            "lifecycle_transition_id",
            "reopened_state_mutation",
            "scar_record_id",
            "scar_replay_id",
            "publication_authorization",
            "canonical_promotion",
            "full_payload_hydration",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
