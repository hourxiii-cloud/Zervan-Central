import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_reflight_trigger.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_reflight_trigger",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_trigger(
    trigger_type="NEW_EVIDENCE"
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
        "landing_witness_reference":
            "landing:test",
        "trigger_type":
            trigger_type,
        "trigger_subject":
            "material analytical change",
        "trigger_evidence_references": [],
        "prior_question":
            "question:a",
        "current_question":
            "question:a",
        "prior_evidence_ceiling":
            "CEILING:A",
        "current_evidence_ceiling":
            "CEILING:A",
        "prior_signal_state_reference":
            None,
        "current_signal_state_reference":
            None,
        "challenged_conclusion_reference":
            None,
        "newly_reachable_surface_reference":
            None,
        "requested_rendering_reference":
            None,
        "material_change_basis": [
            "material condition changed"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "representation_reference":
            "representation:test",
        "cartography_reference":
            "cartography:test",
        "stick_reference":
            "stick:test",
        "readiness_reference":
            "readiness:test",
        "reflight_eligibility":
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
            "landing:test",
            "stick:test"
        ],
        "triggered_at":
            "2026-08-07T20:25:00-04:00",
    }

    if trigger_type in {
        "NEW_EVIDENCE",
        "CONTRADICTION",
    }:
        record[
            "trigger_evidence_references"
        ] = [
            "evidence:test"
        ]

    if trigger_type == "CHANGED_QUESTION":
        record[
            "current_question"
        ] = "materially changed question:b"

    if trigger_type == "CHANGED_EVIDENCE_CEILING":
        record[
            "current_evidence_ceiling"
        ] = "CEILING:B"

    if trigger_type in {
        "SIGNAL_SPLIT",
        "SIGNAL_CONVERGENCE",
    }:
        record[
            "prior_signal_state_reference"
        ] = "signal:prior"

        record[
            "current_signal_state_reference"
        ] = "signal:current"

    if trigger_type == "CHALLENGED_CONCLUSION":
        record[
            "challenged_conclusion_reference"
        ] = "conclusion:test"

    if trigger_type == "NEWLY_REACHABLE_SURFACE":
        record[
            "newly_reachable_surface_reference"
        ] = "surface:test"

    if (
        trigger_type
        == "MATERIALLY_DIFFERENT_RENDERING_REQUESTED"
    ):
        record[
            "requested_rendering_reference"
        ] = "rendering:test"

    record[
        "reflight_trigger_id"
    ] = module.compute_reflight_trigger_id(
        record
    )

    return record


class ReflightTriggerTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_all_source_trigger_types(self):
        for trigger_type in sorted(
            module.TRIGGER_TYPES
        ):
            record = make_trigger(
                trigger_type
            )

            self.assertEqual(
                module.validate_trigger(
                    record
                ),
                [],
                trigger_type
            )

    def test_new_evidence_requires_evidence(self):
        record = make_trigger(
            "NEW_EVIDENCE"
        )

        record[
            "trigger_evidence_references"
        ] = []

        record[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            record
        )

        errors = module.validate_trigger(
            record
        )

        self.assertTrue(
            any(
                "requires trigger evidence"
                in error
                for error in errors
            )
        )

    def test_changed_question_must_actually_change(self):
        record = make_trigger(
            "CHANGED_QUESTION"
        )

        record[
            "current_question"
        ] = record[
            "prior_question"
        ]

        record[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            record
        )

        errors = module.validate_trigger(
            record
        )

        self.assertTrue(
            any(
                "materially changed question"
                in error
                for error in errors
            )
        )

    def test_changed_ceiling_must_actually_change(self):
        record = make_trigger(
            "CHANGED_EVIDENCE_CEILING"
        )

        record[
            "current_evidence_ceiling"
        ] = record[
            "prior_evidence_ceiling"
        ]

        record[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            record
        )

        errors = module.validate_trigger(
            record
        )

        self.assertTrue(
            any(
                "requires changed ceiling"
                in error
                for error in errors
            )
        )

    def test_signal_trigger_requires_prior_and_current_state(self):
        record = make_trigger(
            "SIGNAL_SPLIT"
        )

        record[
            "current_signal_state_reference"
        ] = None

        record[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            record
        )

        errors = module.validate_trigger(
            record
        )

        self.assertTrue(
            any(
                "prior and current signal-state"
                in error
                for error in errors
            )
        )

    def test_challenged_conclusion_requires_reference(self):
        record = make_trigger(
            "CHALLENGED_CONCLUSION"
        )

        record[
            "challenged_conclusion_reference"
        ] = None

        record[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            record
        )

        errors = module.validate_trigger(
            record
        )

        self.assertTrue(
            any(
                "challenged conclusion reference"
                in error
                for error in errors
            )
        )

    def test_new_surface_requires_reference(self):
        record = make_trigger(
            "NEWLY_REACHABLE_SURFACE"
        )

        record[
            "newly_reachable_surface_reference"
        ] = None

        record[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            record
        )

        errors = module.validate_trigger(
            record
        )

        self.assertTrue(
            any(
                "surface reference"
                in error
                for error in errors
            )
        )

    def test_rendering_trigger_requires_reference(self):
        record = make_trigger(
            "MATERIALLY_DIFFERENT_RENDERING_REQUESTED"
        )

        record[
            "requested_rendering_reference"
        ] = None

        record[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            record
        )

        errors = module.validate_trigger(
            record
        )

        self.assertTrue(
            any(
                "requested rendering reference"
                in error
                for error in errors
            )
        )

    def test_blocked_requires_reason(self):
        record = make_trigger()

        record[
            "reflight_eligibility"
        ] = "BLOCKED"

        record[
            "blocking_reasons"
        ] = []

        record[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            record
        )

        errors = module.validate_trigger(
            record
        )

        self.assertTrue(
            any(
                "requires blocking reasons"
                in error
                for error in errors
            )
        )

    def test_material_change_changes_identity(self):
        first = make_trigger()

        changed = dict(
            first
        )

        changed[
            "trigger_subject"
        ] = "different material change"

        changed[
            "reflight_trigger_id"
        ] = module.compute_reflight_trigger_id(
            changed
        )

        self.assertNotEqual(
            first[
                "reflight_trigger_id"
            ],
            changed[
                "reflight_trigger_id"
            ]
        )

    def test_schema_does_not_pull_execution_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "reflight_execution_id",
            "movement_state",
            "new_mission_id",
            "selected_force",
            "formation_selection_id",
            "hydration_request_id",
            "closing_witness_id",
            "replay_envelope_id",
            "scar_record_id",
            "new_room_object_id",
            "canonical_promotion",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
