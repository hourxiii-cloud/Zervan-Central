import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_qualification_request.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_qualification_request",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_request(
    state="READY"
):
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version": "1.0",
        "object_id": object_id,
        "provisional_room_reference":
            "room:provisional:test",
        "origin_reference":
            "origin:test",
        "ingress_reference":
            "ingress:test",
        "zone_id":
            "sha512:" + "5" * 128,
        "space_id":
            "sha512:" + "6" * 128,
        "orientation_reference":
            "orientation:test",
        "territory_reference":
            "territory:test",
        "qualification_mission":
            "establish mission fitness",
        "active_question":
            "is this Room fit for the proposed mission?",
        "entry_constraints": [
            "qualification-only"
        ],
        "evidence_obligations": [
            "preserve provenance"
        ],
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
        "prohibited_assumptions": [
            "no invented evidence"
        ],
        "human_gate_conditions": [
            "preserve gate"
        ],
        "qualification_requirements": [
            "object_identity",
            "boundary",
            "provenance",
            "geometry",
            "mission_fitness",
        ],
        "request_state":
            state,
        "provenance_route": [
            object_id,
            "origin:test",
        ],
        "requested_at":
            "2026-08-07T19:08:00-04:00",
    }

    record[
        "qualification_request_id"
    ] = module.compute_qualification_request_id(
        record
    )

    return record


class QualificationRequestTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_ready_request(self):
        record = make_request()

        self.assertEqual(
            module.validate_request(
                record
            ),
            []
        )

    def test_request_identity_is_deterministic(self):
        record = make_request()

        self.assertEqual(
            record["qualification_request_id"],
            module.compute_qualification_request_id(
                record
            )
        )

    def test_question_change_changes_request_identity(self):
        record = make_request()

        changed = dict(
            record
        )

        changed[
            "active_question"
        ] = "what evidence remains unresolved?"

        changed[
            "qualification_request_id"
        ] = module.compute_qualification_request_id(
            changed
        )

        self.assertNotEqual(
            record["qualification_request_id"],
            changed["qualification_request_id"]
        )

    def test_request_id_does_not_replace_object_id(self):
        record = make_request()

        self.assertNotEqual(
            record["qualification_request_id"],
            record["object_id"]
        )

    def test_ready_requires_mission(self):
        record = make_request()

        record[
            "qualification_mission"
        ] = ""

        record[
            "qualification_request_id"
        ] = module.compute_qualification_request_id(
            record
        )

        errors = module.validate_request(
            record
        )

        self.assertTrue(
            any(
                "qualification_mission"
                in error
                for error in errors
            )
        )

    def test_evidence_cannot_be_both_included_and_excluded(self):
        record = make_request()

        record[
            "excluded_evidence"
        ] = [
            "evidence:a"
        ]

        record[
            "qualification_request_id"
        ] = module.compute_qualification_request_id(
            record
        )

        errors = module.validate_request(
            record
        )

        self.assertTrue(
            any(
                "both included and excluded"
                in error
                for error in errors
            )
        )

    def test_schema_does_not_pull_disposition_or_occupation_forward(self):
        schema = module.load_schema()

        properties = set(
            schema["properties"]
        )

        for field in {
            "qualification_disposition",
            "qualification_record_id",
            "qualification_lead",
            "participating_capabilities",
            "formation_id",
            "formation_type",
            "occupancy_witness_id",
            "capability_mission_id",
            "cartography_changes",
            "distinct_object_result",
            "recommended_formation",
            "replay_route",
        }:
            self.assertNotIn(
                field,
                properties
            )


if __name__ == "__main__":
    unittest.main()
