import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_qualification_record.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_qualification_record",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_record(
    disposition="QUALIFIED"
):
    object_id = (
        "sha512:"
        + "5" * 128
    )

    request_id = (
        "sha512:"
        + "6" * 128
    )

    record = {
        "schema_version": "1.0",
        "qualification_request_reference":
            request_id,
        "object_id":
            object_id,
        "provisional_room_id":
            "room:provisional:test",
        "origin_reference":
            "origin:test",
        "ingress_reference":
            "ingress:test",
        "qualification_mission":
            "establish mission fitness",
        "active_question":
            "is the Room sufficiently established?",
        "qualification_lead":
            "Goblin:test",
        "participating_capabilities": [
            "Goblin:test"
        ],
        "occupied_zone_id":
            "sha512:" + "7" * 128,
        "occupied_space_id":
            "sha512:" + "8" * 128,
        "included_evidence": [
            "evidence:a"
        ],
        "excluded_evidence": [
            "evidence:b"
        ],
        "evidence_boundary": {
            "included": [
                "evidence:a"
            ],
            "excluded": [
                "evidence:b"
            ],
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "observed_geometry": {
            "region": "a"
        },
        "cartographic_change_references": [
            "cartography:update:test"
        ],
        "provenance_anchors": [
            "provenance:test"
        ],
        "uncertainty_frontiers": [
            {
                "frontier": "a"
            }
        ],
        "unresolved_contradictions": [],
        "restricted_or_inaccessible_surfaces": [
            {
                "surface": "restricted"
            }
        ],
        "adjoining_object_candidates": [],
        "distinct_object_result":
            "SAME_OBJECT",
        "recommended_formation_or_next_reconnaissance_action":
            "single route may be considered",
        "qualification_disposition":
            disposition,
        "disposition_basis": [
            "bounded test basis"
        ],
        "return_coordinates": {
            "position": "return"
        },
        "replay_route": [
            "orientation:test"
        ],
        "provenance_route": [
            object_id,
            request_id,
        ],
        "completed_at":
            "2026-08-07T19:19:00-04:00",
    }

    if disposition == "PROVISIONAL":
        record[
            "unresolved_contradictions"
        ] = [
            {
                "contradiction": "unresolved"
            }
        ]

    if disposition == "DEGRADED":
        record[
            "disposition_basis"
        ] = [
            "degraded access prevents prior operation"
        ]

    record[
        "qualification_record_id"
    ] = module.compute_qualification_record_id(
        record
    )

    return record


class QualificationRecordTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_qualified_record(self):
        record = make_record()

        self.assertEqual(
            module.validate_record(
                record
            ),
            []
        )

    def test_all_source_dispositions_validate(self):
        for disposition in (
            "QUALIFIED",
            "PROVISIONAL",
            "REJECTED",
            "DEGRADED",
        ):
            record = make_record(
                disposition
            )

            self.assertEqual(
                module.validate_record(
                    record
                ),
                []
            )

    def test_record_identity_is_deterministic(self):
        record = make_record()

        self.assertEqual(
            record["qualification_record_id"],
            module.compute_qualification_record_id(
                record
            )
        )

    def test_disposition_change_changes_record_identity(self):
        record = make_record()

        changed = dict(
            record
        )

        changed[
            "qualification_disposition"
        ] = "PROVISIONAL"

        changed[
            "unresolved_contradictions"
        ] = [
            {
                "contradiction": "new"
            }
        ]

        changed[
            "qualification_record_id"
        ] = module.compute_qualification_record_id(
            changed
        )

        self.assertNotEqual(
            record["qualification_record_id"],
            changed["qualification_record_id"]
        )

    def test_record_id_does_not_replace_object_or_request_id(self):
        record = make_record()

        self.assertNotEqual(
            record["qualification_record_id"],
            record["object_id"]
        )

        self.assertNotEqual(
            record["qualification_record_id"],
            record["qualification_request_reference"]
        )

    def test_evidence_cannot_be_both_included_and_excluded(self):
        record = make_record()

        record[
            "excluded_evidence"
        ] = [
            "evidence:a"
        ]

        record[
            "qualification_record_id"
        ] = module.compute_qualification_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "both included and excluded"
                in error
                for error in errors
            )
        )

    def test_provisional_preserves_unresolved_basis(self):
        record = make_record(
            "PROVISIONAL"
        )

        record[
            "unresolved_contradictions"
        ] = []

        record[
            "uncertainty_frontiers"
        ] = []

        record[
            "recommended_formation_or_next_reconnaissance_action"
        ] = None

        record[
            "qualification_record_id"
        ] = module.compute_qualification_record_id(
            record
        )

        errors = module.validate_record(
            record
        )

        self.assertTrue(
            any(
                "PROVISIONAL disposition"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_pull_lifecycle_or_occupation_forward(self):
        schema = module.load(
            module.SCHEMA
        )

        properties = set(
            schema["properties"]
        )

        for field in {
            "room_lifecycle_state",
            "ready_state",
            "formation_selection_id",
            "selected_formation",
            "analytical_occupancy_id",
            "occupancy_witness_id",
            "goblin_signal_event_id",
            "capability_mission_id",
            "execution_authorization",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
