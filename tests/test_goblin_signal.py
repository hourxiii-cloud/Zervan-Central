import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_goblin_signal.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_goblin_signal",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_event(
    event_class="ROOM_EVENT",
    event_subtype="GENERIC_ROOM_EVENT",
    source_record_type="ROOM_EVENT_RECORD",
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
        "event_class":
            event_class,
        "event_subtype":
            event_subtype,
        "source_record_type":
            source_record_type,
        "source_record_reference":
            "source:test",
        "source_component":
            "Registry",
        "event_subject":
            "bounded Room event",
        "prior_state_reference":
            None,
        "resulting_state_reference":
            None,
        "zone_references": [],
        "space_references": [],
        "cartography_reference":
            None,
        "stick_reference":
            "stick:test",
        "evidence_boundary": {
            "scope": "test"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "propagation_scope":
            "ROOM",
        "intended_recipients": [
            "TOC"
        ],
        "delivery_state":
            "EMITTED",
        "sequence_coordinate":
            1,
        "provenance_route": [
            object_id,
            "source:test"
        ],
        "emitted_at":
            "2026-08-07T19:42:00-04:00",
    }

    record[
        "goblin_signal_event_id"
    ] = module.compute_event_id(
        record
    )

    return record


class GoblinSignalTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_room_event(self):
        record = make_event()

        self.assertEqual(
            module.validate_event(
                record
            ),
            []
        )

    def test_qualification_event(self):
        record = make_event(
            event_class="QUALIFICATION_CHANGE",
            event_subtype="QUALIFIED",
            source_record_type="LIFECYCLE_TRANSITION",
        )

        self.assertEqual(
            module.validate_event(
                record
            ),
            []
        )

    def test_all_qualification_subtypes(self):
        for subtype in (
            "QUALIFIED",
            "REJECTED",
            "INSTABILITY",
            "BRANCH_AVAILABLE",
            "FURTHER_RECONNAISSANCE_NEEDED",
        ):
            record = make_event(
                event_class="QUALIFICATION_CHANGE",
                event_subtype=subtype,
                source_record_type="LIFECYCLE_TRANSITION",
            )

            self.assertEqual(
                module.validate_event(
                    record
                ),
                []
            )

    def test_occupancy_requires_witness_source(self):
        record = make_event(
            event_class="OCCUPANCY_CHANGE",
            event_subtype="ENTERED",
            source_record_type="ROOM_EVENT_RECORD",
        )

        errors = module.validate_event(
            record
        )

        self.assertTrue(
            any(
                "must bind an Occupancy Witness"
                in error
                for error in errors
            )
        )

    def test_return_notification_requires_return_source(self):
        record = make_event(
            event_class="CAPABILITY_RETURN_NOTIFICATION",
            event_subtype="CAPABILITY_RETURNED",
            source_record_type="ROOM_EVENT_RECORD",
        )

        errors = module.validate_event(
            record
        )

        self.assertTrue(
            any(
                "must bind a Capability Return"
                in error
                for error in errors
            )
        )

    def test_event_identity_is_deterministic(self):
        record = make_event()

        self.assertEqual(
            record["goblin_signal_event_id"],
            module.compute_event_id(
                record
            )
        )

    def test_subject_change_changes_event_identity(self):
        record = make_event()

        changed = dict(
            record
        )

        changed[
            "event_subject"
        ] = "different bounded Room event"

        changed[
            "goblin_signal_event_id"
        ] = module.compute_event_id(
            changed
        )

        self.assertNotEqual(
            record[
                "goblin_signal_event_id"
            ],
            changed[
                "goblin_signal_event_id"
            ]
        )

    def test_schema_does_not_absorb_owner_or_downstream_actions(self):
        schema = module.load(
            module.SCHEMA
        )

        forbidden = {
            "lifecycle_mutation",
            "qualification_disposition",
            "occupancy_event_mutation",
            "formation_type_selection",
            "branch_creation",
            "distinct_object_determination",
            "hydration_request_id",
            "payload_release",
            "publication_authorization",
            "execution_authorization",
        }

        self.assertFalse(
            set(
                schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
