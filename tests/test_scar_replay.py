import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_scar_replay.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_scar_replay",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_record(
    action="REPLAY"
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
        "scar_record_reference":
            "scar:test",
        "replay_envelope_reference":
            "replay:test",
        "observer_reference":
            "observer:test",
        "requested_action":
            action,
        "action_basis": [
            "bounded future-observer Scar operation"
        ],
        "historical_observational_coordinate": {
            "coordinate": "scar:test"
        },
        "historical_question_contract_reference":
            "question:test",
        "historical_zone_reference":
            "zone:test",
        "historical_space_reference":
            "space:test",
        "historical_transform_references": [
            "transform:test"
        ],
        "prior_movement_references": [
            "movement:test"
        ],
        "scar_effect_evidence_references": [
            "evidence:scar:test"
        ],
        "recorded_effect_references": [
            "effect:test"
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
        "reflight_trigger_reference":
            None,
        "branch_control_reference":
            None,
        "challenge_evidence_references": [],
        "ignore_evidence_references": [],
        "action_eligibility":
            "ELIGIBLE",
        "blocking_reasons": [],
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "scar:test",
            "replay:test",
            "movement:test",
            "stick:test"
        ],
        "requested_at":
            "2026-08-07T20:55:00-04:00",
    }

    if action == "CONTINUE":
        record[
            "reflight_trigger_reference"
        ] = "reflight:test"

    if action == "BRANCH":
        record[
            "branch_control_reference"
        ] = "branch-control:test"

    if action == "CHALLENGE":
        record[
            "challenge_evidence_references"
        ] = [
            "evidence:challenge:test"
        ]

    if action == "IGNORE_WITH_EVIDENCE":
        record[
            "ignore_evidence_references"
        ] = [
            "evidence:ignore:test"
        ]

    record[
        "scar_replay_id"
    ] = module.compute_scar_replay_id(
        record
    )

    return record


class ScarReplayTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_all_six_source_actions(self):
        for action in sorted(
            module.ACTIONS
        ):
            record = make_record(
                action
            )

            self.assertEqual(
                module.validate_scar_replay(
                    record
                ),
                [],
                action
            )

    def test_continue_requires_reflight_trigger(self):
        record = make_record(
            "CONTINUE"
        )

        record[
            "reflight_trigger_reference"
        ] = None

        record[
            "scar_replay_id"
        ] = module.compute_scar_replay_id(
            record
        )

        errors = module.validate_scar_replay(
            record
        )

        self.assertTrue(
            any(
                "CONTINUE requires Reflight Trigger"
                in error
                for error in errors
            )
        )

    def test_branch_requires_branch_control(self):
        record = make_record(
            "BRANCH"
        )

        record[
            "branch_control_reference"
        ] = None

        record[
            "scar_replay_id"
        ] = module.compute_scar_replay_id(
            record
        )

        errors = module.validate_scar_replay(
            record
        )

        self.assertTrue(
            any(
                "BRANCH requires branch-control"
                in error
                for error in errors
            )
        )

    def test_challenge_requires_evidence(self):
        record = make_record(
            "CHALLENGE"
        )

        record[
            "challenge_evidence_references"
        ] = []

        record[
            "scar_replay_id"
        ] = module.compute_scar_replay_id(
            record
        )

        errors = module.validate_scar_replay(
            record
        )

        self.assertTrue(
            any(
                "CHALLENGE requires challenge evidence"
                in error
                for error in errors
            )
        )

    def test_ignore_requires_evidence(self):
        record = make_record(
            "IGNORE_WITH_EVIDENCE"
        )

        record[
            "ignore_evidence_references"
        ] = []

        record[
            "scar_replay_id"
        ] = module.compute_scar_replay_id(
            record
        )

        errors = module.validate_scar_replay(
            record
        )

        self.assertTrue(
            any(
                "IGNORE_WITH_EVIDENCE requires ignore evidence"
                in error
                for error in errors
            )
        )

    def test_replay_requires_replay_envelope(self):
        record = make_record(
            "REPLAY"
        )

        record[
            "replay_envelope_reference"
        ] = None

        record[
            "scar_replay_id"
        ] = module.compute_scar_replay_id(
            record
        )

        errors = module.validate_scar_replay(
            record
        )

        self.assertTrue(
            any(
                "REPLAY requires Replay Envelope"
                in error
                for error in errors
            )
        )

    def test_blocked_requires_reason(self):
        record = make_record()

        record[
            "action_eligibility"
        ] = "BLOCKED"

        record[
            "blocking_reasons"
        ] = []

        record[
            "scar_replay_id"
        ] = module.compute_scar_replay_id(
            record
        )

        errors = module.validate_scar_replay(
            record
        )

        self.assertTrue(
            any(
                "requires blocking reasons"
                in error
                for error in errors
            )
        )

    def test_material_observer_change_changes_identity(self):
        first = make_record()

        changed = dict(
            first
        )

        changed[
            "observer_reference"
        ] = "observer:different"

        changed[
            "scar_replay_id"
        ] = module.compute_scar_replay_id(
            changed
        )

        self.assertNotEqual(
            first[
                "scar_replay_id"
            ],
            changed[
                "scar_replay_id"
            ]
        )

    def test_schema_does_not_create_or_delete_world(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "new_object_id",
            "branch_object_id",
            "lifecycle_transition_id",
            "publication_authorization",
            "canonical_promotion",
            "full_payload_hydration",
            "scar_deleted",
            "historical_state_replaced",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
